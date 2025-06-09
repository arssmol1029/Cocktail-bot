INSERT_COCKTAIL = """
INSERT INTO cocktails (name, url, description) 
VALUES ($1, $2, $3) 
RETURNING id, name, url, description
"""

INSERT_INGREDIENT = """
INSERT INTO ingredients (name)
VALUES ($1)
ON CONFLICT (name) DO NOTHING
RETURNING id, name
"""

GET_ALL_COCKTAILS = """
SELECT *
FROM cocktails
ORDER BY name
LIMIT $1 OFFSET $2
"""

GET_COCKTAIL_BY_ID = "SELECT * FROM cocktails WHERE id = $1"

GET_COCKTAILS_BY_NAME = """
SELECT * FROM cocktails
WHERE name ILIKE $1
LIMIT $2 OFFSET $3
"""

GET_RANDOM_COCKTAIL = """
SELECT *
FROM cocktails
ORDER BY RANDOM()
LIMIT 1
"""

GET_INGREDIENTS_FOR_COCKTAIL = """
SELECT ingredients.name AS name, cocktail_ingredients.amount AS amount
FROM ingredients
JOIN cocktail_ingredients ON ingredients.id = cocktail_ingredients.ingredient_id
WHERE cocktail_ingredients.cocktail_id = $1
"""

GET_COCKTAILS_BY_INGREDIENTS = """
SELECT * FROM cocktails
WHERE NOT EXISTS (
    SELECT 1 FROM ingredients
    WHERE ingredients.name ILIKE ANY($1::text[])
    AND NOT EXISTS (
        SELECT 1 FROM cocktail_ingredients
        WHERE cocktail_ingredients.cocktail_id = cocktails.id AND cocktail_ingredients.ingredient_id = ingredients.id
    )
)
ORDER BY name
LIMIT $2 OFFSET $3
"""

GET_INGREDIENT_BY_ID = "SELECT * FROM ingredients WHERE id = $1"

GET_INGREDIENT_BY_NAME = "SELECT * FROM ingredients WHERE name ILIKE $1"

DELETE_COCKTAIL = "DELETE FROM cocktails WHERE id = $1"

DELETE_INGREDIENT = "DELETE FROM ingredients WHERE id = $1"