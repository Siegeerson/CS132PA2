import re
from typing import Set, Any, List

from nltk.tokenize import word_tokenize  # type: ignore
from nltk.stem.porter import PorterStemmer  # type: ignore
from nltk.corpus import stopwords  # type: ignore


class TextProcessing:
    def __init__(self, stemmer, stop_words):
        """
        class TextProcessing is used to tokenize and normalize tokens that will be further used to build inverted index.
        :param stemmer:
        :param stop_words:
        :param args:
        """
        self.stemmer = stemmer
        self.STOP_WORDS = set(stop_words)

    @classmethod
    def from_nltk(
        cls
  ,      stemmer: Any = PorterStemmer().stem,
        stop_words: List[str] = stopwords.words("english"),
    ) -> "TextProcessing":
        """
        initialize from nltk
        :param stemmer:
        :param stop_words:
        :return:
        """
        return cls(stemmer, set(stop_words))

    def normalize(self, token: str) -> str:
        """
        normalize the token based on:
        1. make all characters in the token to lower case
        2. remove any characters from the token other than alphanumeric characters and dash ("-")
        3. after step 1, if the processed token appears in the stop words list or its length is 1, return an empty string
        4. after step 1, if the processed token is NOT in the stop words list and its length is greater than 1, return the stem of the token
        :param token:
        :return:
        """
        # TODO:
        token = token.lower()
        alpha_token = re.sub("[^\\d\\w-]","",token)
        if len(alpha_token)==1 or alpha_token in self.STOP_WORDS:
            return ""
        return self.stemmer(alpha_token)

    def get_normalized_tokens(self, title: str, content: str) -> Set[str]:
        """
        pass in the title and content_str of each document, and return a set of normalized tokens (exclude the empty string)
        you may want to apply word_tokenize first to get un-normalized tokens first
        :param title:
        :param content:
        :return:
        """
        # TODO: Why pass in title?

        tokens = word_tokenize(content) + word_tokenize(title)
        out = set()
        stops = set()
        for token in tokens:
            nom_token = self.normalize(token)
            if nom_token != "":
                out.add(nom_token)
            else:
                stops.add(token)
        return out,stops


if __name__ == "__main__":
    pass
