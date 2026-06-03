class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property 
    def quantity (self):
        return self._quantity


    @quantity.setter
    def quantity (self, value):
        value = float(value)
        if value < 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"
    
    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"
    
    def __eq__(self, ingredient):
        return self.name == ingredient.name and self.unit == ingredient.unit 

class Recipe:
    def __init__(self, title, ingredients):
        self.title = title
        self.ingredients = ingredients

    def add_ingredient(self, ingredient: Ingredient):
        for current in self.ingredients:
            if current == ingredient:
                current.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        if not isinstance(ratio, (int, float)):
            return False
        return ratio > 0

    def scale(self, ratio):

        new_ingredients = []
        for ingredient in self.ingredients:
            new_ingredient = Ingredient(ingredient.name, ingredient.quantity * ratio,ingredient.unit)

            new_ingredients.append(new_ingredient)

        return Recipe(self.title, new_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        result = f"Рецепт: {self.title}\nИнгредиенты:\n"

        for ingredient in self.ingredients:
            result += f"- {ingredient}\n"

        return result

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")

        scaled_recipe = recipe.scale(portions)

        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title):
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self):
        result = {}

        for ingredient, recipe_title in self._items:
            key = (ingredient.name, ingredient.unit)

            if key in result:
                result[key] += ingredient.quantity
            else:
                result[key] = ingredient.quantity

        shopping_ingredients = []

        for key, quantity in result.items():
            name, unit = key
            shopping_ingredients.append(Ingredient(name, quantity, unit))

        shopping_ingredients.sort(key=lambda ingredient: ingredient.name)

        return shopping_ingredients

    def __add__(self, other):
        new_list = ShoppingList()

        new_list._items = self._items.copy() + other._items.copy()

        return new_list