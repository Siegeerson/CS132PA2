import os,heapq
import shelve
from collections import Counter
from typing import Union, List, Tuple
from tqdm import tqdm
from utils import timer,load_wapo
from text_processing import TextProcessing

text_processor = TextProcessing.from_nltk()
# include your customized text processing class


@timer
def build_inverted_index(
    wapo_jl_path: Union[str, os.PathLike], index_shelve_path: str
) -> None:
    """
    load wapo_pa3.jl to build the inverted index and store the index as a shelf in the provided path
    :param wapo_jl_path:
    :param index_shelve_path:
    :return:
    """


    # Note: Generating inverted index and then assigning it to shelf --> big speed improvement
    #---> but doing so ignores the whole point of using shelf for the index
    # Current iteration takes about 15-25 minutes to run
    with shelve.open(index_shelve_path,flag='n',writeback=True) as index:
        index["___count"] = Counter() #this is used for analysis in custom processing
        for doc in load_wapo(wapo_jl_path):
            normal_tokens, stops= text_processor.get_normalized_tokens(doc['title'],doc['content_str'])
            for token in normal_tokens:
                # index_cur = index.get(token,[]) # index[token]
                index.setdefault(token,[])
                index[token].append(doc['id'])
                # index_cur.append(doc['id'])   #note: append operates in place, does not return a value
                # index[token] = index_cur
            index["___count"].update(normal_tokens) #update counter


@timer
def intersection(posting_lists: List[List[int]]) -> List[int]:
    """
    implementation of the intersection of a list of posting lists that have been ordered from the shortest to the longest
    :param posting_lists:
    :return:

    NOTE: maybe use sets --> only worry if becomes a problem
    """
    #edge cases
    if len(posting_lists)==1:
        return posting_lists[0]
    if len(posting_lists)==0:
        print(posting_lists)
        return []
    # Intersects between two lists
    def intersect_two(list1, list2):
        if list2==[] or list1 ==[]:
            return []
        output = []
        head1 = 0
        head2 = 0
        # Standard intersection alg
        while head1<len(list1) and head2<len(list2):
            if   list1[head1] < list2[head2]:
                head1 += 1
            elif list1[head1] > list2[head2]:
                head2 +=1
            else:
                output.append(list2[head2])
                head1+=1
                head2+=1
        print(head1,head2)
        return output
    #get intersect of first two lists
    outlist = intersect_two(posting_lists.pop(0),posting_lists.pop(0))
    #get intersect of intermediary output with next list
    while posting_lists:
        outlist = intersect_two(outlist,posting_lists.pop(0))
    return outlist


def query_inverted_index(
    query: str, shelve_index: shelve.Shelf
) -> Tuple[List[int], List[str], List[str]]:
    """
    conjunctive query over the built index
    return a list of matched document ids, a list of stop words and a list of unknown words separately
    :param query:
    :param shelve_index:
    :return:
    """
    # TODO:
    # Get tokens
    tokens,stops = text_processor.get_normalized_tokens("query",query)
    #get posting lists
    posting_lists = []
    not_found = set()
    inv_index = shelve_index
    for token in tokens:
        if token in inv_index:
            posting_lists.append(inv_index[token])
        else:
            not_found.add(token)
    #sorted(key=len) sorts the posting lists by their length
    return (intersection(sorted(posting_lists,key=len)),list(stops),list(not_found))


if __name__ == "__main__":
    pass
