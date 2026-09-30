"""Stage `ingredients`: canonical food / culinary-herb dictionary.

Tables: ingredient, ingredient_alias, ingredient_xref, ingredient_property (owned entirely by this stage;
`dishes` later appends INDB-derived xrefs with db in ('ifct', 'uk_cofid', 'usda_fdc')).

1. Seeds: CulinaryDB 02/03 (FlavorDB entity ids), FlavorDB2 entities, FooDB Food.csv, IndicRecipeNutri KG
   `ingredient::` nodes (+ FoodOn `grounded_as`), a few curated merge groups / new ingredients, and the targets of
   db/maps/ingredient_map_manual.csv.
2. Merge (union-find) on NCBI taxon → scientific name → light-normalised names/synonyms; a merge that would put two
   different taxa (or two different scientific names) into one group is refused.
3. Herb / materia-medica sources are attached only where they are the same plant/food: by taxon, then scientific
   name (binomial), then pharmacopoeia Latin parsed to genus+species (e.g. 'Curcumae Longae Rhizoma' → Curcuma
   longa; genus-only names need the English name to confirm), then the English name / curated Chinese name.
"""
import os
import re
import unicodedata
from collections import defaultdict

import pandas as pd

from common import DB_DIR, data, norm_text, slug
from build.resolve_ingredients import CJK, IngredientResolver, key_norm, sci_parse

MANUAL_MAP = os.path.join(DB_DIR, "maps", "ingredient_map_manual.csv")
SEED_RANK = {"manual": 0, "culinarydb": 1, "indicrecipenutri": 2, "foodb": 3, "flavordb": 4}

# ---------------------------------------------------------------------------------------------- curated bits
# merge groups: first name = canonical. (scientific name, NCBI taxon) optional.
MANUAL_GROUPS = [
    (["lamb", "mutton", "sheep", "lamb meat", "mutton meat", "sheep meat"], "meat", "Ovis aries", 9940),
    (["goat meat", "goat", "chevon"], "meat", "Capra hircus", 9925),
    (["chili pepper", "chili", "chile", "chilli", "chillies", "chilies", "mirchi", "green chili", "green chilli",
      "red chili", "red chilli", "cayenne", "cayenne pepper", "hot pepper", "chilli pepper", "chile pepper",
      "red pepper flakes", "crushed red pepper", "red pepper flake", "chili flakes", "chilli flakes", "red chili flakes",
      "red chilli powder", "red chili powder", "chili powder", "chilli powder", "kashmiri chilli", "kashmiri red chilli",
      "ground red pepper", "red pepper powder", "ground chili"],
     "spice", None, None),
    (["black pepper", "pepper", "peppercorn", "blackpepper", "kali mirch", "black peppercorn"], "spice",
     "Piper nigrum", 13216),
    (["coriander", "coriander leaves", "cilantro", "coriander leaf", "dhania", "coriander seed", "chinese parsley"],
     "herb", "Coriandrum sativum", 4047),
    (["yogurt", "yoghurt", "curd", "dahi", "yougurt", "plain yogurt", "laban", "thayir"], "dairy", None, None),
    (["fenugreek", "methi", "fenugreek leaves", "methi leaves", "kasuri methi", "fenugreek seed", "hulba",
      "helba"], "spice", "Trigonella foenum-graecum", 78534),
    (["nigella", "nigella seed", "kalonji", "black seed", "black cumin", "habbat al-barakah", "habba sauda",
      "charnushka", "onion seed"], "spice", "Nigella sativa", 555479),
    (["dried lime", "loomi", "black lime", "noomi basra", "omani lime", "dried black lime", "lumi"], "spice",
     None, None),
    (["ghee", "clarified butter", "desi ghee", "samn", "usli ghee"], "dairy", None, None),
    (["green tea", "matcha", "green tea leaves", "sencha"], "beverage", "Camellia sinensis", 4442),
    (["turmeric", "haldi", "turmericpowder", "tumeric", "turmeric powder"], "spice", "Curcuma longa", 136217),
    (["cumin", "jeera", "zeera", "cumin seed", "kammun"], "spice", "Cuminum cyminum", 52462),
    (["cardamom", "elaichi", "green cardamom", "cardamon", "hail"], "spice", "Elettaria cardamomum",
     105181),
    (["cassia", "chinese cinnamon", "cassia bark", "cassia cinnamon"], "spice", "Cinnamomum cassia", 119260),
    (["cinnamon", "dalchini", "cinnamon stick", "cinnamon bark"], "spice", "Cinnamomum", 13428),
    (["saffron", "kesar", "zafran", "zafaran"], "spice", "Crocus sativus", 82528),
    (["licorice", "liquorice", "liqourice", "mulethi", "licorice root", "liquorice root"], "herb",
     "Glycyrrhiza glabra", 49827),
    (["soy sauce", "soya sauce", "shoyu", "light soy sauce", "dark soy sauce", "soybean sauce"], "condiment", None,
     None),
    (["miso", "miso paste", "white miso", "red miso"], "condiment", None, None),
    (["rice", "chawal", "white rice", "raw rice"], "grain", "Oryza sativa", 4530),
    (["lentil", "lentils", "masoor dal", "red lentil", "masoor"], "legume", "Lens culinaris", 3864),
    (["onion", "onions", "pyaz", "garden onion", "yellow onion"], "vegetable", "Allium cepa", 4679),
    (["garlic", "lahsun", "garlic clove"], "spice", "Allium sativum", 4682),
    (["ginger", "adrak", "ginger root", "fresh ginger"], "spice", "Zingiber officinale", 94328),
    (["date", "dates", "khajur", "tamr", "date palm", "dates fruit"], "fruit", "Phoenix dactylifera", 42345),
    (["pomegranate", "anar", "anardana", "pomegranate seeds"], "fruit", "Punica granatum", 22663),
    (["bell pepper", "capsicum", "capsicm", "sweet pepper", "paprika"], "vegetable", "Capsicum annuum", 4072),
    (["scallion", "spring onion", "green onion", "welsh onion"], "vegetable", "Allium fistulosum", 35875),
    (["sesame", "til", "sesame seed"], "nut/seed", "Sesamum indicum", 4182),
    (["jujube", "red date", "chinese date"], "fruit", None, None),
    (["goji", "goji berry", "wolfberry"], "fruit", "Lycium barbarum", 112863),
    (["chickpea", "chana", "kabuli chana", "garbanzo", "channa", "chickpeas"], "legume", "Cicer arietinum", 3827),
    (["gram flour", "besan"], "flour", None, None),
    (["wheat flour", "atta", "whole wheat flour", "flour"], "flour", None, None),
    (["refined wheat flour", "maida", "all purpose flour", "plain flour"], "flour", None, None),
    (["salt", "table salt", "namak", "kosher-salt", "sea-salt", "sea salt"], "additive", None, None),
    (["water", "drinking water"], "beverage", None, None),
    (["sugar", "white sugar", "granulated sugar", "cheeni"], "sweetener", None, None),
    (["vegetable oil", "vegetable-oil", "cooking oil", "oil", "refined oil"], "oil/fat", None, None),
    (["tomato paste", "tomato puree"], "condiment", None, None),
    # --- new ingredients needed by the dish lines (see db/maps/ingredient_map_manual.csv)
    (["cornstarch", "corn starch", "cornflour", "maize starch", "corn flour"], "starch", None, None),
    (["potato starch", "katakuriko"], "starch", None, None),
    (["brown sugar", "light brown sugar", "dark brown sugar", "soft brown sugar", "muscovado"], "sweetener", None, None),
    (["oyster sauce"], "condiment", None, None),
    (["shaoxing wine", "chinese cooking wine", "cooking wine", "huangjiu", "chinese rice wine", "yellow wine",
      "rice wine"],
     "alcoholic beverage", None, None),
    (["sichuan pepper", "szechuan pepper", "sichuan peppercorn", "szechuan peppercorn", "prickly ash"], "spice",
     "Zanthoxylum bungeanum", None),
    (["doubanjiang", "chili bean paste", "broad bean paste", "toban djan", "spicy bean paste"], "condiment", None, None),
    (["glass noodles", "cellophane noodles", "bean thread noodles", "mung bean noodles"], "noodles", None, None),
    (["glutinous rice", "sticky rice", "sweet rice", "mochi rice", "mochigome"], "grain", None, None),
    (["glutinous rice flour", "sweet rice flour", "mochiko", "shiratamako"], "flour", None, None),
    (["fish sauce", "nam pla", "nuoc mam", "patis"], "condiment", None, None),
    (["thai curry paste", "curry paste", "red curry paste", "green curry paste", "thai red curry paste",
      "thai green curry paste", "yellow curry paste"], "condiment", None, None),
    (["dashi", "dashi stock", "japanese soup stock", "katsuo dashi", "dashi broth"], "broth", None, None),
    (["teriyaki sauce"], "condiment", None, None),
    (["white fungus", "snow fungus", "tremella", "silver ear fungus"], "fungus", "Tremella fuciformis", None),
    (["lily bulb", "lily bulbs"], "vegetable", None, None),
    (["celtuce", "stem lettuce", "asparagus lettuce", "wosun"], "vegetable", None, None),
    (["tofu skin", "yuba", "bean curd skin", "dried bean curd stick"], "soy product", None, None),
    (["fermented black beans", "douchi", "fermented black soybeans"], "condiment", None, None),
    (["quail egg", "quail eggs"], "egg", None, None),
    (["crucian carp"], "fish", "Carassius auratus", None),
    (["fried tofu", "aburaage", "abura age", "atsuage", "deep fried tofu", "tofu puffs"], "soy product", None, None),
    (["konjac", "konnyaku", "shirataki", "konjac jelly"], "vegetable", "Amorphophallus konjac", None),
    (["fish cake", "kamaboko", "chikuwa", "surimi"], "fish", None, None),
    (["myoga", "myoga ginger"], "herb", "Zingiber mioga", None),
    (["shimeji mushroom", "shimeji", "beech mushroom"], "fungus", None, None),
    (["mitsuba", "japanese honewort", "japanese wild parsley"], "herb", "Cryptotaenia japonica", None),
    (["sansho", "japanese pepper", "sansho pepper", "kinome"], "spice", "Zanthoxylum piperitum", None),
    (["perilla", "shiso", "perilla leaf", "egoma", "perilla seed", "kkaennip"], "herb", "Perilla frutescens", None),
    (["japanese apricot", "ume", "umeboshi", "pickled plum", "mume"], "fruit", "Prunus mume", None),
    (["sea bream", "red sea bream", "madai"], "fish", None, None),
    (["pacific saury", "sanma", "saury"], "fish", "Cololabis saira", None),
    (["horse mackerel", "jack mackerel", "aji"], "fish", None, None),
    (["water dropwort", "seri", "minari", "water celery"], "herb", "Oenanthe javanica", None),
    (["camel meat", "camel"], "meat", "Camelus dromedarius", None),
    (["jameed", "mree", "dried yogurt", "kashk"], "dairy", None, None),
    (["samh", "samh seed", "samh flour"], "grain", None, None),
    (["tail fat", "sheep tail fat", "fat tail", "liyyah"], "oil/fat", None, None),
    (["barberry", "zereshk", "barberries"], "fruit", "Berberis vulgaris", None),
    (["baharat", "arabic seven spices", "seven spices", "bzar"], "spice", None, None),
    (["indian bay leaf", "tejpatta", "tej patta", "tejpat", "biryani leaf", "malabathrum"], "spice",
     "Cinnamomum tamala", None),
    (["toona", "chinese toon", "toon shoots", "xiangchun"], "vegetable", "Toona sinensis", None),
    (["shepherd's purse", "jicai"], "vegetable", "Capsella bursa-pastoris", None),
    (["daylily", "daylily buds", "golden needles", "day lily"], "vegetable", None, None),
    (["tripe", "beef tripe", "pork stomach"], "meat", None, None),
    (["ayu", "sweetfish"], "fish", "Plecoglossus altivelis", None),
    (["sailfin sandfish", "hatahata"], "fish", "Arctoscopus japonicus", None),
    (["bracken", "bracken fern", "warabi", "gosari"], "vegetable", "Pteridium aquilinum", None),
    (["osmund fern", "zenmai", "royal fern"], "vegetable", "Osmunda japonica", None),
    (["udo", "japanese spikenard"], "vegetable", "Aralia cordata", None),
    (["cutlassfish", "hairtail", "largehead hairtail", "tachiuo"], "fish", "Trichiurus lepturus", None),
    (["lotus", "sacred lotus", "lotus root", "lotus seed", "lotus stem"], "vegetable", "Nelumbo nucifera", None),
    (["tomato", "garden tomato", "tomatoes"], "vegetable", None, None),
    (["cabbage", "common cabbage", "white cabbage", "green cabbage"], "vegetable", None, None),
    (["grape", "common grape", "grapes"], "fruit", None, None),
    (["taro", "colocasia", "arbi", "eddoe", "satoimo", "dasheen", "taro root"], "vegetable", None, None),
    (["peas", "pea", "common pea", "green peas", "green pea", "matar", "garden pea"], "legume", None, None),
    (["basil", "sweet basil"], "herb", None, None),
    (["sunflower oil", "sunflower seed oil", "sunflower-oil"], "oil/fat", None, None),
    # --- spelling variants among the IndicRecipeNutri nodes / CulinaryDB entities
    (["mayonnaise", "mayo", "mayonaise"], "condiment", None, None),
    (["rosewater", "rose water"], "flavouring", None, None),
    (["almond", "badam", "almonds"], "nut/seed", None, None),
    (["khoya", "khova", "mava", "mawa", "khoa", "khoa khoya"], "dairy", None, None),
    (["jaggery", "jagarry", "gur", "gud", "panela"], "sweetener", None, None),
    (["mozzarella", "mozarella", "mozzarella cheese"], "dairy", None, None),
    (["garam masala", "garammasala", "garam", "gorom moshla"], "spice", None, None),
    (["moong dal", "moongdal", "moong-dal", "split moong dal"], "legume", None, None),
    (["parsley", "parsely"], "herb", None, None),
    (["papaya", "pappaya"], "fruit", None, None),
    (["ice cream", "icecream"], "dairy", None, None),
    (["soy milk", "soymilk", "soya milk"], "soy product", None, None),
    (["monosodium glutamate", "msg", "ajinomoto", "ajinomotto"], "additive", None, None),
    (["baking soda", "bicarb", "bicarbonate", "bicarbonate of soda", "sodium bicarbonate", "cooking soda",
      "eating soda"], "additive", None, None),
    (["semolina", "rava", "rawa", "suji", "sooji", "semolina flour"], "grain", None, None),
    (["carom seed", "carrom", "ajwain", "thymol", "ajowan", "omam"], "spice", "Trachyspermum ammi", 52570),
    (["poppy seed", "posto", "khuskhus", "khus khus"], "spice", None, None),
    (["kidney beans", "rajmah", "rajma", "red kidney beans"], "legume", None, None),
    (["keema", "kheema", "minced meat", "mince"], "meat", None, None),
    (["panch phoron", "phoron", "panch pharon seed", "panch phoran"], "spice", None, None),
    (["amchur", "amchoor", "mango powder", "dry mango powder"], "spice", None, None),
    (["kokum", "kokam", "garcinia indica"], "fruit", None, None),
    (["chena", "chenna", "chhena"], "dairy", None, None),
    (["gelatin", "gelatine"], "additive", None, None),
    (["pine nut", "pinenuts", "pine nuts"], "nut/seed", None, None),
    (["pecan", "pecans", "pecan nut"], "nut/seed", None, None),
    (["cheddar", "cheddar cheese"], "dairy", None, None),
    (["feta", "feta cheese", "greek feta cheese"], "dairy", None, None),
    (["parmesan", "parmesan cheese"], "dairy", None, None),
    (["romano", "romano cheese"], "dairy", None, None),
    (["ricotta", "ricotta cheese"], "dairy", None, None),
    (["passion fruit", "passionfruit"], "fruit", None, None),
    (["star fruit", "starfruit", "carambola"], "fruit", None, None),
    (["red currant", "redcurrant"], "fruit", None, None),
    (["black currant", "blackcurrant"], "fruit", None, None),
    (["apple sauce", "applesauce"], "condiment", None, None),
    (["daikon", "daikon radish", "white radish"], "vegetable", None, None),
    (["brussels sprout", "brussel sprouts", "brussels sprouts"], "vegetable", None, None),
    (["lemongrass", "lemon grass"], "herb", None, None),
    (["jaljeera", "jal jeera powder", "jal jeera"], "spice", None, None),
    (["coriander cumin seed powder", "dhanajeera", "dhanajira", "dhana jeera"], "spice", None, None),
    (["chili paste", "chilli paste", "sambal oelek", "chili garlic sauce"], "condiment", None, None),
    (["mustard", "rai", "sarson", "mustard seed", "mustard seeds"], "spice", None, None),
    (["foxnut", "makhana", "phool makhana", "lotus seeds puffed", "fox nut"], "nut/seed", None, None),
    (["tapioca pearl", "sabudana", "sago pearls", "tapioca pearls"], "starch", None, None),
    (["ginger garlic paste", "ginger garlic", "ginger-garlic paste"], "condiment", None, None),
    (["urad dal", "urad-dal", "black gram", "split black gram", "black gram dehusked", "whole black gram",
      "urad"], "legume", None, None),
    (["chana dal", "chana-dal", "split bengal gram"], "legume", None, None),
    (["refined wheat flour", "maida", "all purpose flour", "plain flour", "allpurpose flour", "refined flour",
      "white flour"], "flour", None, None),
]
# scientific names assigned after merging (no merge key: the product is not the plant)
POST_SCI = {"dried lime": "Citrus aurantiifolia", "chili pepper": "Capsicum annuum"}
# extra scientific names (same food in the materia-medica sense)
SCI_ALIASES = {"licorice": ["Glycyrrhiza uralensis", "Glycyrrhiza inflata"], "cassia": ["Cinnamomum aromaticum"],
               "jujube": ["Ziziphus jujuba var. inermis", "Zizyphus jujuba"], "goji": ["Lycium chinense"]}
# single-record renames (source name -> canonical); keeps the original as an alias
RENAME = {
    ("foodb", "Pepper"): "capsicum pepper plant", ("foodb", "Pepper (Spice)"): "black pepper",
    ("foodb", "Garden onion (var.)"): "onion", ("foodb", "Chinese cinnamon"): "cassia",
    ("foodb", "Sheep (Mutton, Lamb)"): "lamb", ("foodb", "Soy bean"): "soybean", ("foodb", "Lentils"): "lentil",
    ("foodb", "Liquorice"): "liquorice candy", ("foodb", "Tea"): "tea plant", ("foodb", "Common wheat"): "wheat",
    ("foodb", "Wheat"): "wheat (genus)", ("foodb", "Cinnamon"): "cinnamon",
    ("culinarydb", "Pepper"): "black pepper", ("culinarydb", "Liqourice"): "licorice",
    ("culinarydb", "Nigella Seed"): "nigella", ("culinarydb", "Soybean Sauce"): "soy sauce",
    ("culinarydb", "Dates"): "date", ("culinarydb", "Lentils"): "lentil", ("culinarydb", "Lavendar"): "lavender",
    ("culinarydb", "Cayenne"): "chili pepper", ("culinarydb", "Capsicum"): "bell pepper",
    ("culinarydb", "Welsh onion"): "scallion", ("culinarydb", "Flour"): "flour",
    ("culinarydb", "Tea"): "tea", ("culinarydb", "Beans"): "beans",
}
# renamed FooDB records whose original name must not be used as an alias/merge key
RENAME_NO_ALIAS = {("foodb", "Tea"), ("foodb", "Pepper"), ("foodb", "Liquorice"), ("foodb", "Wheat")}
# synonyms in CulinaryDB that are misleading for text matching
SYN_DROP = {("Hard wheat", "spaghetti"), ("Baking Powder", "baking soda"), ("Cayenne", "harissa"),
            ("Lamb", "keema"), ("Fish", "pomfret"), ("Corn", "corn starch"), ("Corn", "corn flour"),
            ("Anise", "saunf"), ("Mango", "amchoor"), ("Mango", "amchur"), ("Capsicum", "paprika"),
            ("Pomegranate", "anaardana"), ("Cayenne", "green chile"), ("Beef", "steak"), ("Milk Fat", "cream"),
            ("Radish", "daikon"), ("Water", "ice"), ("Grape", "merlot")}
# IndicRecipeNutri nodes that are not ingredients (adjectives, cuts, units, tokenisation debris)
IRN_JUNK = set("""apf bites boneless bones bonnet belly blend canned carbonate carbonated chill cob condiments cones
cracked crisp crispy crumb crunchy crush crust crystals cutlets dices diabetes diluted drinking ears eyes filet
finger firm flake flavorful floret flower fluffy foil food free freshly fried fruity germ glaze gold grain granulated
granules grass greek grill grilled head health heart heated hulled husk jack juiced juices kernel kidney leafs legs
liners liquid magic melts mineral mixes moms ones organic packed peels peices pieceginger pitted plant plus pops powde
prepared pressed processed quarters rack ready reserved rind ring ripe roast root rounds seasoned seeded seedless
separated shape shelled shreds skin skinless smoke smooth solids spanish sparkling spears splash split sponge springs
sprouted squares squeeze star strained stripes substitute sweetened tablets tails tatse tender thai tops trimmed
uncooked unsweetened vine weight whip whipped wings wrapper wraps bulb chat dana khar kuria massala masalo oma pearl
phool tawa atar beni biber bafat bandhania chilka cane charcoal decoction dum natural""".split())

CAT_CDB = {"Spice": "spice", "Herb": "herb", "Vegetable": "vegetable", "Fruit": "fruit", "Meat": "meat",
           "Fish": "fish", "Seafood": "seafood", "Dairy": "dairy", "Cereal": "grain", "Maize": "grain",
           "Legume": "legume", "Nuts & Seed": "nut/seed", "Bakery": "bakery", "Beverage": "beverage",
           "Beverage Alcoholic": "alcoholic beverage", "Additive": "additive", "Dish": "dish", "Plant": "plant",
           "Essential Oil": "essential oil", "Fungus": "fungus", "Flower": "flower"}
CAT_FOODB = {"Herbs and Spices": "spice", "Herbs and spices": "spice", "Vegetables": "vegetable", "Fruits": "fruit",
             "Aquatic foods": "fish", "Animal foods": "meat", "Milk and milk products": "dairy",
             "Cereals and cereal products": "grain", "Pulses": "legume", "Nuts": "nut/seed", "Gourds": "vegetable",
             "Soy": "soy product", "Teas": "beverage", "Beverages": "beverage", "Fats and oils": "oil/fat",
             "Confectioneries": "confectionery", "Baking goods": "bakery", "Dishes": "dish",
             "Cocoa and cocoa products": "cocoa", "Coffee and coffee products": "beverage", "Eggs": "egg",
             "Snack foods": "snack", "Baby foods": "baby food"}

# curated Chinese names for TCM herbs that are foods (used as zh aliases and to confirm herb mapping)
HERB_ZH = {"生姜": "ginger", "干姜": "ginger", "姜": "ginger", "姜皮": "ginger", "生姜汁": "ginger", "炮姜": "ginger",
           "姜黄": "turmeric", "大蒜": "garlic", "肉桂": "cassia", "桂皮": "cassia", "桂枝": "cassia",
           "西红花": "saffron", "藏红花": "saffron", "番红花": "saffron", "甘草": "licorice", "炙甘草": "licorice",
           "胡芦巴": "fenugreek", "葫芦巴": "fenugreek", "黑种草子": "nigella", "石榴皮": "pomegranate",
           "石榴": "pomegranate", "绿茶": "green tea", "茶叶": "green tea", "小茴香": "fennel", "孜然": "cumin",
           "胡椒": "black pepper", "洋葱": "onion", "大枣": "jujube", "红枣": "jujube", "枸杞子": "goji",
           "山楂": "hawthorn", "花椒": "sichuan pepper", "八角茴香": "star anise", "八角": "star anise",
           "丁香": "clove", "肉豆蔻": "nutmeg", "薄荷": "mint", "紫苏叶": "perilla", "芝麻": "sesame",
           "黑芝麻": "sesame", "薏苡仁": None, "莲子": "lotus", "百合": "lily bulb", "山药": "yam",
           "葱白": "scallion", "韭菜子": "chinese chives", "赤小豆": "adzuki bean", "绿豆": "mung bean",
           "龙眼肉": "longan", "桂圆": "longan", "乌梅": "japanese apricot", "橘皮": "mandarin orange",
           "陈皮": "mandarin orange", "木瓜": "papaya", "佛手": "citron", "芫荽": "coriander",
           "昆布": "kombu", "海带": "kombu", "桑椹": "mulberry", "枇杷叶": "loquat",
           "紫苏": "perilla", "花椒": "sichuan pepper",
           "核桃仁": "walnut", "白果": "ginkgo nuts", "银耳": "white fungus", "黑木耳": "jew's ear",
           "蜂蜜": "honey", "椰子": "coconut", "罗汉果": "monk fruit", "菊花": None,
           "玫瑰花": "rose", "桃仁": "peach", "决明子": None}
# UNaProd index ids (Persian/Arabic drug names without a monograph) hand-matched to foods
UNAPROD_MANUAL = {1450: "cumin", 1130: "turmeric", 669: "cinnamon", 915: "cassia", 393: "green tea",
                  1811: "cardamom", 925: "ghee", 1124: "lentil", 582: "chickpea", 200: "eggplant", 917: "sumac",
                  1406: "coriander", 972: "dill", 1301: "clove", 1646: "bitter orange", 992: "barley",
                  585: "wheat", 208: "broad bean", 1131: "honey", 617: "mustard", 435: "walnut", 855: "olive",
                  202: "star anise", 776: "pomegranate", 352: "date", 948: "licorice", 827: "saffron",
                  1012: "nigella", 843: "ginger", 569: "fenugreek", 382: "garlic", 254: "onion", 1249: "black pepper"}
ISO3 = dict(ARE="AE", SAU="SA", OMN="OM", QAT="QA", KWT="KW", BHR="BH", YEM="YE", IRN="IR", IRQ="IQ", JOR="JO",
            SYR="SY", LBN="LB", ISR="IL", TUR="TR", EGY="EG", MAR="MA", KAZ="KZ", UZB="UZ", KGZ="KG", TJK="TJ",
            TKM="TM", AFG="AF", PAK="PK", IND="IN", BGD="BD", NPL="NP", LKA="LK", CHN="CN", KOR="KR", JPN="JP",
            MNG="MN", IDN="ID", MYS="MY", THA="TH", VNM="VN", PHL="PH")
UNAPROD_LANG = {"فارسی": "fa", "هندی": "hi", "عربی": "ar", "یونانی": "el", "سریانی": "syr", "ترکی": "tr",
                "رومی": "la"}

PHARMA_PARTS = set("""rhizoma radix herba folium folia fructus semen semina cortex flos flores bulbus stigma pericarpium
recens praeparata praeparatum preparata preparatum et cum succus oleum lignum ramulus ramuli caulis exocarpium pollen
resina gummi cacumen spica stamen testa arillus tuber cormus fel pulvis tostus tosta carbonisatus carbonisata extractum
siccus sicca immaturus maturus radicis fructificatio nodus rhizomatis germinatus germinatum fermentata massa medulla
endocarpium pedicellus pseudobulbus sclerotium periostracum calyx receptaculum petiolus plumula embryo concha carapax
os cornu nidus seu vel crudus cruda pulvis mel ramulus folii seminis fructi herbae radici bulbi flore cortici
exsiccatus usta ustus viride virens""".split())
PART_EN = set("""fresh dried dry raw prepared processed root rhizome rootstock tuber seed seeds fruit fruits peel rind
pericarp bark leaf leaves flower flowers bud stigma bulb juice oil powder herb stem stalk twig kernel husk skin
sprout sprouts pulp aril calyx shell tip extract gum resin capsule twig spike pith achene husks""".split())
EN_QUALIFIERS = {"fresh", "dried", "prepared", "common", "garden", "cultivated", "true", "of", "the", "and", "or", "-"}
NON_PLANT_CATS = {"confectionery", "dish", "bakery", "snack", "alcoholic beverage", "baby food"}
TCM_NATURE = ("cold", "cool", "calm", "neutral", "plain", "warm", "hot", "mild", "flat", "even")
TCM_FLAVOUR = ("pungent", "acrid", "sweet", "bitter", "sour", "salty", "astringent", "bland", "light", "slightly")
TCM_TOXIC = ("toxic", "toxicity", "poison")


# ---------------------------------------------------------------------------------------------- utilities
class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x


def s(x):
    """clean string or None"""
    if x is None:
        return None
    if isinstance(x, float) and pd.isna(x):
        return None
    t = str(x).strip()
    return t if t and t.lower() not in ("nan", "na", "n.a.", "none", "-", "null") else None


def to_int(x):
    try:
        v = int(float(x))
        return v if v > 0 else None
    except (TypeError, ValueError):
        return None


def cdb_synonyms(raw):
    out = []
    for syn in str(raw or "").split(";"):
        t = syn.strip().strip("#").strip()
        if not t:
            continue
        t = t.replace("=", " ").replace("’", "'")
        if "-" in t:
            parts = [p.strip() for p in t.split("-") if p.strip()]
            out.append(" ".join(reversed(parts)))
            out.append(" ".join(parts))
        else:
            out.append(t)
    return out


def rec(src, primary, *, names=(), sci=None, taxon=None, cat=None, foodon=None, xrefs=(), aliases=(), rank=None):
    return dict(src=src, primary=primary, names=[primary, *names], sci=sci, taxon=taxon, cat=cat, foodon=foodon,
                xrefs=list(xrefs), aliases=list(aliases), rank=SEED_RANK[src] if rank is None else rank)


# ---------------------------------------------------------------------------------------------- seeds
def load_seeds():
    recs = []
    for names, cat, sci, tax in MANUAL_GROUPS:
        recs.append(rec("manual", names[0], names=names[1:], sci=sci, taxon=tax, cat=cat))

    # CulinaryDB 02 + 03 (entity ids == FlavorDB entity ids)
    d = pd.read_csv(data("culinarydb", "02_Ingredients.csv"), dtype=str)
    for _, r in d.iterrows():
        name = r["Aliased Ingredient Name"].strip()
        syns = [x for x in cdb_synonyms(r["Ingredient Synonyms"]) if (name, x) not in SYN_DROP]
        prim = RENAME.get(("culinarydb", name), name)
        recs.append(rec("culinarydb", prim, names=[name] + syns, cat=CAT_CDB.get(r["Category"], r["Category"]),
                        xrefs=[("culinarydb", r["Entity ID"]), ("flavordb", r["Entity ID"])]))
    d = pd.read_csv(data("culinarydb", "03_Compound_Ingredients.csv"), dtype=str)
    for _, r in d.iterrows():
        name = r["Compound Ingredient Name"].strip()
        prim = RENAME.get(("culinarydb", name), name)
        recs.append(rec("culinarydb", prim, names=[name] + cdb_synonyms(r["Compound Ingredient Synonyms"]),
                        cat=CAT_CDB.get(r["Category"], (r["Category"] or "").lower() or None),
                        xrefs=[("culinarydb", r["entity_id"])]))
    # FlavorDB2 entities (a 48-entity sample; ids shared with CulinaryDB)
    d = pd.read_csv(data("flavordb2", "entities.csv"), dtype=str)
    for _, r in d.iterrows():
        syns = [x.strip() for x in str(r["entity_alias_synonyms"] or "").split(",") if s(x)]
        recs.append(rec("flavordb", r["entity_alias_readable"], names=syns, cat=(r["category"] or "").lower(),
                        xrefs=[("flavordb", r["entity_id"])]))
    # FooDB foods
    d = pd.read_csv(data("foodb", "Food.csv"), dtype=str)
    for _, r in d.iterrows():
        name = r["name"].strip()
        prim = RENAME.get(("foodb", name), name)
        names = [] if ("foodb", name) in RENAME_NO_ALIAS else [name]
        m = re.match(r"^(.*?)\s*\((.*)\)$", name)
        if m and "." not in m.group(2) and m.group(2).lower() not in ("var", "spice", "capsicum"):
            names += [x.strip() for x in m.group(2).split(",")]
        tax = to_int(r["ncbi_taxonomy_id"]) if r["food_type"] == "Type 1" else None
        if tax in (135518,):  # FooDB gives Gooseberry and Watercress the same taxon
            tax = None
        cat = CAT_FOODB.get(r["food_group"])
        if cat == "spice" and r["food_subgroup"] == "Herbs":
            cat = "herb"
        if cat == "fish" and r["food_subgroup"] in ("Mollusks", "Crustaceans", "Seaweed"):
            cat = "seafood" if r["food_subgroup"] != "Seaweed" else "seaweed"
        recs.append(rec("foodb", prim, names=names, sci=s(r["name_scientific"]), taxon=tax, cat=cat,
                        xrefs=[("foodb_food", r["id"]), ("foodb_food", r["public_id"])]))
    # IndicRecipeNutri KG ingredient nodes (+ FoodOn grounding)
    kg = data("indicrecipenutri", "data", "kg")
    import duckdb
    c = duckdb.connect()
    nodes = c.execute(f"""
        SELECT n.node_id, n.name, g.tail FROM '{kg}/kg_nodes.parquet' n
        LEFT JOIN (SELECT head, min(tail) tail FROM '{kg}/kg_edges.parquet' WHERE rel='grounded_as' GROUP BY 1) g
          ON g.head = n.node_id
        WHERE n.type='ingredient'""").fetchall()
    for nid, name, tail in nodes:
        if name in IRN_JUNK:
            continue
        foodon = tail.split("::", 1)[1].replace("_", ":", 1) if tail else None
        recs.append(rec("indicrecipenutri", name.replace("-", " ").strip(), names=[name], foodon=foodon,
                        xrefs=[("indicrecipenutri", nid)]))
    # targets of the manual dish map that are new ingredients
    for iid, canon, cat in manual_targets():
        recs.append(rec("manual", canon, cat=cat))
    return recs


def manual_rows():
    if not os.path.exists(MANUAL_MAP):
        return pd.DataFrame(columns=["raw_norm", "lang", "ingredient_id", "note"])
    m = pd.read_csv(MANUAL_MAP, dtype=str, keep_default_na=False)
    return m[(m.raw_norm != "") & (m.ingredient_id != "")]


def manual_targets():
    """(id, canonical, category) for manual-map targets flagged 'new:<category>' in the note."""
    out = {}
    for _, r in manual_rows().iterrows():
        m = re.search(r"\bnew(?::([\w/ ]+))?", r.note or "")
        if m:
            canon = r.ingredient_id.split(":", 1)[1].replace("-", " ")
            out[r.ingredient_id] = (r.ingredient_id, canon, (m.group(1) or "").strip() or None)
    return list(out.values())


# ---------------------------------------------------------------------------------------------- merging
def merge(recs):
    uf = UF(len(recs))
    tax = [({r["taxon"]} if r["taxon"] else set()) for r in recs]
    sci = [({sci_parse(r["sci"])[0]} if r["sci"] and sci_parse(r["sci"])[0] else set()) for r in recs]

    def union(a, b):
        ra, rb = uf.find(a), uf.find(b)
        if ra == rb:
            return True
        if tax[ra] and tax[rb] and tax[ra] != tax[rb]:
            return False
        if sci[ra] and sci[rb] and not (sci[ra] & sci[rb]) and not (tax[ra] and tax[ra] == tax[rb]):
            return False
        uf.p[rb] = ra
        tax[ra] |= tax[rb]
        sci[ra] |= sci[rb]
        return True

    refused = []
    for keyf in (lambda r: [r["taxon"]] if r["taxon"] else [],
                 lambda r: [sci_parse(r["sci"])[0]] if r["sci"] and sci_parse(r["sci"])[0] else [],
                 lambda r: [key_norm(r["primary"])],
                 lambda r: [key_norm(n) for n in r["names"]]):
        first = {}
        # process in seed-rank order so the preferred record anchors each key
        for i in sorted(range(len(recs)), key=lambda i: recs[i]["rank"]):
            for k in keyf(recs[i]):
                if not k:
                    continue
                if k in first:
                    if not union(first[k], i):
                        refused.append((k, recs[first[k]]["primary"], recs[i]["primary"]))
                else:
                    first[k] = i
    groups = defaultdict(list)
    for i in range(len(recs)):
        groups[uf.find(i)].append(i)
    return list(groups.values()), refused


def build_tables(recs, groups):
    ing, alias, xref = [], [], []
    used = {}
    for g in groups:
        rs = sorted((recs[i] for i in g), key=lambda r: r["rank"])
        canon = rs[0]["primary"].strip().lower()
        canon = re.sub(r"\s+", " ", canon)
        base = "ING:" + slug(canon)
        iid = base
        k = 2
        while iid in used:
            sci0 = next((r["sci"] for r in rs if r["sci"]), None)
            iid = f"{base}-{slug(sci0)}" if sci0 and k == 2 else f"{base}-{k}"
            k += 1
        used[iid] = canon
        # prefer the curated (manual) scientific name/taxon, then FooDB
        sci = next((r["sci"] for r in rs if r["sci"]), None)
        taxa = [r["taxon"] for r in rs if r["taxon"]]
        cat = next((r["cat"] for r in rs if r["cat"]), None)
        foodon = next((r["foodon"] for r in rs if r["foodon"]), None)
        sci = sci or POST_SCI.get(canon)
        if foodon and not foodon.startswith("FOODON:"):
            xref.append((iid, "obo", foodon))
            foodon = None
        ing.append(dict(ingredient_id=iid, canonical_name=canon, category=cat, scientific_name=sci,
                        ncbi_taxon_id=taxa[0] if taxa else None, foodon_id=foodon, is_herb=False))
        for t in dict.fromkeys(taxa):
            xref.append((iid, "ncbi_taxon", str(t)))
        if foodon:
            xref.append((iid, "foodon", foodon))
        for r in rs:
            for n in dict.fromkeys(r["names"]):
                if s(n):
                    alias.append((iid, n.strip(), "en", "canonical" if n.strip().lower() == canon else "common",
                                  "manual" if r["src"] == "manual" else r["src"]))
            if r["sci"]:
                alias.append((iid, r["sci"], "la", "scientific", r["src"]))
            for db, x in r["xrefs"]:
                if s(x):
                    xref.append((iid, db, str(x)))
        for sa in SCI_ALIASES.get(canon, []):
            alias.append((iid, sa, "la", "scientific", "manual"))
    return ing, alias, xref


# ---------------------------------------------------------------------------------------------- herb mapping
def _stem(w):
    w = w.lower().strip(",.;")
    for e in ("ae", "is", "um", "us", "i", "a", "e"):
        if w.endswith(e) and len(w) - len(e) >= 3:
            return w[: -len(e)]
    return w


class HerbMatcher:
    """Maps a herb/materia-medica record to a food ingredient (only when it is the same plant)."""

    def __init__(self, con, R):
        self.R = R
        self.sci = []  # (genus_stem, species_stem, iid, genus)
        rows = con.execute("""SELECT ingredient_id, scientific_name FROM ingredient WHERE scientific_name IS NOT NULL
                              UNION SELECT ingredient_id, alias FROM ingredient_alias WHERE alias_type='scientific'
                              AND source_id IN ('foodb','manual','culinarydb')""").fetchall()
        for iid, sname in rows:
            toks = sname.split()
            if not toks or not toks[0][:1].isupper():
                continue
            g = _stem(toks[0])
            sp = _stem(toks[1]) if len(toks) > 1 and toks[1][:1].islower() else None
            self.sci.append((g, sp, iid, toks[0].lower()))
        self.genus_of = defaultdict(set)
        for g, sp, iid, _ in self.sci:
            self.genus_of[iid].add(g)
        # seed aliases per ingredient (for English confirmation)
        self.en = defaultdict(set)
        for iid, a in con.execute("""SELECT ingredient_id, alias FROM ingredient_alias WHERE lang='en'
                                     AND source_id IN ('manual','culinarydb','indicrecipenutri','foodb','flavordb')""").fetchall():
            k = key_norm(a)
            if len(k) >= 3:
                self.en[iid].add(k)
        self.en_index = defaultdict(set)
        for iid, ks in self.en.items():
            for k in ks:
                self.en_index[k].add(iid)
        self.zh = {}
        for zh, canon in HERB_ZH.items():
            if canon:
                self.zh[zh] = "ING:" + slug(canon)
        self.ids = {r[0] for r in con.execute("SELECT ingredient_id FROM ingredient").fetchall()}
        self.cat = dict(con.execute("SELECT ingredient_id, category FROM ingredient").fetchall())
        # genus names known anywhere (to tell a genitive genus from a genitive species epithet)
        gen = set(pd.read_csv(data("dr-dukes-phytochemical-and-ethnobotanical-databases", "FNFTAX.csv"),
                              dtype=str, usecols=["GENUS"]).GENUS.dropna().str.lower())
        gen |= set(pd.read_csv(data("cmaup", "CMAUPv2.0_download_Plants.txt"), sep="\t", dtype=str,
                               usecols=["Genus_Name"]).Genus_Name.dropna().str.lower())
        gen |= set(pd.read_csv(data("imppat", "Plant_Information_IMPPAT.tsv"), sep="\t", dtype=str,
                               usecols=["Indian_Medicinal_plant"]).Indian_Medicinal_plant.dropna().str.split().str[0].str.lower())
        self.all_genera = {_stem(g) for g in gen if isinstance(g, str)}

    def _latin_stems(self, latin):
        toks = [t for t in re.split(r"[\s,]+", latin or "") if t]
        toks = [t for t in toks if t.lower() not in PHARMA_PARTS and re.fullmatch(r"[A-Za-z-]+", t)]
        return [_stem(t) for t in toks]

    def _english_keys(self, en_names):
        out = []
        for n in en_names:
            n = re.sub(r"\([^)]*\)", " ", n or "")
            words = [w for w in re.findall(r"[a-z']+", n.lower()) if w not in PART_EN and w not in ("of", "the")]
            if words:
                out.append(" ".join(words))
        return out

    def _core(self, n):
        n = re.sub(r"\([^)]*\)", " ", n or "")
        words = [w for w in key_norm(n).split() if w not in PART_EN and w not in EN_QUALIFIERS]
        return " ".join(words)

    def _confirm(self, iid, en_names, n_cands):
        """English name confirms a pharmacopoeia genus match: its core (part words removed) is an alias of the
        ingredient, or ends with one when the genus has at most three candidate foods."""
        ks = self.en.get(iid, set())
        for n in en_names:
            core = self._core(n)
            if not core:
                continue
            if core in ks:
                return True
            if n_cands <= 3 and any(core.endswith(" " + k) for k in ks):
                return True
        return False

    def match(self, *, taxon=None, sci=None, pharma=(), en=(), zh=()):
        """→ (iid, method) or None"""
        pharma = [p for p in pharma if isinstance(p, str) and s(p)]
        en = [e for e in en if isinstance(e, str) and s(e)]
        zh = [z for z in zh if isinstance(z, str) and s(z)]
        if taxon:
            r = self.R.by_taxon(taxon)
            if r:
                return r[0], "taxon"
        for sn in ([sci] if isinstance(sci, str) else [x for x in (sci if isinstance(sci, (list, tuple)) else []) if isinstance(x, str)]):
            if s(sn):
                full, binom = sci_parse(sn)
                if full and (full in self.R.sci_full or binom in self.R.sci_bin):
                    r = self.R.by_scientific(sn)
                    if r and r[1] == "scientific":
                        return r[0], "scientific"
        genera = set()
        for p in pharma:
            st = self._latin_stems(p)
            if not st:
                continue
            genera.add(st[0])
            if len(st) >= 2:
                # genus + species epithet given: only the same species (never a congener)
                hits = {iid for g, sp, iid, _ in self.sci if g == st[0] and sp == st[1]}
                if len(hits) == 1:
                    return hits.pop(), "pharmacopoeia"
                continue
            # a single epithet ('Zingiberis Rhizoma', 'Granati Pericarpium'): genus, or species epithet if the word
            # is not itself a genus name ('Cassiae Semen' is Cassia/Senna, not Cinnamomum cassia); the English name
            # must confirm the food
            cands = {iid for g, sp, iid, _ in self.sci if g == st[0]}
            if st[0] not in self.all_genera:
                cands |= {iid for g, sp, iid, _ in self.sci if sp and sp == st[0]}
            conf = [iid for iid in cands if self._confirm(iid, en, len(cands))]
            if len(conf) == 1:
                return conf[0], "pharmacopoeia+en"
        # English name (part words removed) equal to a seed alias; must not contradict the Latin genus
        for k in self._english_keys(en):
            hits = self.en_index.get(key_norm(k), set())
            # the Latin genus must agree; with a Latin name but no scientific name on our side we cannot verify
            hits = {h for h in hits if self.cat.get(h) and self.cat[h] not in NON_PLANT_CATS
                    and not (genera and not (self.genus_of.get(h, set()) & genera))}
            if len(hits) == 1:
                return hits.pop(), "english"
        for z in zh:
            iid = self.zh.get(s(z) or "")
            if iid and iid in self.ids and not (genera and self.genus_of.get(iid) and not (self.genus_of[iid] & genera)):
                return iid, "zh_curated"
        return None


def split_names(x, seps=r"[;,]"):
    return [t.strip() for t in re.split(seps, x) if t.strip()] if s(x) else []


def tcm_props(iid, props, meridians, src):
    out = []
    for p in split_names(props, r"[;,，、]"):
        pl = p.lower()
        if any(w in pl for w in TCM_TOXIC):
            out.append((iid, "tcm", "toxicity", pl, src))
        elif any(w in pl for w in TCM_NATURE) and not any(w in pl for w in ("pungent", "sweet", "bitter", "sour", "salty")):
            out.append((iid, "tcm", "nature", pl, src))
        else:
            out.append((iid, "tcm", "flavour", pl, src))
    for m in split_names(meridians, r"[;,，、]"):
        out.append((iid, "tcm", "meridian", m.strip().lower(), src))
    return out


def map_herbs(con):
    R = IngredientResolver(con)
    H = HerbMatcher(con, R)
    X, A, P = [], [], []  # xref rows, alias rows, property rows
    stats = defaultdict(lambda: defaultdict(int))

    def note(src, m):
        stats[src][m[1] if m else "unmatched"] += 1

    def al(iid, alias, lang, atype, src):
        if s(alias):
            A.append((iid, str(alias).strip(), lang, atype, src))

    # --- DDID herbs + foods (taxonomy ids; also the HERB_ID / SymMap_ID bridge)
    herb_bridge, symmap_bridge = {}, {}
    dh = pd.read_csv(data("ddid", "herb_information.csv"), dtype=str)
    for _, r in dh.iterrows():
        m = H.match(taxon=to_int(r.Taxonomy_ID), sci=r.Herb_Latin_Name, pharma=[r.Herb_Latin_Name],
                    en=split_names(r.Herb_English_Name), zh=[r.Herb_Chinese_Name])
        note("ddid_herb", m)
        if not m:
            continue
        iid = m[0]
        X.append((iid, "ddid_herb", r.FHDI_Herb_ID))
        if to_int(r.Taxonomy_ID) and m[1] in ("taxon", "scientific"):
            X.append((iid, "ncbi_taxon", str(to_int(r.Taxonomy_ID))))
        if s(r.HERB_ID) and m[1] in ("taxon", "scientific"):
            herb_bridge[r.HERB_ID] = iid
        if s(r.SymMap_ID) and m[1] in ("taxon", "scientific"):
            symmap_bridge[IngredientResolver._xnorm("symmap", r.SymMap_ID)] = iid
        al(iid, r.Herb_Chinese_Name, "zh", "zh", "ddid")
        al(iid, r.Herb_Pinyin_Name, "zh-Latn", "pinyin", "ddid")
        if s(r.Herb_Latin_Name) and not sci_parse(r.Herb_Latin_Name)[0]:
            al(iid, r.Herb_Latin_Name, "la", "pharmacopoeia", "ddid")
    df = pd.read_csv(data("ddid", "food_information.csv"), dtype=str)
    for _, r in df.iterrows():
        m = None
        if s(r.FoodB_ID):
            hit = R.by_xref("foodb_food", r.FoodB_ID)
            m = (hit[0], "xref") if hit else None
        m = m or H.match(taxon=to_int(r.Taxonomy_ID), sci=r.Scientific_Name, en=[r.Food_Name])
        note("ddid_food", m)
        if m:
            X.append((m[0], "ddid_food", r.FHDI_Food_ID))

    # --- SymMap herbs
    sm = pd.read_excel(data("symmap", "symmap_v2_SMHB.xlsx"), dtype=str)
    hb = pd.read_csv(data("herb", "HERB_herb_info_v2.txt"), sep="\t", dtype=str)
    hb_by_id = {r.Herb_id: r for r in hb.itertuples()}
    symmap_map = {}
    for r in sm.itertuples():
        smid = IngredientResolver._xnorm("symmap", r.Herb_id)
        m = (symmap_bridge[smid], "ddid_bridge") if smid in symmap_bridge else None
        if not m and s(r.HERBDB_ID) and r.HERBDB_ID in herb_bridge:
            m = (herb_bridge[r.HERBDB_ID], "ddid_bridge")
        if not m:
            h = hb_by_id.get(r.HERBDB_ID)
            latin = split_names(r.Latin_name, r",")
            m = H.match(sci=[h.Herb_latin_name] if h is not None and s(h.Herb_latin_name) else None,
                        pharma=latin, en=split_names(r.English_name, r"[;,]"), zh=[r.Chinese_name])
        note("symmap", m)
        if not m:
            continue
        iid = m[0]
        symmap_map[smid] = iid
        X.append((iid, "symmap", smid))
        if s(r.TCMSP_id):
            X.append((iid, "tcmsp_herb", str(to_int(r.TCMSP_id))))
        al(iid, r.Chinese_name, "zh", "zh", "symmap")
        al(iid, r.Pinyin_name, "zh-Latn", "pinyin", "symmap")
        for la in split_names(r.Latin_name, r","):
            al(iid, la, "la", "pharmacopoeia", "symmap")
        for en in split_names(r.English_name, r"[;,]"):
            al(iid, en, "en", "common", "symmap")
        P.extend(tcm_props(iid, r.Properties_English, r.Meridians_English, "symmap"))

    # --- HERB herbs
    for r in hb.itertuples():
        m = None
        if r.Herb_id in herb_bridge:
            m = (herb_bridge[r.Herb_id], "ddid_bridge")
        elif s(r.SymMap_id) and IngredientResolver._xnorm("symmap", r.SymMap_id) in symmap_map:
            m = (symmap_map[IngredientResolver._xnorm("symmap", r.SymMap_id)], "symmap_link")
        if not m:
            latins = split_names(r.Herb_latin_name, r";")
            m = H.match(sci=[l for l in latins if sci_parse(l)[0]], pharma=latins,
                        en=split_names(r.Herb_en_name, r";"), zh=[r.Herb_cn_name])
        note("herb", m)
        if not m:
            continue
        iid = m[0]
        X.append((iid, "herb", r.Herb_id))
        al(iid, r.Herb_cn_name, "zh", "zh", "herb")
        al(iid, r.Herb_pinyin_name, "zh-Latn", "pinyin", "herb")
        for la in split_names(r.Herb_latin_name, r";"):
            al(iid, la, "la", "scientific" if (sci_parse(la)[0] and m[1] in ("scientific", "taxon")
                                              and not set(la.lower().split()) & PHARMA_PARTS) else "pharmacopoeia", "herb")
        for en in split_names(r.Herb_en_name, r";"):
            al(iid, en, "en", "common", "herb")
        P.extend(tcm_props(iid, r.Properties, r.Meridians, "herb"))

    # --- TM-MC medicinal materials (xref id = LATIN, the key of medicinal_compound)
    tm = pd.read_excel(data("tm-mc", "medicinal_material.xlsx"), dtype=str)
    for r in tm.itertuples():
        m = H.match(pharma=[r.LATIN], en=split_names(r.COMMON), zh=[r.CHINESE, r.HANJA])
        note("tmmc", m)
        if not m:
            continue
        iid = m[0]
        X.append((iid, "tmmc", r.LATIN))
        al(iid, r.LATIN, "la", "pharmacopoeia", "tmmc")
        for en in split_names(r.COMMON):
            al(iid, en, "en", "common", "tmmc")
        al(iid, r.KOREAN, "ko", "ko", "tmmc")
        al(iid, r.HANJA, "zh-Hant", "zh", "tmmc")
        al(iid, r.CHINESE, "zh", "zh", "tmmc")
        al(iid, r.PINYIN, "zh-Latn", "pinyin", "tmmc")
        al(iid, r.JAPANESE, "ja", "ja", "tmmc")
        al(iid, r.KANJI, "ja", "ja", "tmmc")

    # --- IMPPAT plants
    ip = pd.read_csv(data("imppat", "Plant_Information_IMPPAT.tsv"), sep="\t", dtype=str)
    for r in ip.itertuples():
        m = H.match(sci=[r.Indian_Medicinal_plant] + split_names(r._3, r"\|"))
        note("imppat", m)
        if not m:
            continue
        iid = m[0]
        X.append((iid, "imppat", r.Plant_identifier))
        al(iid, r.Indian_Medicinal_plant, "la", "scientific", "imppat")
        for en in split_names(r.Common_name):
            al(iid, en, "en", "common", "imppat")

    # --- CMAUP plants
    cm = pd.read_csv(data("cmaup", "CMAUPv2.0_download_Plants.txt"), sep="\t", dtype=str)
    for r in cm.itertuples():
        m = H.match(taxon=to_int(r.Species_Tax_ID), sci=[r.Species_Name, r.Plant_Name])
        note("cmaup", m)
        if m:
            X.append((m[0], "cmaup", r.Plant_ID))

    # --- SpiceRx
    sp = pd.read_csv(data("spicerx", "spices.csv"), dtype=str)
    for r in sp.itertuples():
        m = H.match(taxon=to_int(r.tax_id), sci=r.scientific_name, en=[r.common_name])
        note("spicerx", m)
        if m:
            X.append((m[0], "spicerx", str(to_int(r.tax_id))))
            al(m[0], r.common_name, "en", "common", "spicerx")

    # --- UNaProd monographs (scientific names) + index (Persian/Arabic names, Mizaj)
    um = pd.read_csv(data("unaprod", "unaprod_monographs_sample.csv"), dtype=str)
    ui = pd.read_csv(data("unaprod", "unaprod_drug_list.csv"), dtype=str)
    una = {}
    for r in um.itertuples():
        m = H.match(sci=[x for x in [r.SciName1, r.SciName2] if s(x)], en=split_names(r.Commonname, r"[;,]"))
        if not m and to_int(r.ID) in UNAPROD_MANUAL and "ING:" + slug(UNAPROD_MANUAL[to_int(r.ID)]) in H.ids:
            m = ("ING:" + slug(UNAPROD_MANUAL[to_int(r.ID)]), "manual")
        note("unaprod", m)
        if not m:
            continue
        una[r.ID] = m[0]
        al(m[0], r.DrugName, "fa", "fa", "unaprod")
        al(m[0], r.CommonName2, "fa", "fa", "unaprod")
        for syn in re.findall(r"'([^']+)'", s(r.Synonyms) or ""):
            lang, _, name = syn.partition(":")
            if name:
                al(m[0], name.strip(), UNAPROD_LANG.get(lang.strip(), "fa"), UNAPROD_LANG.get(lang.strip(), "fa"), "unaprod")
            else:
                al(m[0], lang.strip(), "fa", "fa", "unaprod")
        if s(r.MizajDegree):
            P.append((m[0], "persian_mizaj", "mizaj_degree", r.MizajDegree, "unaprod"))
    for r in ui.itertuples():
        iid = una.get(r.ID)
        if not iid and to_int(r.ID) in UNAPROD_MANUAL:
            iid = "ING:" + slug(UNAPROD_MANUAL[to_int(r.ID)])
            if iid not in H.ids:
                print(f"  [ingredients] UNaProd manual target missing: {iid}")
                iid = None
            else:
                note("unaprod", (iid, "manual_index"))
                al(iid, r.DrugName, "fa", "fa", "unaprod")
        if not iid:
            continue
        X.append((iid, "unaprod", r.ID))
        for v in dict.fromkeys(split_names(r.MizajType, r";")):
            P.append((iid, "persian_mizaj", "mizaj", v, "unaprod"))

    # --- Dr. Duke's (FNFTAX taxa; xref = FNFNUM and TAXON; aliases from COMMON_NAMES + ETHNOBOT CNAME)
    dk = data("dr-dukes-phytochemical-and-ethnobotanical-databases")
    fnf = pd.read_csv(f"{dk}/FNFTAX.csv", dtype=str, usecols=["FNFNUM", "TAXON"])
    duke_taxa = {}
    for r in fnf.itertuples():
        m = H.match(sci=r.TAXON)
        note("duke", m)
        if m:
            X.append((m[0], "duke", r.FNFNUM))
            X.append((m[0], "duke", r.TAXON))
            duke_taxa[r.FNFNUM] = m[0]
    cn = pd.read_csv(f"{dk}/COMMON_NAMES.csv", dtype=str, usecols=["CNNAM", "FNFNUM"])
    for r in cn.itertuples():
        if r.FNFNUM in duke_taxa:
            al(duke_taxa[r.FNFNUM], r.CNNAM, "en", "common", "duke")
    taxon2iid = {t: iid for (iid, db, t) in X if db == "duke" and not t.isdigit()}
    eb = pd.read_csv(f"{dk}/ETHNOBOT.csv", dtype=str, usecols=["TAXON", "CNAME", "COUNTRY"])
    eb = eb[eb.TAXON.isin(taxon2iid) & eb.CNAME.notna()].drop_duplicates(["TAXON", "CNAME"])
    for r in eb.itertuples():
        al(taxon2iid[r.TAXON], r.CNAME, "und", "common", "duke")

    # --- KNApSAcK world species (edible / medicinal use per country)
    kn = pd.read_csv(data("knapsack-family", "world_country_species.csv"), dtype=str)
    kmap = {}
    for sp_name in kn.species.dropna().unique():
        m = H.match(sci=sp_name)
        note("knapsack", m)
        if m:
            kmap[sp_name] = m[0]
    for r in kn[kn.species.isin(kmap)].itertuples():
        iid = kmap[r.species]
        cc = ISO3.get(r.country_code, r.country_code)
        if s(r.purpose):
            for pu in split_names(r.purpose, r"[;,/|]"):
                P.append((iid, "knapsack_use", f"use_in_{cc}", pu.lower(), "knapsack"))
        for en in split_names(r.common_name, r"\|"):
            al(iid, en, "en", "common", "knapsack")
        for ja in split_names(r.common_name_ja, r"\|"):
            al(iid, ja, "ja", "ja", "knapsack")
    for sp_name, iid in kmap.items():
        X.append((iid, "knapsack", sp_name))

    # --- NPASS species: only taxa already attached to an ingredient
    taxa = {}
    for iid, db, x in X + [(i, "ncbi_taxon", str(t)) for i, t in con.execute(
            "SELECT ingredient_id, ncbi_taxon_id FROM ingredient WHERE ncbi_taxon_id IS NOT NULL").fetchall()]:
        if db == "ncbi_taxon":
            taxa.setdefault(x, iid)
    for iid, x in con.execute("SELECT ingredient_id, xref_id FROM ingredient_xref WHERE db='ncbi_taxon'").fetchall():
        taxa.setdefault(x, iid)
    npc = pd.read_csv(data("npass", "NPASS3.0_species_info.txt"), sep="\t", dtype=str,
                      usecols=["org_id", "org_tax_id", "species_tax_id"])
    n_np = 0
    for r in npc.itertuples():
        iid = taxa.get(r.org_tax_id) or taxa.get(r.species_tax_id)
        if iid:
            X.append((iid, "npass", r.org_id))
            n_np += 1
    stats["npass"]["taxon"] = n_np
    return X, A, P, stats


# ---------------------------------------------------------------------------------------------- build
def build(con):
    for t in ("ingredient_property", "ingredient_xref", "ingredient_alias", "ingredient"):
        con.execute(f"DELETE FROM {t}")
    recs = load_seeds()
    groups, refused = merge(recs)
    ing, alias, xref = build_tables(recs, groups)
    ing_df = pd.DataFrame(ing)
    ing_df["ncbi_taxon_id"] = ing_df["ncbi_taxon_id"].astype("Int64")
    con.execute("INSERT INTO ingredient SELECT ingredient_id, canonical_name, category, scientific_name, ncbi_taxon_id,"
                " foodon_id, is_herb FROM ing_df")
    # curated Chinese names for food herbs + the manual dish-line map become aliases (source 'manual')
    man = manual_rows()
    ids = set(ing_df.ingredient_id)
    missing = sorted(set(man.ingredient_id) - ids)
    if missing:
        print(f"  [ingredients] manual map targets missing ({len(missing)}): {missing[:20]}")
    for _, r in man.iterrows():
        if r.ingredient_id in ids:
            alias.append((r.ingredient_id, r.raw_norm, r.lang or None, r.lang if r.lang in ("zh", "ja", "ko") else "common",
                           "manual"))
    for zh, canon in HERB_ZH.items():
        if canon and "ING:" + slug(canon) in ids:
            alias.append(("ING:" + slug(canon), zh, "zh", "zh", "manual"))
    _insert_alias(con, alias)
    _insert_xref(con, xref)

    X, A, P, stats = map_herbs(con)
    _insert_alias(con, A)
    _insert_xref(con, X)
    if P:
        pdf = pd.DataFrame(P, columns=["ingredient_id", "system", "property", "value", "source_id"]).drop_duplicates()
        con.execute("INSERT INTO ingredient_property SELECT * FROM pdf")
    con.execute("""UPDATE ingredient SET is_herb = ingredient_id IN (SELECT ingredient_id FROM ingredient_xref
                   WHERE db IN ('symmap','herb','tmmc','imppat','unaprod','ddid_herb'))""")
    n = con.execute("SELECT count(*) FROM ingredient").fetchone()[0]
    print(f"  [ingredients] {n} ingredients from {len(recs)} seed records; {len(refused)} merges refused "
          f"(taxon/scientific conflict)")
    for src, d in stats.items():
        print(f"  [ingredients]   {src:10s} " + ", ".join(f"{k}={v}" for k, v in sorted(d.items())))


def _insert_alias(con, rows):
    df = pd.DataFrame(rows, columns=["ingredient_id", "alias", "lang", "alias_type", "source_id"])
    df["alias"] = df["alias"].map(lambda a: unicodedata.normalize("NFC", str(a)).strip())
    df = df[df.alias.str.len() > 0].drop_duplicates(["ingredient_id", "alias", "lang", "alias_type"])
    # drop an alias already present for the same ingredient with the same lower-case text/lang (keep first source)
    df = df.assign(_k=df.alias.str.lower()).drop_duplicates(["ingredient_id", "_k", "lang"]).drop(columns="_k")
    con.execute("INSERT INTO ingredient_alias SELECT * FROM df")


def _insert_xref(con, rows):
    df = pd.DataFrame(rows, columns=["ingredient_id", "db", "xref_id"]).dropna().drop_duplicates()
    con.execute("INSERT INTO ingredient_xref SELECT * FROM df")
