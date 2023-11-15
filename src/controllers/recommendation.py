import json
from src.models.question_bank import QuestionBank;
from src.models.test_result import TestResult;
from src.models.test_result_detail import TestResultDetail;
from src.models.user import User;
from src.utils.response import CustomResponse

from sqlalchemy import create_engine, text

from src.utils.db import db

# import question characteristic 
from src.pipeline.extract_features import extract_features

# import Orange3
import Orange

# import render template
from flask import render_template, jsonify

# import model
from mlxtend.frequent_patterns import fpgrowth

import pandas as pd

class Recommendation():
    def __init__(self, user):
        self.user = user
    def HelloWord():
        return "hello word"
    
    @staticmethod
    def dataset_discretization(dataset):
        # use orange3 for discretization
        discretizer = Orange.preprocess.Discretize()
        disc_data = dataset
        return disc_data
    
    # get recommendation
    @staticmethod
    def recommendation(id):
      #  get user by id 
       user = User.get_by_id(id)

      #  check if user exist or not
       if user is None:
            return CustomResponse.failure("user not found", 404)
       
       # Define your database connection
    #    engine = create_engine('mysql+mysqlconnector://root:@localhost/smarteng_smartengtest')

       # Query to join User, Result, ResultDetail, and QuestionBank with filter by user ID dont use session
       # Define the SQL query to join the tables
    #    sql_query = text('''
    #         SELECT *
    #         FROM users
    #         JOIN test_results ON users.id = test_results.user_id
    #         JOIN test_result_details ON test_results.id = test_result_details.result_id
    #         JOIN question_banks ON test_result_details.question_id = question_banks.id
    #         WHERE users.id = 12
    #     ''')
      
       # Execute the query
    #    with engine.connect() as connection:
    #     result = connection.execute(sql_query)
    
       # fetch all data 
    #    rows = result.all()

       # feature extraction 
    #    pipeline = extract_features(rows[0].question, [2,5,6,13])

       # diskritisasi dataset 
    #    diskrit_data = Recommendation.dataset_discretization(pipeline.pipeline())

       # load dataset 
       data = pd.read_csv('data/smartengtest-dataset.csv')

       # modelling dataset 
       # Apply FP-growth to find frequent itemsets
       frequent_itemsets = fpgrowth(data, min_support=0.5, use_colnames=True)

       maxItem =  len(frequent_itemsets) if len(frequent_itemsets) < 3 else 3 
       detections = []

       for _, item in frequent_itemsets.iterrows():
              detect = {}
              if len(detections) < maxItem:
                detect["support"] = item.support
                detect["item"] = json.dumps({'items': [str(it) for it in item['itemsets']]}) 
                detections.append(detect)
              else:
                break
       
       print(detections)

       threshold = 0.4
       resultDetections = [detection for detection in detections if detection["support"] >= threshold]
       print(resultDetections)


      #set up for generate recommendation based on question characteristics

      #  sentences = []
      #  for detection in resultDetections:
      #     if detection["item"] == "{\"items\": [\"h_n_difficult_word\"]}":
      #        sentence = "ayo belajar tenses"
      #        sentences.append(sentence)
      #     elif detection["solution"] == "t2":
      #        sentence = "ayo belajar vocab"
      #        sentences.append(sentence)
      #     elif detection["solution"] == "t3":
      #        sentence = "ayo belajar coherence"
      #        sentences.append(sentence)

       res = {
            "name": user.name,
            "detections": resultDetections,
            "text": "generated by AI"
            # "recommendation": sentence
        }
       return CustomResponse.success(res)
    
    def getUser(self):
        return self.user