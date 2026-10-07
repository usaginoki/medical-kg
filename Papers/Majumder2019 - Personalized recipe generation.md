---
title: "Generating Personalized Recipes from Historical User Preferences"
citekey: Majumder2019
authors: [Bodhisattwa Prasad Majumder, Shuyang Li, Jianmo Ni, Julian McAuley]
year: 2019
published: 2019-08-31
venue: "EMNLP-IJCNLP 2019"
peer_reviewed: true
url: "https://arxiv.org/abs/1909.00105"
arxiv: "1909.00105"
doi: "10.18653/v1/D19-1613"
pdf: ""
pdf_url: "https://arxiv.org/pdf/1909.00105"
datasets: ["[[Food.com Recipes and Interactions]]"]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
cited_by:
  - "[[Liu2022 - Counterfactual recipe generation]]"
cited_by_count: 1
tags:
  - type/paper
  - relevance/core
  - q/1
  - kind/food
---
# Generating Personalized Recipes from Historical User Preferences

> [!abstract] TL;DR
> UCSD paper that releases the Food.com crawl (230K+ recipes, 1M+ reviews, 2000–2018) and uses a filtered subset
> (180K+ recipes, 700K+ reviews) to train an encoder–decoder that expands a recipe name + a few ingredients + calorie level
> into full instructions, personalised by attending over the user's previously reviewed recipes.

## What was built
- **Dataset(s):** [[Food.com Recipes and Interactions]]
- **Sources & construction:** recipes and user reviews scraped from Food.com over 18 years (2000–2018). For modelling
  they keep recipes with ≥ 3 steps and 4–20 ingredients and users with ≥ 4 reviews; reviews are ordered by time, the most
  recent per user → test, second most recent → validation (sequential leave-one-out).
- **Size & coverage:** 230K+ recipes / 1M+ interactions raw; after filtering, train 25,076 users × 160,901 recipes ×
  698,901 actions (sparsity 99.983 %), dev 7,023, test 12,455 actions. 13K unique ingredients; BPE vocabulary 15K tokens
  over 19M mentions; average recipe 117 tokens (max 256). Cuisine appears only through Food.com tags (the paper does not analyse culture).
- **Evaluation / applications:** personalised recipe generation (BiGRU encoders, GRU decoder, attention fusion over prior
  recipes / names / 58 hand-built cooking techniques); BPE perplexity, BLEU, ROUGE-L, Distinct-n, user-matching accuracy
  (UMA), MRR, recipe-level coherence, step entailment, and human pairwise preference.

## Key findings
1. The Prior Name model reaches the best perplexity (9.516 vs 9.611 for the non-personalised Enc-Dec) and user-matching:
   UMA 0.505 and MRR 0.628 vs 0.100 / 0.293 for the baseline.
2. BLEU is similar across models (BLEU-1 27.9–28.9, BLEU-4 ≈ 3.2–3.4), and the authors argue BLEU does not reflect recipe quality.
3. Personalised outputs are more diverse (Distinct-2 2.06–2.16 % vs 1.93 %).
4. Human raters preferred personalised recipes over the baseline in 61.2–66.0 % of 310 pairs per model (Prior Recipe 66.026 %).
5. The 4 most common techniques (bake, combine, pour, boil) account for 36.5 % of technique mentions.

## Relevance to research questions
### Q1: Cultural food datasets
A large recipe corpus with ingredients, steps, nutrition and tags. Culture labels come only from user tags (72,837 recipes
tagged with one of 69 countries in our count), so it gives many recipes for the US/Europe and a few hundred for
Middle-East/Asian cuisines. The user-interaction side could support personalising advice within a culture.

See [[Q1 Cultural food datasets]]

## Limitations / caveats
- US website; cuisine tags are user-assigned and often denote Americanised dishes. The paper itself does not study cuisine/culture.
- Released ingredient lists lack quantities; nutrition is Food.com's computed %DV.
- Evaluation with n-gram metrics is weak for procedural text (acknowledged by the authors).

## Related work to follow
![[Backlog.base#Cited by this paper]]
