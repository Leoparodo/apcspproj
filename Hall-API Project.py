import requests
import csv

#assigns an empty variable that is used to translate the shortened language name back to the fullsized version
lang_map = {}
#allows the languages.csv to be read and lets the shortened language be expanded to full length
with open("languages.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for i in reader:
        srtnm = i["alpha3-b"].strip()
        lngnm = i["English"].split(";")[0]
        lang_map[srtnm] = lngnm

#Session data to give to OpenLibrary to get the data.
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "AP CSP TEST (myemail@example.com)"
})

#The base URL to use in further searching.
BASE = "https://openlibrary.org"

#Checks what author the user is looking for.
author = input("What author are you looking for? ")

#Gets the location data for the author results.
respauth = SESSION.get(f"{BASE}/search/authors.json", params={"q": author})
#Allows that data to be read by the computer to check.
dataauth = respauth.json()

#Sets top to None so it can be called and edited in the check.
top = None
#Sets top to be whatever the first mention of "top_work" is in the API for the book.
for i in dataauth["docs"]:
    if i.get("top_work") != None:
        top = i.get("top_work")
        break

#Sets name to None so it can be called and edited in the check.
name = None
#Sets name to be whatever the first mention of "name" is in the API for the book.
for i in dataauth["docs"]:
    if i.get("name") != None:
        name = i.get("name")
        break
    
#Gets the location data for the book results.
respbook = SESSION.get(f"{BASE}/search.json", params={"q": top})
#Allows that data to be read by the computer to check.
databook = respbook.json()

#Sets lang to None so it can be called and edited in the check.
lang = None
#Sets lang to be whatever the first mention of "language" is in the API for the book.
for i in databook.get("docs"):
    if i.get("language") != None:
        lang = i["language"]
        break  

#function that converts from shortened form of language back to full length 
def exp_lang(srtnm):
    return lang_map.get(srtnm, srtnm)

#Sets reyear to None so it can be called and edited in the check.
reyear = None
#Sets reyear to be whatever the first mention of "first_publish_year" is in the API for the book.
for i in databook.get("docs"): 
    if i.get("first_publish_year") != None:
        reyear = i["first_publish_year"]
        break 

#Joins the different languages into a list and makes them use the standard English name instead of a shortening
lang = ", ".join(exp_lang(i) for i in lang)

#Prints what your author's top book is and what year it released.
print(name + "'s top selling book is " + top + ", which released in " + str(reyear) + "!")
#Prints what languages the top book was released in.
print(top + ", was released in: " + lang + ".")