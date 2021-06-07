import requests
from bs4 import BeautifulSoup as BS
import sys
import argparse




parser = argparse.ArgumentParser()
parser.add_argument("--link", type=str, help="scrape a single link", default=None)
parser.add_argument("--slides", type=str, help='scrape a whole slideshow of links', default=None)
args = parser.parse_args()



# ing_tag = "sc-pNWdM sc-jrsJWt sc-zLiCd lfZoIg kTchdy FTXLc"
# qnt_tag = "sc-pNWdM sc-jrsJWt sc-ssvJO lfZoIg kTchdy fVwwbP"
# stp_tag = "sc-pNWdM sc-jrsJWt sc-aHTLI lfZoIg gucTqf ionEya"

title_tag = "split-screen-content-header__hed"


# slideshow_tag = "sc-dlnjwi sc-hKFxyN cMtreY bZRgav button button--utility gallery-slide-caption__cta"
slideshow_tag = "button--utility gallery-slide-caption__cta"

SKIP_WORDS = {'assembly', 'equipment', 'filling', 'mortar', 'ricer', 
                'info', 'topping', 'springform', 'thermometer', 
                'canning', 'mill', 'cheesecloth', 'skewers', 'equipment:',
                "diameter", 'pressure', 'foil', 'plastic', 'info:', 'mandoline',
                '9"-diameter', 'pans', 'fryer', 'heatproof'}

EXACT_SKIP_WORDS = {'marinade', 'soup', 'meatballs', 'stir-fry', 'sauce', 'ingredients', 'salad', 'aioli', 'cutter', '', 'crust', 'dressing', 'vegetables'}

# dressing, salad

###----
#    Lists done:
#       Rice bowls
#       Casseroles
#       Cauliflowers
#       salmon
#       vegetarian
#       tofu
#       73 summer
#       58 dutch oven
#       40? easy healthy dinners
#       88 labor days

# DO: 
###----

def process_ingredient(ing):
        ing = ing.replace(',','').lower()
        ing = ing.replace('è', 'e').replace('ñ', 'n').replace('’',"'")
        return ing


def get_ingredient(ing, ing_list):
        # Extract ingredient from ing.
        # Problem: it splits ing by words, so would not recognize "soy sauce" as one ingredient.
        # Problem: if ingredient says multiple things, 
        #       eg "spinach tortellini" and it knows spinach but not the other

        ing = process_ingredient(ing)

        if len( SKIP_WORDS.intersection(ing.split()) ) > 0: return []
        if ing in EXACT_SKIP_WORDS: return []

        new_ings = ing_list.intersection(ing.split())

        # if len(new_ings) == 0:
                # print(ing_list)

        if len(new_ings) == 0:
                new_ings = input("What word in here is the ingredient (singular, lowercase, first word), or type 'm' to enter multiple: {}\n".format(ing))
                if new_ings == 'm':
                        new_ings = input("Type all new ingredients, separated with commas:\n")
                        new_ings = [i.strip() for i in new_ings.split(',')]
                elif new_ings == "SKIP": return []
                else: new_ings = [new_ings]

        for ing in new_ings:
                ing_list.add(ing)
        
        return new_ings




def scrape_link(link, ing_list, recipe_file, recipe_list):

        page = requests.get(link)
        soup = BS(page.content, "html.parser")


        try: 
                ingredients = soup.select('div[class*="recipe__ingredient-list"]')[0].find_all('div')[0].find_all('div') #select relative since tags change
        except:
                print('Skipping one that does not match pattern')
                return # doesn't match the pattern, don't bother
        
        # quantities = soup.find_all('p', class_=qnt_tag)
        # steps = soup.find_all('div', class_=stp_tag)

        title = soup.find('h1', class_=title_tag).get_text().replace(',', '') # remove any commas from title
        print(title)

        if title in recipe_list: 
                print('Already collected')
                return

        new_line = '{},,'.format(title) # leave hole for rating
        recipe_list.append(title)


        # for i, j in zip(ingredients, quantities):
        for i in ingredients:

                ings = get_ingredient(i.get_text(), ing_list)
                # print(ing_list)
                for ing in ings:
                        new_line += '{},'.format(ing)



        recipe_file.write(new_line+'\n')

# Problems:
# 
# what to do for options (soy sauce or tamari)
# 
# How to automatically determine what word is the ingredient??  If I just find a word that matches in the ingredient list,
#         for example, miso-turmeric dressing might get stored as just miso.
#         Maybe that's fine for now.
#         Alternatively, pause and go to such a link and record all ingredients. 

# Recipe calls for ingredient twice, say once in the sauce and one other time.  Should only be added to csv once.




def scrape_slides(link, ing_list, recipe_file, recipe_list):
        page = requests.get(link)
        soup = BS(page.content, "html.parser")

        # links = soup.find_all('a', class_=slideshow_tag)
        # print(soup)
        links = soup.select('a[class*="button--utility gallery-slide-caption__cta"]')

        for link in links:
                # print(link.get('href'))
                print('RECIPE------------')
                # print (link.get('href'))
                
                scrape_link(link.get('href'), ing_list, recipe_file, recipe_list)
                print()





ing_list = None
with open('ingredients.txt', 'r') as ing_file:
        ing_list = set([l.strip() for l in ing_file.readlines()])


recipe_list = None
with open('recipe_data_2.csv', 'r') as recipe_file:
        recipe_list = [l.split(',')[0] for l in recipe_file.readlines()]

with open('recipe_data.csv', 'r') as recipe_file:
        for l in recipe_file.readlines():
                recipe_list.append(l.split(',')[0])
        

recipe_file = open('recipe_data_2.csv', 'a')




if args.link is not None:
        scrape_link(args.link, ing_list, recipe_file, recipe_list)

elif args.slides is not None:
        scrape_slides(args.slides, ing_list, recipe_file, recipe_list)



recipe_file.close()


with open('ingredients.txt', 'w') as ing_file:
        for ing in list(ing_list):
                ing_file.write('{}\n'.format(ing))
