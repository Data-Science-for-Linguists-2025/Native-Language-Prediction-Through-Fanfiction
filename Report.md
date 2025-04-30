# Native Language Prediction Through Fanfiction
    Jenna Higgins  
    University of Pittsburgh LING1340/Data Science for Linguists  
    Spring 2025  
    Professor: Na-Rae Han  
    UTA: Riley Hesbacher  


## Background
[Archive of Our Own](archiveofourown.org)(AO3) is an archive that hosts fanwork (fanfiction, podfics, fanart, etc).  For this project, the assumption that all works are fanfiction will be made. 
- `fanfic` or `fic` is a shortened version of `fanfiction`  
- `fandom` is the group of people who enjoy works from a particular series/author/etc  
- `beta` is an editor or someone who goes over and critiques a work before it is published  
- `tag` is any label added to a work by the author  
    - `Rating` is something used to warn the reader what kind of audience the work is designed with in mind (`General Audiences`, `Teen and Up Audiences`, `Mature`, `Explicit`, and `Unrated`).
        - works that may contain adult content warn the reader before allowing them to read it (this can be turned off in settings if you are logged in), and the spider was not designed to proceed beyond this warning page
    - `Archive Warning` is a collection of preset tags that can be applied to forewarn readers of sensitive content that a work may contain
    - `Category` announces what kind of relationships will be prominent in the work (ie `F/F`, `F/M`, `M/M`, `Gen`, other)
    - `Fandom` is a required tag, but the fandom in question can be a fandom *or* `original work`
    - `Relationships` are romantic/sexual (`slash`) or platonic relationships between characters
    - `Characters` are characters that are prominent in the work, which may include `Original Character(s)`
    - `Additional Tags` are freeform tags that can either be from a preset list or customized. These tend to include hints towards the plot of the work (`Alternate Universe`, `Protective [Character]`, `Masquerade Balls`, etc), but they can also include small notes from the author (`no beta we die like men`, `i love these characters so so much`, `this isn't good`, `like really`, `it's really really bad`, etc)
    - `Language` is another required tag, offering ~150 different languages (including Ainu, Egyptian hieroglyphs, Sindarin (from Lord of the Rings), American Sign Language, and many others). For the purposes of this project, we will only be analyzing works with the language tag `English`
    - `Series` is any ordered grouping of work that the author has placed the work in (particularly for related works such as sequels or other fics in the same fandom)
    - `Collections` is an unordered grouping of work not necessarily involving the author (such as  `XYZ Challenge 2025` or `Inktober 2024`)
    - `Stats` are automated:
        - `Published` is the date published, in YYYY-MM-DD format
        - `Words` is the amount of words (including freestanding punctuation) a work contains
        - `Chapters` are how many chapters a work has
            - `finished` works are ones where the numerator and denominator of a fraction are the same
                - `one-shots` are works with 1/1 chapters
            - `incomplete` works are ones where **either** the numerator is less than the denominator *or* the denominator is `?`
        - `Comments` is a count of how many comments have been left on the work, counting each comment (even those in threads) as its own comment. These can be left anonymously, under a logged in user, or from a `Guest` profile. Authors can limit comments to only logged in users, non-anonymous users, comments that must be approved by the author before publication, or no comments at all
        - `Kudos` are basically likes. Only one can be left per account/IP address
        - `Bookmarks` are saves from those who have read or want to read the work. These can be public or private, and may or may not have comments attached
        - `Hits` are equivalent to views, so multi-chaptered fics that are posted over a period of time tend to have more hits than others because a new hit is added every time the work is opened
    - the title may or may not be unique, as works are identified by a work ID (a number stating the total amount of works posted on AO3 + 1, including deleted works)
    - the author may be a username, `Anonymous`, `Orphan_Account`, or a `pseud` (an alternate username)
    - summaries may be written for the overall work and individual chapters, but are not required
    - notes and end notes may also be written for the overall work and individual chapters
## Webscraping
To begin, I used Scrapy to create a [spider](natfinder/natfinder/spiders/Nat_Finder.py)  
The spider then scraped a collection of webpages from AO3: search results from a combination of a specific language, nationality, or ethnicity and a phrase such as `native language` or `mother tongue`. While this was originally a large amount of manually crafted links (as seen in [Spider_Code.py](Spider_Code.py)), it was altered so that the links were generated while looping through a list of the languages and L2+ disclaimers. The html of the work was then saved to `natfinder/scraped-works`.
I also included some manually collected works from authors who volunteered their works and L1s, which went under `natfinder/manual-works`.
## Parsing Through Works
These two folders had slightly different formatting because of the way in which they were downloaded (an equivalent of `ctrl+s` for the scraped works versus a `download HTML` option on the page for the manual works). This resulted in the scraped works having a LOT of extrenuous data outside of the actual works. [cleaning_and_testing.ipynb](cleaning_and_testing.ipynb#other) contains cells that edited the files to remove this data, but it took me a while to realize it was there which increased processing time by a HUGE margin.
[file_cleaner_1.ipynb](file_cleaner_1.ipynb) and [file_cleaner_2.ipynb](file_cleaner_2.ipynb) were the primary files that parsing through the scraped pages took place. [file_cleaning_manual.py](file_cleaning_manual.py) and [file_cleaning_scraped.py](file_cleaning_scraped.py) are python versions of the jupiter notebooks, but I ended up not using them because there were so many bugs to work out that using the jupiter notebooks was more reasonable (because I could simply rerun a specific cell instead of the entire program).
[fic_cleaning_3.ipynb](fic_cleaning_3.ipynb) was a more streamlined version of [file_cleaner_1.ipynb](file_cleaner_1.ipynb) that utilized Dask for threads to increase the efficiency and speed of processing (because a processing time of 727 minutes and 12.5 seconds was extremely painful and the supercomputer didn't like me so I couldn't use stanza on it...).
[data_organization.ipynb](data_organization.ipynb) was an initial attempt to use Stanza. [spacy_grams.ipynb](spacy_grams.ipynb) was a test of spacy and stanza.
[cleaning_and_testing.ipynb](cleaning_and_testing.ipynb#set-up) was the final parsing to sort through the fics. From there, [playground](cleaning_and_testing.ipynb#playground) was where I found the L1 of the scraped fics. [dealing with punctuation](cleaning_and_testing.ipynb#dealing_with_punctuation) was where I sorted through to determine what kinds of punctuation were used, as dialogue is tagged differently in different languages.
## Classification and Findings
[Classification.ipynb](Classification.ipynb#set-up) is where I finalized the dataframes.
Under [#testing_stuff](Classification.ipynb#testing_stuff), I created bigrams and trigrams both of tokens and word feature information.
[#failure](Classification.ipynb#failure) was my first attempt to use the word features to build a classifier. I split the data into 2:8 train:test groups and vectorized the data using TF-IDF. I then used scikit's multinomial Naive Bayes classifier, which gave me a [4.6875%](cfm_wf_full.png) accuracy (hence me nicknaming the subsection `failure`).
From there, I continued on to [#hope](Classification.ipynb#hope) where I isolated all word features so as to break up different features of words and created a list of all punctuation used. From this, I took out punctuation that can be used in quotations and made a binary feature for each work of whether or not it contains a particular form of quotation markings.
I split the data into a 4:6 train:test grouping, and the accuracy of the resulting Naive Bayes classifier was [29.9212%](cfm_p_full.png).
The distribution of languages was very skewed, so I removed the languages that had 4 or fewer works, resulting in the new distribution found in [this graph](dist_plot.png).
From there, I received a new accuracy of [13.8211%](cfm_wf_sm.png) for the word features and a new accuracy of [29.2682%](cfm_p_sm.png). I found it interesting that while the accuracy of the former nearly tripled, the accuracy of the latter was a little worse.
Studying the confusion matrices, it is apparent that the guesses were largely skewed by the distribution of training data, as you can clearly see vertical and horizontal lines and there is no obvious diagonal relation that would suggest correlation between the guesses and the actual values.
I was also curious about the word features common across each language, so I made these wordclouds: [Polish](wc01.png), [German](wc02.png), [Spanish](wc03.png), [Korean](wc04.png), [Portuguese](wc05.png), [Swedish](wc06.png), [French](wc07.png), [Finnish](wc08.png), [Japanese](wc09.png), [Russian](wc10.png), [Italian](wc11.png), [Chineze](wc12.png), [Czech](wc13.png), [Malay](wc14.png), [Greek](wc15.png), [Turkish](wc16.png), and [Slavak](wc17.png).
## Future Steps
The overall success of my classifiers was not very strong, which I believe is largely due to the skewing of the data. In the future, I shall counter this by:  
    - finding more data (expanding the webscraping to check authors' profiles and searching for their native language on their social media, getting beyond the Adult Content warning page by logging in, and finding locked fics by logging in)  
    - using sentences as data instead of works (to better analyze syntax)  
    - analyzing average and distribution of kband data (which I initially planned on doing for this but forgot about... oops!)  
I also plan on:  
    - analyzing usage of dashes (such as em dashes, en dashes, hyphens; whether there are spaces preceding or succeeding the punctuation marks)
    - analyzing word accuracy (eg typos/spelling errors)
    - checking usage of `their`/`there`/`they're`
    - checking usage of `your`/`you're`
    - checking usage of sentence fragments versus full sentences (which may fall under the whole using-sentences-as-data mentioned above)
Using all data points in *one* classifier instead of one per *type* of data points will also, hopefully, improve accuracy.