import os
import logging

# In[21]:
#constants
defaultpath="/users/dimmymag/datasets/covid"
dirs = ["biorxiv_medrxiv", "comm_use_subset","custom_license", "noncomm_use_subset"]
subdirs = ["pdf_json", "pmc_json"]
extension = "*.json"
dataframe_columns = ['rep', 'filepath']



