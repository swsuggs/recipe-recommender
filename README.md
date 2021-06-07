# recipe-recommender

A little project to collect and recommend recipes from Bon Appetit.

I've been enjoying many Bon Appetit recipes lately and thought it would be fun and useful to build a system to recommend new ones.
So I scraped about 2500 recipes from their website.  The first recommendation approach is a basic nearest-neighbors model in ingredient space.
The second is a simplified matrix-factorization model, where I only learn user features and not recipe features because I only have data for one user, me.
Instead, I use the ingredients as features.  This second model is a definite improvement, if only because it recommends a variety of recipes instead
of ones similar to one I already like.



For a full description, read through the three jupyter notebooks:
  - clean_recipe_data.ipynb
  - recommend_knn.ipynb
  - recommend_matrix_factor.ipynb
