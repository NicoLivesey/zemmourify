from zemmourify.utils import _cast, _clean, query


def test_clean():
    assert _clean("JIN-DUN") == "Jindun"


def test_cast():
    assert _cast("Jindun") == ["JNTN", "JA", "J05305", "JINDUN", "G500"]


def test_query():
    assert query("Jindun") == [
        "Jeannine",
        "Jeanine",
        "Jourdain",
        "Jeannette",
        "Jeannot",
        "Justin",
        "Jean",
        "Jeanne",
        "Ninon",
        "Linda",
    ]
