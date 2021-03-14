from typing import Dict, Union, Iterator
import functools
import os
import time
import json
import re
from pathlib import Path
from tqdm import tqdm

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_t = time.perf_counter()
        f_value = func(*args, **kwargs)
        elapsed_t = time.perf_counter() - start_t
        mins = elapsed_t // 60
        print(
            f"'{func.__name__}' elapsed time: {mins} minutes, {elapsed_t - mins * 60:0.2f} seconds"
        )
        return f_value

    return wrapper_timer

def load_wapo(wapo_jl_path: Union[str, os.PathLike]) -> Iterator[Dict]:
    """
    Unlike HW2, load_wapo should be an iterator in this assignment. It's more memory-efficient when you need to
    load each document and build the inverted index.
    At each time, load_wapo will yield a dictionary of the following format:

    {
        "id": 1,
        "title": "Many Iowans still don't know who they will caucus for",
        "author": "Jason Horowitz",
        "published_date": 1325380672000,
        "content_str": "Iran announced a nuclear fuel breakthrough and test-fired ..."
      }

    It's similar to what you created in HW2 except the value of the key "id". You should replace the original value of
    the key "id" with an integer that corresponds to the order of each document that has been loaded. For example. the
    id of the first yielded document is 0 and the second is 1 and so on. Also make sure to remove any HTML elements from
    the content_str.
    :param wapo_jl_path:
    :return:
    """
    i = 0
    with open(wapo_jl_path,"r") as wapo:                             # open file
        for line in tqdm(wapo.read().splitlines()):                        #read line by line
            doc = json.loads(line)                                   #unpack json
            content = ""
            j = 0
            for cont in doc["contents"]:
                # print(cont)
                if cont and "subtype" in cont and cont["subtype"] == "paragraph":
                    content = content +"</br>"+ re.sub('<.*?>','',cont['content'])     #build text content from paragraphs
            if not "title" in doc or not doc["title"]:
                doc["title"] = ""

            out ={                                                      #build dictionary for document
                "id":i,
                "title":re.sub('<.*?>','',doc["title"]),
                "author":doc["author"],
                "published_date":doc["published_date"],
                "content_str": content
            }
            i+=1
            # print("supplying doc")
            yield out

if __name__ == "__main__":
    pass
