from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
import time
# gets each url from txt and stores url in list
url_list = [line.strip() for line in open('recipe_list.txt')]

dictionary_list = []
time.sleep(3)
# Loop through each recipe
for recipe_url in url_list:
    time.sleep(3)
    # Grabbing HTML data
    uClient = uReq(recipe_url)
    recipe_html = uClient.read()
    uClient.close()

    # HTML parse
    recipe_soup = soup(recipe_html,"html.parser")

    # Recipe Name
    recipe_name = recipe_soup.h1.get_text()

    ## Recipe Rating and number of ratings

    star_tag = recipe_soup.findAll("span",{"class":"review-star-text"})
    if star_tag:
        # New layout
        stars = star_tag[0].get_text()
        stars = stars.strip() #'Rating: ___ stars'

        # Num ratings
        rating_tag = recipe_soup.findAll("span",{"class":"ugc-ratings-item"})
        rating_number = rating_tag[0].get_text()
        rating_number = rating_number.strip() # __ Ratings
    else:
        # Old Layout
        star_tag = recipe_soup.find("meta", {"itemprop":"ratingValue"})
        stars = star_tag["content"].strip()

        rating_tag = recipe_soup.find("meta", {"itemprop":"reviewCount"})
        rating_number = rating_tag["content"].strip()

    ## Total Time and Serving Size

    info_box = recipe_soup.findAll("aside", {"class": "recipe-info-section"})
    if info_box:
        info_box = info_box[0]

        info_header = info_box.findAll("div", {"class": "recipe-meta-item-header"})
        info_data = info_box.findAll("div",{"class": "recipe-meta-item-body"})
        for i in range(len(info_header)):
        # Check to see if tag is total time
            header_tag = info_header[i].get_text()
            header_tag = header_tag.strip()

            # If tag is total time, get value
            if (header_tag == "total:"):
                time_data = info_data[i].get_text()
                time_data = time_data.strip()

            # If tag is serving size, get value
            if (header_tag == "Servings:"):
                serving_size = info_data[i].get_text()
                serving_size = serving_size.strip()
    else:
        time = recipe_soup.findAll("span",{"class": "ready-in-time"})
        time_data = time[box].getText()

        serving = recipe_soup.findAll("span",{"class":"recipe-ingredients__header__toggles"})
        serving_size = serving[0].meta["content"]

    ## Look For ingredients
    ing_list = []

    ingredients = recipe_soup.findAll("span",{"class":"ingredients-item-name"})
    if not ingredients:
        ingredients = recipe_soup.findAll("span", {"class":"recipe-ingred_txt added"})
    # get and store each ingredients
    for ingredient in ingredients:
        ingredient = ingredient.get_text()
        ingredient = ingredient.strip()
        ing_list.append(ingredient)


    ## Steps
    steps = recipe_soup.findAll("div",{"class":"paragraph"})
    if not steps:
        steps = recipe_soup.findAll("span", {"class":"recipe-directions__list--item"})

    # Initialize step list
    step_list = []

    # Loop through each direction and append to list
    for i in range(len(steps)):
        step = steps[i].getText()
        step = step.strip()
        step_list.append("Step: " + str(i) + ": " + step)

    ## Get Nutrition values
    nutrition = recipe_soup.findAll("div",{"class":"section-body"})
    if nutrition:
        nutrition_val = nutrition[-1].getText()
        # Remove "Full Nutrition" substring
        nutrition_val = nutrition_val.split("Full Nutrition",1)[0]
        nutrition_val = nutrition_val.strip()
    else:
        nutrition = recipe_soup.findAll("div",{"class":"nutrition-summary-facts"})
        calories = nutrition.find("span", {"itemprop":"calories"}).getText()
        fat = nutrition.find("span", {"itemprop":"fatContent"}).getText()
        carb = nutrition.find("span", {"itemprop":"carbohydrateContent"}).getText()
        protein = nutrition.find("span", {"itemprop":"proteinContent"}).getText()
        cholesterol = nutrition.find("span", {"itemprop":"holesterolContent"}).getText()
        sodium = nutrition.find("span", {"itemprop":"sodiumContent"}).getText()

        nutrition_val = calories+fat+carb+protein+cholesterol+sodium

    # Store recipe data in temporary dictionary
    dictionary_temp = {"Food": recipe_name,
                       "Stars": stars,
                       "Ratings": rating_number,
                       "Total Time": time_data,
                       "Serving Size": serving_size,
                       "Ingredients": ing_list,
                       "Steps": step_list,
                       "Nutrition": nutrition_val
                       }

    # Store data in dictionary list for each recipe
    #dictionary_list.append(dictionary_temp)

    #list(dictionary_list.keys())
    columns = ["Food", "Stars", "Ratings", "Total Time", "Serving Size",
                "Ingredients", "Steps", "Nutrition"]
    with open('recipe.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, fieldnames=columns)
        writer.writeheader()
        for key, value in dictionary_temp.items():
           writer.writerow([key, value])