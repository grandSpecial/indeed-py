
# coding: utf-8

# In[16]:


import urllib.request
from bs4 import BeautifulSoup
import re
import nltk
from collections import Counter

city = {"Victoria" : "BC", "Vancouver" : "BC", "Calgary" : "AB", "Edmonton" : "AB", "Regina" : "SK", "Saskatoon" : "SK", 
        "Winnipeg" : "MB", "Toronto" : "ON", "Ottawa" : "ON", "Kitchener" : "ON", "Waterloo" : "ON", "Montreal" : "QC", 
        "Quebec City": "QC", "Fredericton" : "NB", "St. John" : "NB", "Moncton" : "NB", "Charlottetown" : "PE",
        "Halifax" : "NS", "St. Johns" : "NL"}

target1 = ['all','computer_programming','real_estate','government','information','finance','science','construction',
           'manufacturing','management','wholesale','entertainment','transportation','education',
           'administrative','health','accomodation','retail']

print("Welcome! This scraper takes two inputs -- Industry and City -- in order to analyze the last 1,000 job posts on INDEED (Canada\'s largest job board). The scraper returns the most in-demand hard-skills in each City and can also classify job postings by industry using lexical categories thanks to Empath -- an amazing Python library developed by Ethan Fast at Stanford.""")

print("\n" + """Available industries: all, computer_programming, real_estate, government, information, finance, science, construction, manufacturing, management, wholesale, entertainment, transportation, education, administrative, health, accomodation, retail""")

print("\n" + """Available cities: Victoria, Vancouver, Calgary, Edmonton, Regina, Saskatoon, Winnipeg, Toronto, Ottawa, Kitchener, Waterloo, Montreal, Quebec City, Fredericton, St. John, Moncton, Charlottetown, Halifax or St. Johns""" + "\n")
              
target2 = input("Industry: ").lower()

if target2 in target1:
    print("\n" + "Awesome! " + target2 + " it is. Now what city would you like to check?" + "\n")
    if target2 != "all":
        ind = target2.replace("_", "+")
    else:
        ind = ""
else:
    print("\n" + """Oops! Make sure your spelling is correct: 'all', 'real_estate', 'government', 'information', 'finance', 'science', 'construction', 'manufacturing', 'management', 'wholesale', 'entertainment', 'transportation', 'education', 'administrative', 'health', 'accomodation', 'retail'""")
    sys.exit()

place = input("City: ").capitalize()
if place in city:
    prov = city[place]
else:
    print("\n" + """Sorry, there's no data on this city yet! Maybe try: Victoria, Vancouver, Calgary, Edmonton, Regina, Saskatoon, Winnipeg, Toronto, Ottawa, Kitchener, Waterloo, Montreal, Quebec City, Fredericton, St. John, Moncton, Charlottetown, Halifax or St. Johns""")
    sys.exit()
    
print("\n" + "Nice! Just one last thing. How in-depth do you want this search to be? The deepest dive -- evaluation of around 1,000 job postings can take upwards of 40 minutes depending on your internet speeds. Analyzing 15 jobs should take less than a minute. Keep in mind, fewer iterations means less reliable results. Enter low, mid or high to select a depth level." + "\n")

depth = input("Depth level: ").lower()

if depth == "high":
    sample = 1100
elif depth == "mid":
    sample = 500
else:
    sample = 10
    
if depth == "high":
    sae = "one thousand"
elif depth == "mid":
    sae = "five hundred"
else:
    sae = "fifteen or twenty"

print("\n" + "Sweet! We're about to look for the last " + sae + " job postings in " + place + " using " + target2 + " as the search term. Sit tight, this shouldn\'t take too long")
url = []
i = 0
j = 1
while i <= sample:
    url.append("https://ca.indeed.com/jobs?q=" + ind + "&l=" + place + "%2C+" + prov + "&radius=" + str(i))
    i += 10
    
inner_url = []
for item in url:
    page = urllib.request.urlopen(item).read()
    soup = BeautifulSoup(page, 'html.parser')
    for a in soup.find_all('a', {'href':re.compile('/rc/')}):
        res = "https://ca.indeed.com" + str(a['href'])
        inner_url.append(res)
        #print(res)
        
    for a in soup.find_all('a', {'href':re.compile('/company/')}):
        res2 = "https://ca.indeed.com" + str(a['href'])
        inner_url.append(res2)
        #print(res2)
        
    for div in soup.find_all("div", "row result"):
        res3 = str("https://ca.indeed.com/rc/clk?jk=") + str(div.get("data-jk")) + str("&fccid=") + str(div.get("id"))
        inner_url.append(res3)
        #print(res3)

def remove_duplicates(inner_url):
    output = []
    seen = set()
    for value in inner_url:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

result = remove_duplicates(inner_url)
len_result = len(result)

holding = []
x = 0
for line in result:
    try:
        pages = urllib.request.urlopen(line).read()
        souper = BeautifulSoup(pages, 'lxml')

        for script in souper(["script", "style"]):
            script.replace_with(" ")
            script.decompose()

        text = souper.get_text(" ")

        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "  ".join(chunk for chunk in chunks if chunk)
    
        str(holding.append(text))
    
        if x <= 5:
            continue
        else:
            break
        
        x =+ 1
        
    except:
        pass

print("Iterating lexical categories" +"\n")
from empath import Empath
lexicon = Empath()

lexicon.create_category("computer_programing", ["computer_programming"], model="reddit", size=300)
lexicon.create_category("real_estate", ["real_estate"], model="reddit", size=300)
lexicon.create_category("government", ["government"], model="reddit", size=300)
lexicon.create_category("information", ["information"], model="reddit", size=300)
lexicon.create_category("finance", ["finance"], model="reddit", size=300)
lexicon.create_category("science", ["science"], model="reddit", size=300)
lexicon.create_category("construction", ["construction"], model="reddit", size=300)
lexicon.create_category("manufacturing", ["manufacturing"], model="reddit", size=300)
lexicon.create_category("management", ["management"], model="reddit", size=300)
lexicon.create_category("wholesale", ["wholesale"], model="reddit", size=300)
lexicon.create_category("entertainment", ["entertainment"], model="reddit", size=300)
lexicon.create_category("transportation", ["transportation"], model="reddit", size=300)
lexicon.create_category("education", ["education"], model="reddit", size=300)
lexicon.create_category("administrative", ["administrative"], model="reddit", size=300)
lexicon.create_category("health", ["health"], model="reddit", size=300)
lexicon.create_category("accomodation", ["accomodation"], model="reddit", size=300)
lexicon.create_category("retail", ["retail"], model="reddit", size=300)

# Get lexical categories
import operator

indie = []
for m in holding:
    individual = m.lower()
    #individual = m.replace(" ", "_")
    keys = {}
    keys.update(lexicon.analyze(individual, categories=["computer_programming"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["real_estate"], normalize=True)) # print the largest
    keys.update(lexicon.analyze(individual, categories=["government"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["information"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["finance"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["science"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["construction"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["manufacturing"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["management"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["wholesale"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["entertainment"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["transportation"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["education"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["administrative"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["health"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["accomodation"], normalize=True))
    keys.update(lexicon.analyze(individual, categories=["retail"], normalize=True))
    industry = max(keys.items(), key=operator.itemgetter(1))[0]
    indie.append(industry)

print("Top-10 job types among your search:" + "\n")
industrial = Counter(indie).most_common(10)
for parts in industrial:
    print(parts)
print("\n")
    
words = [s.lower().split() for s in holding if s]
words = [sublist for l in words for sublist in l]
stop = open('stop.txt','r').read()
stop = stop.split('\n')

words = [''.join(c for c in w if c.isalpha()) for w in words]
words = [w for w in words if w not in stop and w.isalpha()]

print("Top-20 hard skills among your search: " + "\n")
text = nltk.Text(words)
freqs = nltk.FreqDist(text)
skills = freqs.most_common(20)
for parts2 in skills:
    print(parts2)

