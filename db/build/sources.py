"""Stage `sources`: register every source used by the build (source_id → vault dataset note)."""
from common import add_source

SOURCES = [
    # source_id, dataset note, name, version, license
    ("medic", "CTD", "CTD MEDIC disease vocabulary (MeSH + OMIM)", "2026-08", "CTD terms"),
    ("ctd", "CTD", "Comparative Toxicogenomics Database, curated chemical–disease", "2026-08-28", "CTD terms (notify on use)"),
    ("foodb", "FooDB", "FooDB", "2020-04-07 CSV", "CC BY-NC 4.0"),
    ("hmdb", "HMDB", "Human Metabolome Database", "5.0", "CC BY-NC 4.0"),
    ("exposome", "Exposome-Explorer", "Exposome-Explorer", "4.0", "free with citation"),
    ("phenol", "Phenol-Explorer", "Phenol-Explorer", "3.6", "non-commercial"),
    ("npass", "NPASS", "NPASS", "3.0", "CC BY-NC"),
    ("cmaup", "CMAUP", "CMAUP", "2.0 (2024)", "free academic"),
    ("flavordb", "FlavorDB2", "FlavorDB2 (sampled entities)", "2", "not stated"),
    ("culinarydb", "CulinaryDB", "CulinaryDB", "2018", "CC BY-NC-SA 3.0"),
    ("indicrecipenutri", "IndicRecipeNutri", "IndicRecipeNutri", "0.10.0", "CC BY-NC-SA 4.0"),
    ("indb", "Indian Nutrient Databank (INDB)", "Indian Nutrient Databank", "2024", "not stated"),
    ("sfct", "Saudi Food Composition Tables", "Saudi Food Composition Tables", "2025", "SFDA terms"),
    ("bfct", "Bahrain Food Composition Tables", "Bahrain Food Composition Tables", "2025", "not stated"),
    ("kfct", "Kyrgyzstan Food Composition Table", "Kyrgyzstan Food Composition Table", "2022", "CC BY 4.0"),
    ("maff", "Our Regional Cuisines (Japan MAFF)", "Our Regional Cuisines (Japan MAFF)", "2024 snapshot", "MAFF terms / apache-2.0 mirror"),
    ("xiachufang", "XiaChuFang Recipe Corpus", "XiaChuFang Recipe Corpus (4.3% subset)", "2022", "research use"),
    ("foodcom", "Food.com Recipes and Interactions", "Food.com Recipes", "2019", "Kaggle, © original authors"),
    ("usda", "USDA FoodData Central", "USDA FoodData Central", "2026-04 / SR Legacy", "CC0"),
    ("symmap", "SymMap", "SymMap", "2.0", "not stated"),
    ("herb", "HERB", "HERB", "2.0", "not stated"),
    ("tmmc", "TM-MC", "TM-MC", "2.0", "not stated"),
    ("imppat", "IMPPAT", "IMPPAT", "3.0", "CC BY-NC-ND"),
    ("spicerx", "SpiceRx", "SpiceRx (sampled)", "2018", "not stated"),
    ("unaprod", "UNaProd", "UNaProd (sampled monographs)", "1.2", "not stated"),
    ("duke", "Dr. Duke's Phytochemical and Ethnobotanical Databases", "Dr. Duke's databases", "2016", "CC0"),
    ("knapsack", "KNApSAcK Family", "KNApSAcK Family (sampled)", "2024", "CC BY-NC-ND"),
    ("ddid", "DDID", "Diet–Drug Interaction Database", "2024", "not stated"),
    ("drugbank", "DrugBank", "DrugBank (food-interaction sample via DDID)", "2026 sample", "DrugBank terms"),
    ("manual", None, "Curated maps in db/maps/", None, "this repository"),
]


def build(con):
    con.execute("DELETE FROM source")
    for s in SOURCES:
        add_source(con, *s)
