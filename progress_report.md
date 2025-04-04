# progress report
### 2025-02-12
- created repository
- filled out basic information for [README](README.md), [project plan](project_plan.md), & [LICENSE](LICENSE.md)
## first progress report
### 2025-02-25
- finally figured out web-scraping! 0/10 do not recommend!
- sourced data files
    - [spider](Spider_Code.py) used to source data. took 7 minutes and 55 seconds.  
        **this is not an .ipynb because it will not work without being in an active Scrapy project directory, so the code *will not work* as is**  
        - [Scrapy's tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html) used to familiarize self with Scrapy
        - [Rohan's project](https://github.com/Data-Science-for-Linguists-2022/Fanfiction-Classification-Analysis) used to get an idea of how to best navigate AO3 pages
        - the process of creating this spider was a lot more difficult than it looks (based on the end product). it involved a LOT of trial and error with figuring out how data was returned from the spider
        - an example of what the html files look like may be found [here](data_sample.html)
            - due to the fact that works cannot be reposted on other platforms without the author's permission, this is a mostly blank html file. to find an *actual* AO3 html file, go [here](https://archiveofourown.org/works/search?work_search%5Bquery%5D=) and click on a work
    - collected from searches including the phrases "i'm [nationality]" for a series of nationalities with different native languages
        - data must be filtered through to ensure that the author is the nationality and it is not a character within the fic stating their nationality
        - will be done utilizing regex & beautiful soup, sorting out whether the phrase is in the freeform tags, notes, or endnotes
            - summary will also be studied because oftentimes authors put disclaimers there for people who don't read tags/notes
            - this must be compared to the body of the work to ensure it is not a line from the fic itself
                - paragraph containing phrase will be compared
        - additional pages of data will be sourced by following through a search to its "next" page... I am going to let my computer take a nice nap though, because it just spent 2h+ trying to scrape a bunch of webpages :')
        - cons of this data:
            - there is no guarantee that the nationality lines up with the author's native language
                - unfortunately, most authors don't tend to say "my native language is [language]", so this is the best that can be done finding native languages of authors without explicitly asking them
        - pros of this data:
            - easier to access/find than manually sourced data
    - additional data:
        - a selection of html files manually downloaded whose authors' native languages I know for sure
            - this data was found by asking around in fandom spaces about ESL authors and having them or their readers/friends/mutuals responding
        - cons of this data:
            - limited
            - not as diverse
    - overall data size:
        - web-scraped: up to 20 fics per nationality (french, spanish, mexican, brazilian, portuguese, russian, ukrainian, bengali, italian, czech, japanese, korean, chinese, swedish, german, finnish, turkish, greek; also included 'hindi')
        - manually sourced: 2 german authors (23 fics for one; 4 for another); 1 korean author (11 fics); 1 malay author (7 fics); 1 polish author (31 fics); 2 brazilian authors (1 fic; 16 fics); 1 slavak author (4 fics)
    references used:  
    [regex cheatsheet](https://www.rexegg.com/regex-quickstart.php)  
    [reminder of how to actually use regex... shh](https://www.w3schools.com/python/python_regex.asp)  
    [scrapy tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)
## second progress report
### 2025-03-21
- updated Nat_Finder.py
    - added a few more nationalities to spider's search
    - links spider crawls were recreated to increase human legibility
- created file_cleaner.ipynb
    - cleans up file data and places in dataframe
- created data_organization.ipynb
    - creates additional columns for dataframe
    - finds additional information that is not directly in the html file
- TO-DO:
    - review Nat_Finder.py
        - see if there are more nationalities to add
        - have spider create subfolders with each nationality so the language data is easily accessible when creating the dataframe
        - have spider search through additional pages, not just initial page
    - figure out how to use scrapy
    - create classifiers
        - TF-IDF:
            - word count, word length, sentence length, chapters, etc.
        - Naive-Bayes
            - n-grams
            - n-grams *using scrapy POS tags*
            - non-words used
## third progress report
### 2025-04-04
- updated Nat_Finder.py
    - changed link searches to include more languages (scraped fics roughly doubled in size)
- created overall_process.ipynb
    - made a bunch of .md cells and put general workflow into them
    - will create .py cells when everything is finalized
    - (not removing other files---at least yet)
- updated file_cleaner-1.ipynb
    - added code to sort out fics by language
- updated file_cleaner-2.ipynb
    - streamlined code
- updated data_organization.ipynb
    - got rid of most stuff because I plan on using stanza instead of spaCy
- TO-DO:
    - create classifiers
        - K-Nearest Neighbors on supervised data
        - K-Means on unsupervised data
        - Naive-Bayes
    - analysis
    - visualize data
    - *more details available in overall_process.ipynb*