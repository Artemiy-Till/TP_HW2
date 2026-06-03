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
