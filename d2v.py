import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
from gensim import utils
import spacy  # For preprocessing
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt


def run(dataset="biorxiv_medrxiv", test=False):
	filepath = f"{defaultpath}/processed/{dataset}/body.csv"
    print(f"Reading {filepath}")
    df = pd.read_csv(filepath, sep="\t")
    if test:
        df =  df[:10]
    print(f"Dataset size: {len(df)}")
    print(df.shape)
    df = df.dropna().reset_index(drop=True)
    print("Number of Null lines")
    print(df.isnull().sum())
    