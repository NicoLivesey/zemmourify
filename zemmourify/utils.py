import re
from functools import lru_cache

import pandas as pd
import phonetics
import textdistance
import wikipedia
from abydos import phonetic
from unidecode import unidecode

from zemmourify.config import PATH_CSV, WEIGHTS, WIKI_PAGE

wikipedia.set_lang("fr")

fonem = phonetic.FONEM()
phonex = phonetic.Phonex()


def _clean(s):
    return unidecode(s).capitalize().replace("-", "").replace(" ", "").split("(")[0]


def _load_csv():
    df = pd.read_csv(PATH_CSV, sep=";", encoding="latin-1")
    return (
        df[df["03_langage"].str.contains("french", na=False)]["01_prenom"]
        .apply(lambda x: _clean(x))
        .tolist()
    )


def _load_wiki():
    page = wikipedia.page(WIKI_PAGE).content
    prenoms = re.findall(r"(\(f\)|\(x\)) (([A-Z]{1}\S*){1,2})", page, flags=re.UNICODE)
    return [_clean(x[-1]) for x in prenoms]


@lru_cache(maxsize=None)
def _load_firstnames():
    return [x for x in set(_load_csv()).union(_load_wiki()) if len(x) > 1]


def _cast(s):
    return [
        phonetics.metaphone(s),
        phonetics.nysiis(s),
        phonetics.soundex(s),
        fonem.encode(s),
        phonex.encode(s),
    ]


def _distance(s1, s2):
    total = 0
    try:
        l1, l2 = _cast(s1), _cast(s2)
    except Exception:
        return 5
    for i, w in enumerate(WEIGHTS):
        lev = textdistance.levenshtein(l1[i], l2[i])
        total += lev * w
    return total


def query(target):
    table = _load_firstnames()
    return sorted(table, key=lambda x: _distance(x, target))[:10]
