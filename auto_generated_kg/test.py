import entity_algos
import spacy
from spacy import displacy
import re

nlp = spacy.load("en_core_web_lg")

text = """Manchester United offered Jadon Sacho lower wages than he is on at Borussia Dortmund to sign him this summer, according to reports.
Sancho, 20, was United boss Ole Gunnar Solskjaer's No 1 target during the summer transfer window, but Dortmund's £108million valuation proved an insurmountable obstacle despite months of on-off talks.
According to The Athletic, the Old Trafford club were never on the verge of signing the England star and that initial calculations for a deal rose to a staggering £227m (€250m). 

United reportedly argued that Sancho's £108m valuation did not take into account the financial slump caused by the coronavirus pandemic, with club chiefs feeling the price should have been lowered.
But the outlet adds that initial calculations rose to £227m with wages and agent fees, leaving United with no choice but to refuse that amount.
However, the report adds Dortmund originally wanted the £108m fee as a 'minimum' and ideally planned to receive a fee nearer the £133m (€147m) mark that Barcelona paid for Ousmane Dembele in 2017.
United reportedly never got close to that guaranteed sum, with one offer, submitted by chief negotiator Matt Judge through agents in the final week of September, amounting to £80m plus add-ons. 
"""
# replace multiple new lines with '.'
text = re.sub(r'\n+','. ', text)
# remove reference numbers
text = re.sub(r'\[\d+\]', ' ', text)
doc = nlp(text)
sentence_spans = list(doc.sents)

print(entity_algos.entity_pairs(text))
# displacy.serve(sentence_spans, style="dep")