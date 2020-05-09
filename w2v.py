#!/usr/bin/env python
# coding: utf-8
import re  # For preprocessing
import pandas as pd  # For data handling
from collections import defaultdict  # F
import spacy  # For preprocessing
from gensim.models.phrases import Phrases, Phraser
from constants import *
from util import *
from gensim.models.phrases import Phrases, Phraser
import multiprocessing
from gensim.models import Word2Vec

def run(dataset="biorxiv_medrxiv", test=False):
    millis = int(round(time() * 1000))
    logging.basicConfig(
        filename=f"{defaultpath}/results/info_{millis}.log",
        filemode='a',
        format="%(levelname)s - %(asctime)s: %(message)s", 
        datefmt= '%H:%M:%S', 
        level=logging.INFO)

    filepath = f"{defaultpath}/processed/{dataset}/body.csv"
    logging.info(f"Reading {filepath}")
    df = pd.read_csv(filepath, sep="\t")
    if test:
        df =  df[:100]
    logging.info(f"Dataset size: {len(df)}")
    logging.info(df.shape)
    df = df.dropna().reset_index(drop=True)
    logging.info("Number of Null lines")
    logging.info(df.isnull().sum())
    
    nlp = spacy.load('en', disable=['ner', 'parser'])

    brief_cleaning = (re.sub("[^A-Za-z']+", ' ', str(row)).lower() for row in df['body'])
    
    t = time()
    logging.info("Cleanning")
    txt = [cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=8, n_threads=-1)]
    
    logging.info(printTime(t))

    df_clean = pd.DataFrame({'clean': txt})
    df_clean = df_clean.dropna().drop_duplicates()
    logging.info(print(df_clean.shape))
    sent = [row.split() for row in df_clean['clean']]
    phrases = Phrases(sent, min_count=30, progress_per=10000)
    sentences = phrases[sent]


    word_freq = defaultdict(int)
    for sent in sentences:
        for i in sent:
            word_freq[i] += 1
    print(len(word_freq))

    sorted(word_freq, key=word_freq.get, reverse=True)

    cores = multiprocessing.cpu_count()

    w2v_model = Word2Vec(min_count=20,
                     window=2,
                     size=300,
                     sample=6e-5, 
                     alpha=0.03, 
                     min_alpha=0.0007, 
                     negative=20,
                     workers=cores-1)

    t = time()
    w2v_model.build_vocab(sentences, progress_per=10000)
    logging.info(printTime(t))


    t = time()
    w2v_model.train(sentences, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)
    logging.info(printTime(t))

    w2v_model.init_sims(replace=True)

    w2v_model.save(f"{defaultpath}/results/word2Vec.model")
    logging.info("Finished")





if __name__ == '__main__':
    run(test=False)