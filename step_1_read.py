#!/usr/bin/env python
# coding: utf-8

# In[191]:


#imports
import sys, os, glob
import pandas as pd
import json
import os
import shutil

from util import *
from constants import *


# In[195]:


def mountDatasetFile():
    pathLists = []
    df = pd.DataFrame(columns=dataframe_columns)
    i = 0
    for d in dirs:
        subpath = f"{defaultpath}\\{d}\\{d}"
        for subdir in subdirs:
            _subpath = f"{subpath}\\{subdir}"
            filepaths = glob.glob(os.path.join(_subpath, extension))
            file_size = len(filepaths)
            if file_size==0:
                print(f"pro {_subpath}")
                continue
            for filepath in filepaths:
                head, tail = os.path.split(filepath)
                relative_path = f"\\{d}\\{d}\\{subdir}\\{tail}"
                df.loc[i] = [d, relative_path]
                i+=1

    print(len(df))
    df.to_csv(f"{defaultpath}/processed/dataset.csv", index=False)


# In[256]:


def prepareDataset(rep_target = 'biorxiv_medrxiv', subset_size=3):
    processed_dir = f"{defaultpath}/processed"
    df = pd.read_csv(f"{processed_dir}/dataset.csv")
    df.columns = dataframe_columns
    
    if rep_target:
        df = df[df['rep'].str.match(rep_target)]
        
        
    if os.path.exists(f"{processed_dir}/{rep_target}") and os.path.isdir(f"{processed_dir}/{rep_target}"):
        shutil.rmtree(f"{processed_dir}/{rep_target}")
    os.mkdir(f"{processed_dir}/{rep_target}")
        
    
    print(f"Dataset length: {len(df)}")
    
    if subset_size>0:
        df = df[:subset_size]
        
    print(f"subset from Dataset length: {len(df)}")

    ids = []
    titles = []
    authors = set()
    abstracts = []
    
    authors_paper = []
    author_id = 0
    
    citation_id = 0
    citations = []
    citations_titles = []
    
    bodies = []
    
    
    
    for k, row in df.iterrows():
        rep, filepath = row['rep'], row['filepath']
        filepath = filepath.replace("\\", "/")
        with open(f'{defaultpath}{filepath}') as json_file:
            data = json.load(json_file)
            id = data['paper_id']
            ids.append(id)
            title = data['metadata']['title']
            titles.append([id, title])
            _authors = data['metadata']['authors']
            for author in _authors:
                middle = " ".join([m for m in author['middle']])
                author_name = f"{author['first']} {middle} {author['last']}" 
                institution = ""
                country = ""
                if author['affiliation']:
                    institution = author['affiliation']['institution']
                    if 'country' in author['affiliation']['location']:
                        country = author['affiliation']['location']['country']
                authors.add((author_id, author_name, institution, country))
                authors_paper.append([author_id, id])
                author_id+=1
                
            _abstract = ""

            _bib_entries = data['bib_entries']
            for be in _bib_entries:
                _be = data['bib_entries'][be]
                _be_title = _be['title']
                _be_doi = ""
                if 'DOI' in _be['other_ids']:
                    _be_doi = _be['other_ids']['DOI'][0]
                citations.append([citation_id, be, id, _be_title, _be_doi])
                citation_id+=1
            
            for item in data['abstract']:
                text = item['text']
                _abstract=f"{_abstract}{text} "
                
            abstracts.append([id, _abstract])
            
            
            _body = ""
            for k, body in enumerate(data['body_text']):
                text = body['text']
                section = body['section']
                tag = f"###paragraph_{k}_section_{section}### "
                _body = f"{_body}{tag}{text} "
            
            bodies.append([id, str(_body)])

            
            
                
            
    id_str = "\n".join([i for i in ids])
    with open(f'{processed_dir}/{rep_target}/ids.csv', "w", encoding="utf-8") as ids_file:
        print("Saving ID file")
        ids_file.write("paper_id\n")
        ids_file.write(id_str)
    with open(f'{processed_dir}/{rep_target}/titles.csv', "w", encoding="utf-8") as titles_file:
        print("Saving title file")
        titles_file.write(f"paper_id\title\n")
        for id, title in titles:
            titles_file.write(f"{id}\t{title}\n")
    with open(f'{processed_dir}/{rep_target}/authors.csv', "w", encoding="utf-8") as authors_file:
        print("Saving authors file")
        authors_file.write(f"name\tinst\tcountry\n")
        for id, name, inst, country in authors:
            authors_file.write(f"{id}\t{name}\t{inst}\t{country}\n")
    with open(f'{processed_dir}/{rep_target}/author_paper.csv', "w", encoding="utf-8") as author_paper_file:
        print("Saving author_paper_file file")
        author_paper_file.write(f"author_id\tpaper_id\n")
        for id, paper_id in authors_paper:
            author_paper_file.write(f"{id}\t{paper_id}\t\n")
    
    with open(f'{processed_dir}/{rep_target}/abstract.csv', "w", encoding="utf-8") as abstract_file:
        print("Saving abstracts file")
        abstract_file.write(f"paper_id\tabstract\n")
        for id, abstract in abstracts:
            abstract_file.write(f"{id}\t{abstract}\n")
            
    with open(f'{processed_dir}/{rep_target}/citations.csv', "w", encoding="utf-8") as citations_file:
        print("Saving citations file")
        for citation_id, ref_file_id, paper_id, title, doi in citations:
            citations_file.write(f"{citation_id}\t{ref_file_id}\t{paper_id}\t{title}\t{doi}\n")
    
    ids = []
    bodies_v = []
    for paper_id, text in bodies:
        ids.append(paper_id)
        bodies_v.append(text)
    
    
    df = pd.DataFrame(columns=["paper_id", "body"])
    df['paper_id'] = df['paper_id'].astype(str)
    df['body'] = df['body'].astype(str)
    
    df['paper_id'] = ids
    df['body'] = bodies_v
    
    df.to_csv(f'{processed_dir}/{rep_target}/body.csv', index=False, sep="\t")
    print(df.head())

        
    
    
            


# In[258]:
if __name__ == '__main__':
    prepareDataset(subset_size=-1)


# In[ ]:




