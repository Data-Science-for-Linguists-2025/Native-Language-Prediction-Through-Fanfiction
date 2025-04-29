
## IMPORTS
from bs4 import BeautifulSoup as beau
import pandas as pd
import pickle
import os
import re

# create empty dataframe
fics_df = pd.DataFrame(columns=['L1', 'author', 'title', 'chapters', 'work', 'summary', 'notes', 'endnotes', 'rating', 'warnings', 'fandoms', 'ships', 'charas', 'freeform'])

# compile patterns for regex
ratings = re.compile(r'Rating:</dt>\n<dd>.*</dd>', re.S)
warnings = re.compile(r'Archive Warnings*:</dt>\n<dd>.*</dd>', re.S)
fandoms = re.compile(r'Fandoms*:</dt>\n<dd>.*</dd>', re.S)
ships = re.compile(r'Relationships*:</dt>\n<dd>.*</dd>', re.S)
charas = re.compile(r'Characters*:</dt>\n<dd>.*</dd>', re.S)
freeforms = re.compile(r'Additional Tags:</dt>\n<dd>.*</dd>', re.S)
r_summary = re.compile(r'(?<=Summary</p>).*?Notes', re.S)
r_notes = re.compile(r'(?<=Notes</p>).+', re.S)
r_endnotes = re.compile(r'(?<=End Notes).*?</blockquote', re.S)
notes_clean = re.compile(r'<p>.*?(?=</blockquote)', re.S)
chap_cont = re.compile(r'<!--chapter content-->.*?<!--/chapter content-->', re.S)
span_init = re.compile(r'\n<span>', re.S)
span_close = re.compile(r'</span>\n', re.S)
p = re.compile(r'</p><p>')
init = re.compile(r'(?<=<div id="chapters" class="userstuff">).*', re.S)
w = re.compile(r'(?<=<p>).*', re.S)
divbr = re.compile(r'.*(?=</div>\n</div>)', re.S)

# define functions
def get_work(s): 
    s = re.sub(r'[^\S\n]+', ' ', s)
    c = re.findall(chap_cont, s)
    for ch in c:
        ch = re.sub(r'\n \n', '\n', ch)
        ch = re.sub(r'(\n){3,}', '\n\n\n', ch)
        ch = re.sub(r'^\n', '', ch)
        ch = re.sub(r'\n*<span>', '', ch)
        ch = re.sub(r'</span>\n*', '', ch)
        ch = re.sub(span_init, '', ch)
        ch = re.sub(span_close, '', ch)
        ch = re.sub(p, '\n', ch)
    return [beau(x).text for x in c]

def get_only_chap(s):
    s = re.sub(r'[^\S\n]+', ' ', s)
    c = re.search(divbr, s)[0]
    c = re.search(init, c)[0]
    c = re.search(w, c)[0]
    c = re.sub(r'\n \n', '\n', c)
    c = re.sub(r'(\n){3,}', '\n\n\n', c)
    c = re.sub(r'^\n', '', c)
    c = re.sub(r'\n*<span>', '', c)
    c = re.sub(r'</span>\n*', '', c)
    c = re.sub(span_init, '', c)
    c = re.sub(span_close, '', c)
    c = re.sub(p, '\n', c)
    return [c]

def get_tags(pat, s):
    lst = []
    a = re.search(pat, str(s))[0]
    b = re.findall(r'(?<=">).*?</a', a)
    for x in b:
        c = re.search(r'.*(?=<)', x)[0]
        lst.append(c)
    return lst

def get_notes(pat, soup):
    s = re.search(pat, str(soup))[0]
    return beau(re.search(notes_clean, s)[0]).text

def get_chap(x):
    return re.search(r'(?<=Chapters: ).*', str(x))[0]

def parse_fic(st):
    soup = beau(st)
    L1 = soup.find(class_='L1').text
    try:
        author = soup.find(rel='author').text
    except:
        author = 'Anonymous'
    title = soup.find('h1').text
    chapters = get_chap(soup)
    try:
        work = get_only_chap(st)
    except:
        work = get_work(st)
    try:
        summary = get_notes(r_summary, soup)
    except:
        summary = None
    try:
        note = get_notes(r_notes, soup)
    except:
        note = None
    try:
        endnote = get_notes(r_endnotes, soup)
    except:
        endnote = None
    rating = get_tags(ratings, soup)
    try:
        warning = get_tags(warnings, soup)
    except:
        warning = None
    try:
        fandom = get_tags(fandoms, soup)
    except:
        fandom = None
    try:
        ship = get_tags(ships, soup)
    except:
        ship = None
    try:
        chara = get_tags(charas, soup)
    except:
        chara = None
    try:
        freeform = get_tags(freeforms, soup)
    except:
        freeform = None
    return pd.DataFrame({'L1':[L1], 'author':[author], 'title':[title], 'chapters':[chapters], 'work':[work], 'summary':[summary], 'notes':[note], 'endnotes':[endnote], 'rating':[rating], 'warnings':[warning], 'fandoms':[fandom], 'ships':[ship], 'charas':[chara],'freeform':[freeform]})

# parse fics
files = []
directory = 'natfinder/natfinder/manual-works'
for f in os.scandir(directory):
    files.append(f.name)
for f in files:
    st = open(directory + '/' + f).read()
    temp_df = parse_fic(st)
    fics_df = pd.concat([fics_df, temp_df], ignore_index=True)

# pickle dataframe
with open('fics_df_manual.pkl', 'wb') as file:
    pickle.dump(fics_df, file)