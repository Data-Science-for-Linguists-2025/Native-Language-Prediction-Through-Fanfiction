### imports
import pickle
import dask
from dask.distributed import Client, LocalCluster
client = Client(processes=True, n_workers=4, threads_per_worker=20)
import pandas as pd
import re
from bs4 import BeautifulSoup as beau
import stanza

manual = pickle.load(open('fics_df_manual.pkl', 'rb'))
scraped = pickle.load(open('scraped_fics_dataframe.pkl', 'rb'))

manual['work'] = manual.work.map(lambda x : [beau(y).text for y in x][0])
manual = manual[['L1', 'work']]
scraped = scraped[['L1', 'work']]
all_df = pd.concat([manual, scraped], ignore_index=True)
all_df_trunc = all_df[['L1', 'work']]
all_df_trunc['work'] = all_df_trunc.work.map(lambda x : ''.join(x))

def get_punct(s):
    remove_n = re.compile(r'\s*\n+', re.S)
    s = re.sub(remove_n, ' ', s)
    return [x for x in s if not x.isalpha() and not x.isdigit()]

all_df_trunc['punct'] = all_df_trunc.work.map(lambda x : get_punct(x))
all_df_trunc['work'] = all_df_trunc.work.map(lambda x : (re.sub(r'\n', ' ', x)))

config = {
    'processors':'tokenize,mwt,pos,lemma',
    'lang':'en',
    'download_method':None
}
stnz = stanza.Pipeline(**config)

all_df_trunc['toks'] = all_df_trunc.work.map(lambda x : [word.text for sent in stnz(x).sentences for word in sent.words])
all_df_trunc['word_feats'] = all_df_trunc.work.map(lambda x : [word.feats for sent in stnz(x).sentences for word in sent.words])

pickle.dump(all_df_trunc, open('trunc_df.pkl', 'wb'))