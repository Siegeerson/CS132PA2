from nltk.stem.porter import PorterStemmer  # type: ignore
from nltk.stem import SnowballStemmer
from text_processing import TextProcessing
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords  # type: ignore
from pathlib import Path

"""
    I made this simple script to test the effectiveness of three popular stemming
    algorithms on the number of tokens returned. In increacing agressiveness:
    - Porter
    - Snowball
    - Lancaster
"""

snow = TextProcessing(stemmer=SnowballStemmer('english').stem,stop_words=stopwords.words("english"))
port = TextProcessing.from_nltk()
lan = TextProcessing(stemmer=LancasterStemmer().stem,stop_words=stopwords.words("english"))
from utils import load_wapo

data_dir = Path("pa3_data")
wapo_path = data_dir.joinpath("wapo_pa3.jl")
ss = set()
ps = set()
ls = set()

for doc in list(load_wapo(wapo_path))[:200]:
    ss = ss.union(snow.get_normalized_tokens("",doc['content_str'])[0])
    ps = ps.union(port.get_normalized_tokens("",doc['content_str'])[0])
    ls = ls.union(lan.get_normalized_tokens("",doc['content_str'])[0])
print("Snow",len(ss),"port",len(ps),"lan",len(ls))


"""
    Tested on the first 200 documents in the corpus here are the results:
    Porter:     12365
    Snowball:   12277
    Lancaster:  10831

    Conclusion: Lancaster results in a smaller set of tokens by arround 2000
                Not a drastic result but still possibly useful
"""
