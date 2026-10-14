"""Regression check for ingredient / dish-line matching: the cases of the matching audit (October 2026).

Usage:
  uv run db/checks/ingredients_regress.py      # resolves against db/unified.duckdb (or $UNIFIED_DB), read-only

Each case gives a text, its language and what it must resolve to: an ingredient id, '!ING:x' (anything but x),
None (unmatched), or a list of ids (the line is split into these parts). Line-level helpers of the `dishes` stage
(junk / header filter, units, names) are checked too. Exits 1 if any case fails.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import DB_PATH, connect  # noqa: E402
from build.dishes import grams_of, irn_name, junk_line, parse_zh, xcf_has  # noqa: E402
from build.resolve_ingredients import IngredientResolver  # noqa: E402

TEXT = [
    # 1. fragment rows of the manual map apply to the exact residual key only
    ("meat", "en", "!ING:stock"),
    ("ground meat", "en", "!ING:stock"),
    ("lamb or mutton", "en", "ING:lamb"),
    ("ground round", "en", "!ING:samh"),
    ("ginger", "en", "ING:ginger"),
    ("coriander", "en", "ING:coriander"),
    ("chili", "en", "ING:chili-pepper"),
    ("black", "en", "!ING:gram"),
    ("roasted", "en", "!ING:gram"),
    ("brown", "en", "ING:sugar"),            # still meant as 'brown [sugar]' when it is the whole line
    ("brown rice", "en", "!ING:sugar"),
    ("hot sauce", "en", "!ING:water"),
    ("pinch", "en", "ING:salt"),
    ("roasted gram", "en", "ING:chana-dal"),
    ("split bengal gram", "en", "ING:chana-dal"),
    ("washed urad dal", "en", "ING:urad-dal"),
    ("black gram dal", "en", "ING:urad-dal"),
    # duplicates merged (issue #10): jowar is sorghum
    ("jowar", "en", "ING:sorghum"),
    ("jowar flour", "en", "!ING:jowar"),
    ("cholam", "en", "ING:sorghum"),
    # 2. CJK substrings: the animal beats generic heads that default to pork
    ("牛肉片", "zh", "ING:beef"),
    ("羊肉片", "zh", "ING:lamb"),
    ("鸭肉", "zh", "ING:wild-duck"),
    ("鴨肉", "ja", "ING:wild-duck"),
    ("牛里脊肉", "zh", "ING:beef"),
    ("羊里脊肉", "zh", "ING:lamb"),
    ("瘦牛肉糜", "zh", "ING:beef"),
    ("鸡脯肉", "zh", "ING:chicken"),
    ("鱼肉沫", "zh", "!ING:pork"),
    ("肉末", "zh", "ING:pork"),
    # 7. fuzzy false friends
    ("leaves", "en", "!ING:leaven"),
    ("fruity", "en", "!ING:fruit"),
    ("crisco", "en", "ING:shortening"),
    ("marsala", "en", "!ING:masala"),
    ("sambal powder", "en", "!ING:sambar-powder"),
    ("pimenton", "en", "!ING:pimento"),
    ("craisins", "en", "!ING:raisin"),
    # 8. inherited aliases
    ("jalapeno pepper", "en", "ING:jalapeno"),
    ("jalapeño peppers", "en", "ING:jalapeno"),
    ("vegetable bouillon", "en", "ING:vegetable-stock"),
    ("besan flour", "en", "ING:chickpea"),
    ("besan / gram flour", "en", "ING:chickpea"),
    ("amaranth flour", "en", "ING:amaranth"),
    ("rajgiri atta", "en", "ING:amaranth"),
    ("chicken drumsticks", "en", "ING:chicken"),
    ("soy cheese", "en", "!ING:cheese"),
    # 9. texts that CulinaryDB's entity ids got wrong
    ("kaffir lime leaves", "en", "ING:kaffir-lime"),
    ("oyster sauce", "en", "ING:oyster-sauce"),
    ("red-pepper flakes", "en", "ING:chili-pepper"),
    ("szechuan peppercorns", "en", "ING:sichuan-pepper"),
    ("poblano", "en", "ING:chili-pepper"),
    ("aleppo pepper", "en", "ING:chili-pepper"),
    ("paprika", "en", "ING:paprika"),
    ("kimchi", "en", "ING:kimchi"),
    ("tuna", "en", "!ING:bonito"),
    ("cherries", "en", "!ING:plum"),
    ("oregano", "en", "!ING:marjoram"),
    # 6. lines naming several ingredients
    ("salt and pepper", "en", ["ING:salt", "ING:black-pepper"]),
    ("ginger green chillies garlic", "en", ["ING:ginger", "ING:chili-pepper", "ING:garlic"]),
    ("土豆，面粉，鸡蛋，葱花", "zh", ["ING:potato", "ING:wheat-flour", "ING:egg", "ING:scallion"]),
    ("rice bran oil", "en", "!ING:rice"),     # a product named after its ingredients stays one row
    ("onion, chopped", "en", "ING:onion"),
    ("ghee or oil", "en", "ING:ghee"),
]

JUNK = ["home", "recipes", "gardening", "about", "contact", "note: some ingredients can be replaced",
        "* 1 cup = 235 ml", "= 250 ml", "2", "3-4", "for tempering", "for the chocolate cream:", "for seasoning:",
        "#主料", "#调料", "主料", "辅料", "调料", "馅料：", "other ingredients:"]
NOT_JUNK = ["salt :", "coriander leaves:", "for deep frying oil", "onion", "鸡蛋", "鸡蛋：4个"]


def main():
    con = connect(DB_PATH, read_only=True)
    R = IngredientResolver(con)
    fails = []
    for text, lang, want in TEXT:
        parts = R.by_text_parts(text, lang)
        got = [r[0] if r else None for _, r in parts]
        if isinstance(want, list):
            ok = got == want
        elif want is None:
            ok = got == [None]
        elif want.startswith("!"):
            ok = want[1:] not in got
        else:
            ok = got == [want]
        if not ok:
            fails.append(f"{text!r} ({lang}): want {want}, got {[(p, r) for p, r in parts]}")
    for t in JUNK:
        if junk_line(t) is not None:
            fails.append(f"junk line kept: {t!r}")
    for t in NOT_JUNK:
        if junk_line(t) is None and junk_line(t.rstrip(" :：")) is None:
            fails.append(f"ingredient line dropped as junk: {t!r}")
    # 5. units
    checks = [(parse_zh("2个人份")[1] != "个", "'个' read as a unit in '个人'"),
              (parse_zh("1个半洋葱")[:2] == (1.5, "个"), "'个半' not read as 1.5 pieces"),
              (grams_of(2, "小勺") == 10 and grams_of(1, "汤匙") == 15, "Chinese spoon units"),
              (irn_name("Avial Recipe - Kerala Style Aviyal Recipe - How to make Avial") == "Avial", "IRN SEO name"),
              (irn_name("Varavarasi Recipe | VaraPayiru Recipe") == "Varavarasi", "IRN name with '|'"),
              (not xcf_has("川", "川贝炖雪梨") and xcf_has("川", "川味回锅肉"), "川贝 is not Sichuan")]
    fails += [msg for ok, msg in checks if not ok]
    n = len(TEXT) + len(JUNK) + len(NOT_JUNK) + len(checks)
    print(f"{n - len(fails)}/{n} checks pass ({DB_PATH})")
    for f in fails:
        print("  FAIL", f)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
