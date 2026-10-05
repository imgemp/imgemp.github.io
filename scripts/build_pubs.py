#!/usr/bin/env python3
"""Generate the publication list in pubs.html from pubs.bib and coauthors.json.

Usage: python3 scripts/build_pubs.py

Only the region between the BEGIN/END GENERATED markers in pubs.html is
replaced; everything else in the page is edited by hand. Uses only the Python
standard library.

Each pubs.bib entry is a normal BibTeX entry plus these optional fields, which
are used to build the page and left out of the BibTeX shown to visitors:

  display_venue   Venue as shown on the page, e.g. "AAMAS (Best Paper Award)".
  pdf             Link for the "Paper (PDF)" download button.
  dataset         Link for a "Datasets (.zip)" download button.
  abstract        Abstract text (HTML allowed).
  main_authors    1-based positions of highlighted authors (default: 1).
                  Use an empty value to highlight nobody.
  display_authors Author list to show instead of `author`; "..." elides names.

Entries appear in file order, grouped under their `year`.
"""
import html
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIB = os.path.join(ROOT, 'pubs.bib')
COAUTHORS = os.path.join(ROOT, 'coauthors.json')
PAGE = os.path.join(ROOT, 'pubs.html')
BEGIN = '<!-- BEGIN GENERATED PUBLICATIONS: edit pubs.bib, then run scripts/build_pubs.py -->'
END = '<!-- END GENERATED PUBLICATIONS -->'

CUSTOM_FIELDS = ['display_venue', 'pdf', 'dataset', 'main_authors', 'display_authors', 'abstract']
FIELD_ORDER = ['title', 'author', 'journal', 'booktitle', 'volume', 'number', 'pages', 'publisher',
               'year']

# --- BibTeX parsing -----------------------------------------------------------


def parse_bib(text):
  """Parse @type{key, field = {value} | "value" | number, ...} entries."""
  entries, i = [], 0
  start = re.compile(r'@(\w+)\s*\{\s*([^,\s]*)\s*,')
  field = re.compile(r'\s*([\w-]+)\s*=\s*')
  while True:
    m = start.search(text, i)
    if not m:
      return entries
    entry = {'type': m.group(1).lower(), 'key': m.group(2), 'fields': {}}
    i = m.end()
    while True:
      fm = field.match(text, i)
      if not fm:
        break
      i = fm.end()
      if text[i] == '{':
        depth, j = 0, i
        while True:
          if text[j] == '\\':
            j += 2
            continue
          depth += {'{': 1, '}': -1}.get(text[j], 0)
          if depth == 0:
            break
          j += 1
        value, i = text[i + 1:j], j + 1
      elif text[i] == '"':
        j = text.index('"', i + 1)
        value, i = text[i + 1:j], j + 1
      else:
        vm = re.compile(r'[^,}\s]+').match(text, i)
        value, i = vm.group(0), vm.end()
      entry['fields'][fm.group(1).lower()] = value
      cm = re.compile(r'\s*,').match(text, i)
      if cm:
        i = cm.end()
    end = re.compile(r'\s*\}').match(text, i)
    if end:
      i = end.end()
    entries.append(entry)


def split_authors(value):
  """Split a BibTeX author field on top-level ' and '."""
  out, depth, cur, k = [], 0, '', 0
  while k < len(value):
    c = value[k]
    depth += {'{': 1, '}': -1}.get(c, 0)
    if depth == 0 and value[k:k + 5].lower() == ' and ':
      out.append(cur)
      cur, k = '', k + 5
      continue
    cur += c
    k += 1
  out.append(cur)
  return [' '.join(a.split()) for a in out if a.strip()]


def write_bib(entries):
  """Serialize entries; standard fields first, then the page-only fields."""
  chunks = []
  for e in entries:
    f = e['fields']
    names = ([n for n in FIELD_ORDER if n in f]
             + [n for n in f if n not in FIELD_ORDER and n not in CUSTOM_FIELDS]
             + [n for n in CUSTOM_FIELDS if n in f])
    lines = [f'@{e["type"]}{{{e["key"]},']
    lines += [f'  {n} = {{{f[n]}}},' for n in names]
    lines[-1] = lines[-1].rstrip(',')
    chunks.append('\n'.join(lines) + '\n}\n')
  return '\n'.join(chunks)

# --- LaTeX and names ----------------------------------------------------------

ACCENTS = {"'": '\u0301', '`': '\u0300', '^': '\u0302', '"': '\u0308', '~': '\u0303',
           'c': '\u0327', 'v': '\u030c', '=': '\u0304', '.': '\u0307', 'u': '\u0306'}
SYMBOLS = {'\\times': '×', '\\%': '%', '\\&': '&', '\\textendash': '–', '---': '—', '--': '–',
           '\\rightarrow': '→', '\\epsilon': 'ε', '\\ln': 'ln'}


def latex_to_text(s):
  """Convert the bits of LaTeX that appear in titles and names to plain text."""
  s = re.sub(r'\\([\'`^"~=.]|[cvu](?=[{\s]))\s*\{?\\?([A-Za-z])\}?',
             lambda m: m.group(2) + ACCENTS[m.group(1)], s)
  for k, v in SYMBOLS.items():
    s = s.replace(k, v)
  s = s.replace('$', '').replace('{', '').replace('}', '')
  return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', s)).strip()


def person_key(name):
  """'Last, First Middle' or 'First Last' -> 'Last, First' (used to look up co-authors)."""
  if name.startswith('{') and name.endswith('}'):
    return latex_to_text(name)  # Corporate author, e.g. {Google DeepMind}.
  name = latex_to_text(name)
  if ',' in name:
    last, first = [p.strip() for p in name.split(',', 1)]
  else:
    *first, last = name.split()
    first = ' '.join(first)
  first = first.split()[0] if first else ''
  return f'{last}, {first}' if first else last


def fold(key):
  """Accent- and case-insensitive form of a person key, for lookups."""
  return unicodedata.normalize('NFKD', key).encode('ascii', 'ignore').decode().lower()


def default_short(key):
  if ', ' not in key:
    return key
  last, first = key.split(', ', 1)
  return f'{first[0]}. {last}'

# --- Rendering ----------------------------------------------------------------


def render_authors(entry, coauthors, warnings):
  f = entry['fields']
  names = split_authors(f.get('display_authors') or f['author'])
  mains = {int(x) for x in re.findall(r'\d+', f.get('main_authors', '1'))}
  parts = []
  for i, name in enumerate(names, 1):
    if name == '...':
      parts.append('...')
      continue
    key = person_key(name)
    info = coauthors.get(fold(key))
    if info is None:
      warnings.append(f'{entry["key"]}: {key} is not in coauthors.json (shown without a link)')
      info = {}
    short = html.escape(info.get('short', default_short(info.get('key', key))))
    cls = 'mainAuthor' if i in mains else 'author'
    inner = f'<a href="{html.escape(info["url"])}">{short}</a>' if info.get('url') else short
    parts.append(f'<span class="{cls}">{inner}</span>')
  line = ', '.join(parts)
  return line + (' ' if line.endswith('...') else '. ')


def render_bibtex(entry):
  f = entry['fields']
  names = [n for n in FIELD_ORDER if n in f and n not in CUSTOM_FIELDS]
  names += [n for n in f if n not in FIELD_ORDER and n not in CUSTOM_FIELDS]
  lines = [f'          @{entry["type"]}{{{entry["key"]},']
  lines += [f'            {n}={{{html.escape(f[n], quote=False)}}},' for n in names]
  lines[-1] = lines[-1].rstrip(',')
  return '\n'.join(lines) + '\n          }'


def render_entry(entry, coauthors, warnings):
  f, key = entry['fields'], entry['key']
  title = html.escape(latex_to_text(f['title']), quote=False)
  venue = html.escape(f.get('display_venue') or latex_to_text(f.get('journal') or f.get('booktitle', '')), quote=False)
  links = [(f[k], label) for k, label in (('pdf', 'Paper (PDF)'), ('dataset', 'Datasets (.zip)')) if f.get(k)]
  out = [f'          <li>\n\n          {render_authors(entry, coauthors, warnings)}'
         f'<span class="title">{title}. </span><span class="venue">{venue}. </span>'
         f'<span class="year">{f["year"]}</span><br/>\n']
  if links:
    items = '\n'.join(f'          <li><a href="{html.escape(u)}">{label}</a></li>' for u, label in links)
    out.append('          <div class="btn-group">\n'
               '          <button type="button" class="btn btn-default details-btn dropdown-toggle" '
               'data-toggle="dropdown">Download<span class="caret"></span></button>\n'
               '          <ul class="dropdown-menu details-panel" role="menu">\n'
               f'{items}\n          </ul>\n          </div>\n')
  buttons = [('btn-primary', 'abstract', 'Abstract')] if f.get('abstract') else []
  buttons.append(('btn-info', 'bibtex', 'BibTex'))
  out.append('          <div class="btn-group" data-toggle="buttons">\n' + ''.join(
      f'          <label class="btn {cls} details-btn" data-toggle="collapse" data-target="#{key}_{kind}">\n'
      f'          <input type="checkbox" /> {label}\n          </label>\n' for cls, kind, label in buttons)
      + '          </div>\n')
  if f.get('abstract'):
    out.append(f'          <div class="collapse" id="{key}_abstract">\n'
               '          <div class="panel panel-primary">\n'
               '          <div class="panel-body details-panel">\n'
               f'          {f["abstract"]}\n'
               '          </div>\n          </div>\n          </div>\n')
  out.append(f'          <div class="collapse" id="{key}_bibtex">\n'
             '          <div class="panel panel-info">\n'
             '          <pre class="panel-body details-panel">\n'
             f'{render_bibtex(entry)}\n'
             '          </pre>\n          </div>\n          </div>\n\n'
             '          </li>\n')
  return '\n'.join(out)


def render(entries, coauthors, warnings):
  keys = [e['key'] for e in entries]
  dupes = {k for k in keys if keys.count(k) > 1}
  if dupes:
    sys.exit(f'Duplicate BibTeX keys: {sorted(dupes)}')
  groups = []
  for e in entries:
    year = e['fields']['year']
    if not groups or groups[-1][0] != year:
      groups.append((year, []))
    groups[-1][1].append(e)
  seen = [y for y, _ in groups]
  if len(seen) != len(set(seen)):
    warnings.append('Entries for the same year are not contiguous in pubs.bib; years appear more than once')
  return '\n'.join(
      f'          <span id="{year}" class="yearGroup">{year}</span>\n          <ul class="papers">\n\n'
      + '\n'.join(render_entry(e, coauthors, warnings) for e in group)
      + '\n          </ul>\n'
      for year, group in groups)


def main():
  entries = parse_bib(open(BIB, encoding='utf-8').read())
  coauthors = {}
  for key, info in json.load(open(COAUTHORS, encoding='utf-8')).items():
    if fold(key) in coauthors:
      sys.exit(f'coauthors.json lists {key} twice (names differing only in accents or case)')
    coauthors[fold(key)] = dict(info, key=key)
  warnings = []
  body = render(entries, coauthors, warnings)
  page = open(PAGE, encoding='utf-8').read()
  if page.count(BEGIN) != 1 or page.count(END) != 1:
    sys.exit(f'pubs.html must contain exactly one BEGIN and one END marker:\n  {BEGIN}\n  {END}')
  head, rest = page.split(BEGIN)
  _, tail = rest.split(END)
  new = f'{head}{BEGIN}\n{body}          {END}{tail}'
  if new != page:
    open(PAGE, 'w', encoding='utf-8').write(new)
  for w in warnings:
    print('warning:', w, file=sys.stderr)
  print(f'pubs.html: {len(entries)} publications{" (unchanged)" if new == page else ""}')


if __name__ == '__main__':
  main()
