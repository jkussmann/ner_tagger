# Named Entity Recognition Tagger
This is a named entity recognition tagger using NLTK, Spacy, and Stanford Core NLP. The results of each one is consolidated to include any tags ommitted by one of the taggers. If there is disagreement among the taggers for a word, the majority is used. If all 3 taggers disagree, Spacy is used.

## Getting Started

This code is initially written to run on a Windows 10 environment. The program is run from the command line and any IDE can be used.

### Prerequisites

What things you need to install the software and how to install them
* Python 3 (https://www.python.org/downloads/windows/)
* NLTK (https://www.nltk.org/)
* Spacy (https://spacy.io/)
* Stanford CoreNLP (https://stanfordnlp.github.io/CoreNLP/)

## Running the code

Open a command line window and change to the directory the code is located

```
c:\ner_tagger>python main.py
Initializing CoreNLP....

Enter a sentence: Apple announced it would negotiate a deal with Microsoft for $1 billion.

Stanford Named Entities:
$ 1 billion: MONEY

NLTK Named Entities:
Apple: PERSON, Microsoft: ORGANIZATION

Spacy Named Entities:
Apple: ORGANIZATION, Microsoft: ORGANIZATION, $1 billion: MONEY

Consolidated Named Entities:
Apple: ORGANIZATION, Microsoft: ORGANIZATION, $1 billion: MONEY

Enter a sentence: end
Ending Program ...

c:\ner_tagger>
```

## Author

* **John Kussmann** - *Initial work*