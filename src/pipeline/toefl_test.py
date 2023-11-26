import json
from src.utils.helper_functions import get_training_data, preprocess_underlined
import random

def preprocess(self, text):
        return text.replace('.', '').replace(',', '').lower()

def mock():
    training_data = get_training_data()
    counter = 0
    random.shuffle(training_data['data'])
    for data in training_data['data']:
        if counter < 5 and data['answer'] != None:
            print(data['text'].replace('\n', ' '))
            print(preprocess_underlined(data['underline']))
            # print(data['answer'])
            counter += 1
    return True