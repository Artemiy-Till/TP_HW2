import pytest

from recipes import Ingredient, Recipe, ShoppingList


def test_ingredient_init():
    ingredient = Ingredient("Мука", 500, "г")

    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"


def test_ingredient_str():
    ingredient = Ingredient("Мука", 500, "г")

    assert str(ingredient) == "Мука: 500.0 г"


def test_ingredient_eq_same_name_and_unit():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Мука", 1000, "г")

    assert ingredient1 == ingredient2


def test_ingredient_eq_different_name():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Сахар", 500, "г")

    assert ingredient1 != ingredient2


def test_ingredient_eq_different_unit():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Мука", 500, "кг")

    assert ingredient1 != ingredient2


def test_recipe_init():
    ingredients = [
        Ingredient("Мука", 500, "г"),
        Ingredient("Сахар", 100, "г")
    ]

    recipe = Recipe("Пирог", ingredients)

    assert recipe.title == "Пирог"
    assert len(recipe.ingredients) == 2


def test_recipe_add_ingredient_new():
    recipe = Recipe("Пирог", [])

    recipe.add_ingredient(Ingredient("Мука", 500, "г"))

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Мука"
    assert recipe.ingredients[0].quantity == 500.0
    assert recipe.ingredients[0].unit == "г"


def test_recipe_add_ingredient_existing():
    recipe = Recipe("Пирог", [])

    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 700.0


def test_recipe_scale_returns_recipe_and_does_not_change_original():
    recipe = Recipe("Пирог", [
        Ingredient("Мука", 500, "г"),
        Ingredient("Сахар", 100, "г")
    ])

    scaled_recipe = recipe.scale(2)

    assert isinstance(scaled_recipe, Recipe)
    assert scaled_recipe is not recipe

    assert scaled_recipe.ingredients[0].quantity == 1000.0
    assert scaled_recipe.ingredients[1].quantity == 200.0

    assert recipe.ingredients[0].quantity == 500.0
    assert recipe.ingredients[1].quantity == 100.0


def test_recipe_len():
    recipe = Recipe("Пирог", [
        Ingredient("Мука", 500, "г"),
        Ingredient("Сахар", 100, "г")
    ])

    assert len(recipe) == 2


def test_shopping_list_add_recipe():
    recipe = Recipe("Пирог", [
        Ingredient("Мука", 500, "г"),
        Ingredient("Сахар", 100, "г")
    ])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)

    result = shopping_list.get_list()

    assert len(result) == 2
    assert result[0].name == "Мука"
    assert result[0].quantity == 1000.0
    assert result[1].name == "Сахар"
    assert result[1].quantity == 200.0


def test_shopping_list_add_recipe_invalid_portions():
    recipe = Recipe("Пирог", [
        Ingredient("Мука", 500, "г")
    ])

    shopping_list = ShoppingList()

    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, 0)


def test_shopping_list_remove_recipe():
    recipe1 = Recipe("Пирог", [
        Ingredient("Мука", 500, "г")
    ])

    recipe2 = Recipe("Салат", [
        Ingredient("Помидоры", 2, "шт")
    ])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe1, 1)
    shopping_list.add_recipe(recipe2, 1)

    shopping_list.remove_recipe("Пирог")

    result = shopping_list.get_list()

    assert len(result) == 1
    assert result[0].name == "Помидоры"


def test_shopping_list_remove_missing_recipe():
    recipe = Recipe("Пирог", [
        Ingredient("Мука", 500, "г")
    ])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)

    shopping_list.remove_recipe("Суп")

    result = shopping_list.get_list()

    assert len(result) == 1
    assert result[0].name == "Мука"


def test_shopping_list_get_list_sums_same_ingredients():
    recipe1 = Recipe("Пирог", [
        Ingredient("Мука", 500, "г")
    ])

    recipe2 = Recipe("Блины", [
        Ingredient("Мука", 300, "г")
    ])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe1, 1)
    shopping_list.add_recipe(recipe2, 1)

    result = shopping_list.get_list()

    assert len(result) == 1
    assert result[0].name == "Мука"
    assert result[0].quantity == 800.0
    assert result[0].unit == "г"


def test_shopping_list_get_list_sorted_by_name():
    recipe = Recipe("Завтрак", [
        Ingredient("Яйца", 2, "шт"),
        Ingredient("Мука", 300, "г"),
        Ingredient("Сахар", 100, "г")
    ])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)

    result = shopping_list.get_list()

    assert result[0].name == "Мука"
    assert result[1].name == "Сахар"
    assert result[2].name == "Яйца"


def test_shopping_list_add():
    recipe1 = Recipe("Пирог", [
        Ingredient("Мука", 500, "г")
    ])

    recipe2 = Recipe("Салат", [
        Ingredient("Помидоры", 2, "шт")
    ])

    list1 = ShoppingList()
    list2 = ShoppingList()

    list1.add_recipe(recipe1, 1)
    list2.add_recipe(recipe2, 1)

    combined = list1 + list2

    result = combined.get_list()

    assert len(result) == 2
    assert result[0].name == "Мука"
    assert result[1].name == "Помидоры"


def test_shopping_list_add_does_not_change_original_lists():
    recipe1 = Recipe("Пирог", [
        Ingredient("Мука", 500, "г")
    ])

    recipe2 = Recipe("Салат", [
        Ingredient("Помидоры", 2, "шт")
    ])

    list1 = ShoppingList()
    list2 = ShoppingList()

    list1.add_recipe(recipe1, 1)
    list2.add_recipe(recipe2, 1)

    combined = list1 + list2

    assert len(list1.get_list()) == 1
    assert len(list2.get_list()) == 1
    assert len(combined.get_list()) == 2
