#!/usr/bin/env python
# coding: utf-8

# In[2]:

from time import time 

def cleaning(doc):
    # Lemmatizes and removes stopwords
    # doc needs to be a spacy Doc object
    txt = [token.lemma_ for token in doc if not token.is_stop]
    if len(txt) > 2:
        return ' '.join(txt)

def printTime(t):
	text = f'Time to build vocab: {round((time() - t) / 60, 2)} mins'
	print(text)
	return text

# In[ ]:




