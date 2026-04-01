import requests
import random
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

#function that converts from shortened form of language back to full length 
def exp_lang(srtnm):
    return lang_map.get(srtnm, srtnm)

yes = ["yes", "yeah", "yep", "yup", "yah", "yea", "indeed", "absolutely", "definitely", "certainly", "sure", "surely", "of course", "naturally", "obviously", "exactly", "right", "correct", "true", "agreed", "ok", "okay", "okey-dokey", "alright", "all right", "fine", "very well", "so be it", "affirmative", "affirmed", "positive", "aye", "aye aye", "uh-huh", "mm-hmm", "mhm", "you bet", "you betcha", "bet", "for sure", "by all means", "without a doubt", "no problem", "why not", "fair enough", "certain", "undoubtedly", "gladly", "happily", "I agree", "I do", "I will", "that works", "works for me", "I'm in", "count me in", "go ahead", "make sense", "sounds good", "sounds right", "totally", "exactly right", "100%", "one hundred percent", "roger", "roger that", "copy that", "word", "aye indeed", "by all means yes"]
maybe = ["maybe", "perhaps", "possibly", "could be", "might be", "may or may not", "hard to say", "not sure", "uncertain", "we'll see", "time will tell", "it depends", "up in the air", "if it works out", "to be determined", "surprise me", "you decide", "your choice", "dealer's choice", "whatever you think", "anything works", "I'm open", "I'm flexible", "go with whatever", "pick for me", "your call", "do what you want", "choose at random", "anything you recommend", "free choice", "let fate decide", "perchance", "idk"]

cont = True

while cont == True:
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
    
    if name == None:
        print("Please input a valid author.")
        cont == True
        continue

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

    #Sets reyear to None so it can be called and edited in the check.
    reyear = None
    #Sets reyear to be whatever the first mention of "first_publish_year" is in the API for the book.
    for i in databook.get("docs"): 
        if i.get("first_publish_year") != None:
            reyear = i["first_publish_year"]
            break 

    #Joins the different languages into a list and makes them use the standard English name instead of a shortening
    if lang != None:
        lang = ", ".join(exp_lang(i) for i in lang)

    #Prints what your author's top book is and what year it released.
    if name != None and top != None and reyear != None:
        print(name + "'s top selling book is " + top + ", which released in " + str(reyear) + "!")
    #Prints what languages the top book was released in.
    if top != None and lang != None:
        print(top + ", was released in: " + lang + ".")

    cont = input("Would you like to know about any other authors? y/n ")
    if cont.lower() in yes:
        cont = True
    elif cont.lower() in maybe:
        index = random.choice([1,2])
        if index == 1:
            cont = True
        elif index == 2:
            cont = False
    else:
        cont = False