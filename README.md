# Benin: law history in git

The law of Benin as a git history: one file per provision, one commit per law on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change; picking a date gives the text in force that day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

**What is in it now (a first build, not complete)**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution/` | Constitution de la République du Bénin (Loi n° 90-32 du 11 décembre 1990) | 2 | 1990-12-11 as promulgated (Assemblée nationale copy); 2019-11-07 consolidated after Loi n° 2019-40 (Cour constitutionnelle copy) |

**Language.** French (the official language of Benin; no official English text was found). The texts are in French and so is the git history.

**Source.** Assemblée nationale du Bénin (1990 text, retyped copy, read from the Internet Archive capture of 2020-12-04 because the site's TLS certificate has expired) and Cour constitutionnelle du Bénin (text consolidated to the revision of Loi n° 2019-40, 7 November 2019). Both publish the text openly on their own sites.

## Dates

The 1990 version is dated from the promulgation of Loi n° 90-32 (11 December 1990); the text sets no other commencement date. The 2019 version is dated from the promulgation of Loi n° 2019-40 (7 November 2019), whose article 2 brings it into force on promulgation.

## How it is checked

Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`) and must match `corpus.json`; results are in `REPRODUCE.md`.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist (`<law key>@benin-law.invalid`). Changes in the 2019 version marked "(nouveau)" by the Cour constitutionnelle, and the repeal of articles 46 and 47, are credited to Loi n° 2019-40. The two copies are different transcriptions, so about a hundred articles also differ in spelling, capitalisation or paragraph breaks only; those changes have no credited law and appear as unexplained changes by the publisher. The committer is always Lexifina.

## Limits

This is a first build, not complete and not the text in force today. The Constitution was revised again by Loi n° 2025-20 of 17 December 2025; that text is published only as a scan with no text layer, so this history stops at the 2019 revision. No statutes are included yet: the available copies of the Code du numérique and the Code pénal have unusable text layers. Read the official text for anything that matters.
