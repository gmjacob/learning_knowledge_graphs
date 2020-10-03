from neo4j import GraphDatabase
import pandas as pd
import re

uri= "bolt://localhost:7687"
username='neo4j'
password='neo4j'

graph_db = GraphDatabase.driver(uri,auth=(username, password))

def createRelationship(subject, object, relation):
    createRelationship = """
        MERGE (subj:subject {{name: "{}" }})
        MERGE (obj:object {{name: "{}" }})
        MERGE  (subj)-[:{}]->(obj)""".format(subject, object, relation)
    
    print("\n",createRelationship)
    with graph_db.session() as session:
        session.run(createRelationship)

def readFromCSV():
    return pd.read_csv('entity_pairs.csv')

def run():
    data = readFromCSV()
    # sample = data.sample(n=5, random_state=6)
    as_dict = data.to_dict('records')
    for row in as_dict:
        createRelationship(
            re.sub('[^A-Za-z ]+', '', row['subject'].strip()),
            row['object'], 
            row['relation'].replace(r' ', '_')
            )
run()