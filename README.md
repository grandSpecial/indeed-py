## Indeed job skill scraper

# indeed-py searches Indeed (Canada's largest job board) for job postings by select keyword and lists the top-20 hard-skills found in that search. It also classifies each job posting into an industry created using lexical categories with Empath, taking from the Reddit corpus.

Requirements: Python3.6, pip, BS4, NLTK, EMPATH (can be installed by running requirements.txt file)

To try out, open a cmd prompt or terminal and copy/paste the following commands. 

git clone https://github.com/grandSpecial/indeed-py.git

cd indeed-py

pip install -r requirements.txt

python pydee.py


If all goes well, you should be prompted to choose an,

1) Industry

2) Canadian city

3) Depth of search 

Available industries: all, computer_programming, real_estate, government, information, finance, science, construction, manufacturing, management, wholesale, entertainment, transportation, education, administrative, health, accomodation and retail

Available cities: Victoria, Vancouver, Calgary, Edmonton, Regina, Saskatoon, Winnipeg, Toronto, Ottawa, Kitchener, Waterloo, Montreal, Quebec City, Fredericton, St. John, Moncton, Charlottetown, Halifax or St. Johns
