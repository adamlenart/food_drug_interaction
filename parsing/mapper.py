#!/home/adam/anaconda3/envs/python2/bin/python
from __future__ import unicode_literals
import os
import sys 
import numpy as np
import json
import pickle
import codecs
import jellyfish
from collections import defaultdict
import pubmed.utils as pb
from nltk.tokenize import sent_tokenize



# --------------------------------------- helper functions --------------------------- #
def list_loader(data):
    test = pickle.load(open( data , "rb"))
    foodlist = []
    for food in test.keys():
        foodlist.append(food.decode('utf-8').lower())
    return set(foodlist)

def abstract_loader(name):
    with codecs.open(name,"r","utf-8") as data_file:
        data = json.load(data_file)        
    return data.itervalues()

def splitSentences(abstract):
    sentences = sent_tokenize(abstract)
    return sentences

def flat_map(sentences):
    return [sent for s in sentences for sent in s]

def find_ngrams(sentence, n):
    ''' Return list of ngrams from a sentence
    '''
    words_list = sentence.split()
    ngrams = zip(*[words_list[i:] for i in range(n)])
    return [''.join([unicode(w)+' ' for w in ngram if type(w)==unicode]).strip() for ngram in ngrams]

def spark_imitator(abstracts, drugkeyword, distance):
    split_sentences = map(lambda abstract: splitSentences(abstract), abstracts)
    flat_sentences = flat_map(split_sentences)
    substituted_sentences = map(lambda sentence, drugkeyword: pb.ace_substitutor(sentence, drugkeyword), flat_sentences,
                                drugkeyword)
    drug_filtered_sentences = filter(lambda sentence: drugkeyword in sentence, substituted_sentences)
    food_filtered_sentences = filter(lambda sentence: includeFoodCmpd(sentence, foodlist, distance), drug_filtered_sentences)
    return food_filtered_sentences

def includeFoodCmpd(sentence, fdlist, distance, verbose = False):
    ''' Calculates the Jaro Wrinkler distance between food name and ngrams in the sentence.
        Returns True if distance > 0.95
    '''
    result = False
    for food in fdlist:
        n = min(3, len(food.split()))  # Assuming max as trigram        
        sentence_ngrams = find_ngrams(sentence, n)  # Note: punctuation at end of sentence will be included with
                                                    # last word. For now ok, since the JW will still be > 0.95
        for ngram in sentence_ngrams:
            ngram_distance = jellyfish.jaro_winkler(food.lower(), ngram.lower())
            if verbose:
                print food, ngram, ngram_distance
            if ngram_distance > distance: 
                result = True
                break
    return result

if __name__ == "__main__":
    # ------------------ input settings ------------------ #
    NAME = "../analysis/pbabstract"+ sys.argv[1] +  ".json"
    FOODLIST = "data/" + sys.argv[2] + ".pickle" 
    DRUGKEYWORD = sys.argv[3]

    
    # ------------------------ run ----------------------- #
    foodlist = list_loader(FOODLIST)
    abstracts = abstract_loader(NAME)
    #split_sentences = map(lambda abstract: splitSentences(abstract), abstracts)
    #flat_sentences = flat_map(split_sentences)
    #substituted_sentences = map(lambda sentence, drugkeyword: pb.ace_substitutor(sentence, drugkeyword), flat_sentences,'ACEI')
    #drug_filtered_sentences = filter(lambda sentence: DRUGKEYWORD in sentence, substituted_sentences)
    #food_filtered_sentences = filter(lambda sentence: includeFoodCmpd(sentence, foodlist, 0.95), drug_filtered_sentences)
    food_filtered_sentences = spark_imitator(abstracts, DRUGKEYWORD, 0.95)
    print food_filtered_sentences 