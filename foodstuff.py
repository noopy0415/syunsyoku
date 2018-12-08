from random import choice
import urllib.request, urllib.error
from bs4 import BeautifulSoup
from random import choice


class Foodstuff(object):
    def get_foods(self, category="all"):
        month_ = date.today().month

        url = f"https://k52.org/syokuzai/{category}/{month_}"

        html = urllib.request.urlopen(url)

        soup = BeautifulSoup(html, "html.parser")

        td_ = soup.find_all('td')

        foods_list = []

        for tag in td_:
            try:
                if tag.get("class").pop(0) in "name":
                    foods_list.append(tag.string)
            except:
                pass

        foods_list.remove("食材名")

        if None in foods_list: foods_list.remove(None)

        return foods_list

    def get_vegetable(self):
        vegetable_list = Foodstuff().get_foods("vegetable")
        return vegetable_list

    def get_fruits(self):
        fruits_list = Foodstuff().get_foods("fruit")
        return fruits_list

    def get_fish(self):
        fish_list = Foodstuff().get_foods("fish")
        return fish_list

    def get_marine(self):
        marine_list = Foodstuff().get_foods("marine")
        return marine_list

    def get_food(self):
        foods = Foodstuff().get_foods()
        return choice(foods)

if __name__ == "__main__":
    food = Foodstuff()

    # print(food.get_foods())

    print(food.get_food())
