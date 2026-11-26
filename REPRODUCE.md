# How this repository was made (Benin)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Assemblée nationale du Bénin: La Constitution de la République du Bénin (1990) | <https://assemblee-nationale.bj/wp-content/uploads/2017/10/Benin-La-Constitution-1990.pdf> | 2026-10-30 | Official text of a law, published openly by the national assembly |
| Cour constitutionnelle du Bénin: Constitution à jour de la révision de 2019 | <https://courconstitutionnelle.bj/files/documents/1677952525_constitution_de_.pdf> | 2026-10-30 | Official text of a law, published openly by the constitutional court |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Constitution de la République du Bénin | 2 | 1990-12-11 to 2019-11-07 |

The build made 3 commits:

| Commits | Kind |
| ---: | --- |
| 1 | first version of an act |
| 1 | one law on its in-force day |
| 1 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `futur`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 2 laws in the record.
- 4 tags.

## Dates

Each commit is dated at noon (Africa/Porto-Novo) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Loi 90-32 was promulgated on 11 December 1990 and its text sets no other commencement date, so it is dated from promulgation; Loi 2019-40 art. 2 brings the revision into force on promulgation (7 November 2019). https://courconstitutionnelle.bj/fr/docs/textes-fondamentaux

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `c105f1d3af572dce0e4fb9375cfccb504bd5e3d6d9fe3fdca3fc431c508a7a0c` (190356 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3e59cb6f05eccb94a9ec14431a7f6781221e83ef`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- Version 1 (1990-12-11) is the Assemblée nationale retyped text of Loi 90-32 dated from promulgation; version 2 (2019-11-07) is the Cour constitutionnelle consolidated text dated from the promulgation of Loi 2019-40 (its art. 2).
- Units marked "(nouveau)" in the consolidated text, and arts 46 and 47 (marked abrogated there and removed here), are credited to Loi 2019-40; every other unit that differs between the two copies (transcription, spacing and wording of the retyped text) is left uncredited and so appears as an unexplained change.
- The Constitution was revised again by Loi 2025-20 of 17 December 2025; that text is published only as a scan, so this history stops at the 2019 revision and is not the text in force today.
- The consolidated text keeps "Forces armées ou de sécurité" in art. 64 and applies art. 157-3 to the 2021 and 2023 elections; no typed applicability is recorded.
- Titles are separate units (titre-NN); the closing signatures of 1990 stay at the end of art. 160.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none

## Runner (2026-11-26)

The acts outside `constitution/` are written by `scripts/benin-law/runner/bj_build.py acts` (one commit per act, pushed
as fast-forward batches; no rebuild of earlier history):

- Listing: the SGG documenthèque (`/documentheque/lois|ordonnances|arretes|decrets/<page>/`), each entry's title giving
  the number and the promulgation or signature day; FAOLEX records for Benin from FAOLEX's public sitemaps.
- Each act is taken from the SGG PDF when its text layer passes the gate, otherwise from the FAOLEX PDF
  (`Source-status: secondary copy (FAOLEX, <url>)`). Gate: at least 250 characters a page, no scanned page without
  text, at least 88% word-like tokens, at least 17% French function words and almost no tokens of the SGG OCR's
  a->o damage ("lo", "portont", "esl"). A layer laid by the publisher over a scan is tagged `Text-source: publisher OCR`.
  We do no OCR.
- Date: the day in the official title (SGG listing, or FAOLEX title); for a FAOLEX copy of a law the SGG lists, the SGG
  title's day; otherwise the President's "Fait à Cotonou, le …" at the end of the text. FAOLEX's `date_of_text` alone is
  not used (it is often the Assembly's adoption day): such acts are held.
- Codes ("portant Code …") go to `codes/<code>/`; a later law instituting the same code is a new version of that folder.
- Appointment decrees and other individual acts are skipped.
- At this push: 8 acts taken (8 lois); 2 acts held (scans, unreadable layers, no reliable date).
