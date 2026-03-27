import requests

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
for d in dataauth["docs"]:
    if d.get("top_work") != None:
        top = d.get("top_work")
        break

#Sets name to None so it can be called and edited in the check.
name = None
#Sets name to be whatever the first mention of "name" is in the API for the book.
for d in dataauth["docs"]:
    if d.get("name") != None:
        name = d.get("name")
        break
    
#Gets the location data for the book results.
respbook = SESSION.get(f"{BASE}/search.json", params={"q": top})
#Allows that data to be read by the computer to check.
databook = respbook.json()

#Sets lang to None so it can be called and edited in the check.
lang = None
#Sets lang to be whatever the first mention of "language" is in the API for the book.
for d in databook.get("docs"):
    if d.get("language") != None:
        lang = d["language"]
        break  

#Sets reyear to None so it can be called and edited in the check.
reyear = None
#Sets reyear to be whatever the first mention of "first_publish_year" is in the API for the book.
for d in databook.get("docs"): 
    if d.get("first_publish_year") != None:
        reyear = d["first_publish_year"]
        break 

#Joins the different languages into a list
lang = ", ".join(lang)

#Prints what your author's top book is and what year it released.
print(name + "'s top selling book is " + top + ", which released in " + str(reyear) + "!")
#Prints what languages the top book was released in.
print(top + ", was released in: " + str(lang) + ".")