import unittest
import warnings
from sys import executable
import socket
import time
from subprocess import Popen, CREATE_NEW_CONSOLE
from named_entity_tagger import get_stanford_named_entities, get_spacy_named_entities, get_nltk_named_entities, get_named_entities


def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)
    return do_test

class TestNER(unittest.TestCase):

    @ignore_warnings
    def test_stanford(self):        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(("localhost", 9000))

        if result != 0:
            Popen(
                [executable, "core_nlp.py"],
                cwd="c:\stanford-corenlp-full-2018-02-27",
                creationflags=CREATE_NEW_CONSOLE,
            )
            print(
                "Initializing CoreNLP...."
            )  # Give CoreNLP some time to get going before accepting input.
            time.sleep(120)
        
        self.assertEqual(get_stanford_named_entities("Apple announced it would negotiate a deal with Microsoft for $1 billion."), [('MONEY', '$ 1 billion')])
        sock.close()

    @ignore_warnings
    def test_spacy(self):        
        self.assertEqual(get_spacy_named_entities("Apple announced it would negotiate a deal with Microsoft for $1 billion."), [('ORGANIZATION', 'Apple'), ('ORGANIZATION', 'Microsoft'), ('MONEY', '$1 billion')])

    @ignore_warnings
    def test_nltk(self):        
        self.assertEqual(get_nltk_named_entities("Apple announced it would negotiate a deal with Microsoft for $1 billion."), [('PERSON', 'Apple'), ('ORGANIZATION', 'Microsoft')])

    @ignore_warnings
    def test_consolidated(self):        
        self.assertEqual(get_named_entities("Apple announced it would negotiate a deal with Microsoft for $1 billion."), [('ORGANIZATION', 'Apple'), ('ORGANIZATION', 'Microsoft'), ('MONEY', '$1 billion')])

if __name__ == '__main__':
    unittest.main()