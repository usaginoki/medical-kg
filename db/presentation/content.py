"""Curated presentation text: the datasets and how each one was integrated into each table of db/unified.duckdb.

Pure data, stdlib only. Read by db/presentation/export.py.

DATASETS[source_id]["tables"][table] = {"how": [...], "raw": {"file": ..., "row": {...}}, "result": {...}}
  raw    = one real row of the raw file (key columns only, long values cut with "…")
  result = the row it became in unified.duckdb (same record; values copied from the DB)
Examples on the patient trace (Timman Rice → turmeric → curcumin → type 2 diabetes / warfarin) use the trace rows.

Notes on layout:
  * seed sources of the ingredient dictionary (manual, culinarydb, flavordb, foodb, indicrecipenutri) are shown under
    "ingredient"; their names also become ingredient_alias rows and their ids ingredient_xref rows.
  * herb / materia-medica sources are shown under "ingredient_xref" (attach to an existing food); aliases and
    properties get their own entry where the source adds something distinctive.
  * compound sources are shown under "compound"; their ids become compound_xref rows (shown as "compound_xref").
  * 'usda' is registered in build/sources.py but no row in any table carries it (the 38 usda_fdc ingredient_xref
    rows are learned from INDB 'US-' food codes), so it has no entry here.
"""

CURCUMIN = "IK:VFLDPWHFBUODDF-FCXRPNKRSA-N"

DATASETS = {
    # ------------------------------------------------------------------------------------------------ conditions
    "medic": {
        "name": "CTD MEDIC",
        "note": "CTD",
        "what": "CTD's merged disease vocabulary: MeSH diseases plus OMIM, with synonyms and tree numbers",
        "origin": "CTD, NC State Univ. · release 2026-08",
        "access": "direct TSV.gz download, no login",
        "tables": {
            "condition": {
                "how": [
                    "Backbone: every MEDIC row becomes a condition, id = MESH:… or OMIM:…",
                    "type from tree numbers: C23.888 → symptom, other C23 → finding, else disease",
                    "Later layers only fill empty columns: UMLS/ICD-10-CM from SymMap/HERB, ICD-11 via same_as",
                    "Name + synonyms → condition_alias; OMIM/DOID alt ids → xref aliases",
                ],
                "raw": {"file": "Data/ctd/CTD_diseases.tsv.gz", "row": {
                    "DiseaseName": "Diabetes Mellitus, Type 2",
                    "DiseaseID": "MESH:D003924",
                    "AltDiseaseIDs": "DO:DOID:9352|OMIM:125853",
                    "ParentIDs": "MESH:D003920",
                    "TreeNumbers": "C18.452.394.750.149|C19.246.300",
                    "Synonyms": "Adult-Onset Diabetes Mellitus|Diabetes, Maturity-Onset|Diabetes Mellitus, Adult Onset|…",
                }},
                "result": {
                    "condition_id": "MESH:D003924",
                    "name": "Diabetes Mellitus, Type 2",
                    "type": "disease",
                    "umls_cui": "C1852091",
                    "icd11": "5A11",
                    "icd10cm": "E11",
                    "doid": "DOID:9352",
                    "source_vocab": "medic",
                },
            },
            "condition_relation": {
                "how": [
                    "ParentIDs → is_a edges (child → parent), 22,423 rows",
                    "Lets a query on 'Diabetes Mellitus' pick up type 2 evidence",
                    "Edges to ids outside the vocabulary are dropped",
                ],
                "raw": {"file": "Data/ctd/CTD_diseases.tsv.gz", "row": {
                    "DiseaseID": "MESH:D003924",
                    "ParentIDs": "MESH:D003920",
                }},
                "result": {"from_id": "MESH:D003924", "to_id": "MESH:D003920", "rel": "is_a"},
            },
        },
    },
    # ------------------------------------------------------------------------------------------------ compounds
    "ctd": {
        "name": "CTD",
        "note": "CTD",
        "what": "Curated chemical–disease links from the literature, with direct-evidence type and PubMed ids",
        "origin": "CTD, NC State Univ. · files of 2026-08-28",
        "access": "direct TSV.gz download, no login",
        "tables": {
            "compound": {
                "how": [
                    "Loads only chemicals in the curated file + nutrient MeSH ids from nutrient_map.csv",
                    "Merged with other sources on InChIKey → PubChem CID → explicit ids → CAS → unique name",
                    "Owns compound.mesh_id; how the MeSH id was reached → compound_xref 'ctd_match'",
                    "Curated file's ChemicalID lacks the 'MESH:' prefix; CTD_chemicals.tsv has it",
                ],
                "raw": {"file": "Data/ctd/CTD_chemicals.tsv", "row": {
                    "ChemicalName": "Curcumin",
                    "ChemicalID": "MESH:D003474",
                    "CasRN": "458-37-7",
                    "PubChemCID": "CID:969516",
                    "InChIKey": "VFLDPWHFBUODDF-FCXRPNKRSA-N",
                    "ParentIDs": "MESH:D002396|MESH:D036381",
                }},
                "result": {
                    "compound_id": CURCUMIN,
                    "name": "Curcumin",
                    "pubchem_cid": 969516,
                    "cas": "458-37-7",
                    "chebi_id": "CHEBI:3962",
                    "mesh_id": "MESH:D003474",
                    "is_nutrient": False,
                    "compound_xref": "ctd MESH:D003474 · ctd_match inchikey",
                },
            },
            "compound_condition": {
                "how": [
                    "Rows with DirectEvidence only (inferred gene links skipped)",
                    "therapeutic → beneficial, marker/mechanism → marker; evidence curated_literature",
                    "Attached to the CTD-owning compound + same-MeSH variants that occur in foods",
                    "score 1.0 for InChIKey/CID/id matches, 0.7 for CAS/name/skeleton matches",
                ],
                "raw": {"file": "Data/ctd/CTD_chemicals_diseases_curated.tsv", "row": {
                    "ChemicalName": "Curcumin",
                    "ChemicalID": "D003474",
                    "CasRN": "458-37-7",
                    "DiseaseName": "Diabetes Mellitus, Type 2",
                    "DiseaseID": "MESH:D003924",
                    "DirectEvidence": "therapeutic",
                    "PubMedIDs": "18403477",
                }},
                "result": {
                    "compound_id": CURCUMIN,
                    "condition_id": "MESH:D003924",
                    "direction": "beneficial",
                    "evidence_type": "curated_literature",
                    "source_id": "ctd",
                    "pmids": "18403477",
                    "score": 1.0,
                },
            },
        },
    },
    "foodb": {
        "name": "FooDB",
        "note": "FooDB",
        "what": "Food constituent database: ~1,000 foods, compounds with measured or predicted content, health effects",
        "origin": "Wishart lab, U. Alberta · 2020-04-07 CSV dump",
        "access": "browser download (Cloudflare blocks scripts)",
        "tables": {
            "ingredient": {
                "how": [
                    "Food.csv rows are ingredient seeds (rank 3, after manual, CulinaryDB, IndicRecipeNutri)",
                    "NCBI taxon kept for 'Type 1' foods only; merged on taxon → scientific name → name",
                    "food_group → category; name + parenthesised synonyms → ingredient_alias",
                    "Both numeric id and FOOD public id → ingredient_xref 'foodb_food'",
                ],
                "raw": {"file": "Data/foodb/Food.csv", "row": {
                    "id": "68",
                    "name": "Turmeric",
                    "name_scientific": "Curcuma longa",
                    "food_group": "Herbs and Spices",
                    "food_subgroup": "Spices",
                    "food_type": "Type 1",
                    "ncbi_taxonomy_id": "136217",
                    "public_id": "FOOD00068",
                }},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "canonical_name": "turmeric",
                    "category": "spice",
                    "scientific_name": "Curcuma longa",
                    "ncbi_taxon_id": 136217,
                    "foodon_id": "FOODON:00003753",
                    "is_herb": True,
                    "ingredient_xref": "foodb_food 68 · foodb_food FOOD00068",
                },
            },
            "compound": {
                "how": [
                    "Compounds that occur in Content or CompoundsHealthEffect only",
                    "Compound.csv header is shifted: read by position (cas = col 7, inchikey = col 11)",
                    "ChEBI from CompoundExternalDescriptor; synonyms from CompoundSynonym",
                    "Both FDB public id and numeric id → compound_xref 'foodb'",
                ],
                "raw": {"file": "Data/foodb/Compound.csv", "row": {
                    "id": "12295",
                    "public_id": "FDB012292",
                    "name": "Curcumin",
                    "cas_number (col 7)": "458-37-7",
                    "moldb_inchikey (col 11)": "VFLDPWHFBUODDF-FCXRPNKRSA-N",
                }},
                "result": {
                    "compound_id": CURCUMIN,
                    "name": "Curcumin",
                    "pubchem_cid": 969516,
                    "cas": "458-37-7",
                    "mesh_id": "MESH:D003474",
                    "is_nutrient": False,
                    "compound_xref": "foodb FDB012292 · foodb 12295",
                },
            },
            "ingredient_compound": {
                "how": [
                    "Content.csv rows with source_type = Compound; food and compound resolved by FooDB ids",
                    "Predicted/unknown rows without an amount dropped; citation_type decides the evidence",
                    "orig_unit normalised to mg/100 g (mg/100g, mg/kg, µg/g…); values > 100 g/100 g nulled",
                    "One row per (food, compound): median mg/100 g, distinct parts and citations",
                ],
                "raw": {"file": "Data/foodb/Content.csv", "row": {
                    "id": "687581",
                    "source_id": "12295",
                    "source_type": "Compound",
                    "food_id": "68",
                    "orig_food_common_name": "Turmeric, dried",
                    "orig_content": "2213.571428571",
                    "orig_unit": "mg/100g",
                    "citation": "PHENOL EXPLORER",
                }},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "compound_id": CURCUMIN,
                    "amount": 2213.571428571,
                    "unit": "mg/100g",
                    "mg_per_100g": 2507.0107142855,
                    "plant_part": "Rhizome|Plant|Resin, Exudate, Sap|Root",
                    "evidence_type": "curated_literature",
                    "citation": "DUKE|PHYTOHUB|KNAPSACK|PHENOL EXPLORER",
                },
            },
            "compound_condition": {
                "how": [
                    "CompoundsHealthEffect × HealthEffect names ('anti asthmatic') → conditions",
                    "Action names go through db/maps/action_map.csv to their target conditions",
                    "citation CHEBI → curated_literature; everything else (mostly DUKE) → traditional",
                ],
                "raw": {"file": "Data/foodb/CompoundsHealthEffect.csv", "row": {
                    "id": "1079",
                    "compound_id": "12295",
                    "health_effect_id": "134",
                    "orig_health_effect_name": "Antiasthmatic",
                    "orig_compound_name": "CURCUMIN",
                    "citation": "DUKE",
                    "HealthEffect.name": "anti asthmatic",
                }},
                "result": {
                    "compound_id": CURCUMIN,
                    "condition_id": "MESH:D001249",
                    "direction": "beneficial",
                    "evidence_type": "traditional",
                    "source_id": "foodb",
                    "condition.name": "Asthma",
                },
            },
        },
    },
    "hmdb": {
        "name": "HMDB",
        "note": "HMDB",
        "what": "Human Metabolome Database: metabolites with identifiers, biospecimens and disease associations",
        "origin": "Wishart lab, U. Alberta · version 5.0",
        "access": "browser download (Cloudflare blocks scripts)",
        "tables": {
            "compound": {
                "how": [
                    "Metabolites with a FooDB id or at least one disease row",
                    "foodb_id and phenol_explorer_compound_id used as explicit merge keys",
                    "Highest priority source for the chosen PubChem CID, ChEBI, InChIKey and name",
                ],
                "raw": {"file": "Data/hmdb/hmdb_metabolites.csv", "row": {
                    "accession": "HMDB0002269",
                    "name": "Curcumin",
                    "cas_registry_number": "458-37-7",
                    "inchikey": "VFLDPWHFBUODDF-FCXRPNKRSA-N",
                    "pubchem_compound_id": "969516",
                    "chebi_id": "3962",
                    "foodb_id": "FDB012292",
                    "phenol_explorer_compound_id": "713",
                }},
                "result": {
                    "compound_id": CURCUMIN,
                    "name": "Curcumin",
                    "pubchem_cid": 969516,
                    "cas": "458-37-7",
                    "chebi_id": "CHEBI:3962",
                    "mesh_id": "MESH:D003474",
                    "compound_xref": "hmdb HMDB0002269",
                },
            },
            "compound_condition": {
                "how": [
                    "hmdb_metabolite_diseases: disease by OMIM id, else by name text",
                    "direction marker, evidence epidemiological (biomarker association)",
                    "20k templated cardiolipin → Barth syndrome rows dropped",
                ],
                "raw": {"file": "Data/hmdb/hmdb_metabolite_diseases.csv", "row": {
                    "accession": "HMDB0002269",
                    "metabolite_name": "Curcumin",
                    "disease_name": "Colorectal cancer",
                    "omim_id": "114500",
                    "n_references": "15",
                    "pubmed_ids": "7482520|22148915|19006102|23940645|24424155|20156336|…",
                }},
                "result": {
                    "compound_id": CURCUMIN,
                    "condition_id": "MESH:D015179",
                    "direction": "marker",
                    "evidence_type": "epidemiological",
                    "source_id": "hmdb",
                    "pmids": "28587349|7482520|22148915|21773981|27107423|23940645|24424155|…",
                    "condition.name": "Colorectal Neoplasms",
                },
            },
        },
    },
    "exposome": {
        "name": "Exposome-Explorer",
        "note": "Exposome-Explorer",
        "what": "Curated dietary and pollutant biomarkers, with cohort-level cancer associations",
        "origin": "IARC/WHO, Lyon · version 4.0 (Oct 2025)",
        "access": "CSV zips from the downloads page",
        "tables": {
            "compound_condition": {
                "how": [
                    "cancer_associations.csv: biomarker name → compound via InChIKey, HMDB, CID, FooDB, CAS, name",
                    "Free-text cancer name → condition by alias match",
                    "direction association, evidence epidemiological; 275 rows",
                    "Quirk: 'Breast cancer' lands on MeSH 'Breast Cancer, Familial'",
                ],
                "raw": {"file": "Data/exposome-explorer/cancer_associations.csv", "row": {
                    "ID": "6",
                    "Population": "Breast cancer cases and their controls",
                    "Country": "Netherlands",
                    "Cohort": "EPIC (European Prospective Investigation into Cancer and Nutrition)",
                    "Biospecimen": "Plasma, fasting and non-fasting",
                    "Biomarker": "alpha-Carotene",
                    "Cancer": "Breast cancer",
                    "Publication": "Bakker 2016",
                }},
                "result": {
                    "compound_id": "IK:ANVAOWXLWRTKGA-JLTXGRSLSA-N",
                    "condition_id": "MESH:C562840",
                    "direction": "association",
                    "evidence_type": "epidemiological",
                    "source_id": "exposome",
                    "compound.name": "alpha-carotene",
                    "condition.name": "Breast Cancer, Familial",
                },
            },
        },
    },
    "phenol": {
        "name": "Phenol-Explorer",
        "note": "Phenol-Explorer",
        "what": "Polyphenol contents of foods, aggregated from the literature per food × compound × method",
        "origin": "INRA / IARC, with the Wishart lab · version 3.6",
        "access": "direct download from the downloads page",
        "tables": {
            "compound": {
                "how": [
                    "All 501 compounds; PubChem CID, CAS, ChEBI and synonyms",
                    "HMDB's phenol_explorer_compound_id links them to HMDB/FooDB clusters",
                    "id → compound_xref 'phenol_explorer'",
                ],
                "raw": {"file": "Data/phenol-explorer/compounds.csv", "row": {
                    "id": "713",
                    "compound_class": "Other polyphenols",
                    "compound_subclass": "Curcuminoids",
                    "name": "Curcumin",
                    "cas_number": "458-37-7",
                    "chebi_id": "3962",
                    "pubchem_compound_id": "969516",
                }},
                "result": {
                    "compound_id": CURCUMIN,
                    "name": "Curcumin",
                    "pubchem_cid": 969516,
                    "cas": "458-37-7",
                    "chebi_id": "CHEBI:3962",
                    "compound_xref": "phenol_explorer 713",
                },
            },
            "ingredient_compound": {
                "how": [
                    "composition-data.xlsx: food → ingredient by scientific name, else base name ('Turmeric, dried' → turmeric)",
                    "Compound by Phenol-Explorer id, else by name",
                    "mean kept as amount; mg_per_100g only for 'mg/100 g …' units",
                    "pubmed_ids → citation 'PMID:…'",
                ],
                "raw": {"file": "Data/phenol-explorer/composition-data.xlsx", "row": {
                    "food": "Turmeric, dried",
                    "compound": "Curcumin",
                    "units": "mg/100 g fresh weight",
                    "mean": "2213.57143",
                    "min": "580",
                    "max": "5650",
                    "n": "14",
                    "pubmed_ids": "12059141; 25324941",
                }},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "compound_id": CURCUMIN,
                    "amount": 2213.57143,
                    "unit": "mg/100 g fresh weight",
                    "mg_per_100g": 2213.57143,
                    "evidence_type": "curated_literature",
                    "source_id": "phenol",
                    "citation": "PMID:12059141|PMID:25324941",
                },
            },
        },
    },
    "npass": {
        "name": "NPASS",
        "note": "NPASS",
        "what": "Natural products with their source species, activities and some measured quantities",
        "origin": "BIDD group · version 3.0 (2025)",
        "access": "direct download of all 11 files",
        "tables": {
            "compound": {
                "how": [
                    "Only products of CMAUP plants or FooDB food taxa",
                    "Shares NPC ids with CMAUP; HERB's NPASS_id is an extra merge key",
                    "InChIKey used as pref_name is discarded in favour of the IUPAC name",
                ],
                "raw": {"file": "Data/npass/NPASS3.0_naturalproducts_generalinfo.txt", "row": {
                    "np_id": "NPC160900",
                    "inchikey": "VFLDPWHFBUODDF-FCXRPNKRSA-N",
                    "pref_name": "(1E,6E)-1,7-Bis(4-Hydroxy-3-Methoxyphenyl)Hepta-1,6-Diene-3,5-Dione",
                    "chembl_id": "CHEMBL140",
                    "pubchem_id": "969516",
                    "num_of_organism": "46",
                }},
                "result": {
                    "compound_id": CURCUMIN,
                    "name": "Curcumin",
                    "pubchem_cid": 969516,
                    "mesh_id": "MESH:D003474",
                    "compound_xref": "npass NPC160900",
                },
            },
            "ingredient_xref": {
                "how": [
                    "NPASS organisms attached only by NCBI taxon already on an ingredient",
                    "org_tax_id or species_tax_id → ingredient_xref 'npass'",
                ],
                "raw": {"file": "Data/npass/NPASS3.0_species_info.txt", "row": {
                    "org_id": "NPO24124",
                    "org_name": "Curcuma longa",
                    "org_tax_level": "Species",
                    "org_tax_id": "136217",
                    "family_name": "Zingiberaceae",
                    "num_of_np_quantity": "279",
                }},
                "result": {"ingredient_id": "ING:turmeric", "db": "npass", "xref_id": "NPO24124"},
            },
            "ingredient_compound": {
                "how": [
                    "species_pair file: organism → ingredient, NPC id → compound",
                    "org_isolation_part → plant_part; PMID refs → 'PMID:…', database refs kept by name",
                    "Scraped quantity sample adds amounts where units convert",
                ],
                "raw": {"file": "Data/npass/NPASS3.0_naturalproducts_species_pair.txt", "row": {
                    "src_org_record_id": "1575485",
                    "src_org_pair": "NPO24124-NPC160900",
                    "org_id": "NPO24124",
                    "np_id": "NPC160900",
                    "org_isolation_part": "Rhizome",
                    "ref_type": "Database",
                    "ref_id": "FooDB",
                }},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "compound_id": CURCUMIN,
                    "plant_part": "Rhizome",
                    "evidence_type": "curated_literature",
                    "source_id": "npass",
                    "citation": "TCMID|FooDB|HerDing|Phenol-Explorer|PMID:28068085|TM-MC",
                },
            },
        },
    },
    "cmaup": {
        "name": "CMAUP",
        "note": "CMAUP",
        "what": "Useful plants with their ingredients, targets and plant–disease associations (ICD-11)",
        "origin": "BIDD group · version 2.0 (2024)",
        "access": "direct download, 10 of 13 files",
        "tables": {
            "compound": {
                "how": [
                    "All CMAUP ingredients; NPC ids shared with NPASS",
                    "InChIKey-looking pref_name replaced by the IUPAC name",
                ],
                "raw": {"file": "Data/cmaup/CMAUPv2.0_download_Ingredients_All.txt", "row": {
                    "np_id": "NPC160900",
                    "pref_name": "(1E,6E)-1,7-Bis(4-Hydroxy-3-Methoxyphenyl)Hepta-1,6-Diene-3,5-Dione",
                    "pubchem_cid": "969516",
                    "InChIKey": "VFLDPWHFBUODDF-FCXRPNKRSA-N",
                }},
                "result": {
                    "compound_id": CURCUMIN,
                    "name": "Curcumin",
                    "pubchem_cid": 969516,
                    "mesh_id": "MESH:D003474",
                    "compound_xref": "cmaup NPC160900",
                },
            },
            "ingredient_xref": {
                "how": [
                    "Plants matched to foods by taxon, then scientific name",
                    "Plant_ID → ingredient_xref 'cmaup' (same NPO id space as NPASS)",
                ],
                "raw": {"file": "Data/cmaup/CMAUPv2.0_download_Plants.txt", "row": {
                    "Plant_ID": "NPO24124",
                    "Plant_Name": "Curcuma Longa",
                    "Species_Tax_ID": "136217",
                    "Species_Name": "Curcuma longa",
                    "Family_Name": "Zingiberaceae",
                }},
                "result": {"ingredient_id": "ING:turmeric", "db": "cmaup", "xref_id": "NPO24124"},
            },
            "ingredient_compound": {
                "how": [
                    "Plant_Ingredient_Associations: plant → ingredient, NPC id → compound",
                    "Presence only (no amounts); evidence curated_literature",
                    "Mixed LF/CRLF line endings: read with pandas, not DuckDB",
                ],
                "raw": {"file": "Data/cmaup/CMAUPv2.0_download_Plant_Ingredient_Associations_allIngredients.txt",
                        "row": {"Plant_ID": "NPO24124", "Ingredient_ID": "NPC160900"}},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "compound_id": CURCUMIN,
                    "evidence_type": "curated_literature",
                    "source_id": "cmaup",
                },
            },
            "ingredient_condition": {
                "how": [
                    "Plant–disease rows with a clinical trial → evidence clinical",
                    "Target/transcriptome-only rows → predicted, kept for ICD-11 chapter 21 or category-level codes",
                    "ICD-11 code → ICD11:… condition, followed via same_as to MeSH",
                    "direction association; note = disease + NCT ids",
                ],
                "raw": {"file": "Data/cmaup/CMAUPv2.0_download_Plant_Human_Disease_Associations.txt", "row": {
                    "Plant_ID": "NPO24124",
                    "ICD-11 Code": "FA00-FA05",
                    "Disease_Category": "15.Diseases of the musculoskeletal system or connective tissue",
                    "Disease": "Osteoarthritis",
                    "Association_by_Therapeutic_Target": "n.a.",
                    "Association_by_Clinical_Trials_of_Plant": "NCT03017118,NCT00792818",
                }},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "condition_id": "MESH:D010003",
                    "direction": "association",
                    "evidence_type": "clinical",
                    "source_id": "cmaup",
                    "note": "Osteoarthritis; NCT03017118,NCT00792818",
                },
            },
            "condition": {
                "how": [
                    "ICD-11 codes used by CMAUP become ICD11:… conditions (with DDID's)",
                    "Name = most frequent disease label; chapter 21 → symptom",
                    "same_as edge to the MEDIC condition with an exact normalised name",
                ],
                "raw": {"file": "Data/cmaup/CMAUPv2.0_download_Plant_Human_Disease_Associations.txt", "row": {
                    "Plant_ID": "NPO7513",
                    "ICD-11 Code": "MC41",
                    "Disease_Category": "21.Symptoms, signs or clinical findings, not elsewhere classified",
                    "Disease": "Tinnitus",
                    "Association_by_Clinical_Trials_of_Plant": "NCT01969474",
                }},
                "result": {
                    "condition_id": "ICD11:MC41",
                    "name": "Tinnitus",
                    "type": "symptom",
                    "icd11": "MC41",
                    "source_vocab": "icd11",
                    "condition_relation": "same_as MESH:D014012",
                },
            },
        },
    },
    "flavordb": {
        "name": "FlavorDB2",
        "note": "FlavorDB2",
        "what": "Flavour molecules per food entity, with PubChem ids and flavour profiles",
        "origin": "CoSyLab, IIIT-Delhi · FlavorDB2 (2024), 48-entity sample",
        "access": "undocumented JSON endpoints, per entity",
        "tables": {
            "ingredient": {
                "how": [
                    "entities.csv rows are ingredient seeds; entity ids equal CulinaryDB entity ids",
                    "entity_alias_synonyms → aliases ('Saunf', 'Kayam', 'Ingu')",
                    "entity_id → ingredient_xref 'flavordb'",
                ],
                "raw": {"file": "Data/flavordb2/entities.csv", "row": {
                    "entity_id": "341",
                    "category": "spice",
                    "entity_alias_readable": "Turmeric",
                    "entity_alias_synonyms": "Turmeric",
                    "natural_source_name": "Curcuma",
                    "n_molecules": "130",
                }},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "canonical_name": "turmeric",
                    "category": "spice",
                    "scientific_name": "Curcuma longa",
                    "ingredient_xref": "flavordb 341",
                },
            },
            "compound": {
                "how": [
                    "molecules.csv: PubChem id, common name, CAS",
                    "fooddb_id (FDB…) is an explicit merge key to FooDB",
                    "PubChem id → compound_xref 'flavordb'; curcumin itself is not in the sample",
                ],
                "raw": {"file": "Data/flavordb2/molecules.csv", "row": {
                    "pubchem_id": "92139",
                    "common_name": "Curcumene",
                    "iupac_name": "1-methyl-4-(6-methylhept-5-en-2-yl)benzene",
                    "cas_id": "644-30-4",
                    "fooddb_id": "FDB005326",
                    "flavor_profile": "herb",
                }},
                "result": {
                    "compound_id": "IK:VMYXUZSZMNBRCN-UHFFFAOYSA-N",
                    "name": "alpha-curcumene",
                    "pubchem_cid": 92139,
                    "cas": "644-30-4",
                    "mesh_id": "MESH:C086829",
                    "compound_xref": "flavordb 92139",
                },
            },
            "ingredient_compound": {
                "how": [
                    "entity_molecules.csv: entity → ingredient, PubChem id → compound",
                    "Presence only; evidence curated_literature",
                ],
                "raw": {"file": "Data/flavordb2/entity_molecules.csv", "row": {"entity_id": "341", "pubchem_id": "92139"}},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "compound_id": "IK:VMYXUZSZMNBRCN-UHFFFAOYSA-N",
                    "evidence_type": "curated_literature",
                    "source_id": "flavordb",
                },
            },
        },
    },
    # ------------------------------------------------------------------------------------------------ recipes
    "culinarydb": {
        "name": "CulinaryDB",
        "note": "CulinaryDB",
        "what": "45k recipes from 4 sites, lines aliased to 1k ingredient entities, cuisine-labelled",
        "origin": "CoSyLab, IIIT-Delhi · 2018 release",
        "access": "direct zip download, no login",
        "tables": {
            "ingredient": {
                "how": [
                    "02/03 ingredient tables are top-rank seeds after the curated groups",
                    "Synonyms split on ';' ('bread-rye' → 'rye bread'); misleading ones dropped",
                    "Entity ID → ingredient_xref 'culinarydb' and 'flavordb'",
                ],
                "raw": {"file": "Data/culinarydb/02_Ingredients.csv", "row": {
                    "Aliased Ingredient Name": "Turmeric",
                    "Ingredient Synonyms": "turmeric; tumeric",
                    "Entity ID": "341",
                    "Category": "Spice",
                }},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "canonical_name": "turmeric",
                    "category": "spice",
                    "ingredient_xref": "culinarydb 341 · flavordb 341",
                },
            },
            "dish": {
                "how": [
                    "Priority cuisines only: Indian Subcontinent, Middle East, China, Japan, Korea, Thailand, SE Asia",
                    "Region labels kept as cuisine_label; country only where the cuisine is a country",
                    "Tarla Dalal recipes → country IN",
                ],
                "raw": {"file": "Data/culinarydb/01_Recipe_Details.csv", "row": {
                    "Recipe ID": "3491",
                    "Title": "Authentic Tabbouleh",
                    "Source": "ALLRECIPES",
                    "Cuisine": "Middle East",
                }},
                "result": {
                    "dish_id": "culinarydb:3491",
                    "name": "Authentic Tabbouleh",
                    "lang": "en",
                    "country_iso2": None,
                    "cuisine_label": "Middle East",
                    "has_amounts": True,
                },
            },
            "dish_ingredient": {
                "how": [
                    "Entity ID → ingredient by xref (match_method xref, score 1.0)",
                    "Quantity/unit parsed from the original line; cups/tbsp → grams at density 1",
                    "CulinaryDB's own aliasing kept ('green onions' → onion)",
                ],
                "raw": {"file": "Data/culinarydb/04_Recipe-Ingredients_Aliases.csv", "row": {
                    "Recipe ID": "3491",
                    "Original Ingredient Name": "5 bunches Italian parsley, minced",
                    "Aliased Ingredient Name": "parsley ",
                    "Entity ID": "338",
                }},
                "result": {
                    "dish_id": "culinarydb:3491",
                    "ingredient_id": "ING:parsley",
                    "raw_text": "5 bunches Italian parsley, minced",
                    "quantity": 5.0,
                    "unit": "bunches",
                    "grams": None,
                    "match_method": "xref",
                    "match_score": 1.0,
                },
            },
        },
    },
    "indicrecipenutri": {
        "name": "IndicRecipeNutri",
        "note": "IndicRecipeNutri",
        "what": "219k Indian recipes with parsed, gram-weighted ingredients, region labels and a knowledge graph",
        "origin": "Poshaka Research Lab · v0.10.0 (Sept 2026)",
        "access": "GitHub clone + LFS parquet fetch",
        "tables": {
            "ingredient": {
                "how": [
                    "KG ingredient:: nodes are seeds (rank 2); tokenisation debris filtered",
                    "grounded_as edge → FoodOn id on the ingredient",
                    "node id → ingredient_xref 'indicrecipenutri'",
                ],
                "raw": {"file": "Data/indicrecipenutri/data/kg/kg_nodes.parquet + kg_edges.parquet", "row": {
                    "node_id": "ingredient::turmeric",
                    "type": "ingredient",
                    "name": "turmeric",
                    "grounded_as": "foodclass::FOODON_00003753",
                }},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "canonical_name": "turmeric",
                    "foodon_id": "FOODON:00003753",
                    "ingredient_xref": "indicrecipenutri ingredient::turmeric",
                },
            },
            "dish": {
                "how": [
                    "Recipes with a sub-national Region (not Pan-Indian), ≤ 1,500 per region, hash-sampled",
                    "Region → subregion (Kerala, Goa, Parsi…); Cuisine → cuisine_label",
                    "20,415 dishes, the largest dish source",
                ],
                "raw": {"file": "Data/indicrecipenutri/data/corpus/recipes.parquet + labels.parquet", "row": {
                    "recipe_id": "109888",
                    "RecipeName": "Naadan Fish Fry | Kerala Fish Fry",
                    "Lang_base": "en",
                    "Servings": "3 servings",
                    "Region": "Kerala",
                    "Cuisine": "Kerala",
                }},
                "result": {
                    "dish_id": "indicrecipenutri:109888",
                    "name": "Naadan Fish Fry | Kerala Fish Fry",
                    "lang": "en",
                    "country_iso2": "IN",
                    "subregion": "Kerala",
                    "cuisine_label": "Kerala",
                    "servings": "3 servings",
                },
            },
            "dish_ingredient": {
                "how": [
                    "Source grams used as is; weight tier appended to raw_text",
                    "Tier E lines are defaults (e.g. 'salt' → 20 g), not measurements",
                    "Name → ingredient by alias text (exact → normalised → fuzzy)",
                ],
                "raw": {"file": "Data/indicrecipenutri/data/enrichment/ingredients_weights.parquet", "row": {
                    "recipe_id": "109888",
                    "ing_index": "7",
                    "name": "turmeric",
                    "quantity": "1.0",
                    "unit": "tsp",
                    "grams": "2.3",
                    "tier": "A",
                }},
                "result": {
                    "dish_id": "indicrecipenutri:109888",
                    "ingredient_id": "ING:turmeric",
                    "raw_text": "turmeric [weight tier A]",
                    "quantity": 1.0,
                    "unit": "tsp",
                    "grams": 2.3,
                    "match_method": "exact",
                },
            },
        },
    },
    "indb": {
        "name": "INDB",
        "note": "Indian Nutrient Databank (INDB)",
        "what": "1,014 Indian recipes with standard ingredient codes and computed nutrients per 100 g",
        "origin": "Jaacks group, U. Edinburgh · GitHub, 2025",
        "access": "git clone; IFCT source tables not included",
        "tables": {
            "dish": {
                "how": [
                    "recipes_names.xlsx: one dish per recipe_code",
                    "country IN, cuisine_label 'Indian (INDB)', no sub-region",
                ],
                "raw": {"file": "Data/indian-nutrient-databank-indb/recipes_names.xlsx", "row": {
                    "recipe_code_org": "10.1",
                    "recipe_code": "ASC167",
                    "recipe_name": "Sambar",
                    "primarysource": "asc_manual",
                }},
                "result": {
                    "dish_id": "indb:ASC167",
                    "name": "Sambar",
                    "country_iso2": "IN",
                    "cuisine_label": "Indian (INDB)",
                    "has_amounts": True,
                },
            },
            "dish_ingredient": {
                "how": [
                    "IFCT codes (G033), UK-… and US-… food codes tried as xrefs first",
                    "Else text match on the line, then on the standard food name",
                    "Confident text matches teach code → ingredient xrefs (ifct, uk_cofid, usda_fdc)",
                    "tsp = 5 g, C = 240 g",
                ],
                "raw": {"file": "Data/indian-nutrient-databank-indb/recipes.xlsx", "row": {
                    "recipe_code": "ASC167",
                    "ingredient_name_org": "Turmeric powder",
                    "food_code_org": "G033",
                    "food_name": "Turmeric powder (Curcuma domestica)",
                    "amount": "0.25",
                    "unit": "tsp",
                }},
                "result": {
                    "dish_id": "indb:ASC167",
                    "ingredient_id": "ING:turmeric",
                    "raw_text": "Turmeric powder",
                    "quantity": 0.25,
                    "unit": "tsp",
                    "grams": 1.25,
                    "match_method": "exact",
                    "ingredient_xref": "ifct G033 (learned)",
                },
            },
            "dish_nutrient": {
                "how": [
                    "INDB.xlsx columns '<name>_<unit>' → nutrient compound via nutrient_map.csv",
                    "unit_serving_* (per serving) columns skipped",
                    "37,518 rows; the densest nutrient source",
                ],
                "raw": {"file": "Data/indian-nutrient-databank-indb/INDB.xlsx", "row": {
                    "food_code": "ASC167",
                    "food_name": "Sambar",
                    "protein_g": "3.3500633239746094",
                    "iron_mg": "1.2364188432693481",
                    "sodium_mg": "159.53822326660156",
                }},
                "result": {
                    "dish_id": "indb:ASC167",
                    "nutrient_compound_id": "IK:XEEYBQQBJWHFJM-UHFFFAOYSA-N",
                    "amount_per_100g": 1.2364188432693481,
                    "unit": "mg",
                    "source_id": "indb",
                    "compound.name": "Iron",
                },
            },
        },
    },
    "sfct": {
        "name": "Saudi FCT",
        "note": "Saudi Food Composition Tables",
        "what": "130 lab-analysed Saudi regional dishes: recipes with gram amounts and ~50 nutrients",
        "origin": "Saudi Food and Drug Authority · 1st edition, 2026 PDF",
        "access": "PDF download; tables parsed to CSV",
        "tables": {
            "dish": {
                "how": [
                    "sfct_dishes.csv: one dish per recipe; region → subregion (Hail, Najran…)",
                    "serves_adults → servings; preparation steps kept",
                    "country SA, has_amounts true",
                ],
                "raw": {"file": "Data/saudi-food-composition-tables/extracted/sfct_dishes.csv", "row": {
                    "dish_id": "68",
                    "dish_name": "Timman Rice",
                    "region": "Hail",
                    "serves_adults": "4",
                    "recipe_page": "162",
                    "preparation_steps": "1. In a pressure cooker, place the rendered fat (waddak), onion, | and lamb piec…",
                }},
                "result": {
                    "dish_id": "sfct:68",
                    "name": "Timman Rice",
                    "lang": "en",
                    "country_iso2": "SA",
                    "subregion": "Hail",
                    "cuisine_label": "Saudi",
                    "servings": "4 adults",
                    "has_amounts": True,
                },
            },
            "dish_ingredient": {
                "how": [
                    "'5g', '1.5 l' parsed to quantity + unit + grams",
                    "Descriptors stripped for matching ('Ground turmeric' → turmeric, score 0.92)",
                    "Local terms via the manual map ('Rendered fat (waddak)' → tail fat)",
                ],
                "raw": {"file": "Data/saudi-food-composition-tables/extracted/sfct_ingredients.csv", "row": {
                    "dish_id": "68",
                    "dish_name": "Timman Rice",
                    "component": "Ingredients",
                    "ingredient": "Ground turmeric",
                    "quantity": "5g",
                }},
                "result": {
                    "dish_id": "sfct:68",
                    "ingredient_id": "ING:turmeric",
                    "raw_text": "Ground turmeric",
                    "quantity": 5.0,
                    "unit": "g",
                    "grams": 5.0,
                    "match_method": "normalised",
                    "match_score": 0.92,
                },
            },
            "dish_nutrient": {
                "how": [
                    "Loader reads sfct_nutrients_long.csv (same values as sfct_per100g_wide.csv)",
                    "Analyte label + unit → nutrient compound via nutrient_map.csv",
                    "ND / trace / '<x' values skipped; energy and moisture not mapped",
                    "'Vitamin K' lands on the phylloquinone compound (5.6 µg for sfct:68)",
                ],
                "raw": {"file": "Data/saudi-food-composition-tables/extracted/sfct_nutrients_long.csv", "row": {
                    "dish_id": "68",
                    "dish_name": "Timman Rice",
                    "analyte": "Sodium",
                    "per_100g": "162",
                    "full_recipe": "3940",
                    "unit": "mg",
                }},
                "result": {
                    "dish_id": "sfct:68",
                    "nutrient_compound_id": "IK:MPMYQQHEHYDOCL-UHFFFAOYSA-N",
                    "amount_per_100g": 162.0,
                    "unit": "mg",
                    "source_id": "sfct",
                    "compound.name": "Sodium",
                },
            },
        },
    },
    "bfct": {
        "name": "Bahrain FCT",
        "note": "Bahrain Food Composition Tables",
        "what": "Composition of Bahraini dishes and sweets, with Arabic names; no recipes",
        "origin": "Ministry of Health, Bahrain · 1st edition, 2025",
        "access": "PDF download; tables parsed to CSV",
        "tables": {
            "dish": {
                "how": [
                    "Dish list from the three dish tables, deduplicated on code",
                    "English name title-cased; Arabic name → name_local",
                    "No ingredient table in the book → no dish_ingredient rows",
                ],
                "raw": {"file": "Data/bahrain-food-composition-tables/extracted/bfct_dishes_macronutrients.csv", "row": {
                    "category": "Chicken-based dishes",
                    "code": "3.1",
                    "english_name": "MACHBOOS DAJAJ",
                    "arabic_name": "مجبوس دجاج",
                    "source": "Direct chemical analysis (MOH Bahrain)",
                }},
                "result": {
                    "dish_id": "bfct:3.1",
                    "name": "Machboos Dajaj",
                    "name_local": "مجبوس دجاج",
                    "lang": "ar",
                    "country_iso2": "BH",
                    "cuisine_label": "Bahraini (Chicken-based dishes)",
                    "has_amounts": False,
                },
            },
            "dish_nutrient": {
                "how": [
                    "Column headers 'Protein (g/100g)' split into label + unit",
                    "Label + unit → nutrient compound via nutrient_map.csv",
                    "Units kept as printed (mg, mcg, IU)",
                ],
                "raw": {"file": "Data/bahrain-food-composition-tables/extracted/bfct_dishes_macronutrients.csv", "row": {
                    "code": "3.1",
                    "english_name": "MACHBOOS DAJAJ",
                    "Protein (g/100g)": "12.40",
                    "Fat (g/100g)": "7.33",
                    "CHO (g/100g)": "15.00",
                }},
                "result": {
                    "dish_id": "bfct:3.1",
                    "nutrient_compound_id": "MESH:D004044",
                    "amount_per_100g": 12.4,
                    "unit": "g",
                    "source_id": "bfct",
                    "compound.name": "Dietary Proteins",
                },
            },
        },
    },
    "kfct": {
        "name": "Kyrgyz FCT",
        "note": "Kyrgyzstan Food Composition Table",
        "what": "Kyrgyzstan's first national food composition table, including 11 cooked national dishes",
        "origin": "Kyrgyz State Tech. Univ. et al. · 1st edition 2022",
        "access": "figshare PDF; tables parsed to CSV",
        "tables": {
            "dish": {
                "how": [
                    "Dishes from dish_recipes_ingredients.csv (food group 13)",
                    "Kyrgyz name (Cyrillic) → name_local",
                ],
                "raw": {"file": "Data/kyrgyzstan-food-composition-table/extracted/dishes_proximates.csv", "row": {
                    "food_code": "13001",
                    "name_kyrgyz": "Бешбармак",
                    "name_english": "Beshbarmak",
                    "PROT": "9.22",
                    "FAT": "5.24",
                }},
                "result": {
                    "dish_id": "kfct:13001",
                    "name": "Beshbarmak",
                    "name_local": "Бешбармак",
                    "country_iso2": "KG",
                    "cuisine_label": "Kyrgyz",
                    "has_amounts": True,
                },
            },
            "dish_ingredient": {
                "how": [
                    "raw_weight_g per line → grams (unit 'g raw')",
                    "Yield lines skipped ('Mass of dough', 'TOTAL COOKED WEIGHT')",
                ],
                "raw": {"file": "Data/kyrgyzstan-food-composition-table/extracted/dish_recipes_ingredients.csv", "row": {
                    "recipe_no": "1",
                    "food_code": "13001",
                    "dish_name": "Beshbarmak",
                    "ingredient": "Lamb, horse or beef meat",
                    "raw_weight_g": "218",
                    "edible_weight_g": "156",
                }},
                "result": {
                    "dish_id": "kfct:13001",
                    "ingredient_id": "ING:lamb",
                    "raw_text": "Lamb, horse or beef meat",
                    "quantity": 218.0,
                    "unit": "g raw",
                    "grams": 218.0,
                    "match_method": "normalised",
                    "match_score": 0.92,
                },
            },
            "dish_nutrient": {
                "how": [
                    "INFOODS tagnames (PROT, FAT, NA…) → nutrient compound via nutrient_map.csv",
                    "Units from a fixed tagname → unit table in the loader",
                ],
                "raw": {"file": "Data/kyrgyzstan-food-composition-table/extracted/dishes_proximates.csv", "row": {
                    "food_code": "13001",
                    "name_english": "Beshbarmak",
                    "PROT": "9.22",
                }},
                "result": {
                    "dish_id": "kfct:13001",
                    "nutrient_compound_id": "MESH:D004044",
                    "amount_per_100g": 9.22,
                    "unit": "g",
                    "source_id": "kfct",
                    "compound.name": "Dietary Proteins",
                },
            },
        },
    },
    "maff": {
        "name": "Japan MAFF regional cuisines",
        "note": "Our Regional Cuisines (Japan MAFF)",
        "what": "Japan's 郷土料理 database: regional dishes per prefecture with history, recipe and steps",
        "origin": "MAFF Japan · Hugging Face scrape, Dec 2024",
        "access": "Hugging Face CSV mirror (JP + EN)",
        "tables": {
            "dish": {
                "how": [
                    "Japanese rows are the dishes; prefecture → subregion",
                    "EN name paired from parsed_eng.csv on identical gram signatures (no shared id)",
                    "Japanese name → name_local; lang ja",
                ],
                "raw": {"file": "Data/our-regional-cuisines-japan-maff/parsed_jpn.csv", "row": {
                    "row_id": "4",
                    "dish_name": "石狩鍋",
                    "prefecture": "北海道",
                    "lore_area": "石狩地方",
                    "main_ingredients": "サケ、キャベツ、大根、味噌",
                    "servings": "4人分",
                }},
                "result": {
                    "dish_id": "maff:4",
                    "name": "Ishikarinabe(Ishikari hot pot)",
                    "name_local": "石狩鍋",
                    "lang": "ja",
                    "country_iso2": "JP",
                    "subregion": "北海道",
                    "cuisine_label": "Japanese regional (郷土料理)",
                    "servings": "4人分",
                },
            },
            "dish_ingredient": {
                "how": [
                    "One line per '- name: amount'; 【group】 prefixes stripped",
                    "大さじ = 15 g, 小さじ = 5 g, カップ = 200 g; 少々 / 適量 → no amount",
                    "Japanese names mostly resolved by the curated manual map",
                ],
                "raw": {"file": "Data/our-regional-cuisines-japan-maff/parsed_jpn.csv", "row": {
                    "row_id": "4",
                    "ingredients_with_amounts (line 16)": "- 【合わせ味噌】 味噌: 100g",
                }},
                "result": {
                    "dish_id": "maff:4",
                    "ingredient_id": "ING:miso",
                    "raw_text": "【合わせ味噌】 味噌: 100g",
                    "quantity": 100.0,
                    "unit": "g",
                    "grams": 100.0,
                    "match_method": "manual",
                    "match_score": 1.0,
                },
            },
        },
    },
    "xiachufang": {
        "name": "XiaChuFang",
        "note": "XiaChuFang Recipe Corpus",
        "what": "1.5M user-written Chinese home-cooking recipes from 下厨房, mapped to canonical dish names",
        "origin": "xiachufang.com users · research corpus (2022)",
        "access": "Hugging Face mirror, first 80 MB read",
        "tables": {
            "dish": {
                "how": [
                    "5,000 recipes hash-sampled from those with a canonical dish label",
                    "Western/baking keywords excluded (蛋糕, 烘焙, 披萨…)",
                    "Province from title keywords (新疆 → Xinjiang, 川 → Sichuan)",
                    "Canonical dish → name, recipe title → name_local",
                ],
                "raw": {"file": "Data/xiachufang-recipe-corpus/recipe_corpus_full_first80MB.jsonl", "row": {
                    "line": "52871 (0-based)",
                    "name": "地道新疆大盘鸡",
                    "dish": "大盘鸡",
                    "keywords[5:]": "家常菜, 下酒菜, 下饭菜, 新疆菜",
                }},
                "result": {
                    "dish_id": "xiachufang:52871",
                    "name": "大盘鸡",
                    "name_local": "地道新疆大盘鸡",
                    "lang": "zh",
                    "country_iso2": "CN",
                    "subregion": "Xinjiang",
                    "cuisine_label": "Chinese home cooking (家常菜, 下酒菜, 下饭菜)",
                },
            },
            "dish_ingredient": {
                "how": [
                    "Leading/trailing amounts parsed: '20-30粒花椒' → 25 粒",
                    "克/斤/两/毫升 convert to grams; count units (粒, 个, 片) do not",
                    "适量 / 少许 → no amount; names resolved by curated zh aliases",
                ],
                "raw": {"file": "Data/xiachufang-recipe-corpus/recipe_corpus_full_first80MB.jsonl", "row": {
                    "line": "52871",
                    "recipeIngredient[13]": "20-30粒花椒",
                }},
                "result": {
                    "dish_id": "xiachufang:52871",
                    "ingredient_id": "ING:sichuan-pepper",
                    "raw_text": "20-30粒花椒",
                    "quantity": 25.0,
                    "unit": "粒",
                    "grams": None,
                    "match_method": "manual",
                },
            },
        },
    },
    "foodcom": {
        "name": "Food.com",
        "note": "Food.com Recipes and Interactions",
        "what": "230k English recipes with tags, steps and ingredient names (no amounts)",
        "origin": "Food.com via Kaggle (Majumder et al.) · 2019",
        "access": "Kaggle download (kagglehub)",
        "tables": {
            "dish": {
                "how": [
                    "Recipes tagged with a priority-region cuisine (indian, saudi-arabian, szechuan…)",
                    "Most specific tag wins → country / subregion",
                    "Steps list joined with ' | '",
                ],
                "raw": {"file": "Data/food-com-recipes-and-interactions/RAW_recipes.csv", "row": {
                    "id": "289878",
                    "name": "al kabsa   traditional saudi rice    chicken  dish",
                    "minutes": "100",
                    "tags": "['time-to-make', 'course', 'main-ingredient', 'cuisine', 'preparation', 'occasion', 'saudi…",
                    "n_ingredients": "23",
                }},
                "result": {
                    "dish_id": "foodcom:289878",
                    "name": "al kabsa   traditional saudi rice    chicken  dish",
                    "country_iso2": "SA",
                    "cuisine_label": "saudi-arabian",
                    "has_amounts": False,
                },
            },
            "dish_ingredient": {
                "how": [
                    "ingredients list: names only, quantity/grams always NULL",
                    "Text match on the English alias index",
                ],
                "raw": {"file": "Data/food-com-recipes-and-interactions/RAW_recipes.csv", "row": {
                    "id": "289878",
                    "ingredients[22]": "dried limes",
                }},
                "result": {
                    "dish_id": "foodcom:289878",
                    "ingredient_id": "ING:dried-lime",
                    "raw_text": "dried limes",
                    "quantity": None,
                    "grams": None,
                    "match_method": "normalised",
                    "match_score": 0.95,
                },
            },
        },
    },
    # ------------------------------------------------------------------------------------------------ herbs / TM
    "symmap": {
        "name": "SymMap",
        "note": "SymMap",
        "what": "TCM herbs linked to TCM symptoms, modern symptoms, syndromes, ingredients and diseases",
        "origin": "BUCM / ICT-CAS · version 2.0",
        "access": "xlsx downloads + scraped herb relation pages",
        "tables": {
            "ingredient_xref": {
                "how": [
                    "Herb matched to a food via DDID bridge, else Latin/English/Chinese name",
                    "Herb id → 'symmap'; TCMSP id → 'tcmsp_herb'",
                    "Chinese, pinyin, pharmacopoeia Latin and English names → aliases",
                ],
                "raw": {"file": "Data/symmap/symmap_v2_SMHB.xlsx", "row": {
                    "Herb_id": "198",
                    "Chinese_name": "姜黄",
                    "Pinyin_name": "Jianghuang",
                    "Latin_name": "Rhizoma Curcumae Longae,Curcumae Longae Rhizoma",
                    "English_name": "rhizome of Common Turmeric",
                    "TCMSP_id": "198",
                    "HERBDB_ID": "HERB002840",
                }},
                "result": {"ingredient_id": "ING:turmeric", "db": "symmap", "xref_id": "SMHB00198"},
            },
            "ingredient_alias": {
                "how": [
                    "Chinese name → zh alias (lets 姜黄 in XiaChuFang resolve)",
                    "Pinyin → zh-Latn; Latin → pharmacopoeia",
                ],
                "raw": {"file": "Data/symmap/symmap_v2_SMHB.xlsx", "row": {
                    "Herb_id": "198", "Chinese_name": "姜黄", "Pinyin_name": "Jianghuang"}},
                "result": {"ingredient_id": "ING:turmeric", "alias": "姜黄", "lang": "zh", "alias_type": "zh",
                           "source_id": "symmap"},
            },
            "ingredient_property": {
                "how": [
                    "Properties_English split into nature (warm, cold) and flavour (pungent, bitter)",
                    "Meridians_English → meridian rows; system 'tcm'",
                ],
                "raw": {"file": "Data/symmap/symmap_v2_SMHB.xlsx", "row": {
                    "Herb_id": "198",
                    "Properties_English": "Pungent,Bitter,Warm",
                    "Meridians_English": "Spleen,Liver",
                }},
                "result": {"ingredient_id": "ING:turmeric", "system": "tcm", "property": "nature", "value": "warm",
                           "source_id": "symmap"},
            },
            "compound": {
                "how": [
                    "SMIT ingredients from the scraped herb → ingredient pages",
                    "PubChem CID + CAS only (no InChIKey) → merged by CID",
                ],
                "raw": {"file": "Data/symmap/scrape/herb_ingredient_relations.csv", "row": {
                    "source_herb_id": "SMHB00198",
                    "MOL_id": "SMIT01361",
                    "TCMSP_id": "MOL000090",
                    "Molecule_name": "Curcumin",
                    "PubChem_CID": "969516",
                    "CAS_id": "458-37-7|485-37-7",
                }},
                "result": {"compound_id": CURCUMIN, "name": "Curcumin", "pubchem_cid": 969516,
                           "compound_xref": "symmap SMIT01361 · symmap SMIT01681"},
            },
            "ingredient_compound": {
                "how": [
                    "Scraped herb → SMIT pairs; presence only",
                    "evidence traditional (herb-level TCM compilation)",
                ],
                "raw": {"file": "Data/symmap/scrape/herb_ingredient_relations.csv", "row": {
                    "source_herb_id": "SMHB00198",
                    "source_herb": "Jianghuang (turmeric)",
                    "MOL_id": "SMIT01361",
                    "Molecule_name": "Curcumin",
                }},
                "result": {"ingredient_id": "ING:turmeric", "compound_id": CURCUMIN, "evidence_type": "traditional",
                           "source_id": "symmap"},
            },
            "condition": {
                "how": [
                    "SMMS modern symptoms / SMDE diseases merged into MEDIC by MeSH, OMIM, UMLS; else UMLS:… rows",
                    "TCM symptoms → TCM:SMTS…, syndromes → TCMSY:SMSY… (type tcm_symptom / tcm_syndrome)",
                    "Chinese + pinyin names → condition_alias",
                ],
                "raw": {"file": "Data/symmap/symmap_v2_SMTS.xlsx", "row": {
                    "TCM_symptom_id": "139",
                    "TCM_symptom_name": "刺痛",
                    "Symptom_pinYin": "Ci Tong",
                    "Symptom_definition": "刺激皮肉而感到疼痛：感到剧烈的烧灼样的疼痛",
                    "Symptom_property": "瘀血",
                    "Type": "Ontological terms",
                }},
                "result": {"condition_id": "TCM:SMTS00139", "name": "刺痛", "type": "tcm_symptom",
                           "source_vocab": "symmap", "condition_alias": "刺痛 (zh) · Ci Tong (pinyin)"},
            },
            "ingredient_condition": {
                "how": [
                    "Scraped herb → TCM symptom / modern symptom / syndrome: beneficial, traditional, tcm",
                    "Inferred herb → disease kept only at FDR(BH) ≤ 0.05: association, predicted",
                    "9,908 rows, 8,940 of them predicted",
                ],
                "raw": {"file": "Data/symmap/scrape/herb_tcm_symptom_relations.csv", "row": {
                    "source_herb_id": "SMHB00198",
                    "source_herb": "Jianghuang (turmeric)",
                    "Symptom_pinyin": "Ci Tong",
                    "Symptom_property": "瘀血",
                    "TCM_symptom_id": "SMTS00139",
                    "TCM_symptom_name": "刺痛",
                }},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "condition_id": "TCM:SMTS00139",
                    "direction": "beneficial",
                    "evidence_type": "traditional",
                    "tradition": "tcm",
                    "source_id": "symmap",
                    "note": "刺痛 Ci Tong",
                },
            },
        },
    },
    "herb": {
        "name": "HERB",
        "note": "HERB",
        "what": "TCM herb database: herbs, ingredients, DisGeNET diseases and herb clinical trials",
        "origin": "BUCM / ICT-CAS · HERB 2.0 (NAR 2025)",
        "access": "download endpoint + scraped herb pages",
        "tables": {
            "ingredient_xref": {
                "how": [
                    "Herb matched via DDID bridge, SymMap link, else Latin/English/Chinese name",
                    "Herb_id → 'herb'; cn / pinyin / Latin / English names → aliases",
                ],
                "raw": {"file": "Data/herb/HERB_herb_info_v2.txt", "row": {
                    "Herb_id": "HERB002840",
                    "Herb_pinyin_name": "Jiang Huang",
                    "Herb_cn_name": "姜黄",
                    "Herb_en_name": "Turmeric; Rhizome of Common Turmeric",
                    "Herb_latin_name": "Rhizoma Curcumae Longae; Curcumae Longae Rhizoma",
                    "SymMap_id": "SMHB00198",
                }},
                "result": {"ingredient_id": "ING:turmeric", "db": "herb", "xref_id": "HERB002840"},
            },
            "ingredient_property": {
                "how": ["Properties / Meridians split into tcm nature, flavour, meridian rows"],
                "raw": {"file": "Data/herb/HERB_herb_info_v2.txt", "row": {
                    "Herb_id": "HERB002840", "Properties": "Pungent; Bitter; Warm", "Meridians": "Spleen; Liver"}},
                "result": {"ingredient_id": "ING:turmeric", "system": "tcm", "property": "flavour", "value": "pungent",
                           "source_id": "herb"},
            },
            "compound": {
                "how": [
                    "Only ingredients linked to herbs in the scraped herb → ingredient table",
                    "NPASS_id (NPC…) used as an explicit merge key",
                ],
                "raw": {"file": "Data/herb/HERB_ingredient_info_v2.txt", "row": {
                    "Ingredient_id": "HBIN021985",
                    "Ingredient_name": "Curcumin",
                    "InChIKey": "VFLDPWHFBUODDF-FCXRPNKRSA-N",
                    "CAS_id": "485-37-7",
                    "PubChem_id": "969516",
                    "NPASS_id": "NPC160900",
                }},
                "result": {"compound_id": CURCUMIN, "name": "Curcumin", "pubchem_cid": 969516,
                           "compound_xref": "herb HBIN021985"},
            },
            "ingredient_compound": {
                "how": ["Scraped herb → ingredient pairs; presence only; evidence traditional"],
                "raw": {"file": "Data/herb/scrape/herb_ingredient.csv", "row": {
                    "source_herb_id": "HERB002840",
                    "source_herb": "Jiang Huang",
                    "Ingredient id": "HBIN021985",
                    "Ingredient name": "Curcumin",
                    "Molecular formula": "C21H20O6",
                }},
                "result": {"ingredient_id": "ING:turmeric", "compound_id": CURCUMIN, "evidence_type": "traditional",
                           "source_id": "herb"},
            },
            "condition": {
                "how": [
                    "DisGeNET diseases merged into existing rows by MeSH, then UMLS",
                    "New UMLS:… rows only for 'Sign or Symptom' or terms with a MeSH/DO id",
                    "HERB and ICD-10 ids → xref aliases",
                ],
                "raw": {"file": "Data/herb/HERB_disease_info_v2.txt", "row": {
                    "Disease_id": "HBDIS011780",
                    "Disease_name": "Nausea In Pregnancy",
                    "DisGeNET_disease_type": "phenotype",
                    "UMLS_disease_type": "Sign or Symptom",
                    "DisGeNET_id": "C0848080",
                    "MeSH_id": "NA",
                }},
                "result": {"condition_id": "UMLS:C0848080", "name": "Nausea In Pregnancy", "type": "symptom",
                           "umls_cui": "C0848080", "source_vocab": "herb",
                           "condition_alias": "HERB:HBDIS011780 (xref)"},
            },
            "ingredient_condition": {
                "how": [
                    "Scraped herb clinical trials; study condition → condition by text",
                    "beneficial only if the conclusion reads positive and not negative; else association",
                    "evidence clinical; 18 rows (turmeric, cassia)",
                ],
                "raw": {"file": "Data/herb/scrape/clinical_herb.csv", "row": {
                    "source_herb_id": "HERB002840",
                    "NCT id": "NCT01831193",
                    "NCT title": "Effect of Oral Supplementation With Curcumin (Turmeric) in Patients With Proteinuric…",
                    "Study condition": "Proteinuria",
                    "PubMed id": "37916745",
                    "Conclusion": "We found no evidence that antioxidants reduced death or improved kidney transplant…",
                }},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "condition_id": "MESH:D011507",
                    "direction": "association",
                    "evidence_type": "clinical",
                    "pmids": "37916745",
                    "source_id": "herb",
                    "note": "NCT01831193 Proteinuria",
                },
            },
        },
    },
    "tmmc": {
        "name": "TM-MC",
        "note": "TM-MC",
        "what": "Medicinal materials of Northeast Asian traditional medicine with literature-curated compounds",
        "origin": "Korea Institute of Oriental Medicine · TM-MC 2.0",
        "access": "direct xlsx download, no login",
        "tables": {
            "ingredient_xref": {
                "how": [
                    "Material matched by pharmacopoeia Latin genus + species, confirmed by English name",
                    "xref id = LATIN (the join key of medicinal_compound)",
                ],
                "raw": {"file": "Data/tm-mc/medicinal_material.xlsx", "row": {
                    "LATIN": "Curcumae Longae Rhizoma",
                    "COMMON": "Curcuma Longa Rhizome",
                    "KOREAN": "강황",
                    "HANJA": "薑黃",
                    "CHINESE": "姜黄",
                    "JAPANESE": "ウコン",
                    "KANJI": "鬱金",
                }},
                "result": {"ingredient_id": "ING:turmeric", "db": "tmmc", "xref_id": "Curcumae Longae Rhizoma"},
            },
            "ingredient_alias": {
                "how": ["Korean, Hanja, Chinese, pinyin, Japanese and kanji names → aliases"],
                "raw": {"file": "Data/tm-mc/medicinal_material.xlsx", "row": {
                    "LATIN": "Curcumae Longae Rhizoma", "KOREAN": "강황"}},
                "result": {"ingredient_id": "ING:turmeric", "alias": "강황", "lang": "ko", "alias_type": "ko",
                           "source_id": "tmmc"},
            },
            "compound": {
                "how": [
                    "chemical_property rows linked to a material; InChIKey + CID",
                    "Compound names from medicinal_compound become synonyms",
                ],
                "raw": {"file": "Data/tm-mc/chemical_property.xlsx", "row": {
                    "ID": "969516",
                    "INCHIKEY": "VFLDPWHFBUODDF-FCXRPNKRSA-N",
                    "CID": "969516",
                    "FORMULA": "C21H20O6",
                    "MW": "368.385",
                }},
                "result": {"compound_id": CURCUMIN, "name": "Curcumin", "pubchem_cid": 969516,
                           "compound_xref": "tmmc 969516"},
            },
            "ingredient_compound": {
                "how": [
                    "medicinal_compound: material × compound, one row per paper",
                    "PMIDs aggregated into citation; evidence curated_literature",
                ],
                "raw": {"file": "Data/tm-mc/medicinal_compound.xlsx", "row": {
                    "LATIN": "Curcumae Longae Rhizoma",
                    "ID": "969516",
                    "COMPOUND": "(1E,6E)-1,7-bis(4-hydroxy-3-methoxyphenyl)-1,6-heptadiene-3,5-dione",
                    "PMID": "24300368",
                }},
                "result": {"ingredient_id": "ING:turmeric", "compound_id": CURCUMIN,
                           "evidence_type": "curated_literature", "source_id": "tmmc",
                           "citation": "PMID:15668484|PMID:20092313|PMID:25846263|…"},
            },
        },
    },
    "imppat": {
        "name": "IMPPAT",
        "note": "IMPPAT",
        "what": "Indian medicinal plants with phytochemicals and therapeutic uses (Ayurveda, Siddha, Unani…)",
        "origin": "IMSc Chennai (Samal lab) · IMPPAT 3.0 (2026)",
        "access": "TSV batch downloads",
        "tables": {
            "ingredient_xref": {
                "how": [
                    "Plant matched by scientific name or listed synonyms",
                    "Plant_identifier → 'imppat'; common name → alias",
                ],
                "raw": {"file": "Data/imppat/Plant_Information_IMPPAT.tsv", "row": {
                    "Plant_identifier": "IMPPAT3_PLTID000933",
                    "Indian_Medicinal_plant": "Curcuma longa",
                    "Synonymous names": "Curcuma domestica|Curcuma longa|Curcuma longas|Curcuma ionga",
                    "Common_name": "Turmeric",
                    "System_of_Medicine": "Ayurveda,Homeopathy,Siddha,Sowa Rigpa,Unani",
                }},
                "result": {"ingredient_id": "ING:turmeric", "db": "imppat", "xref_id": "IMPPAT3_PLTID000933"},
            },
            "compound": {
                "how": ["Phytochemical table: standardised name, CID, ChEBI, InChIKey, synonyms"],
                "raw": {"file": "Data/imppat/Chemical_Information_IMPPAT_Phytochemicals.tsv", "row": {
                    "IMPPAT_Phytochemical_identifier": "IMPPAT3_PHYID005594",
                    "Phytochemical name_standardised": "Curcumin",
                    "Pubchem_CID": "CID_969516",
                    "ChEBI": "CHEBI:3962",
                    "InChIKey": "VFLDPWHFBUODDF-FCXRPNKRSA-N",
                }},
                "result": {"compound_id": CURCUMIN, "name": "Curcumin", "pubchem_cid": 969516,
                           "compound_xref": "imppat IMPPAT3_PHYID005594"},
            },
            "ingredient_compound": {
                "how": ["Phytochemical–plant association; Plant_part → plant_part; reference kept as citation"],
                "raw": {"file": "Data/imppat/IMPPAT_Phytochemical_Plant_Association.tsv", "row": {
                    "Plant_identifier": "IMPPAT3_PLTID000933",
                    "Indian_Medicinal_plant": "Curcuma longa",
                    "Plant_part": "rhizome",
                    "IMPPAT_Phytochemical_identifier": "IMPPAT3_PHYID005594",
                    "Reference_identifier": "CID_969516",
                }},
                "result": {"ingredient_id": "ING:turmeric", "compound_id": CURCUMIN, "plant_part": "rhizome|whole plant",
                           "evidence_type": "curated_literature", "source_id": "imppat", "citation": "CID_969516"},
            },
            "ingredient_condition": {
                "how": [
                    "Therapeutic_use text → condition, or action → its targets via action_map.csv",
                    "'hypoglycemic agents' → Diabetes Mellitus + Hyperglycemia",
                    "tradition from System_of_Medicine (ayurveda if listed); evidence traditional",
                ],
                "raw": {"file": "Data/imppat/IMPPAT_TherapeuticUse_Plant_Association.tsv", "row": {
                    "IMPPAT_Plant_identifier": "IMPPAT3_PLTID000933",
                    "Indian_Medicinal_plant": "Curcuma longa",
                    "Plant_part": "rhizome",
                    "IMPPAT_Therapeutic_use_identifier": "IMPPAT3_TPUID000770",
                    "Therapeutic_use": "hypoglycemic agents",
                }},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "condition_id": "MESH:D003920",
                    "direction": "beneficial",
                    "evidence_type": "traditional",
                    "tradition": "ayurveda",
                    "plant_part": "rhizome",
                    "source_id": "imppat",
                    "note": "hypoglycemic agents; diabetes mellitus",
                },
            },
        },
    },
    "spicerx": {
        "name": "SpiceRx",
        "note": "SpiceRx",
        "what": "Spice–disease associations text-mined from MEDLINE, with positive/negative abstract counts",
        "origin": "CoSyLab, IIIT-Delhi · 2018 (sampled)",
        "access": "small polite scrape of JSON endpoints",
        "tables": {
            "ingredient_xref": {
                "how": ["Spice matched by NCBI taxon; tax_id → 'spicerx'; common name → alias"],
                "raw": {"file": "Data/spicerx/spices.csv", "row": {
                    "tax_id": "136217", "common_name": "Turmeric", "scientific_name": "Curcuma Longa",
                    "disease_pages": "22"}},
                "result": {"ingredient_id": "ING:turmeric", "db": "spicerx", "xref_id": "136217"},
            },
            "ingredient_condition": {
                "how": [
                    "Disease by MeSH id; n_pos > n_neg → beneficial, < → harmful, = → association",
                    "PMIDs joined from spice_disease_references.csv",
                    "evidence text_mined",
                ],
                "raw": {"file": "Data/spicerx/spice_disease_associations.csv", "row": {
                    "tax_id": "136217", "spice": "Turmeric", "mesh_id": "MESH:D003920",
                    "disease": "Diabetes Mellitus", "n_positive": "45", "n_negative": "0"}},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "condition_id": "MESH:D003920",
                    "direction": "beneficial",
                    "evidence_type": "text_mined",
                    "n_pos": 45,
                    "n_neg": 0,
                    "pmids": "22855997|27325504|22980852|19765405|…",
                    "source_id": "spicerx",
                },
            },
        },
    },
    "unaprod": {
        "name": "UNaProd",
        "note": "UNaProd",
        "what": "Persian medicine materia medica: monographs with Mizaj (temperament), actions and uses",
        "origin": "School of Persian Medicine, Tehran UMS · v1.2 beta",
        "access": "site table backend + sampled monographs",
        "tables": {
            "ingredient_xref": {
                "how": [
                    "Monographs matched by scientific name; index-only drugs via a curated id map",
                    "ID → 'unaprod'; Persian/Arabic names → aliases (fa, ar, hi, syr)",
                ],
                "raw": {"file": "Data/unaprod/unaprod_drug_list.csv", "row": {
                    "ID": "1130",
                    "DrugName": "عروق الصفر",
                    "Pronunciation": "ʔæruɢossofr",
                    "Origin": "herbal",
                    "MizajType": "Unbalanced Hot And Dry Mizaj",
                }},
                "result": {"ingredient_id": "ING:turmeric", "db": "unaprod", "xref_id": "1130",
                           "ingredient_alias": "عروق الصفر (fa)"},
            },
            "ingredient_alias": {
                "how": ["DrugName, CommonName2 and language-tagged Synonyms ('هندی: کیسر' → hi)"],
                "raw": {"file": "Data/unaprod/unaprod_monographs_sample.csv", "row": {
                    "ID": "827", "DrugName": "زعفران", "SciName1": "Crocus sativus",
                    "Synonyms": "['سریانی: کرکم', 'سریانی: جاوی', 'فارسی: لرکیماس', 'هندی: کیسر']"}},
                "result": {"ingredient_id": "ING:saffron", "alias": "زعفران", "lang": "fa", "alias_type": "fa",
                           "source_id": "unaprod"},
            },
            "ingredient_property": {
                "how": ["MizajType → persian_mizaj 'mizaj'; MizajDegree → 'mizaj_degree'"],
                "raw": {"file": "Data/unaprod/unaprod_drug_list.csv", "row": {
                    "ID": "1130", "DrugName": "عروق الصفر", "MizajType": "Unbalanced Hot And Dry Mizaj"}},
                "result": {"ingredient_id": "ING:turmeric", "system": "persian_mizaj", "property": "mizaj",
                           "value": "Unbalanced Hot And Dry Mizaj", "source_id": "unaprod"},
            },
            "ingredient_condition": {
                "how": [
                    "DiseaseType terms → conditions (text); ActionType only through the action map",
                    "Persian-transliterated terms (Shoseh, Barsam) mostly stay unmapped",
                    "direction beneficial, evidence traditional, tradition persian",
                ],
                "raw": {"file": "Data/unaprod/unaprod_monographs_sample.csv", "row": {
                    "ID": "827",
                    "DrugName": "زعفران",
                    "SciName1": "Crocus sativus",
                    "MizajDegree": "DryFirst; HotSecond; DrySecond; HotThird",
                    "DiseaseType": "brain obstruction; spleen obstruction; difficult delivery; alcohol withdrawal; …; gout; …",
                }},
                "result": {
                    "ingredient_id": "ING:saffron",
                    "condition_id": "MESH:D006073",
                    "direction": "beneficial",
                    "evidence_type": "traditional",
                    "tradition": "persian",
                    "source_id": "unaprod",
                    "note": "gout",
                },
            },
        },
    },
    "duke": {
        "name": "Dr. Duke's",
        "note": "Dr. Duke's Phytochemical and Ethnobotanical Databases",
        "what": "USDA phytochemical and ethnobotany tables: plant uses by country, chemical activities",
        "origin": "USDA ARS (J. Duke) · Ag Data Commons, CSVs 2016",
        "access": "figshare API download, full",
        "tables": {
            "ingredient_xref": {
                "how": [
                    "FNFTAX taxa matched by scientific name; FNFNUM and TAXON → 'duke'",
                    "COMMON_NAMES + ETHNOBOT local names → aliases ('Kunyit', 'Temu kuning')",
                ],
                "raw": {"file": "Data/dr-dukes-phytochemical-and-ethnobotanical-databases/FNFTAX.csv", "row": {
                    "FNFNUM": "331", "TAXON": "Curcuma longa", "TAXAUTHOR": "L.", "FAMILY": "Zingiberaceae",
                    "SPCMT": "Synonyms: Curcuma domestica Valeton"}},
                "result": {"ingredient_id": "ING:turmeric", "db": "duke", "xref_id": "331"},
            },
            "ingredient_condition": {
                "how": [
                    "ETHNOBOT activity per taxon and country → condition or action targets",
                    "direction beneficial, evidence traditional, tradition folk; country kept in note",
                ],
                "raw": {"file": "Data/dr-dukes-phytochemical-and-ethnobotanical-databases/ETHNOBOT.csv", "row": {
                    "ETHNO": "13032", "ACTIVITY": "Conjunctivitis", "TAXON": "Curcuma longa", "CNAME": "Kunir",
                    "COUNTRY": "Java", "REFERENCE": "Burkill,1966"}},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "condition_id": "MESH:D003231",
                    "direction": "beneficial",
                    "evidence_type": "traditional",
                    "tradition": "folk",
                    "source_id": "duke",
                    "note": "Conjunctivitis (Java)",
                },
            },
            "compound_condition": {
                "how": [
                    "AGGREGAC chemical activities; chemical resolved by name",
                    "Activity → condition via action map ('Hypocholesterolemic' → Hypercholesterolemia)",
                    "evidence traditional; 9,849 rows",
                ],
                "raw": {"file": "Data/dr-dukes-phytochemical-and-ethnobotanical-databases/AGGREGAC.csv", "row": {
                    "AGGNO": "134134", "CHEM": "CURCUMIN", "ACTIVITY": "Hypocholesterolemic",
                    "DOSAGE": "0.15% diet 7 wks", "REFERENCE": "FT68:483"}},
                "result": {
                    "compound_id": CURCUMIN,
                    "condition_id": "MESH:D006937",
                    "direction": "beneficial",
                    "evidence_type": "traditional",
                    "source_id": "duke",
                    "condition.name": "Hypercholesterolemia",
                },
            },
        },
    },
    "knapsack": {
        "name": "KNApSAcK",
        "note": "KNApSAcK Family",
        "what": "Species uses per country (edible / medicinal) and Indonesian Jamu formula claims",
        "origin": "Kanaya lab, NAIST Japan · web DBs (sampled)",
        "access": "polite scrape of country and Jamu pages",
        "tables": {
            "ingredient_xref": {
                "how": ["World species names matched by scientific name; species string → 'knapsack'"],
                "raw": {"file": "Data/knapsack-family/world_country_species.csv", "row": {
                    "country_code": "JPN", "species": "Curcuma longa", "family": "Zingiberaceae",
                    "common_name": "Turmeric | Haridra", "purpose": "edible"}},
                "result": {"ingredient_id": "ING:turmeric", "db": "knapsack", "xref_id": "Curcuma longa"},
            },
            "ingredient_alias": {
                "how": ["common_name → en aliases; common_name_ja → ja aliases (ウコン, ターメリック)"],
                "raw": {"file": "Data/knapsack-family/world_country_species.csv", "row": {
                    "country_code": "JPN", "species": "Curcuma longa",
                    "common_name_ja": "ウコン | ターメリック | クルクマ | アキウコン | キゾメグサ | ウッチン | ハルディ | クニッツ"}},
                "result": {"ingredient_id": "ING:turmeric", "alias": "ターメリック", "lang": "ja", "alias_type": "ja",
                           "source_id": "knapsack"},
            },
            "ingredient_property": {
                "how": ["purpose per country → knapsack_use 'use_in_<ISO2>' = edible / medicinal"],
                "raw": {"file": "Data/knapsack-family/world_country_species.csv", "row": {
                    "country_code": "JPN", "country": "Japan", "species": "Curcuma longa", "purpose": "edible"}},
                "result": {"ingredient_id": "ING:turmeric", "system": "knapsack_use", "property": "use_in_JP",
                           "value": "edible", "source_id": "knapsack"},
            },
            "ingredient_condition": {
                "how": [
                    "Jamu formula effect text split into terms → conditions",
                    "Every herb in the formula gets the formula's claim; tradition jamu",
                    "27 rows; loose matches occur ('tongue…' → Tongue Neoplasms)",
                ],
                "raw": {"file": "Data/knapsack-family/jamu_formula_herbs.csv", "row": {
                    "company": "PJ. Cap Kresno Narodo", "jamu_name": "Jamu Batuk", "jamu_effect": "Cure cough",
                    "herb_name_indonesia": "Jahe", "scientific_name": "Zingiber officinale Rosc",
                    "plant_part": "Rhizome"}},
                "result": {
                    "ingredient_id": "ING:ginger",
                    "condition_id": "MESH:D003371",
                    "direction": "beneficial",
                    "evidence_type": "traditional",
                    "tradition": "jamu",
                    "plant_part": "Rhizome",
                    "source_id": "knapsack",
                    "note": "cough medicine; jamu formula 'Jamu Batuk': Cure cough",
                },
            },
        },
    },
    # ------------------------------------------------------------------------------------------------ drugs
    "ddid": {
        "name": "DDID",
        "note": "DDID",
        "what": "Curated food/herb–drug interactions with effect, mechanism and PMID; drug indications",
        "origin": "Hangzhou Normal Univ. · Brief Bioinform 2024",
        "access": "direct CSV download (slow server)",
        "tables": {
            "ingredient_xref": {
                "how": [
                    "Foods by FoodB_ID first, then taxon / scientific / English name",
                    "Herbs by taxon, Latin, pharmacopoeia, English, Chinese; bridge for SymMap/HERB",
                    "FHDI ids → 'ddid_food' / 'ddid_herb'; herb Chinese + pinyin → aliases",
                ],
                "raw": {"file": "Data/ddid/food_information.csv", "row": {
                    "FHDI_Food_ID": "F00015", "Food_Name": "Turmeric", "Scientific_Name": "Curcuma longa",
                    "Group": "Spices", "FoodB_ID": "FOOD00068", "Taxonomy_ID": "136217"}},
                "result": {"ingredient_id": "ING:turmeric", "db": "ddid_food", "xref_id": "F00015"},
            },
            "drug": {
                "how": [
                    "drug_information.csv: id DB:<DrugBank id>, else DRUGNAME:<slug>",
                    "InChIKey kept for joins to compounds",
                ],
                "raw": {"file": "Data/ddid/drug_information.csv", "row": {
                    "FHDI_Drug_ID": "D01217", "Drug_Name": "Warfarin", "Drug_Type": "Small molecular drug",
                    "InChIKey": "PJVWKTKQMONHTI-UHFFFAOYSA-N", "DrugBank_ID": "DB00682", "CAS_Number": "CAS 81-81-2"}},
                "result": {"drug_id": "DB:DB00682", "name": "Warfarin", "drugbank_id": "DB00682",
                           "inchikey": "PJVWKTKQMONHTI-UHFFFAOYSA-N"},
            },
            "drug_condition": {
                "how": [
                    "Indication '… [ICD-11: code]' → ICD11 condition, followed via same_as to MeSH",
                    "1,610 rows; unresolved codes dropped",
                ],
                "raw": {"file": "Data/ddid/disease_information.csv", "row": {
                    "TTD_ID": "D0E3OF", "Indication": "Atrial fibrillation [ICD-11: BC81.3]", "State": "Approved",
                    "FHDI_Drug_ID": "D01217"}},
                "result": {"drug_id": "DB:DB00682", "condition_id": "MESH:D001281", "source_id": "ddid",
                           "condition.name": "Atrial Fibrillation"},
            },
            "condition": {
                "how": [
                    "Indication ICD-11 codes → ICD11:… conditions (shared with CMAUP codes)",
                    "Indication label → condition_alias (source ddid)",
                ],
                "raw": {"file": "Data/ddid/disease_information.csv", "row": {
                    "TTD_ID": "D0Z8EV", "Indication": "Coronavirus Disease 2019 (COVID-19) [ICD-11: 1D6Y]",
                    "State": "Investigative", "FHDI_Drug_ID": "D00775"}},
                "result": {"condition_id": "ICD11:1D6Y", "name": "COVID-19", "type": "disease", "icd11": "1D6Y",
                           "source_vocab": "icd11", "condition_alias": "Coronavirus Disease 2019 (COVID-19) (ddid)",
                           "condition_relation": "same_as MESH:D000086382"},
            },
            "ingredient_drug": {
                "how": [
                    "Food_Herb_ID → ingredient via ddid_food / ddid_herb xref; Drug_ID → drug",
                    "Effect kept (Harmful, Negative, Positive, No Effect, Possible); Potential_Target → mechanism",
                    "PMID → curated_literature; Possible without PMID → predicted",
                    "Note = Conclusion (or Result), prefixed with [Component]",
                ],
                "raw": {"file": "Data/ddid/interaction_information.csv", "row": {
                    "Drug_ID": "D01217",
                    "Drug_Name": "Warfarin",
                    "Food_Herb_ID": "F00015",
                    "Food_Herb_Name": "Turmeric",
                    "Note": "Curcuma xanthorrhiza Roxb. (Zingiberaceae)",
                    "Experimental_Species": "Rat",
                    "Effect": "Possible",
                    "PMID": "34062109",
                }},
                "result": {
                    "ingredient_id": "ING:turmeric",
                    "drug_id": "DB:DB00682",
                    "effect": "Possible",
                    "evidence_type": "curated_literature",
                    "pmid": "34062109",
                    "source_id": "ddid",
                    "note": "The CX administration in a higher dose caused alteration on WF pharmacokinetics suggest…",
                },
            },
        },
    },
    "drugbank": {
        "name": "DrugBank",
        "note": "DrugBank",
        "what": "Drug knowledgebase; here only food-interaction text and 12 public drug cards",
        "origin": "OMx / U. Alberta · DrugBank 6.0 (sample)",
        "access": "downloads disabled (403); public pages sampled",
        "tables": {
            "drug": {
                "how": [
                    "Drugs from the food-interaction sample and public drug cards, if not already from DDID",
                    "InChIKey from the drug card",
                ],
                "raw": {"file": "Data/drugbank/public_drug_cards.csv", "row": {
                    "drugbank_id": "DB11672", "name": "Curcumin",
                    "primary_indication": "No approved therapeutic indications.", "CAS": "458-37-7",
                    "PubChem": "969516", "InChIKey": "VFLDPWHFBUODDF-FCXRPNKRSA-N"}},
                "result": {"drug_id": "DB:DB11672", "name": "Curcumin", "drugbank_id": "DB11672",
                           "inchikey": "VFLDPWHFBUODDF-FCXRPNKRSA-N"},
            },
            "ingredient_drug": {
                "how": [
                    "Food_Herb_Name → ingredient by text (no fuzzy); only pairs DDID lacks",
                    "Possible → predicted, else curated_literature; no PMIDs; 121 rows",
                ],
                "raw": {"file": "Data/drugbank/food_interactions_via_ddid.csv", "row": {
                    "drugbank_id": "DB04846", "Drug_Name": "Celiprolol", "Food_Herb_Name": "Orange", "Type": "Food",
                    "Result": "Orange juice may reduce the absorption of celiprolol.", "Effect": "Negative",
                    "Conclusion": "Avoid fruit juice."}},
                "result": {"ingredient_id": "ING:orange", "drug_id": "DB:DB04846", "effect": "Negative",
                           "evidence_type": "curated_literature", "source_id": "drugbank",
                           "note": "Avoid fruit juice."},
            },
        },
    },
    # ------------------------------------------------------------------------------------------------ curated
    "manual": {
        "name": "Curated maps (db/maps)",
        "note": None,
        "what": "Hand-made maps: ingredient merge groups, dish-line matches, nutrients, actions, condition synonyms",
        "origin": "this repository · db/maps/*.csv + build/ingredients.py",
        "access": "in the repository",
        "tables": {
            "ingredient": {
                "how": [
                    "149 merge groups in build/ingredients.py: first name canonical, plus taxon / scientific name",
                    "Rank 0 seeds: win canonical names ('turmeric', 'haldi', 'tumeric')",
                    "New ingredients for dish lines flagged 'new:<category>' in ingredient_map_manual.csv",
                ],
                "raw": {"file": "db/build/ingredients.py (MANUAL_GROUPS)", "row": {
                    "names": "turmeric, haldi, turmericpowder, tumeric, turmeric powder",
                    "category": "spice",
                    "scientific_name": "Curcuma longa",
                    "taxon": "136217",
                }},
                "result": {"ingredient_id": "ING:turmeric", "canonical_name": "turmeric", "category": "spice",
                           "scientific_name": "Curcuma longa", "ncbi_taxon_id": 136217},
            },
            "dish_ingredient": {
                "how": [
                    "ingredient_map_manual.csv rows (849) load as aliases with source 'manual'",
                    "A hit on one is reported as match_method 'manual'",
                    "Covers local terms (waddak, 味噌, 花椒) the source vocabularies miss",
                ],
                "raw": {"file": "db/maps/ingredient_map_manual.csv", "row": {
                    "raw_norm": "rendered fat", "lang": "en", "ingredient_id": "ING:tail-fat",
                    "note": "Saudi recipe: rendered sheep fat"}},
                "result": {"dish_id": "sfct:68", "ingredient_id": "ING:tail-fat", "raw_text": "Rendered fat (waddak)",
                           "quantity": 50.0, "unit": "g", "grams": 50.0, "match_method": "manual",
                           "match_score": 0.95},
            },
            "compound": {
                "how": [
                    "nutrient_map.csv: source nutrient label → MeSH nutrient concept",
                    "Concepts not in CTD become compounds (NAME:… / MESH:…); all flagged is_nutrient",
                ],
                "raw": {"file": "db/maps/nutrient_map.csv", "row": {
                    "nutrient_key": "Sum of Omega-9 (n-9) [g]", "source": "sfct", "name": "Sum of Omega-9 (n-9)",
                    "unit": "g", "mesh_id": "", "compound_name": "Omega-9 fatty acids"}},
                "result": {"compound_id": "NAME:omega-9-fatty-acids", "name": "Omega-9 fatty acids",
                           "is_nutrient": True},
            },
            "condition": {
                "how": [
                    "action_map.csv: 'hypoglycemic', 'antiemetic'… → ACT:… conditions (type action)",
                    "Spelling variants of each action → aliases",
                    "condition_synonyms.csv: folk / obsolete terms ('dropsy') → aliases of MeSH conditions",
                ],
                "raw": {"file": "db/maps/action_map.csv", "row": {
                    "action": "hypoglycemic", "condition_id": "MESH:D003920", "direction": "beneficial",
                    "note": "Diabetes Mellitus; blood-glucose lowering"}},
                "result": {"condition_id": "ACT:hypoglycemic", "name": "hypoglycemic", "type": "action",
                           "source_vocab": "action_map"},
            },
            "condition_relation": {
                "how": [
                    "One action_targets edge per action_map row (202 rows)",
                    "Link loaders replace an action hit by its targets with the map's direction",
                ],
                "raw": {"file": "db/maps/action_map.csv", "row": {
                    "action": "hypoglycemic", "condition_id": "MESH:D006943", "direction": "beneficial",
                    "note": "Hyperglycemia; blood-glucose lowering"}},
                "result": {"from_id": "ACT:hypoglycemic", "to_id": "MESH:D006943", "rel": "action_targets"},
            },
        },
    },
}


TABLES = {
    "source": {
        "title": "Source",
        "role": "One registered dataset: code, vault note, version, licence",
        "why": ["Every row in the database points here through source_id",
                "Licence and version let the agent qualify what it cites"],
    },
    "evidence_type": {
        "title": "Evidence type",
        "role": "One evidence grade, ranked 1 (clinical) to 6 (predicted)",
        "why": ["Lets the agent rank and filter claims by strength",
                "Separates a trial from a folk use from a prediction"],
    },
    "dish": {
        "title": "Dish",
        "role": "One recipe or dish from a source, with country and region",
        "why": ["Entry point: what the patient ate, in their own cuisine",
                "Local names, sub-regions and steps keep cultural context"],
    },
    "dish_ingredient": {
        "title": "Dish ingredient",
        "role": "One recipe line, matched to an ingredient, with grams if known",
        "why": ["Grams turn 'contains turmeric' into a dose",
                "match_method and score show how much to trust the link"],
    },
    "dish_nutrient": {
        "title": "Dish nutrient",
        "role": "One measured nutrient value per 100 g of a dish",
        "why": ["Lab values for sodium, sugar, fat… in regional dishes",
                "Direct input for diet advice (e.g. salt limits)"],
    },
    "ingredient": {
        "title": "Ingredient",
        "role": "One canonical food or culinary herb",
        "why": ["Hub joining recipes, compounds, traditional uses and drug interactions",
                "Taxon and scientific name keep food and herb records the same plant"],
    },
    "ingredient_alias": {
        "title": "Ingredient alias",
        "role": "One name of an ingredient in some language or script",
        "why": ["Resolves 姜黄, ウコン, haldi and عروق الصفر to one turmeric",
                "Lets the agent read recipes written in the patient's language"],
    },
    "ingredient_xref": {
        "title": "Ingredient xref",
        "role": "One id of an ingredient in an external database",
        "why": ["Deterministic joins to herb, food and drug-interaction sources",
                "Shows how widely an ingredient is documented"],
    },
    "ingredient_property": {
        "title": "Ingredient property",
        "role": "One traditional property: TCM nature, Persian Mizaj, use by country",
        "why": ["Frames advice in the patient's own medical tradition",
                "Records where a plant is eaten versus used as medicine"],
    },
    "compound": {
        "title": "Compound",
        "role": "One chemical or nutrient, merged across sources by structure",
        "why": ["Bridge from food to mechanism: what in turmeric acts",
                "Nutrient concepts (dietary protein, fibre) sit beside molecules"],
    },
    "compound_xref": {
        "title": "Compound xref",
        "role": "One external id or synonym of a compound",
        "why": ["Name and id lookup across 11 compound sources",
                "ctd_match records how the MeSH id was reached"],
    },
    "ingredient_compound": {
        "title": "Ingredient compound",
        "role": "One compound found in an ingredient, with amount if measured",
        "why": ["mg/100 g × grams in the dish estimates actual intake",
                "Presence-only rows still show which foods carry a compound"],
    },
    "condition": {
        "title": "Condition",
        "role": "One disease, symptom, finding, TCM term or action",
        "why": ["One vocabulary for MeSH, UMLS, ICD-11 and TCM terms",
                "Symptoms and TCM syndromes match how patients describe complaints"],
    },
    "condition_alias": {
        "title": "Condition alias",
        "role": "One name or external id of a condition",
        "why": ["Maps free text ('dropsy', 刺痛, 'type 2 diabetes') to a condition",
                "Carries UMLS / OMIM / ICD ids for cross-vocabulary lookup"],
    },
    "condition_relation": {
        "title": "Condition relation",
        "role": "One edge: is_a, same_as, or action_targets",
        "why": ["is_a lets evidence on a child count for its parent",
                "action_targets turns 'hypoglycemic' into Diabetes Mellitus"],
    },
    "compound_condition": {
        "title": "Compound condition",
        "role": "One compound–condition claim with direction, evidence and PMIDs",
        "why": ["Mechanistic evidence: curcumin → type 2 diabetes (CTD, PMID)",
                "direction separates benefit, harm and biomarker"],
    },
    "ingredient_condition": {
        "title": "Ingredient condition",
        "role": "One direct food/herb–condition claim, by tradition and evidence",
        "why": ["Traditional, text-mined and trial evidence at the food level",
                "tradition column says which medical system makes the claim"],
    },
    "drug": {
        "title": "Drug",
        "role": "One drug, keyed by DrugBank id",
        "why": ["Target of the food–drug safety check",
                "InChIKey joins drugs that are also food compounds"],
    },
    "drug_condition": {
        "title": "Drug condition",
        "role": "One drug indication",
        "why": ["Infers why a patient takes a drug (warfarin → atrial fibrillation)",
                "Links a patient's condition to the drugs likely in use"],
    },
    "ingredient_drug": {
        "title": "Ingredient drug",
        "role": "One food/herb–drug interaction with effect and evidence",
        "why": ["Safety layer: flags turmeric with warfarin",
                "Effect and PMID let the agent weigh the warning"],
    },
}
