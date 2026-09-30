-- Analysis views over the unified database (loaded by stage `views`).
-- Evidence rank: 1 = strongest (clinical) … 6 = weakest (predicted). A path is only as strong as its weakest hop.

-- Every ingredient → condition path: direct links, plus ingredient → compound → condition.
CREATE OR REPLACE VIEW v_ingredient_condition_all AS
SELECT ic.ingredient_id,
       ic.condition_id,
       ic.direction,
       ic.evidence_type,
       e.rank                           AS evidence_rank,
       'direct'                         AS path_kind,
       NULL::VARCHAR                    AS compound_id,
       NULL::DOUBLE                     AS compound_mg_per_100g,
       ic.source_id                     AS link_source,
       NULL::VARCHAR                    AS content_source,
       ic.tradition,
       ic.pmids,
       ic.note
FROM ingredient_condition ic
JOIN evidence_type e ON e.code = ic.evidence_type
UNION ALL
SELECT icp.ingredient_id,
       cc.condition_id,
       cc.direction,
       CASE WHEN e1.rank >= e2.rank THEN icp.evidence_type ELSE cc.evidence_type END,
       greatest(e1.rank, e2.rank),
       'via_compound',
       cc.compound_id,
       icp.mg_per_100g,
       cc.source_id,
       icp.source_id,
       NULL,
       cc.pmids,
       NULL
FROM ingredient_compound icp
JOIN compound_condition cc ON cc.compound_id = icp.compound_id
JOIN evidence_type e1 ON e1.code = icp.evidence_type
JOIN evidence_type e2 ON e2.code = cc.evidence_type
-- predicted food→compound rows are only kept when an amount was reported
WHERE NOT (icp.evidence_type = 'predicted' AND icp.mg_per_100g IS NULL);

-- Ingredient → condition roll-up: one row per (ingredient, condition, direction). Materialised by the `views` stage
-- (it depends on the link tables, so re-run `views` after `links`). v_ingredient_condition_all has ~6M paths
-- (common spices reach thousands of conditions through CTD-linked compounds); joining those paths to 470k dish lines
-- directly would be ~700M rows, so dish-level views work on this roll-up instead.
-- How characteristic a compound is of an ingredient. Ubiquitous compounds (minerals, vitamins, sugars: 700+ of ~935
-- ingredients) would otherwise link every dish to the same broad CTD conditions.
CREATE OR REPLACE TABLE compound_profile AS
SELECT compound_id,
       count(DISTINCT ingredient_id) AS n_ingredients,   -- ingredients that contain it
       max(mg_per_100g)              AS max_mg_per_100g  -- richest known source
FROM ingredient_compound GROUP BY compound_id;

-- A path is *salient* when it is a direct ingredient → condition link, or goes through a characteristic compound:
-- a measured amount ≥ 1 mg/100 g of a compound that is either rare (≤ 20 ingredients) or of which this ingredient
-- is a major source (≥ 10% of the richest source; e.g. sodium in soy sauce, sugars in dates, curcumin in turmeric).
-- Half of all compounds occur in a single food at trace/unknown amounts, so rarity alone is not enough, and
-- ubiquitous nutrients only count where the food is a major source.
CREATE OR REPLACE TABLE ingredient_condition_rollup AS
WITH p AS (
  SELECT v.*,
         v.path_kind = 'direct'
         OR (v.compound_mg_per_100g >= 1
             AND (cp.n_ingredients <= 20 OR v.compound_mg_per_100g >= 0.1 * cp.max_mg_per_100g)) AS salient
  FROM v_ingredient_condition_all v
  LEFT JOIN compound_profile cp USING (compound_id)
)
SELECT ingredient_id, condition_id, direction,
       min(evidence_rank)                              AS best_evidence_rank,
       count(*)                                        AS n_paths,
       count(DISTINCT compound_id)                     AS n_compounds,
       count(DISTINCT link_source)                     AS n_sources,   -- independent link sources (corroboration)
       bool_or(path_kind = 'direct')                   AS has_direct,
       bool_or(salient)                                AS salient,
       min(evidence_rank) FILTER (WHERE salient)       AS salient_rank,
       count(DISTINCT link_source) FILTER (WHERE salient) AS salient_sources
FROM p
GROUP BY ingredient_id, condition_id, direction;

-- UK FSA front-of-pack "high" thresholds per 100 g (food), in mg. A lab-measured dish nutrient only counts as a
-- salient path when it is high; otherwise every dish would "reach" hypertension through its sodium.
CREATE OR REPLACE TABLE nutrient_high_threshold AS
SELECT * FROM (VALUES
  ('MESH:D012964', 'sodium',              600.0),
  ('MESH:D017673', 'salt',               1500.0),
  ('MESH:D000073417', 'sugars',         22500.0),
  ('MESH:D005227', 'saturated fat',      5000.0),
  ('MESH:D004041', 'fat',               17500.0)
) t(mesh_id, label, high_mg_per_100g);

-- Dish → condition, aggregated over ingredient roll-ups and lab-measured dish nutrients.
-- Always query it filtered (by dish_id or condition_id): unfiltered it is hundreds of millions of rows.
CREATE OR REPLACE VIEW v_dish_condition AS
WITH ing_paths AS (
  SELECT di.dish_id, r.condition_id, r.direction, r.best_evidence_rank AS evidence_rank, r.n_paths,
         r.n_compounds, r.n_sources, di.ingredient_id, di.grams, false AS via_nutrient,
         r.salient, r.salient_rank, r.salient_sources
  FROM dish_ingredient di
  JOIN ingredient_condition_rollup r USING (ingredient_id)
), nut AS (   -- lab-measured nutrients, in mg/100 g, flagged when above the FSA "high" threshold
  SELECT dn.dish_id, dn.nutrient_compound_id,
         dn.amount_per_100g * CASE lower(dn.unit) WHEN 'g' THEN 1000 WHEN 'µg' THEN 0.001 WHEN 'ug' THEN 0.001
                                                  WHEN 'mcg' THEN 0.001 ELSE 1 END AS mg,
         t.high_mg_per_100g
  FROM dish_nutrient dn
  JOIN compound c ON c.compound_id = dn.nutrient_compound_id
  LEFT JOIN nutrient_high_threshold t ON t.mesh_id = c.mesh_id
), nut_paths AS (
  SELECT n.dish_id, cc.condition_id, cc.direction, min(e.rank) AS evidence_rank, count(*) AS n_paths,
         count(DISTINCT cc.compound_id) AS n_compounds, count(DISTINCT cc.source_id) AS n_sources,
         NULL::VARCHAR AS ingredient_id, NULL::DOUBLE AS grams, true AS via_nutrient,
         bool_or(n.mg >= n.high_mg_per_100g) AS salient,
         min(e.rank) FILTER (WHERE n.mg >= n.high_mg_per_100g) AS salient_rank,
         count(DISTINCT cc.source_id) FILTER (WHERE n.mg >= n.high_mg_per_100g) AS salient_sources
  FROM nut n
  JOIN compound_condition cc ON cc.compound_id = n.nutrient_compound_id
  JOIN evidence_type e ON e.code = cc.evidence_type
  GROUP BY n.dish_id, cc.condition_id, cc.direction
), all_paths AS (SELECT * FROM ing_paths UNION ALL SELECT * FROM nut_paths),
dish_grams AS (SELECT dish_id, sum(grams) AS total_g FROM dish_ingredient GROUP BY dish_id)
SELECT p.dish_id,
       p.condition_id,
       p.direction,
       sum(p.n_paths)::BIGINT                     AS n_paths,
       min(p.evidence_rank)                       AS best_evidence_rank,
       count(DISTINCT p.ingredient_id)            AS n_ingredients,
       string_agg(DISTINCT p.ingredient_id, ', ') AS ingredients,
       -- distinct compounds per ingredient, summed over ingredients (a compound in two ingredients counts twice)
       sum(p.n_compounds)::BIGINT                 AS n_compounds,
       -- most independent link sources behind any one ingredient's claim (corroboration)
       max(p.n_sources)                           AS max_sources,
       -- share of the dish weight made up by the ingredient lines on these paths (when grams are known)
       sum(p.grams) / nullif(any_value(g.total_g), 0) AS weight_share,
       bool_or(p.via_nutrient)                    AS via_measured_nutrient,
       -- salience: only characteristic compounds, direct links and "high" nutrients (see ingredient_condition_rollup)
       count(DISTINCT p.ingredient_id) FILTER (WHERE p.salient)            AS n_salient_ingredients,
       string_agg(DISTINCT p.ingredient_id, ', ') FILTER (WHERE p.salient) AS salient_ingredients,
       min(p.salient_rank)                        AS best_salient_rank,
       max(p.salient_sources)                     AS max_salient_sources,
       bool_or(p.via_nutrient AND p.salient)      AS via_high_nutrient
FROM all_paths p
LEFT JOIN dish_grams g USING (dish_id)
GROUP BY p.dish_id, p.condition_id, p.direction;

-- Condition → dish is the same data keyed by condition, with names and the dish's culture attached;
-- condition expansion (narrower terms, TCM equivalents) is done in db/trace.py with a recursive query.
CREATE OR REPLACE VIEW v_condition_dish AS
SELECT c.condition_id, c.name AS condition_name, c.type AS condition_type,
       d.dish_id, d.name AS dish_name, d.country_iso2, d.subregion, d.cuisine_label,
       v.direction, v.n_paths, v.best_evidence_rank, v.max_sources, v.ingredients, v.weight_share, v.via_measured_nutrient,
       v.n_salient_ingredients, v.salient_ingredients, v.best_salient_rank, v.max_salient_sources, v.via_high_nutrient
FROM v_dish_condition v
JOIN condition c USING (condition_id)
JOIN dish d USING (dish_id);
