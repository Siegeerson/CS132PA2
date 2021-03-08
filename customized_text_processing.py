from typing import Set
from re import sub,fullmatch
# utilize these for base and then improve
from nltk.tokenize import word_tokenize  # type: ignore
from nltk.stem.porter import PorterStemmer  # type: ignore
from nltk.corpus import stopwords  # type: ignore


"""
    implimentation notes for self and others:
    - numbers: when numbers in query also use word representations
        if single words (up to 19)
    - punctuation: several possible directions
        * use isalpha() to filter out --> removes word entirely not just punct
        * use re.sub to replace any punctuation with -- re.sub(r'[^\\d\\w]+)
    - possibly use shelf index when choosing stop words
        * change shelf build to also build counter in ['___count']
"""
class CustomizedTextProcessing:
    def __init__(self, *args, **kwargs):
        """
        the default TextProcessing class uses Porter stemmer and stopwords list from nltk to process tokens.
        in the Python class, please include at least one other approach for each of the following:
        - to identify a list of terms that should also be ignored along with stopwords
        (not needed to be programatically, preferable to be automatic)
        - to normalize tokens other than stemming and lemmatization
        (numbers, multiword, punctuation)

        Your implementation should be in this class. Create more helper functions as you needed. Your approaches could
        be based on heuristics, the usage of a tool from nltk or some new feature you implemented using Python. Be creative!

        # TODO:
        :param args:
        :param kwargs:
        """


    @classmethod
    def from_customized(cls, *args, **kwargs) -> "CustomizedTextProcessing":
        """
        You don't necessarily need to implement a class method, but if you do, please use this boilerplate.
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError


    def subnums(self, number:int) ->str:
        """
        converts a number to the equivelnt word for all 1 word numbers (0-19)
        :param number:
        :return word:
        """
        num2words = {   0:'zero',1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
                        6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
                        11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
                        15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen'}
        return num2words[number]
    def normalize(self, token: str) -> str:
        """
        your approach to normalize a token. You can still adopt the criterion and methods from TextProcessing along with your own approaches
        :param token:
        :return:
        """
        # TODO:
        raise NotImplementedError


    #note --> maybe remove most frequent words?
    def get_normalized_tokens(self, title: str, content: str) -> Set[str]:
        """
        pass in the title and content_str of each document, and return a set of normalized tokens (exclude the empty string)
        :param title:
        :param content:
        :return:
        """

        # TODO:
        raise NotImplementedError


if __name__ == "__main__":
    pass
