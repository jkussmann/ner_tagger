"""
This module utilizes 3 part of speech taggers and returns the
consolidated results
"""

import pickle
import os
import sys

from nltk.tag.sequential import ClassifierBasedPOSTagger
from nltk.tag import DefaultTagger

# from nltk.tree import *
from nltk.corpus import treebank
from nltk.parse import CoreNLPParser

import common_nlp_functions as cnf

MODEL_PATH = "models/"

if sys.version_info[0] == 3:
    Unicode = str


def get_stanford_pos_tags(line):
    """
    Get part of speech tags using the Stanford POS tagger
    """

    st_pos = CoreNLPParser(url="http://localhost:9000", tagtype="pos")
    tokenized_line = cnf.TOKENIZER.tokenize(line)
    line_tagged_initial = st_pos.tag(tokenized_line)
    line_tagged_output = []

    for item in line_tagged_initial:
        line_tagged_output.append((item[0], item[1]))

    return line_tagged_output


def train_tagger():
    """
	This function trains the tagger
	"""
    print("Training POS tagger...")
    # https://github.com/japerk/nltk3-cookbook/blob/master/chapter4.py

    tagged_sentences = treebank.tagged_sents()
    size = int(len(tagged_sentences) * 0.9)
    train_sents = tagged_sentences[:size]
    test_sents = tagged_sentences[3000:]

    default = DefaultTagger("NN")
    tagger = ClassifierBasedPOSTagger(
        train=train_sents, backoff=default, cutoff_prob=0.3
    )
    print(tagger.evaluate(test_sents))  # 0.9613641269156055

    # save model to pickle file as binary
    file_name = MODEL_PATH + "tag_model.pkl"
    with open(file_name, "wb") as fout:
        pickle.dump(tagger, fout)

    print("model written to: " + file_name)
    print("")

    return tagger


def get_pos_tagger():
    """
	This function gets the tagger if it is stored. If no
	tagger is found, it trains one.
	"""

    # check if models exist, if not run training
    if not os.path.isfile(MODEL_PATH + "tag_model.pkl"):
        print("")
        print("Creating Tag Model.....")
        tagger = train_tagger()
    else:
        # read the file in as binary
        tagger = pickle.load(open(MODEL_PATH + "tag_model.pkl", "rb"))

    return tagger


def get_nltk_pos_tags(line):
    """
    Get the part of speech tags using the nltk classifier tagger
    """

    tagger = get_pos_tagger()
    tokenized_line = cnf.TOKENIZER.tokenize(line)
    tag_list = tagger.tag(tokenized_line)
    line_tagged_output = []

    for item in tag_list:
        line_tagged_output.append((item[0], item[1]))

    return line_tagged_output


def get_spacy_pos_tags(line):
    """
    Get the part of speech tags using the Spacy tagger
    """

    tagged_line = cnf.SPACY_NLP(line)
    line_tagged_output = []
    for word in tagged_line:
        line_tagged_output.append((str(word), str(word.tag_)))

    return line_tagged_output


def get_pos_tags(line):
    """
    Consolidate the tags from NLTK, Spacy, and Stanford
    """

    stanford_list = get_stanford_pos_tags(line)
    nltk_list = get_nltk_pos_tags(line)
    spacy_list = get_spacy_pos_tags(line)

    temp_list = []
    consolidated_list = []

    for item1 in stanford_list:
        for item2 in nltk_list:
            if item1[0] == item2[0]:
                if item1[1] != item2[1]:
                    temp_list.append(
                        (item1[0], item1[1])
                    )  # Use Stanford tags if there is disagreement
                else:
                    temp_list.append((item2[0], item2[1]))

    for item3 in temp_list:
        for item4 in spacy_list:
            if item3[0] == item4[0]:
                if item3[1] != item4[1]:
                    consolidated_list.append(
                        (item4[0], item4[1])
                    )  # Use Spacy tags if there is disagreement
                else:
                    consolidated_list.append((item3[0], item3[1]))

    return consolidated_list
