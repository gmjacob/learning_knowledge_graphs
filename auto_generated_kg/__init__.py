import pandas as pd
from entity_algos import entity_pairs
from display import draw_kg

wiki_data = pd.read_csv('wiki_data.csv')
pairs = entity_pairs(wiki_data.loc[0,'text'])
print(pairs)

draw_kg(pairs)