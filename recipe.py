import random
import requests
from bs4 import BeautifulSoup


class Recipe(object):
    def get_recipes(self, food):
        url = f"https://cookpad.com/search/{food}"

        html = requests.get(url)

        soup = BeautifulSoup(html.text, "html.parser")

        tags = soup.find_all("div", class_="recipe-preview")

        recipes = []
        recipe_urls = []
        recipe_names = []
        recipe_images = []

        for tag in tags:

            try:
                recipe = tag.find_all("a")[1].text
                link = tag.find_all("a")[0].get("href")
                image = tag.img["src"]
                recipes.append({"recipe": recipe, "link": link, "image": image})

            except:
                pass
        recipes = random.sample(recipes, 3)

        return recipes


if __name__ == "__main__":
    recipe = Recipe()

    result = recipe.get_recipes("マッシュルーム")
    print(result)
