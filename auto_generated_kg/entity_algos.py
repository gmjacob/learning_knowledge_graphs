import pandas as pd
import re
import spacy 
import neuralcoref

nlp = spacy.load("en_core_web_lg")
neuralcoref.add_to_pipe(nlp)

def entity_pairs(text, coref=True):
    # replace multiple new lines with '.'
    text = re.sub(r'\n+','. ', text)
    # remove reference numbers
    text = re.sub(r'\[\d+\]', ' ', text)
    # Load language model with the text base
    text = nlp(text)

    if coref:
        # resolve coreference clusters
        text = nlp(text._.coref_resolved)
    # split text into an array of sentences
    sentences = [sent.string.strip() for sent in text.sents]
    # entity pairs
    ent_pairs = list()

    for sent in sentences:
        sent = nlp(sent)
        spans = list(sent.ents) + list(sent.noun_chunks)
        spans = spacy.util.filter_spans(spans)

        with sent.retokenize() as retokenizer:
            [retokenizer.merge(span) for span in spans]
        
        dep = [token.dep_ for token in sent]
        
        if(dep.count('obj')+dep.count('nsubj')) == 1 \
            and (dep.count('subj')+dep.count('nsubj'))==1:
        
            for token in sent:
                #identify object nodes
                if token.dep_ in ('obj', 'dobj'):
                    subject = [w for w in token.head.lefts if w.dep_ in ('subj', 'nsubj')]

                    if subject:
                        subject = subject[0]
                        # identify relationship by root dependency
                        relation = [w for w in token.ancestors if w.dep_ == 'ROOT']
                        if relation:
                            relation = relation[0]
                            # add adposition or particle to relationship
                            if relation.nbor(1).pos_ in ('ADP', 'PART'):
                                relation = ' '.join((
                                    str(relation),
                                    str(relation.nbor(1))
                                ))
                        else:
                            relation = 'unknown'
                        subject, subject_type = refine_ent(subject, sent)
                        token, object_type = refine_ent(token, sent)
                        ent_pairs.append([
                            str(subject),
                            str(relation),
                            str(token),
                            str(subject_type),
                            str(object_type),
                        ])
    
    filtered_ent_pairs = [
        sublist for sublist in ent_pairs
        if not any(str(x) == '' for x in sublist)
        ]
    
    pairs = pd.DataFrame(
        filtered_ent_pairs,
        columns=['subject', 'relation', 'object', 'subject_type', 'object_type']
    )

    print('Entity pairs extracted: ', str(len(filtered_ent_pairs)))
    return pairs

def refine_ent(ent, sent):
    unwanted_tokens = (
        'PRON',  # pronouns
        'PART',  # particle
        'DET',  # determiner
        'SCONJ',  # subordinating conjunction
        'PUNCT',  # punctuation
        'SYM',  # symbol
        'X',  # other
    )
    ent_type = ent.ent_type_
    
    if ent_type == '':
        ent_type = 'NOUN_CHUNK'
        ent = ' '.join(str(t.text) for t in
                nlp(str(ent)) if t.pos_
                not in unwanted_tokens and t.is_stop == False)
    elif ent_type in ("NOMINAL", "CARDINAL", "ORDINAL") and str(ent).find(' ') == -1:
        t = ''
        for i in range(len(sent)-ent.i):
            if ent.nbor(i).pos_ not in ('VERB', 'PUNCT') :
                t += ' ' + str(ent.nbor(i))
            else:
                ent = t.strip()
                break
        
    return ent, ent_type