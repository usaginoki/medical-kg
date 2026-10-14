"""Cultural-cue and diet keyword flags for the patient-case table (Questions/Q7 Cultural cues in evaluation datasets.md).

`tag(df)` adds the flags to a case table and is called by db/cases.py, so the columns are part of
db/export/cases.parquet. Run on its own to count them:

  uv run db/cues.py                  # Markdown table of cases with each cue type, per dataset
  uv run db/cues.py --examples 5     # also print matched snippets per dataset and cue type (to check precision)

A cue is a pattern match in the `case` text (what the model sees), counted once per case. The patterns are keyword
lists for English, Russian, Kazakh, Chinese, Arabic and Persian, chosen by the row's `lang`: they are a cheap first
screen (a lower bound on recall, not disambiguated), meant to be checked by a stricter step (db/llm/). Cue types:

  place       a country, city, nationality word or a migration / travel phrase
  ethnicity   a stated race or ethnic group
  religion    a religion or a religious practice (Ramadan fasting, halal, prayer, festivals…)
  habit       a culture-linked substance or habit (betel, khat, waterpipe, kava…; Chinese: taste preferences such
              as 嗜食辛辣)
  food        a food or dish tied to a cuisine (kimchi, kumys, ghee…), not generic foods; in FAM-Bench and NGQA,
              whose case is a dish, also a nationality word in the dish text ("Mexican style", "Persian salad")
  tradmed     traditional or folk medicine used by the patient or asked about (herbal remedy, cupping, TCM…)

`diet` is a separate, broader flag: any food, diet, supplement or herb word in the case text.

Before matching, medical terms that contain a cue word are blanked out (STOP: India ink, Japanese encephalitis, the
FISH test, 食物过敏史…; in the dish datasets also ingredient names such as Greek yogurt). A match is *negated* when a
negation stands before it in the same clause ("denied recent travel", 否认…, не…) or a denial follows it ("travel
history was negative", "выезд за границу отр."); negated matches do not set the flag and are listed in
`cues_negated`. Race words and bare country / nationality / city names are *weak* cues (usually incidental: "a
71-year-old Caucasian man"); travel or migration phrases, specific ethnic groups, religion, habits, cuisine foods and
traditional medicine are *strong*. `cue_strength` is strong / weak / none.
"""
import argparse, os, re, sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export import OUT  # noqa: E402


def W(p):
    """Mark a pattern as a weak cue (incidental unless a stricter check says otherwise)."""
    return ("weak", p)


# Country names that are also common words or first names are left out (Turkey, Chad, Jordan, Georgia, Guinea, Niger).
COUNTRIES = """Afghanistan Albania Algeria Angola Argentina Armenia Australia Austria Azerbaijan Bahrain Bangladesh
Belarus Belgium Benin Bhutan Bolivia Bosnia Botswana Brazil Brunei Bulgaria Burundi Cambodia Cameroon Canada Chile
China Colombia Congo Croatia Cuba Cyprus Czechia Denmark Djibouti Ecuador Egypt Eritrea Estonia Ethiopia Fiji Finland
France Gabon Gambia Germany Ghana Greece Guatemala Haiti Honduras Hungary Iceland India Indonesia Iran Iraq Ireland
Israel Italy Jamaica Japan Kazakhstan Kenya Korea Kuwait Kyrgyzstan Laos Latvia Lebanon Lesotho Liberia Libya
Lithuania Madagascar Malawi Malaysia Maldives Mali Mauritania Mexico Moldova Mongolia Morocco Mozambique Myanmar Namibia
Nepal Netherlands Nicaragua Nigeria Norway Oman Pakistan Palestine Panama Paraguay Peru Philippines Poland Portugal
Qatar Romania Russia Rwanda Senegal Serbia Singapore Slovakia Slovenia Somalia Spain Sudan Sweden Switzerland Syria
Taiwan Tajikistan Tanzania Thailand Togo Trinidad Tunisia Turkmenistan Uganda Ukraine Uruguay Uzbekistan Venezuela
Vietnam Yemen Zambia Zimbabwe""".split()
COUNTRIES += ["Saudi Arabia", "Sri Lanka", "South Africa", "United Arab Emirates", "United Kingdom", "United States",
              "New Zealand", "Hong Kong", "Puerto Rico", "Dominican Republic", "Costa Rica", "El Salvador",
              "Sierra Leone", "Burkina Faso", "Ivory Coast", "Papua New Guinea", "Czech Republic", "East Timor",
              "Türkiye", "Middle East", "Central Asia", "Southeast Asia", "South Asia", "East Asia", "West Africa",
              "East Africa", "North Africa", "sub-Saharan Africa", "Latin America", "Caribbean", "Gulf states"]
# Cities of the priority regions and other large cities that case reports name as a place of residence or travel.
CITIES = ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Wuhan", "Chengdu", "Tokyo", "Osaka", "Seoul", "Busan",
          "Bangkok", "Jakarta", "Manila", "Hanoi", "Ho Chi Minh City", "Kuala Lumpur", "Mumbai", "Bombay", "Delhi",
          "New Delhi", "Kolkata", "Calcutta", "Chennai", "Bangalore", "Bengaluru", "Hyderabad", "Karachi", "Lahore",
          "Islamabad", "Dhaka", "Kathmandu", "Colombo", "Kabul", "Tehran", "Mashhad", "Isfahan", "Baghdad", "Basra",
          "Damascus", "Beirut", "Amman", "Jerusalem", "Riyadh", "Jeddah", "Mecca", "Makkah", "Medina", "Dubai",
          "Abu Dhabi", "Sharjah", "Doha", "Manama", "Muscat", "Kuwait City", "Sanaa", "Cairo", "Alexandria",
          "Khartoum", "Casablanca", "Tunis", "Algiers", "Istanbul", "Ankara", "Almaty", "Astana", "Shymkent",
          "Tashkent", "Samarkand", "Bishkek", "Osh", "Dushanbe", "Ashgabat", "Ulaanbaatar", "Lagos", "Nairobi",
          "Addis Ababa", "Accra", "Kinshasa"]
# Nationality words as used for people ("a 45-year-old Japanese man"); cuisine uses are caught too ("Mexican rice").
DEMONYMS = """Afghan Albanian Algerian Argentin(?:e|ian) Armenian Australian Austrian Bangladeshi Belgian Bosnian
Brazilian British Cambodian Canadian Chilean Chinese Colombian Congolese Croatian Cuban Czech Danish Dutch Egyptian
Eritrean Ethiopian Filipin[oa] Finnish French German Ghanaian Greek Guatemalan Haitian Hungarian Indian Indonesian
Iranian Iraqi Irish Israeli Italian Jamaican Japanese Jordanian Kazakh Kenyan Korean Kuwaiti Kyrgyz Lebanese Libyan
Malaysian Mexican Mongolian Moroccan Nepal(?:i|ese) Nigerian Norwegian Pakistani Palestinian Persian Peruvian Polish
Portuguese Puerto\\s+Rican Romanian Russian Saudi Scottish Serbian Somali Spanish Sri\\s+Lankan Sudanese Swedish
Swiss Syrian Taiwanese Tajik Thai Tunisian Turkish Ukrainian Uzbek Vietnamese Yemeni Emirati Qatari Omani Bahraini Tibetan
Uyghur Punjabi Bengali Tamil Gujarati Kurdish Hmong Samoan Tongan Middle\\s+Eastern Mediterranean Cajun Creole
Caribbean Levantine""".split()
_names = lambda xs: r"\b(?:%s)\b" % "|".join(re.escape(x) for x in xs)  # noqa: E731

EN = {
    "place": [W(_names(COUNTRIES)), W(r"\b(?:%s)\b" % "|".join(DEMONYMS)), W(_names(CITIES)),
              W(r"\b[A-Z][a-z]+-born\b"),
              r"(?i:\b(?:immigra\w+|emigrat\w+|refugee\w*|migrant\w*|asylum seeker\w*|originally from|native of|"
              r"travel(?:l)?(?:ed|ing)? (?:to|from|in|abroad)|travel history|trip (?:to|abroad)|returned from|"
              r"recent(?:ly)? (?:travel\w*|trip\w*|visit\w*|return\w*)|visit(?:ed|ing) (?:family|relatives|friends|"
              r"his|her|their) (?:in|home)|resident of|endemic (?:area|region|zone|for)|moved (?:here )?from))\b"
              r"|\b[Bb]orn in [A-Z]|\blived (?:in|for \w+ years in) [A-Z]"],
    "ethnicity": [W(r"\bAfrican[- ]American|\b(?:Black|White|black|white) (?:man|woman|male|female|boy|girl|patient|"
                    r"gentleman|lady|adult|child|infant)\b|\b(?:Caucasian|Hispanic|Latin[oa]|Latinx|Asian(?:[- ]American)?)\b"),
                  r"\b(?:Native American|American Indian|Alaska(?:n)? Native|Pacific Islander|Native Hawaiian|Ashkenazi|"
                  r"Sephardi\w*|Arab|Bedouin|Aboriginal|Indigenous|First Nations|Maori|Māori|Inuit|Roma|Han|"
                  r"Afro-Caribbean|Polynesian|Melanesian|Pashtun|Berber|Amazigh|Fulani|Yoruba|Igbo|Hausa)\b",
                  r"(?i)\b(?:ethnicity|ethnic (?:group|origin|background|minority)|of \w+ (?:descent|ancestry|heritage|"
                  r"origin))\b"],
    "religion": [r"(?i)\b(?:ramadan|muslim|islam\w*|hindu\w*|buddhis\w+|jewish|judaism|sikh\w*|jain\w*|"
                 r"jehovah'?s witness|christian|catholic|orthodox christian|amish|mennonite|halal|haram|kosher (?:diet|food)|"
                 r"religious (?:fast\w*|belief\w*|reason\w*|practice\w*|festival\w*|ceremon\w*|ritual\w*)|yom kippur|"
                 r"pilgrim\w*|hajj|umrah|mosque|church|prayers?|praying|daily prayer\w*|fasting month|"
                 r"lunar new year|chinese new year|nowruz|navratri|hanukkah|ritual (?:bath|fast\w*|circumcision))\b",
                 r"\b(?:Lent|Eid(?:[- ]al[- ]\w+)?|Diwali|Passover|Sabbath|Shabbat|Easter|Christmas)\b"],
    "habit": [r"(?i)\b(?:betel|areca|paan|gutk[ah]|khat|qat\b|hookah|shisha|water[- ]?pipe|narghile|kava|kratom|"
              r"yerba mate|coca lea\w+|snus|naswar|nasvay|toddy|palm wine|kumis|koumiss|kumys|chewing tobacco|"
              r"strict vegetarian|lifelong vegetarian|lacto-?vegetarian|vegan diet|geophagia|pica for (?:clay|earth))\b"],
    "food": [r"(?i)\b(?:kimchi|sushi|sashimi|miso|natto|tofu|tempeh|soy sauce|congee|dim sum|ramen|pho\b|curry|"
             r"biryani|chapati|roti\b|naan|dal\b|dhal|ghee|paneer|masala|chutney|samosa|idli|dosa|hummus|falafel|"
             r"tahini|shawarma|kebab|kabsa|couscous|tagine|injera|fufu|cassava|plantain|yam\b|tortilla|taco|"
             r"burrito|tamale|enchilada|quesadilla|empanada|menudo|pozole|pupusa|salsa|pilaf|plov|pilau|beshbarmak|"
             r"baursak|borscht|pelmeni|pierogi|kefir|ayran|lassi|camel milk|raw (?:fish|milk|meat|pork|liver)|"
             r"unpasteuri[sz]ed|bush ?meat|star ?fruit|bitter melon|fava beans?|broad beans?|ackee|durian|jackfruit|"
             r"seaweed|fish sauce|sticky rice|fermented (?:fish|soy\w*|milk|food\w*)|green tea|matcha|turmeric|"
             r"fenugreek|black seed|nigella|ginseng|goji|jujube|gyros?|baklava|moussaka|spanakopita|paella|risotto|"
             r"gnocchi|pesto|kimbap|bibimbap|bulgogi|teriyaki|tempura|udon|soba|pad thai|laksa|rendang|satay|adobo|"
             r"lumpia|pancit|jollof|gumbo|jambalaya|tzatziki|dolma|halva|lavash|manti|lagman|shashlik|kumquat)\b"],
    "tradmed": [r"(?i)\b(?:traditional (?:chinese |korean |indian |african |tibetan |persian |arabic )?"
                r"(?:medicine\w*|healer\w*|remed\w+|herb\w*)|herbal (?:medicine\w*|remed\w+|supplement\w*|tea\w*|"
                r"product\w*|preparation\w*|mixture\w*|concoction\w*|decoction\w*|drug\w*|formula\w*|extract\w*)|"
                r"herbalist\w*|chinese herb\w*|ayurved\w+|unani|kampo|siddha|folk (?:medicine|remed\w+|healer\w*)|"
                r"home remed\w+|acupunctur\w+|(?:wet |dry )?cupping therapy|wet cupping|hijama|moxibustion|gua ?sha|"
                r"homeopath\w+|naturopath\w+|faith healer\w*|shaman\w*|TCM|decoction\w*|alternative medicine\w*|"
                r"complementary and alternative|bone ?setter\w*|native healer\w*|witch ?doctor\w*)\b",
                # herbal products named in case reports (hepatotoxicity, interactions)
                r"(?i)\b(?:tripterygium|ginkgo|st\.? john'?s wort|hypericum|echinacea|black cohosh|ephedra|ma huang|"
                r"comfrey|aristolochi\w+|germander|chaparral|ashwagandha|garcinia|yohimbe|valerian|saw palmetto|"
                r"milk thistle|silymarin|green tea extract|senna|cascara|licorice root|liquorice|pennyroyal|"
                r"noni juice|herbalife|kampo medicine|jamu)\b"],
}
RU = {
    "place": [W(r"(?i)\b(?:казахстан\w*|киргизи\w*|кыргызстан\w*|узбекистан\w*|таджикистан\w*|туркмени\w*|"
                r"азербайджан\w*|армени\w+|грузи[июяей]\w*|кавказ\w*|средн\w+ ази\w+|турци\w+|египт\w+|египет|"
                r"кита[йяею]\w*|таиланд\w*|тайланд\w*|вьетнам\w*|инди[июяей]\b|монголи\w+|оаэ|эмират\w*)\b"),
              r"(?i)\b(?:приехал\w* из|вернул\w+ из|мигрант\w*|переехал\w* из|выезд\w* за (?:границу|пределы)|"
              r"за границ\w+ (?:был\w*|находил\w*|отдыхал\w*)|ездил\w* (?:в|на) отдых|командировк\w+)\b"],
    "ethnicity": [r"(?i)\b(?:национальност\w+|казах\w*|киргиз\w*|кыргыз\w*|узбек\w*|таджик\w*|татар\w*|бурят\w*|"
                  r"якут\w*|цыган\w*|хант\w*|манси|ненц\w*|селькуп\w*)\b"],
    "religion": [r"(?i)\b(?:рамадан\w*|ураза\w*|мусульман\w*|православн\w+|соблюда\w+ пост|держ\w+ пост|великий пост|"
                 r"в пост\b|во время поста|после поста|постит\w*|постил\w*|"
                 r"халял\w*|намаз\w*)"],
    "habit": [r"(?i)\b(?:насвай|кальян\w*|кумыс\w*|самогон\w*|чифир\w*)\b"],
    "food": [r"(?i)\b(?:бешбармак\w*|плов(?:а|е|ом|у)?|манты|лагман\w*|шашлык\w*|сало\b|квас\w*|кефир\w*|пельмен\w*|"
             r"борщ\w*|строганин\w*|сыр(?:ой|ую|ая) рыб\w+|речн\w+ рыб\w+|вялен\w+ рыб\w+|солен\w+ рыб\w+|"
             r"черемш\w+|кедров\w+ орех\w*)\b"],
    "tradmed": [r"(?i)\b(?:народн\w+ (?:медицин\w+|средств\w+|метод\w+)|знахар\w*|трав(?:ы|ами|яной|яные|яным\w*) "
                r"|отвар(?:ы|ом|ов|а)? (?:трав\w*|шиповник\w*|ромашк\w*|зверобо\w*|календул\w*|лекарственн\w*|"
                r"корн\w*|лист\w*|из трав\w*)|насто(?:й|ем|я|йк\w+)\b (?:трав\w*|на|из)|гомеопат\w+|"
                r"иглоукалыван\w+|банки ставил\w*|прополис\w*|мумие|фитотерапи\w+)"],
}
ZH = {
    "place": [W(r"(?:籍贯|出生于|(?<!发)生于(?!久居|原籍)|北京|上海|广东|广州|四川|湖南|湖北|河南|河北|山东|山西|陕西|"
                r"江苏|浙江|福建|云南|贵州|广西|新疆|西藏|内蒙古|东北|黑龙江|吉林|辽宁|安徽|江西|甘肃|青海|宁夏|海南|"
                r"台湾|香港)"), r"(?:久居|移居|旅居|外出旅游|出差|从外地)"],
    "ethnicity": [r"(?:民族|汉族|回族|藏族|维吾尔|蒙古族|壮族|苗族|满族|朝鲜族|哈萨克族)"],
    "religion": [r"(?:清真|穆斯林|伊斯兰|佛教|信佛|道教|基督教|天主教|吃斋|斋戒)"],
    "habit": [r"(?:槟榔|嗜茶|喜食|嗜食|偏嗜|喜饮|嗜饮)"],
    "food": [r"(?:火锅|辣椒|白酒|黄酒|米酒|红枣|枸杞|生姜|羊肉|狗肉|鱼生|生鱼|腌制|咸菜|腊肉|豆腐|茶叶|药膳|食疗)"],
    # explicit traditional-medicine words only: 舌 / 脉 (tongue, pulse findings) are in every TCM record
    "tradmed": [r"(?:中药|中医|中成药|汤剂|方剂|针灸|艾灸|拔罐|推拿|刮痧|膏方|偏方|草药|经方|验方|食疗)"],
}
AR = {
    "place": [W(r"(?:السعودية|مصر|الأردن|الإمارات|الكويت|قطر|البحرين|اليمن|العراق|سوريا|لبنان|فلسطين|المغرب|"
                r"الجزائر|تونس|ليبيا|السودان|الخليج)"), r"(?:سافرت|مسافر|سفر|مغترب|غربة)"],
    "ethnicity": [r"(?:قبيلة|بدوي)"],
    "religion": [r"(?:رمضان|صيام|صائم|الصوم|أصوم|صوم|الحج|العمرة|حلال|حرام|رقية|صلاة|الصلاة|العيد)"],
    "habit": [r"(?:شيشة|أرجيلة|نرجيلة|القات|قات|معسل|سواك)"],
    "food": [r"(?:تمر|قهوة عربية|قهوة|شاي|لبن|زيت الزيتون|حمص|كبسة|عسل|حليب الإبل|زعتر)"],
    "tradmed": [r"(?:أعشاب|عشبة|طب بديل|طب شعبي|حجامة|حبة البركة|الحبة السوداء|قرفة|زنجبيل|حلبة|كركم|ميرمية|"
                r"يانسون|بابونج|خل التفاح|كي بالنار)"],
}
KK = {
    "place": [W(r"(?i)(?:қазақстан\w*|астана\w*|алматы\w*|шымкент\w*)")],
    "ethnicity": [r"(?i)(?:қазақ\b|қазақтар\w*|ұлты)"],
    "religion": [r"(?i)(?:ораза\w*|рамазан\w*|мұсылман\w*|намаз\w*|халал\w*)"],
    "habit": [r"(?i)(?:насыбай\w*|қымыз\w*|шұбат\w*)"],
    "food": [r"(?i)(?:бешбармақ\w*|бауырсақ\w*|қазы|құрт|палау\w*|наурыз[- ]көже|айран\w*|ет тағам\w*)"],
    "tradmed": [r"(?i)(?:халық емі|халықтық медицина\w*|шөп\w* шай\w*|емдік шөп\w*)"],
}
FA = {
    "place": [W(r"(?:ایران|تهران|مشهد|اصفهان|شیراز|تبریز|افغانستان|عراق)"), r"(?:خارج از کشور|شهرستان|روستا|مهاجر\S*)"],
    "ethnicity": [r"(?:قومیت|کرد هستم|ترک هستم|لر هستم|بلوچ|عرب هستم|افغان هستم)"],
    "religion": [r"(?:رمضان|ماه مبارک|روزه‌داری|روزه داری|روزه دار|روزه بگیرم|روزه بگیرد|روزه بگیره|روزه گرفتن|"
                 r"روزه هستم|نماز|حلال|حرام)"],
    "habit": [r"(?:قلیان|ناس|تریاک)"],
    "food": [r"(?:کله پاچه|آبگوشت|دوغ|کشک|ترشی|خرما|زرشک|سماق|نان سنگک)"],
    "tradmed": [r"(?:طب سنتی|طب اسلامی|داروی گیاهی|داروهای گیاهی|دارو گیاهی|دمنوش|عرقیات|عرق نعنا|حجامت|زالو|عطاری|"
                r"عطار|طبع گرم|طبع سرد|جوشانده|سیاه دانه|سیاهدانه|گل گاوزبان|خاکشیر)"],
}
LEX = {"en": EN, "ru": RU, "kk": KK, "zh": ZH, "ar": AR, "fa": FA}
CUES = ["place", "ethnicity", "religion", "habit", "food", "tradmed"]
DISH = {"FAM-Bench", "NGQA"}  # the case is a dish + a condition: nationality words name the cuisine, not a patient

# food, diet, supplement or herb content in the case text (broader than the cuisine-linked `food` cue)
DIET = {
    "en": r"(?i)\b(?:diet(?:s|ary|ician\w*|etic\w*)?|food\w*|eat(?:s|ing|en)?|ate|meals?|nutrition\w*|malnutrition|"
          r"vitamin\w*|supplements|(?:dietary|herbal|nutritional) supplement\w*|herb\w*|vegetarian|vegan|milk|dairy|"
          r"meat|fish|seafood|fruits?|vegetables?|grapefruit|juice|caffeine|coffee|tea|honey|ramadan|"
          r"fasting (?:during|month)|(?:religious|intermittent|ramadan) fast\w*|"
          r"consum\w+ (?:of )?(?:raw|unpasteuri[sz]ed|large amounts)|breastfe\w+|formula[- ]fed|gluten|lactose|"
          r"fish oil|omega-3|melatonin|probiotic\w*|multivitamin\w*|"
          # alcohol is a drink, and symptoms triggered by food count as diet content (issue #9)
          r"alcohol\w*|ethanol|beer|wine|vodka|whisk(?:e)?y|binge drinking|drinks? (?:daily|heavily|socially)|"
          r"postprandial\w*|after (?:eating|meals?|food|intake)|food[- ](?:induced|triggered|related)|"
          # minerals only as supplements ('taking magnesium', 'zinc tablets') or in a consumer question, not lab values
          r"(?:taking|takes|took|started on|oral|dose of|supplement\w* of)\s+(?:magnesium|zinc|selenium|iodine)|"
          r"(?:magnesium|zinc|selenium|iodine)\s+(?:supplement\w*|citrate|oxide|gluconate|chelate\w*|glycinate|"
          r"tablet\w*|capsule\w*|pill\w*)|"
          r"^(?:what|how|when|is|can|does|should|why)\b[^?\n]{0,40}\b(?:magnesium|zinc|selenium|iodine))\b",
    "ru": r"(?i)\b(?:диет\w*|питани\w+|пищ[аеиу]\w*|продукт\w* питани\w+|молок\w+|молочн\w+|мяс\w+|рыб[аыуе]\w*|"
          r"фрукт\w*|овощ\w*|витамин\w*|(?-i:БАД\w*)|трав(?:ы|ами|ян\w+)|фитотерапи\w+|чай|чая|кофе|голодани\w+|"
          r"жирн\w+ пищ\w+|остр\w+ пищ\w+|сладк(?:ое|ого|им|ому|ие|их|ая|ую)|мучн(?:ое|ого|ые|ых)|жарен\w+|копчен\w+|"
          r"фастфуд\w*|газировк\w*|напитк\w*|прикорм\w*|вскармливан\w*|"
          r"(?:холе|коле)кальциферол\w*|аквадетрим\w*|вигантол\w*|сорбифер\w*|мальтофер\w*|феррум\w*|"
          r"магне[- ]?в6|омега\w*|пробиотик\w*|алкогол\w*|спиртн\w+|пив[оа]\b|вин[оа]\b|водк\w*|"
          r"после (?:еды|приема пищи|приёма пищи))\b",
    "kk": r"(?i)(?:тамақ\w*|диета\w*|тағам\w*|сүт\w*|ет|дәрумен\w*|алкоголь\w*|ішімдік\w*)",
    "zh": r"(?:饮食|食物|进食|忌口|忌食|食疗|膳食|药膳|辛辣|油腻|生冷|饮酒|嗜酒|酗酒|喝酒|啤酒|茶|牛奶|海鲜|水果|蔬菜|肥甘|"
          r"饭后|食后|餐后)",
    "ar": r"(?:حمية|رجيم|غذاء|غذائي|أكل|اكل|طعام|وجبة|وجبات|فيتامين|فيتامينات|مكمل|مكملات|أعشاب|حليب|قهوة|شاي|صيام|"
          r"عسل|تمر|قرفة|زنجبيل|كحول|خمر)",
    "fa": r"(?:رژیم|غذا|غذایی|تغذیه|خوراکی|ویتامین|مکمل|گیاهی|دمنوش|شیر|چای|قهوه|میوه|لبنیات|عسل|روزه داری|رمضان|الکل|مشروب|"
          r"روزه گرفتن|روزه بگیرم)",
}

# Medical terms and template fields that contain a cue or diet word; blanked out before matching.
STOP = {
    "en": [r"\bIndia ink\b", r"(?i)\bJapanese (?:B )?(?:encephalitis|spotted fever)\b",
           r"(?i)\bMiddle East respiratory syndrome\b", r"\bMERS(?:-CoV)?\b", r"\bFISH\b", r"\bTACO\b",
           r"(?i)\bdiethyl\w*", r"(?i)\bSwiss[- ]cheese\b", r"(?i)\bGerman measles\b",
           r"(?i)\b(?:Spanish|Asian|Hong Kong|Russian) (?:flu|influenza)\b", r"(?i)\bChinese hamster\b",
           r"(?i)\bfasting (?:blood|plasma|serum|glucose|lipid|insulin|state|sample|levels?|C-peptide)\w*",
           r"(?i)\b(?:gastric|pancreatic|duodenal) juice\b", r"(?i)\bcoffee[- ]ground\w*",
           r"(?i)\b(?:tea|cola|coffee)[- ]colou?red\b", r"(?i)\bcaf[eé][- ]au[- ]lait\b", r"(?i)\bcurrant[- ]jelly\b",
           r"(?i)\bstrawberry (?:tongue|cervix|gallbladder)\b", r"(?i)\bmilk(?:y)? (?:of magnesia|discharge)\b",
           r"(?i)\bWhite (?:blood|matter|count)\b", r"(?i)\bNorth American blastomycosis\b",
           r"(?i)\b(?:isopropyl|ethyl|benzyl|polyvinyl|cetyl|methyl|absolute|dehydrated) alcohol\b",
           r"(?i)\balcohol(?:[- ]based|[- ]containing| swabs?| wipes?| pads?| gel| sanitizer| septal ablation| ablation|"
           r" sclerotherapy| injection| fixation| fixed| dehydrogenase)\b", r"(?i)\bwine[- ]colou?red\b",
           r"(?i)\bport[- ]wine stain\b"],
    "ru": [r"(?i)молочн\w+\s+желез\w*", r"(?i)пищевод\w*", r"(?i)пищеварит\w*", r"(?i)кофейн\w+\s+гущ\w+",
           r"(?i)цвет\w*\s+(?:чая|пива|кофе)"],
    "zh": [r"发病节气", r"(?:食物|药物)过敏史", r"(?:生于|久居)(?:原籍|本地|当地)", r"旅居史",
           r"中医(?:望闻切诊|诊断|辨证|证型|病名)", r"中西医结合", r"浓茶[似样色]", r"茶色", r"咖啡色", r"米泔样"],
}
# Ingredient names that contain a nationality word: in the dish datasets they do not name the cuisine.
DISH_STOP = [r"(?i)\bGreek[- ]yog(?:h)?urt\b", r"(?i)\bkosher salt\b",
             r"(?i)\bFrench (?:fries|toast|dressing|bread|vanilla|onion|green beans)\b", r"(?i)\bSwiss (?:chard|cheese)\b",
             r"(?i)\bItalian (?:seasoning|dressing|parsley|bread ?crumbs|herbs?)\b", r"(?i)\bEnglish (?:muffins?|cucumbers?|mustard)\b",
             r"(?i)\bCanadian bacon\b", r"(?i)\bGerman chocolate\b", r"(?i)\bSpanish onions?\b", r"(?i)\bDutch oven\b",
             r"(?i)\bAmerican cheese\b", r"(?i)\bMexican (?:cheese|blend)\b", r"(?i)\bBrussels sprouts?\b"]

# A negation before the match in the same clause, or a denial right after it. English ethnicity is only negated
# by a "non-" prefix ("non-Hispanic white"): "no fever, a Caucasian man" is not a negation of the race word.
_CLAUSE = (r"(?:(?!\b(?:but|however|although|though|except|was|were|is|are|has|had|who|which|presented|admitted|"
           r"developed|reported|complained|employed|working|works|lives|living|came|arrived|returned|born)\b)"
           r"[^.;:\n]){0,60}$")
NEG_PRE = {
    "en": r"(?i)\b(?:no|not|denie[sd]|deny|denying|denial of|without|negative for|absence of|nor|never|neither|"
          r"ruled out|free of)\b" + _CLAUSE,
    "ru": r"(?i)(?:\bне\b(?!\s+(?:менее|более|только|раньше|позднее|реже|чаще|смотря))|\bнет\b|отрица\w*|\bбез\b|"
          r"\bотр\b\.?)[^.;:\n]{0,40}$",
    "kk": r"(?i)(?<!\w)(?:жоқ|емес)(?!\w)[^.;:\n]{0,20}$",
    "zh": r"(?:否认[^。；;，,\n]{0,30}|(?:无|未|不|没有|未见|未曾)[^。；;，,、\n]{0,2})$",
    "ar": r"(?<!\w)(?:لا|لم|لن|ليس|ليست|بدون|غير|ما|دون)\s+(?:\S+\s+){0,3}$",
    "fa": r"(?<!\w)(?:نه|بدون|هیچ|ندارم|ندارد)\s+(?:\S+\s+){0,3}$",
}
NEG_POST = {
    "en": r"(?i)^[^.;\n]{0,40}?\b(?:was|were|is|are)\s+(?:negative|denied|unremarkable|non-?contributory)\b",
    "ru": r"(?i)^[^.;\n]{0,90}?(?:\bотр\b\.?|отрица\w*|\bнет\b|\bне было\b|\bне выезжал\w*)",
    "kk": r"(?i)^[^.;\n]{0,25}?(?<!\w)(?:жоқ|емес|ішпей\w*|қолданбай\w*)",
    "fa": r"^\s*(?:\S+\s+)?(?:نمی\S*|نخور\S*|ندار\S*)",
}
ARABIC_SCRIPT = {"ar", "fa"}
AR_PREFIX = r"(?:[وف]?(?:[بكل]|لل)?(?:ال)?)"  # و/ف "and", ب/ك/ل "with/like/for", لل "for the", ال "the"
AR_SUFFIX = r"(?:ه|ها|ات|ي)?"
FA_SUFFIX = r"(?:\u200c?ها(?:ی)?|ی)?"


def _compile(p, lang):
    """Compile a lexicon pattern for a language. Arabic-script patterns match whole words (short words such as تمر
    occur inside longer ones, e.g. مستمر) but allow the attached clitics and suffixes; Kazakh patterns get a leading
    word boundary (ет "meat" is inside қажет, рет, котлет)."""
    flags = 0
    if p.startswith("(?i)"):
        p, flags = p[4:], re.I
    if lang == "ar":
        p = rf"(?<!\w){AR_PREFIX}(?:{p}){AR_SUFFIX}(?!\w)"
    elif lang == "fa":
        p = rf"(?<!\w)(?:{p}){FA_SUFFIX}(?!\w)"
    elif lang == "kk":
        p = rf"(?<!\w)(?:{p})(?!\w)"
    return re.compile(p, flags)


def _lexicon(lang):
    """[(cue, weak, compiled pattern)] for a language (English for languages without a list)."""
    lex = LEX.get(lang, EN)
    out = []
    for cue in CUES:
        for p in lex[cue]:
            weak = isinstance(p, tuple)
            out.append((cue, weak, _compile(p[1] if weak else p, lang)))
    return out


def _mask(text, regs):
    """Blank out stop terms with spaces of the same length, so match offsets stay valid."""
    for r in regs:
        text = r.sub(lambda m: " " * len(m.group(0)), text)
    return text


def negated(text, start, end, lang, cue=None):
    if lang == "en" and re.search(r"(?i)\bnon[- ]?$", text[max(0, start - 4):start]):
        return True
    if lang == "en" and cue == "ethnicity":
        return False
    pre, post = NEG_PRE.get(lang), NEG_POST.get(lang)
    if pre and re.search(pre, text[max(0, start - 90):start]):
        return True
    return bool(post and re.search(post, text[end:end + 100]))


def scan(text, lexicon, lang):
    """All matches of a lexicon in a text: {cue: [(matched text, start, weak, negated)]}."""
    hits = {}
    for cue, weak, r in lexicon:
        for m in r.finditer(text):
            hits.setdefault(cue, []).append((m.group(0).strip(), m.start(), weak,
                                             negated(text, m.start(), m.end(), lang, cue)))
    return hits


def _uniq(xs, n=5):
    out = []
    for x in xs:
        if x not in out:
            out.append(x)
    return out[:n]


def tag(df, keep_matches=False):
    """Add `cue_<type>` booleans, `cue_strength`, `cue_hits`, `cues_negated` and `diet`, all read from `case`, to a
    case table with columns `source`, `lang`, `case`. With keep_matches, also `m_<type>` (list of matched texts) and
    `span_<type>` (offset of the first one), for explanations."""
    df = df.copy()
    rows = {}
    for (source, lang), part in df.groupby(["source", "lang"]):
        lexicon = _lexicon(lang)
        stop = [re.compile(p) for p in STOP.get(lang, STOP["en"] if lang not in LEX else [])]
        if source in DISH:
            stop += [re.compile(p) for p in DISH_STOP]
        diet = _compile(DIET.get(lang, DIET["en"]), lang)
        for i, text in part["case"].items():
            text = _mask(str(text), stop)
            hits = scan(text, lexicon, lang)
            if source in DISH:  # a nationality word in a dish text names the cuisine: a strong food cue
                moved = [(t, s, False, n) for c in ("place", "ethnicity") for t, s, _, n in hits.pop(c, [])]
                hits["food"] = hits.get("food", []) + moved
            row = {}
            pos = {c: [h for h in hs if not h[3]] for c, hs in hits.items()}
            for cue in CUES:
                row[f"cue_{cue}"] = bool(pos.get(cue))
                row[f"m_{cue}"] = _uniq(h[0] for h in pos.get(cue, []))
                row[f"span_{cue}"] = min((h[1] for h in pos.get(cue, [])), default=None)
            strong = any(not h[2] for hs in pos.values() for h in hs)
            row["cue_strength"] = "strong" if strong else "weak" if any(pos.values()) else "none"
            row["cue_hits"] = "; ".join(f"{c}: {', '.join(row[f'm_{c}'])}" for c in CUES if row[f"m_{c}"])
            neg = {c: _uniq(h[0] for h in hs if h[3]) for c, hs in hits.items()}
            row["cues_negated"] = "; ".join(f"{c}: {', '.join(v)}" for c, v in neg.items() if v)
            row["diet"] = any(not negated(text, m.start(), m.end(), lang) for m in diet.finditer(text))
            rows[i] = row
    out = pd.DataFrame.from_dict(rows, orient="index")
    for c in out.columns:
        df[c] = out[c]
    if keep_matches:
        return df
    return df.drop(columns=[f"{p}_{c}" for c in CUES for p in ("m", "span")])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--examples", type=int, default=0)
    ap.add_argument("--source", help="only this dataset")
    a = ap.parse_args()
    df = pd.read_parquet(f"{OUT}/cases.parquet", columns=["case_id", "source", "lang", "case"])
    if a.source:
        df = df[df.source == a.source]
    df = tag(df, keep_matches=True)
    cols = [f"cue_{c}" for c in CUES]
    df["any"] = df[cols].any(axis=1)
    df["strong"] = df.cue_strength.eq("strong")
    df["negated"] = df.cues_negated.ne("")
    show = cols + ["any", "strong", "negated", "diet"]
    print("| Dataset | Cases | " + " | ".join(c.replace("cue_", "") for c in show) + " |\n|---|---|" + "---|" * len(show))
    for source, part in list(df.groupby("source")) + [("All", df)]:
        cells = [f"{part[c].sum():,} ({part[c].mean():.1%})" for c in show]
        print(f"| {source} | {len(part):,} | " + " | ".join(cells) + " |")
    if a.examples:
        for source, part in df.groupby("source"):
            for cue in CUES:
                col = f"span_{cue}"
                has = part[col].notna()
                if not has.any():
                    continue
                print(f"\n### {source} / {cue}")
                for _, r in part[has].sample(min(a.examples, has.sum()), random_state=0).iterrows():
                    i = int(r[col])
                    print(f"- [{', '.join(r['m_' + cue])}] …" + r["case"][max(0, i - 50):i + 60].replace("\n", " ") + "…")


if __name__ == "__main__":
    main()
