"""
This module uses multiple named entity taggers and returns a
consolidated result
"""

from difflib import SequenceMatcher
from nltk import ne_chunk
from nltk.parse import CoreNLPParser

import common_nlp_functions as cnf
import pos_tagger as pt


def get_similarity_score(string1, string2):
    """
	This function returns a similarity score comparing 2 strings
	"""
    return SequenceMatcher(None, string1, string2).ratio()


def get_stanford_named_entities(line):
    """
	Get named entities from the Stanford NER tagger
	"""

    entity_item = ""
    entity_list = []
    previous_type = ""

    st_ner = CoreNLPParser(url="http://localhost:9000", tagtype="ner")
    line_tagged_ner = st_ner.tag(line.split())
    line_tagged = []

    # Tag the input using the tagger
    # The tagger returns in the order (entity, type). Change the
	# order to be consistent with the other taggers (type, entity)
    for item_ner in line_tagged_ner:
        if item_ner[1] != "O":
            line_tagged.append((item_ner[1], item_ner[0]))

    # Consolidate multi-word entities
    if len(line_tagged) == 1:
        entity_list = line_tagged
    elif len(line_tagged) > 1:
        for index, item in enumerate(line_tagged):
            if item[0] == previous_type:
                if item[0] != "O":
                    entity_item += " " + item[1]
            else:
                if item[0] != "O":
                    entity_item = item[1]
                else:
                    entity_list.append((previous_type, entity_item))
                    entity_item = ""

            if index == (len(line_tagged) - 1):
                entity_list.append((previous_type, entity_item))

            previous_type = item[0]

    return entity_list


def get_spacy_named_entities(line):
    """
	Use the Spacy NER tagger
	"""

    entities = cnf.SPACY_NLP(line)
    entity_list = []
    normalized_label = ""
    determiners = [
        "the",
        "a",
        "an",
        "this",
        "that",
        "those",
        "these",
        "my",
        "your",
        "his",
        "her",
        "its",
        "our",
        "their",
        "a few",
        "a little",
        "much",
        "many",
        "a lot of",
        "most",
        "some",
        "any",
        "enough",
        "all",
        "both",
        "half",
        "either",
        "neither",
        "each",
        "every",
        "other",
        "another",
        "such",
        "what",
        "rather",
        "quite",
    ]

    updated_string = ""
    for ent in entities.ents:
        if str(ent.label_) == "ORG":
            normalized_label = "ORGANIZATION"
        elif str(ent.label_) == "LOC":
            normalized_label = "LOCATION"
        else:
            normalized_label = str(ent.label_)

        for item in determiners:
            if item in str(ent):
                updated_string = str(ent).replace(item + " ", "")

        if updated_string == "":
            entity_list.append((normalized_label, str(ent)))
        else:
            entity_list.append((normalized_label, updated_string))

    return entity_list


def get_nltk_named_entities(line):
    """
    Use the NLTK NER tagger
    """

    tagger = pt.get_pos_tagger()
    tokenized_line = cnf.TOKENIZER.tokenize(line)
    tag_list = tagger.tag(tokenized_line)
    chunked_sentence = ne_chunk(tag_list)
    entity_list = []

    for subtree in chunked_sentence.subtrees():
        if subtree.label() in [
            "NE",
            "PERSON",
            "ORGANIZATION",
            "GPE",
            "LOCATION",
            "DATE",
            "TIME",
            "MONEY",
            "PERCENT",
            "FACILITY",
        ]:
            entity_name = " ".join([a for (a, b) in subtree.leaves()])
            entity_list.append((subtree.label(), entity_name))

    return entity_list


def get_named_entities(line):
    """
    Consolidate the results from the named entity identification
    from Stanford, Spacy, and NLTK. Use Spacy as the default. If a NE
    is in Stanford or NLTK and not in Spacy, add it to the Spacy list.
    """

    stanford_list = get_stanford_named_entities(line)
    spacy_list = get_spacy_named_entities(line)
    nltk_list = get_nltk_named_entities(line)

    entity_list = []

    append_item = True
    for item1 in stanford_list:
        for item2 in spacy_list:
            if (get_similarity_score(item1[1], item2[1]) > 0.80) or (
                item1[1] in item2[1] or item2[1] in item1[1]
            ):
                append_item = False

        if append_item:
            spacy_list.append((item1[0], item1[1]))

        append_item = True

    append_item = True
    for item1 in nltk_list:
        for item2 in spacy_list:
            if (get_similarity_score(item1[1], item2[1]) > 0.80) or (
                item1[1] in item2[1] or item2[1] in item1[1]
            ):
                append_item = False

        if append_item:
            spacy_list.append((item1[0], item1[1]))

        append_item = True

    entity_list = spacy_list

    return entity_list
