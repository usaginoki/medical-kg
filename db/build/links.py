"""Stage `links`: every link table.

  ingredient_compound, dish_nutrient      -> build/links_compounds.py
  compound_condition                      -> build/links_conditions.py
  ingredient_condition                    -> build/links_ingredients.py
  drug, drug_condition, ingredient_drug   -> build/links_drugs.py

Resolvers (build/resolve.py) are loaded once and applied to distinct source keys; the joins run in DuckDB.
`build/links_symmap_scrape.py` is a separate, network-using helper that extended the SymMap scrape (not run here).
"""
from build.resolve import CompoundResolver, ConditionResolver, IngredientResolver
from build.links_common import log, CondText, icd11_resolver
from build.links_compounds import build_ingredient_compound, build_dish_nutrient
from build.links_conditions import build_compound_condition
from build.links_ingredients import build_ingredient_condition
from build.links_drugs import build_drugs


def build(con):
    ir, cr, kr = IngredientResolver(con), CompoundResolver(con), ConditionResolver(con)
    ct = CondText(kr)
    icd11 = icd11_resolver(con, kr)
    log("resolvers loaded")
    build_dish_nutrient(con, cr)
    build_ingredient_compound(con, ir, cr)
    build_compound_condition(con, cr, kr, ct)
    build_ingredient_condition(con, ir, kr, ct, icd11)
    build_drugs(con, ir, icd11)
