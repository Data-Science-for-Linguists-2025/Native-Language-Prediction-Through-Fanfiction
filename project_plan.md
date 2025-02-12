# project plan
## summary
    this is an investigation regarding to what degree a speaker's mother tongue can be predicted based on their usage of English as a second language
## data
### appearance
    fanfiction sourced from [Archive of Our Own (AO3)](https://archiveofourown.org/)
### data sourcing & cleanup
    a combination between downloaded html files of fanfiction from authors whose native languages are known; and data where the author's native language can be found within webscraped fanfiction  
    beautiful soup will be used to clean up the html files
### size of data
    unknown as of 2025-02-12
## analysis
    spaCy will be used to determine sentence structure  
    nltk's word tokenizer (or perhaps a custom one) will be used to extract lexical information from the corpora  
### end goal
    finding patterns between authors' native languages and their use of English
### hypothesis
    my hypothesis is that the sentence structure will be the most telling aspect of an author's native language. as such, the majority of differences may be able to reveal an author's native language family, but perhaps not the native language itself  
    vocabulary will likely be telling of cultural background more than language itself (and therefore hint at geographic location)
## presentation