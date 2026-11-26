# Structure du dépôt / Repository layout

Un dossier par texte, un fichier par article. / One folder per text, one file per article.

| Dossier | Contenu |
| --- | --- |
| `constitution/` | La Constitution du 11 décembre 1990 : `preambule.md`, `titre-NN.md` (intitulés), `art-NNN.md` (`art-054-01.md` = article 54-1) |
| `codes/<code>/` | Les codes institués par une loi ou une ordonnance (« portant Code … ») : `codes/code-penal/`, `codes/code-des-personnes-et-de-la-famille/`, `codes/code-foncier-et-domanial/` … Une nouvelle loi instituant le même code est une nouvelle version du même dossier. |
| `lois/<année>/<numéro>-<objet>/` | Les autres lois (`lois/2019/2019-45-portant-statut-de-l-opposition…/`) |
| `ordonnances/<année>/<numéro>-<objet>/` | Les ordonnances |
| `decrets/<année>/<numéro>-<objet>/` | Les décrets (sans les actes individuels : nominations, promotions, mutations) |
| `arretes/<année>/<numéro>-<objet>/` | Les arrêtés |
| `corpus.json` | La liste des textes du dépôt (`bj/national/acts`) |

Dans chaque dossier de texte / In each text folder:

- `README.md` : intitulé, source (URL du PDF), date retenue et sa justification, nature de la couche texte ;
- `visas.md` : l’en-tête, les visas et la formule de promulgation ;
- `art-NNN.md` (`art-012-bis.md`) : un article ; `# Article N` puis le texte ;
- `signatures.md` : la formule finale et les signatures ;
- `texte-integral.md` : le texte entier, quand aucun article n’a pu être repéré.

Numéros / Numbers: `<année>-<n>` sur quatre chiffres d’année et deux chiffres au moins (`2013-01`, `1990-32`).
Les arrêtés sans numéro national gardent le numéro de leur fiche FAOLEX (`faolex-<id>`).

Dates : chaque commit est daté à midi (Africa/Porto-Novo, UTC+1) du jour de promulgation ou de signature donné par
l’intitulé du texte ; trailers `In-force`, `In-force-basis`, `Source`, `Text-layer`, et `Source-status: secondary copy (…)`
pour les copies FAOLEX, `Text-source: publisher OCR` pour les couches texte posées par l’éditeur sur un scan.
Avant 1970 : commit au 1970-01-01, jour réel dans l’objet et dans `In-force`.

Each commit is dated at noon (Africa/Porto-Novo) on the promulgation or signature day named in the text's title. Before
1970, the commit is stamped 1970-01-01 with the real day in the subject and the `In-force` trailer.
