import os
from enum import Enum
import requests
import pandas as pd
import re
import plotly.express as px


models = ["model_2", "fineTune"]

NUM_CLASSES = 10
CLASSES = ["machine learning", "cooking", "crime", "politics", "kid", "comedy", "sport", "culture", "lifestyle", "business"]


def preprocess(text:str):
    return re.sub("\"|\'","",text)

def send_request(model, text:str, verbose:int=0):
        
    url = f"http://35.222.6.176/topicmodelling/prediction/{model}?verbose={verbose}"
    result = requests.get(url, json={'sentence':preprocess(text)}).json()
    result = {
        key: [value] for key,value in result.items() if key != "preprocessed sentence"
    }
    result = pd.DataFrame(result).T
    result = result.reset_index()
    result.columns = ['label','probabilities']

    return result

def get_initial_fig():
    startup_table = pd.DataFrame({
        'label':CLASSES,
        'probabilities':[100/NUM_CLASSES for i in range(NUM_CLASSES)]
    })
    return px.pie(startup_table, values='probabilities', names='label', title='Labels probabilities')