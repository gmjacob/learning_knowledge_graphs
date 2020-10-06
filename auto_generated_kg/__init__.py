import pandas as pd
from entity_algos import entity_pairs
from display import draw_kg

wiki_data = pd.read_csv('wiki_data.csv')
print("page")
for i in range(len(wiki_data)):
    print(wiki_data.loc[i, 'page'])

# print(wiki_data.loc[0,'text'])
# pairs = entity_pairs(wiki_data.loc[0,'text'])
# print(pairs)

# draw_kg(pairs)