from bs4 import BeautifulSoup as beau
import pandas as pd
import pickle
import nltk
import os
import re

# create empty dataframe
fics_df = pd.DataFrame(columns=['L1', 'author', 'title', 'chapters', 'work', 'summary', 'notes', 'endnotes', 'rating', 'warnings', 'fandoms', 'ships', 'charas', 'freeform'])
langs = ['afrikaans', 'albanian', 'amharic', 'anii', 'arabic', 'araona', 'armenian', 'assamese', 'aymara', 'ayoreo', 'azerbaijan', 'balanta', 'bambara', 'bariba', 'basque', 'bassari', 'baure', 'bedik', 'belarusian', 'bengali', 'berber', 'biali', 'bislama', 'boko', 'bomu', 'bosnian', 'bozo', 'buduma', 'bulgarian', 'burmese', 'canichana', 'cantonese', 'carolinian', 'catalan', 'cayubaba', 'chacobo', 'chamorro', 'chichewa', 'chinese', 'chirbawe', 'comorian', 'corsican', 'creole', 'croation', 'czech', 'dagaare', 'dagbani', 'dangme', 'danish', 'dari', 'daroese', 'dendi', 'dhivehi', 'dioula', 'dogon', 'dutch', 'estonian', 'fante', 'figian', 'filipino', 'finnish', 'foodo', 'formosan', 'french', 'fula', 'gaelic', 'gbe', 'georgian', 'german', 'gonja', 'gourmanche', 'greek', 'guarani', 'guarayu', 'gujarati', 'hakka', 'hassaniya', 'hausa', 'hebrew', 'hindi', 'hiri', 'hokkien', 'hungarian', 'icelandic', 'igbo', 'indonesian', 'irish', 'italian', 'itene', 'itonama', 'japanese', 'javanese', 'jerriais', 'jola', 'kabye', 'kalanga', 'kallawaya', 'kannada', 'kanuri', 'kasem', 'kazakh', 'khmer', 'kinyarwanda', 'kirundi', 'kissi', 'koisan', 'korean', 'kpelle', 'kurdish', 'kyrgyz', 'lao', 'latvian', 'leco', 'lithuanian', 'lukpa', 'luzembourgish', 'macedonian', 'malagasy', 'malay', 'malayalam', 'malinke', 'maltese', 'mamara', 'mandarin', 'manding', 'mandinka', 'mandjak', 'manipuri', 'mankanya', 'maori', 'marathi', 'marshallese', 'mbelime', 'meitei', 'mongolian', 'montenegrin', 'moseten', 'mossi', 'motu', 'movima', 'moxos', 'nambya', 'nateni', 'nauruan', 'ndau', 'ndebele', 'nepali', 'norwegian', 'nzema', 'oniyan', 'oriya', 'oromo', 'ossetian', 'pakawara', 'palauan', 'papiamento', 'pashto', 'persian', 'pisin', 'polish', 'portuguese', 'punjabi', 'puquina', 'quechua', 'romanian', 'romansh', 'russian', 'safen', 'sango', 'scots', 'scottish', 'sena', 'serbian', 'serer', 'sewdish', 'shinhala', 'shona', 'siriono', 'slovak', 'slovene', 'somali', 'soninke', 'sonsorolese', 'sotho', 'spanish', 'susu', 'swahili', 'swati', 'syenara', 'tacana', 'tagalog', 'tajik', 'tamasheq', 'tamil', 'tammari', 'tapiete', 'tasawaq', 'tebu', 'telugu', 'tetum', 'thai', 'tigrinya', 'tobian', 'toma', 'tonga', 'tongan', 'toromono', 'tsonga', 'tswana', 'turkish', 'turkmen', 'tuvaluan', 'twi', 'ukrainian', 'urdu', 'uzbek', 'venda', 'vietnamese', 'waama', 'wamey', 'weenhayek', 'welsh', 'wolof', 'xhosa', 'yaminawa', 'yobe', 'yom', 'yoruba', 'yuki', 'yuracare', 'zarma', 'zulu']

# compile patterns for regex
ratings = r'Rating:</dt>\n<dd>.*</dd>'
warnings = r'Archive Warnings*:</dt>\n<dd>.*</dd>'
fandoms = r'Fandoms*:</dt>\n<dd>.*</dd>'
ships = r'Relationships*:</dt>\n<dd>.*</dd>'
charas = r'Characters*:</dt>\n<dd>.*</dd>'
freeforms = r'Additional Tags:</dt>\n<dd>.*</dd>'
r_summary = re.compile(r'(?<=Summary</p>).*?Notes', re.S)
r_notes = re.compile(r'(?<=Notes</p>).+', re.S)
r_endnotes = re.compile(r'(?<=End Notes).*?</blockquote', re.S)
notes_clean = re.compile(r'<p>.*?(?=</blockquote)', re.S)
cc2 = re.compile(r'<!--chapter content-->.*?<!--/chapter-->', re.S)
emm = re.compile(r'\n<span>', re.S)
emmm = re.compile(r'</span>\n', re.S)
p = re.compile(r'</p><p>')
init = re.compile(r'(?<=<div id="chapters" class="userstuff">).*', re.S)
w = re.compile(r'(?<=<p>).*', re.S)
cc1 = re.compile(r'.*(?=</div>\n</div>)', re.S)

# define functions
def get_work(s): 
    s = re.sub(r'[^\S\n]+', ' ', s)
    c = re.findall(cc2, s)
    for ch in c:
        ch = re.sub(r'\n \n', '\n', ch)
        ch = re.sub(r'(\n){3,}', '\n\n\n', ch)
        ch = re.sub(r'^\n', '', ch)
        ch = re.sub(r'\n*<span>', '', ch)
        ch = re.sub(r'</span>\n*', '', ch)
        ch = re.sub(emm, '', ch)
        ch = re.sub(emmm, '', ch)
        ch = re.sub(p, '\n', ch)
    return [beau(x).text for x in c]

def get_only_chap(s):
    s = re.sub(r'[^\S\n]+', ' ', s)
    c = re.search(cc1, s)[0]
    c = re.search(init, c)[0]
    c = re.search(w, c)[0]
    c = re.sub(r'\n \n', '\n', c)
    c = re.sub(r'(\n){3,}', '\n\n\n', c)
    c = re.sub(r'^\n', '', c)
    c = re.sub(r'\n*<span>', '', c)
    c = re.sub(r'</span>\n*', '', c)
    c = re.sub(emm, '', c)
    c = re.sub(emmm, '', c)
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
    return re.search(r'(?<=Chapters:).*', str(x))[0]

def find_lang(fic):
    for l in langs:
        if l in nltk.word_tokenize(fic.lower()):
            return l.upper()
        
def find_lang_tags(fic):
    for l in langs:
        for x in fic:
            if l in nltk.word_tokenize(x.lower()):
                return l.upper()

def parse_fic(st):
    soup = beau(st)
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
    try:
        rating = get_tags(ratings, soup)
    except:
        rating = None
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
    return pd.DataFrame({'author':[author], 'title':[title], 'chapters':[chapters], 'work':[work], 'summary':[summary], 'notes':[note], 'endnotes':[endnote], 'rating':[rating], 'warnings':[warning], 'fandoms':[fandom], 'ships':[ship], 'charas':[chara],'freeform':[freeform]})

# parse fics
files = []
directory = 'natfinder/natfinder/scraped-works'
for f in os.scandir(directory):
    files.append(f.name)
for f in files:
    st = open(directory + '/' + f).read()
    temp_df = parse_fic(st)
    fics_df = pd.concat([fics_df, temp_df], ignore_index=True)

# find language
fics_df['L1s'] = fics_df.summary.map(lambda x : find_lang(x))
fics_df['L1n'] = fics_df.notes.map(lambda x : find_lang(x))
fics_df['L1e'] = fics_df.endnotes.map(lambda x : find_lang(x))
fics_df['L1t'] = fics_df.tags.map(lambda x : find_lang_tags(x))
fics_df['L1'] = fics_df[['L1s', 'L1n', 'L1e', 'L1t']].bfill(axis=1).iloc[:, 0]
fics_df.drop(columns=['L1s', 'L1n', 'L1e', 'L1t'], inplace=True)
fics_df_lang = fics_df[fics_df['L1'].notna()]
fics_df_mys = fics_df[fics_df['L1'].isna()]

# pickle dataframe
with open('fics_df_scraped.pkl', 'wb') as file:
    pickle.dump(fics_df, file)
with open('fics_df_scraped_lang.pkl', 'wb') as file:
    pickle.dump(fics_df_lang, file)
with open('fics_df_scraped_mys.pkl', 'wb') as file:
    pickle.dump(fics_df_mys, file)