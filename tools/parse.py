"""Benin Constitution: two versions (1990 as promulgated; 2019 consolidated). Reads v1.txt / v2.txt (pdftotext -layout)
and v1.pdf / v2.pdf from the work folder (argv[1]) and writes corpus.json. Deterministic, no network."""
import hashlib, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r'~\Documents\bj-work')


def norm(s):
    s = s.replace('\u00a0', ' ').replace('\u2019', "'").replace('\u2018', "'").replace('\u2013', '-').replace('\u2014', '-')
    s = s.replace('\u201c', '"').replace('\u201d', '"')
    s = re.sub(r"(\w) ' (\w)", r"\1'\2", s)
    s = re.sub(r'\s+([;:,.!?])', r'\1', s)
    s = re.sub(r'\s{2,}', ' ', s)
    return s.strip()


ROM = {'PREMIER': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10, 'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14}
TIT = re.compile(r'^TITRE\s+(PREMIER|[IVX]+)(?:-(\d+))?\b\s*(\(NOUVEAU\))?\s*:?\s*(.*)$')
A1 = re.compile(r'^Article\s+(\d+|1er)(?:-(\d+))?\s*$')
A2 = re.compile(r'^Article\s+(\d+|1er)(?:-(\d+))?\s*(\(nouveau\))?[\s.\-]+(.*)$')
BUL = re.compile(r'^(-|\d+[-.)]|[a-z]\)|\u2022)\s*')


def key(n, sub):
    n = 1 if n == '1er' else int(n)
    return f'art-{n:03d}' + (f'-{int(sub):02d}' if sub else ''), f'Art. {n}' + (f'-{sub}' if sub else '')


def paras(lines):
    out, cur, blank = [], '', True
    for raw in lines:
        if not raw.strip():
            blank = True
            continue
        ln = norm(raw)
        if cur and ((blank and not ln[:1].islower()) or BUL.match(ln)):
            out.append(cur)
            cur = ''
        cur = (cur + ' ' + ln).strip()
        blank = False
    if cur:
        out.append(cur)
    return out


def parse(text, v1):
    L = text.split('\n')
    start = next(i for i, l in enumerate(L) if l.strip() == 'Préambule')
    units, nouveau = {}, set()
    cur = ['preambule', 'Préambule', 'preamble', []]

    def flush():
        k, lab, kind, body = cur
        if k in units:
            raise SystemExit('dup ' + k)
        ps = paras(body)
        if not ps:
            return
        t = (f'# {lab}\n' if kind != 'title' else '') + '\n'.join(ps) + '\n'
        units[k] = {'label': lab, 'kind': kind, 'text': t}

    i = start + 1
    while i < len(L):
        s = L[i].strip()
        m_t = TIT.match(s)
        m_a = (A1 if v1 else A2).match(s)
        if m_t:
            flush()
            n = ROM[m_t.group(1)]
            head = m_t.group(4)
            tk = f'titre-{n:02d}' + (f'-{int(m_t.group(2)):02d}' if m_t.group(2) else '')
            tl = f'Titre {n}' + (f'-{m_t.group(2)}' if m_t.group(2) else '')
            if m_t.group(3) and not v1:
                nouveau.add(tk)
            nxt = L[i + 1].strip() if i + 1 < len(L) else ''
            if nxt.isupper() and not TIT.match(nxt):
                head += ' ' + nxt
                i += 1
            cur = [tk, tl, 'title', [f'{tl} : {norm(head)}']]
        elif m_a:
            flush()
            k, lab = key(m_a.group(1), m_a.group(2))
            first = '' if v1 else m_a.group(4)
            if not v1 and m_a.group(3):
                nouveau.add(k)
            cur = [k, lab, 'art', [first] if first else []]
        else:
            cur[3].append(L[i])
        i += 1
    flush()
    return units, nouveau


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


u1, _ = parse((WORK / 'v1.txt').read_text(encoding='utf8'), True)
u2, nouv = parse((WORK / 'v2.txt').read_text(encoding='utf8'), False)
removed = [k for k, u in u2.items() if k.startswith('art-') and re.search(r'\(abrog', u['text'])]
for k in removed:
    del u2[k]
credit = {}
for k in sorted(set(u1) | set(u2)):
    if u1.get(k) != u2.get(k) and (k in nouv or k in removed):
        credit[k] = ['loi-2019-40']
unexp = sorted(k for k in set(u1) | set(u2) if u1.get(k) != u2.get(k) and k not in credit)
SRC1 = 'https://assemblee-nationale.bj/wp-content/uploads/2017/10/Benin-La-Constitution-1990.pdf'
SRC2 = 'https://courconstitutionnelle.bj/files/documents/1677952525_constitution_de_.pdf'
corpus = {
    'country': {'code': 'BJ', 'name': 'Benin', 'slug': 'benin', 'lang': 'fr', 'tz': 'Africa/Porto-Novo', 'future_branch': 'futur',
                'publisher': {'name': 'Assemblée nationale and Cour constitutionnelle du Bénin', 'email': 'benin@lexifina.invalid'},
                'default_in_force_rule': {'text': 'Loi 90-32 was promulgated on 11 December 1990 and its text sets no other commencement date, so it is dated from promulgation; Loi 2019-40 art. 2 brings the revision into force on promulgation (7 November 2019).',
                                          'source': 'https://courconstitutionnelle.bj/fr/docs/textes-fondamentaux'},
                'licence_note': 'Official constitutional text of the Republic of Benin, published openly by the Assemblée nationale du Bénin and the Cour constitutionnelle du Bénin.'},
    'sources': [
        {'name': 'Assemblée nationale du Bénin: La Constitution de la République du Bénin (1990)', 'url': SRC1, 'retrieved': '2026-10-30',
         'licence': 'Official text of a law, published openly by the national assembly',
         'notes': "The site's TLS certificate has expired, so the bytes were read from the Internet Archive capture of 2020-12-04."},
        {'name': 'Cour constitutionnelle du Bénin: Constitution à jour de la révision de 2019', 'url': SRC2, 'retrieved': '2026-10-30',
         'licence': 'Official text of a law, published openly by the constitutional court', 'notes': 'Consolidated text; revised articles are marked "(nouveau)".'}],
    'laws': {
        'loi-90-32': {'label': 'Loi n° 90-32', 'title': 'Loi n° 90-32 du 11 décembre 1990 portant Constitution de la République du Bénin', 'kind': 'law', 'enacted': '1990-12-11', 'published': None, 'url': SRC1, 'temporary_until': None, 'restores': None, 'note': None},
        'loi-2019-40': {'label': 'Loi n° 2019-40', 'title': 'Loi n° 2019-40 du 7 novembre 2019 portant révision de la loi n° 90-32 du 11 décembre 1990 portant Constitution de la République du Bénin', 'kind': 'law', 'enacted': '2019-11-07', 'published': None, 'url': SRC2, 'temporary_until': None, 'restores': None, 'note': None}},
    'acts': [{'slug': 'constitution', 'short': 'Constitution', 'title': 'Constitution de la République du Bénin', 'url': 'https://courconstitutionnelle.bj/fr/docs/textes-fondamentaux',
              'first_law': 'loi-90-32', 'earlier_laws': [],
              'versions': [
                  {'from': '1990-12-11', 'source_url': 'https://web.archive.org/web/20201204234550id_/' + SRC1, 'sha256': sha(WORK / 'v1.pdf'), 'units': u1},
                  {'from': '2019-11-07', 'source_url': SRC2, 'sha256': sha(WORK / 'v2.pdf'), 'units': u2, 'credits': credit,
                   'note': 'Consolidated text of the Cour constitutionnelle. The 1990 text is the Assemblée nationale retyped copy, so some units differ only by transcription; those are committed as unexplained.'}]}],
    'applies': [],
    'decisions': [
        'Version 1 (1990-12-11) is the Assemblée nationale retyped text of Loi 90-32 dated from promulgation; version 2 (2019-11-07) is the Cour constitutionnelle consolidated text dated from the promulgation of Loi 2019-40 (its art. 2).',
        'Units marked "(nouveau)" in the consolidated text, and arts 46 and 47 (marked abrogated there and removed here), are credited to Loi 2019-40; every other unit that differs between the two copies (transcription, spacing and wording of the retyped text) is left uncredited and so appears as an unexplained change.',
        'The Constitution was revised again by Loi 2025-20 of 17 December 2025; that text is published only as a scan, so this history stops at the 2019 revision and is not the text in force today.',
        'The consolidated text keeps "Forces armées ou de sécurité" in art. 64 and applies art. 157-3 to the 2021 and 2023 elections; no typed applicability is recorded.',
        'Titles are separate units (titre-NN); the closing signatures of 1990 stay at the end of art. 160.'],
    'ai_use': ['none']}
Path(HERE / 'corpus.json').write_text(json.dumps(corpus, ensure_ascii=False, indent=1) + '\n', encoding='utf8', newline='\n')
print(len(u1), len(u2), 'credited', len(credit), 'unexplained', len(unexp), unexp[:60], 'removed', removed)
