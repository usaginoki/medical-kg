# FoodAtlas: API key request (contact form, not email)

- **Where:** https://www.foodatlas.ai/contact?api-access (a web form; paste the text below into the message field)
- **Why:** the GitHub repos (IBPA/FoodAtlas-KGv2, now AI-Institute-Food-Systems/foodatlas) contain only code. The built
  knowledge graph ships as bundles that need a free API key.
- **After you get the key:** download the newest bundle zip from https://www.foodatlas.ai/food-composition-downloads (or
  `curl -H "Authorization: Bearer <key>" https://api.foodatlas.ai/v1/bundles`) and unzip it into `Data/foodatlas/`
  (entities.tsv, triplets.tsv, relationships.tsv, metadata_*.tsv). Then ask Claude to profile it and to rebuild the CTD
  disease edges (the recipe is in `Datasets/FoodAtlas.md`). Don't commit the key; put it in `.env` if needed.

---

**Name:** Artur Pak
**Email:** artur.pak@mbzuai.ac.ae
**Organization:** Mohamed bin Zayed University of Artificial Intelligence (MBZUAI), Abu Dhabi, UAE
**Intended use:** Academic, non-commercial research

**Message:**

Hello FoodAtlas team,

I am a student at MBZUAI working under the supervision of Dr. Fajri Koto. We are building a research prototype of an
AI assistant for health questions that takes users' food cultures into account. It connects dishes and ingredients
common in the Middle East, Central Asia and South/East Asia to the chemicals they contain and to evidence about their
health effects.

The FoodAtlas knowledge graph (Li et al., npj Science of Food 2026; Youn et al., Comput Biol Med 2024) is the most
complete provenance-tracked food → chemical → disease resource we have found, and we would like to request an API key
to download the KG bundles for academic research. We would use them only within our research group and cite your work
in any publication.

Thank you!
Artur Pak
