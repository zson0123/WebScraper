import time
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = "https://www.allrecipes.com/recipes/?page=1"

time.sleep(3)

# opening up connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parse
page_soup = soup(page_html, "html.parser")

# grabs each recipe card
cards = page_soup.findAll("article",{"class":"fixed-recipe-card"})

url_list = []

# get recipe url for page 1
for card in cards:
    recipe_url = card.div.a["href"]
    url_list.append(recipe_url)

# output url list as a txt file
with open("recipe_list.txt", 'w') as f:
    for item in url_list:
        f.write(item + '\n')

