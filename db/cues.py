"""Cultural-cue and diet keyword flags for the patient-case table (Questions/Q7 Cultural cues in evaluation datasets.md).

`tag(df)` adds the flags to a case table and is called by db/cases.py, so the columns are part of
db/export/cases.parquet. Run on its own to count them:

  uv run db/cues.py                  # Markdown table of cases with each cue type, per dataset
  uv run db/cues.py --examples 5     # also print matched snippets per dataset and cue type (to check precision)

A cue is a pattern match in the `case` text (what the model sees), counted once per case. The patterns are keyword
lists for English, Russian, Kazakh, Chinese, Arabic and Persian, chosen by the row's `lang`: they are a lower bound
on recall and they are not disambiguated, so read the examples before quoting a number. Cue types:

  place       a country, a nationality word or a migration / travel phrase
  ethnicity   a stated race or ethnic group
  religion    a religion or a religious practice (Ramadan fasting, halal…)
  habit       a culture-linked substance or habit (betel, khat, waterpipe, kava…; Chinese: taste preferences such
              as 嗜食辛辣 and the solar term 节气 of onset)
  food        a food or dish tied to a cuisine (kimchi, kumys, ghee…), not generic foods; in FAM-Bench and NGQA,
              whose case is a dish, also a nationality word in the dish text ("Mexican style", "Persian salad")
  tradmed     traditional or folk medicine used by the patient or asked about (herbal remedy, cupping, TCM…)

`diet` is a separate, broader flag: any food, diet, supplement or herb word in the case text.
"""
import argparse, os, re, sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export import OUT  # noqa: E402

# Country names that are also common words or first names are left out (Turkey, Chad, Jordan, Georgia, Guinea, Niger).
COUNTRIES = """Afghanistan Albania Algeria Angola Argentina Armenia Australia Austria Azerbaijan Bahrain Bangladesh
Belarus Belgium Bolivia Brazil Bulgaria Cambodia Cameroon Canada Chile China Colombia Croatia Cuba Cyprus Denmark
Ecuador Egypt Eritrea Estonia Ethiopia Finland France Germany Ghana Greece Guatemala Haiti Honduras Hungary Iceland
India Indonesia Iran Iraq Ireland Israel Italy Jamaica Japan Kazakhstan Kenya Korea Kuwait Kyrgyzstan Laos Latvia
Lebanon Libya Lithuania Malaysia Mali Mexico Moldova Mongolia Morocco Mozambique Myanmar Nepal Netherlands Nicaragua
Nigeria Norway Oman Pakistan Palestine Panama Paraguay Peru Philippines Poland Portugal Qatar Romania Russia Rwanda
Senegal Serbia Singapore Slovakia Slovenia Somalia Spain Sudan Sweden Switzerland Syria Taiwan Tajikistan Tanzania
Thailand Tunisia Turkmenistan Uganda Ukraine Uruguay Uzbekistan Venezuela Vietnam Yemen Zambia Zimbabwe""".split()
COUNTRIES += ["Saudi Arabia", "Sri Lanka", "South Africa", "United Arab Emirates", "United Kingdom", "United States",
              "New Zealand", "Hong Kong", "Puerto Rico", "Dominican Republic", "Costa Rica", "El Salvador",
              "Sierra Leone", "Burkina Faso", "Ivory Coast", "Papua New Guinea", "Türkiye", "Middle East",
              "Central Asia", "Southeast Asia", "South Asia", "East Asia", "sub-Saharan Africa", "Latin America",
              "Caribbean"]
# Nationality words as used for people ("a 45-year-old Japanese man"); cuisine uses are caught too ("Mexican rice").
DEMONYMS = """Afghan Algerian Argentin(?:e|ian) Armenian Australian Bangladeshi Brazilian British Cambodian Chilean
Chinese Colombian Cuban Dutch Egyptian Eritrean Ethiopian Filipin[oa] Ghanaian Greek Guatemalan Haitian Indian
Indonesian Iranian Iraqi Israeli Italian Jamaican Japanese Jordanian Kazakh Kenyan Korean Kuwaiti Kyrgyz Lebanese
Libyan Malaysian Mexican Mongolian Moroccan Nepal(?:i|ese) Nigerian Pakistani Palestinian Persian Peruvian Polish
Portuguese Puerto\\s+Rican Romanian Russian Saudi Somali Spanish Sri\\s+Lankan Sudanese Syrian Taiwanese Tajik Thai
Tunisian Turkish Ukrainian Uzbek Vietnamese Yemeni Emirati Qatari Omani Bahraini Tibetan Uyghur Punjabi Bengali
Tamil Gujarati Kurdish Hmong Samoan Tongan""".split()

EN = {
    "place": [r"\b(?:%s)\b" % "|".join(re.escape(c) for c in COUNTRIES),
              r"\b(?:%s)\b" % "|".join(DEMONYMS),
              r"(?i:\b(?:immigra\w+|emigrat\w+|refugee|migrant|asylum seeker|originally from|native of|"
              r"travel(?:l)?ed (?:to|from)|returned from (?:a trip|travel)|recent travel))|\b[Bb]orn in [A-Z]"],
    "ethnicity": [r"\bAfrican[- ]American|\b(?:Black|White|black|white) (?:man|woman|male|female|boy|girl|patient|"
                  r"gentleman|lady)\b|\b(?:Caucasian|Hispanic|Latin[oa]|Asian|Native American|American Indian|"
                  r"Alaska Native|Pacific Islander|Ashkenazi|Sephardi\w*|Arab|Bedouin|Aboriginal|Indigenous|"
                  r"First Nations|Maori|Māori|Inuit|Roma|Han)\b",
                  r"(?i)\b(?:ethnicity|ethnic (?:group|origin|background)|of \w+ (?:descent|ancestry|heritage))\b"],
    "religion": [r"(?i)\b(?:ramadan|muslim|islam\w*|hindu\w*|buddhis\w+|jewish|judaism|sikh\w*|jain\w*|"
                 r"jehovah'?s witness|christian|catholic|orthodox christian|amish|mennonite|halal|haram|kosher (?:diet|food)|"
                 r"religious (?:fast\w*|belief\w*|reason\w*|practice\w*)|yom kippur|pilgrim\w*|hajj|umrah|mosque)\b"],
    "habit": [r"(?i)\b(?:betel|areca|paan|gutk[ah]|khat|qat\b|hookah|shisha|water[- ]?pipe|narghile|kava|kratom|"
              r"yerba mate|coca lea\w+|snus|naswar|nasvay|toddy|palm wine|kumis|koumiss|kumys|chewing tobacco)\b"],
    "food": [r"(?i)\b(?:kimchi|sushi|sashimi|miso|natto|tofu|tempeh|soy sauce|congee|dim sum|ramen|pho\b|curry|"
             r"biryani|chapati|roti\b|naan|dal\b|dhal|ghee|paneer|masala|chutney|samosa|idli|dosa|hummus|falafel|"
             r"tahini|shawarma|kebab|kabsa|couscous|tagine|injera|fufu|cassava|plantain|yam\b|tortilla|taco|"
             r"burrito|tamale|enchilada|salsa|pilaf|plov|pilau|beshbarmak|baursak|borscht|pelmeni|kefir|ayran|"
             r"lassi|camel milk|raw (?:fish|milk|meat|pork|liver)|unpasteuri[sz]ed|bush ?meat|star ?fruit|"
             r"bitter melon|fava beans?|broad beans?|ackee|durian|jackfruit|seaweed|fish sauce|sticky rice|"
             r"fermented (?:fish|soy\w*|milk|food\w*)|green tea|matcha|turmeric|fenugreek|black seed|nigella|"
             r"ginseng|goji|jujube)\b"],
    "tradmed": [r"(?i)\b(?:traditional (?:chinese |korean |indian |african |tibetan |persian |arabic )?"
                r"(?:medicine\w*|healer\w*|remed\w+|herb\w*)|herbal (?:medicine\w*|remed\w+|supplement\w*|tea\w*|"
                r"product\w*|preparation\w*|mixture\w*|concoction\w*|decoction\w*)|chinese herb\w*|ayurved\w+|"
                r"unani|kampo|siddha|folk (?:medicine|remed\w+|healer\w*)|home remed\w+|acupunctur\w+|"
                r"(?:wet |dry )?cupping therapy|wet cupping|hijama|moxibustion|gua ?sha|homeopath\w+|naturopath\w+|faith healer\w*|shaman\w*|TCM|"
                r"decoction\w*|alternative medicine\w*|complementary and alternative)\b"],
}
RU = {
    "place": [r"(?i)\b(?:казахстан\w*|киргизи\w*|кыргызстан\w*|узбекистан\w*|таджикистан\w*|приехал\w* из|"
              r"вернул\w+ из|мигрант\w*)\b"],
    "ethnicity": [r"(?i)\b(?:национальност\w+|казах\w*|киргиз\w*|кыргыз\w*|узбек\w*|таджик\w*|татар\w*|бурят\w*|"
                  r"якут\w*|цыган\w*)\b"],
    "religion": [r"(?i)\b(?:рамадан\w*|мусульман\w*|православн\w+|соблюда\w+ пост|великий пост|в пост\b|халял\w*)"],
    "habit": [r"(?i)\b(?:насвай|кальян\w*|кумыс\w*|самогон\w*)\b"],
    "food": [r"(?i)\b(?:бешбармак\w*|плов\w*|манты|лагман\w*|шашлык\w*|сало\b|квас\w*|кефир\w*|пельмен\w*|борщ\w*|"
             r"строганин\w*|сыр(?:ой|ую|ая) рыб\w+|речн\w+ рыб\w+|вялен\w+ рыб\w+|солен\w+ рыб\w+)\b"],
    "tradmed": [r"(?i)\b(?:народн\w+ (?:медицин\w+|средств\w+|метод\w+)|знахар\w*|трав(?:ы|ами|яной|яные|яным\w*) "
                r"|отвар\w*|насто(?:й|ем|я|йк\w+)\b|гомеопат\w+|иглоукалыван\w+|банки ставил\w*|прополис\w*|мумие)"],
}
ZH = {
    "place": [r"(?:籍贯|出生于|生于(?!久居|原籍)|北京|上海|广东|广州|四川|湖南|湖北|河南|河北|山东|山西|陕西|江苏|浙江|"
              r"福建|云南|贵州|广西|新疆|西藏|内蒙古|东北|黑龙江|吉林|辽宁|安徽|江西|甘肃|青海|宁夏|海南|台湾|香港)"],
    "ethnicity": [r"(?:民族|汉族|回族|藏族|维吾尔|蒙古族|壮族|苗族|满族|朝鲜族|哈萨克族)"],
    "religion": [r"(?:清真|穆斯林|伊斯兰|佛教|信佛|道教|基督教|天主教|吃斋|斋戒)"],
    "habit": [r"(?:槟榔|嗜茶|喜食|嗜食|偏嗜|喜饮|嗜饮|节气)"],
    "food": [r"(?:火锅|辣椒|白酒|黄酒|米酒|红枣|枸杞|生姜|羊肉|狗肉|鱼生|生鱼|腌制|咸菜|腊肉|豆腐|茶叶|药膳|食疗)"],
    # both sets are TCM benchmarks: these count explicit mentions, the whole dataset is traditional medicine anyway
    "tradmed": [r"(?:中药|中医|汤剂|方剂|针灸|艾灸|拔罐|推拿|刮痧|膏方|偏方|草药|舌|脉)"],
}
AR = {
    "place": [r"(?:السعودية|مصر|الأردن|الإمارات|الكويت|قطر|البحرين|اليمن|العراق|سوريا|لبنان|فلسطين|المغرب|"
              r"الجزائر|تونس|ليبيا|السودان|سافرت|مسافر|مغترب)"],
    "ethnicity": [r"(?:قبيلة|بدوي)"],
    "religion": [r"(?:رمضان|صيام|صائم|الصوم|أصوم|الحج|العمرة|حلال|حرام|رقية)"],
    "habit": [r"(?:شيشة|الشيشة|أرجيلة|نرجيلة|القات|معسل|سواك)"],
    "food": [r"(?:تمر|التمر|قهوة عربية|القهوة|شاي|لبن|زيت الزيتون|حمص|كبسة|عسل|العسل|حليب الإبل|زعتر)"],
    "tradmed": [r"(?:أعشاب|الأعشاب|عشبة|طب بديل|الطب البديل|طب شعبي|حجامة|الحجامة|حبة البركة|الحبة السوداء|قرفة|"
                r"القرفة|زنجبيل|الزنجبيل|حلبة|الحلبة|كركم|ميرمية|يانسون|بابونج|خل التفاح)"],
}
KK = {
    "place": [r"(?i)(?:қазақстан\w*|астана\w*|алматы\w*|шымкент\w*)"],
    "ethnicity": [r"(?i)(?:қазақ\b|қазақтар\w*|ұлты)"],
    "religion": [r"(?i)(?:ораза\w*|рамазан\w*|мұсылман\w*|намаз\w*|халал\w*)"],
    "habit": [r"(?i)(?:насыбай\w*|қымыз\w*|шұбат\w*)"],
    "food": [r"(?i)(?:бешбармақ\w*|бауырсақ\w*|қазы\b|құрт\b|палау\w*|наурыз[- ]көже|айран\w*|ет тағам\w*)"],
    "tradmed": [r"(?i)(?:халық емі|халықтық медицина\w*|шөп\w* шай\w*|емдік шөп\w*)"],
}
FA = {
    "place": [r"(?:ایران|تهران|مشهد|اصفهان|شیراز|تبریز|افغانستان|عراق|خارج از کشور|شهرستان|روستا)"],
    "ethnicity": [r"(?:قومیت|کرد هستم|ترک هستم|لر هستم|بلوچ|عرب هستم|افغان هستم)"],
    "religion": [r"(?:رمضان|ماه مبارک|روزه‌داری|روزه داری|روزه دار|روزه بگیرم|روزه بگیرد|روزه بگیره|روزه گرفتن|"
                 r"روزه هستم|نماز|حلال|حرام)"],
    "habit": [r"(?:قلیان|ناس|تریاک)"],
    "food": [r"(?:کله پاچه|آبگوشت|دوغ|کشک|ترشی|خرما|زرشک|سماق|نان سنگک)"],
    "tradmed": [r"(?:طب سنتی|طب اسلامی|داروی گیاهی|داروهای گیاهی|دارو گیاهی|دمنوش|عرقیات|عرق نعنا|حجامت|زالو|عطاری|"
                r"عطار|طبع گرم|طبع سرد|جوشانده|سیاه دانه|سیاهدانه|گل گاوزبان|خاکشیر)"],
}
LEX = {"en": EN, "ru": RU, "kk": KK, "zh": ZH, "ar": AR, "fa": FA}
WHOLE_WORD = {"ar", "fa"}  # short Arabic-script words occur inside longer ones (تمر is inside مستمر)
CUES = ["place", "ethnicity", "religion", "habit", "food", "tradmed"]
DISH = {"FAM-Bench", "NGQA"}  # the case is a dish + a condition: nationality words name the cuisine, not a patient

# food, diet, supplement or herb content in the case text (broader than the cuisine-linked `food` cue)
DIET = {
    "en": r"(?i)\b(?:diet\w*|food\w*|eat(?:s|ing|en)?|ate|meals?|nutrition\w*|malnutrition|vitamin\w*|supplements|(?:dietary|herbal|nutritional) supplement\w*|"
          r"herb\w*|vegetarian|vegan|milk|dairy|meat|fish|seafood|fruits?|vegetables?|grapefruit|juice|caffeine|"
          r"coffee|tea|honey|ramadan|fasting (?:during|month|for)|consum\w+ (?:of )?(?:raw|unpasteuri[sz]ed|large amounts)|breastfe\w+|"
          r"formula[- ]fed|gluten|lactose)\b",
    "ru": r"(?i)\b(?:диет\w*|питани\w+|пищ[аеиу]\w*|продукт\w* питани\w+|молок\w+|молочн\w+|мяс\w+|рыб[аыуе]\w*|"
          r"фрукт\w*|овощ\w*|витамин\w*|БАД\w*|трав(?:ы|ами|ян\w+)|фитотерапи\w+|чай|чая|кофе|голодани\w+|жирн\w+ пищ\w+|остр\w+ пищ\w+)\b",
    "kk": r"(?i)(?:тамақ\w*|диета\w*|тағам\w*|сүт\w*|ет\b|дәрумен\w*)",
    "zh": r"(?:饮食|食物|进食|忌口|忌食|食疗|膳食|药膳|辛辣|油腻|生冷|饮酒|茶|牛奶|海鲜|水果|蔬菜|肥甘)",
    "ar": r"(?:حمية|رجيم|غذاء|الغذاء|غذائي|أكل|الأكل|اكل|طعام|الطعام|وجبة|وجبات|فيتامين|فيتامينات|مكمل|مكملات|أعشاب|"
          r"الأعشاب|حليب|قهوة|القهوة|شاي|الشاي|صيام|عسل|تمر|قرفة|القرفة|زنجبيل)",
    "fa": r"(?:رژیم|غذا|غذایی|تغذیه|خوراکی|ویتامین|مکمل|گیاهی|دمنوش|شیر|چای|قهوه|میوه|لبنیات|عسل|روزه داری|رمضان|روزه گرفتن|روزه بگیرم)",
}


def _wrap(p, lang):
    return rf"(?<!\w){p}(?!\w)" if lang in WHOLE_WORD else p


def first_match(text, regs):
    for r in regs:
        m = r.search(text)
        if m:
            return m
    return None


def tag(df, keep_matches=False):
    """Add `cue_<type>` booleans and `diet`, both read from `case`, to a case table with columns `source`, `lang`,
    `case`. With keep_matches, also `m_<type>`: the matched text, for explanations."""
    df = df.copy()
    for cue in CUES:
        df[f"cue_{cue}"] = False
        df[f"m_{cue}"] = None
    df["diet"] = False
    for (source, lang), part in df.groupby(["source", "lang"]):
        lex = LEX.get(lang, EN)
        for cue in CUES:
            regs = [re.compile(_wrap(p, lang)) for p in lex[cue]]
            ms = part["case"].map(lambda t: first_match(t, regs))
            to = "food" if source in DISH and cue in ("place", "ethnicity") else cue
            hit = ms.dropna()
            df.loc[hit.index, f"cue_{to}"] = True
            df.loc[hit.index, f"m_{to}"] = df.loc[hit.index, f"m_{to}"].fillna(hit.map(lambda m: m.group(0)))
            df.loc[hit.index, f"_span_{cue}"] = hit.map(lambda m: m.start())
        rg = re.compile(_wrap(DIET.get(lang, DIET["en"]), lang))
        df.loc[part.index, "diet"] = part["case"].map(lambda t: bool(rg.search(t)))
    spans = [c for c in df.columns if c.startswith("_span_")]
    if keep_matches:
        return df.rename(columns={c: c[1:] for c in spans})
    return df.drop(columns=spans + [f"m_{c}" for c in CUES])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--examples", type=int, default=0)
    a = ap.parse_args()
    df = pd.read_parquet(f"{OUT}/cases.parquet", columns=["case_id", "source", "lang", "case"])
    df = tag(df, keep_matches=True)
    cols = [f"cue_{c}" for c in CUES]
    df["any"] = df[cols].any(axis=1)
    show = cols + ["any", "diet"]
    print("| Dataset | Cases | " + " | ".join(c.replace("cue_", "") for c in show) + " |\n|---|---|" + "---|" * len(show))
    for source, part in list(df.groupby("source")) + [("All", df)]:
        cells = [f"{part[c].sum():,} ({part[c].mean():.1%})" for c in show]
        print(f"| {source} | {len(part):,} | " + " | ".join(cells) + " |")
    if a.examples:
        for source, part in df.groupby("source"):
            for cue in CUES:
                col = f"span_{cue}"
                if col not in part or part[col].notna().sum() == 0:
                    continue
                print(f"\n### {source} / {cue}")
                for _, r in part[part[col].notna()].sample(min(a.examples, part[col].notna().sum()), random_state=0).iterrows():
                    i = int(r[col])
                    print("- …" + r["case"][max(0, i - 50):i + 60].replace("\n", " ") + "…")


if __name__ == "__main__":
    main()
