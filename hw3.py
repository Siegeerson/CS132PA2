from pathlib import Path
import argparse,shelve,time
from dbm import error as dberror#specific error codes for database loading
from flask import Flask, render_template, request, Markup, flash
from utils import load_wapo,timer
from inverted_index import build_inverted_index, query_inverted_index

app = Flask(__name__)
app.secret_key = str(time.time())  #set secret key

#GLOBALS
data_dir = Path("pa3_data")
wapo_path = str(data_dir.joinpath("wapo_pa3.jl"))
shelf_path = str(data_dir.joinpath("WAPO_CORPUS"))
# Will house shelves
WAPO_SHELF = None
INDEX_SHELF = None
QUERY_SHELF = None

def shelve_wapo(wapo_path,shelf_path):
    """
    Function to shelve wapo corpus for use, called when built
    """
    wapo_dict = {str(doc["id"]):doc for doc in load_wapo(wapo_path)}
    with shelve.open(str(shelf_path)) as wapo_s:
        wapo_s.update(wapo_dict)
# home page
@app.route("/")
def home():
    return render_template("home.html")


# result page
@app.route("/results", methods=["POST"])
def results():
    text = request.form["query"]
    query_text = text
    result = query_inverted_index(query_text[:],INDEX_SHELF)
    # Store results in cookie to enable page navigation
    # Not as shelf --> queries are personal data
    QUERY_SHELF[query_text] = result[0]
    matches = []
    for doc_id in result[0]:
        doc = WAPO_SHELF[str(doc_id)]
        # NOTE: I dont escape the snipit because it causes issues with unfinished html tags
        snipit = doc["content_str"][:150]
        # add match to match results
        matches.append((doc["title"],doc_id,snipit))
    # message flashing for required prompts, only appear after search
    # will not reappear after page navigation
    if matches:
        flash(f"found {len(matches)} matches")
    if result[1]:
        flash(f"stop word(s) {result[1]} removed")
    if result[2]:
        flash(f"words {result[2]} not found in corpus")
    # TODO: possibly clean up template params
    return render_template("results.html",matches=matches[:min(8,len(matches))],page=1,prev=0,query=text,maxpages=len(matches)/8)  # add variables as you wish


# "next page" to show more results
@app.route("/results/<int:page_id>", methods=["POST"])
def next_page(page_id):
    # NOTE:
    query_text = request.form["query"]
    if query_text in QUERY_SHELF:
        print("Query found in session")
        result_ids = QUERY_SHELF[query_text]
    else:
        print("Query not found in session")
        result = query_inverted_index(query_text,INDEX_SHELF)
        result_ids = result[0]
    matches = []
    for doc_id in result_ids:
        doc = WAPO_SHELF[str(doc_id)]
        # NOTE: I dont escape the snipit because it causes issues with unfinished html tags
        snipit = doc["content_str"][:150]
        # add match to match results
        matches.append((doc["title"],doc_id,snipit))
    return render_template("results.html",matches=matches[8*page_id:min(8*(page_id+1),len(matches))],page=page_id+1,prev=page_id-1,query=query_text,maxpages=len(matches)/8)

# document page
@app.route("/doc_data/<int:doc_id>")
def doc_data(doc_id):
    # TODO:
    return render_template("doc.html",doc=WAPO_SHELF[str(doc_id)],text=Markup(WAPO_SHELF[str(doc_id)]["content_str"]))


if __name__ == "__main__":
    """
        I am using sessions to store results for navigating pages
        this is done over just putting query results in a shelf simply because
        the stored results are deleted after the browser is closed and thus
        are less permanent
    """
    parser = argparse.ArgumentParser(description="Boolean IR system")
    parser.add_argument("--build")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    print(args)
    if args.test:
        wapo_path = data_dir.joinpath("test_corpus.jl")
        # print("TEST")

    if args.build:
        build_inverted_index(
            wapo_path, str(data_dir.joinpath(args.build))
        )  # shelve.open cannot recognize Path
        shelve_wapo(
            wapo_path, shelf_path
        )
    if args.run:
        # Use context managers for safe open and close
        with shelve.open(shelf_path,flag='r') as wapo:
            # Name full inverted index FULL
            with shelve.open(str(data_dir.joinpath("FULL")),flag='r') as index:
                with shelve.open(str(data_dir.joinpath("QUERY")),flag='n') as query:
                    WAPO_SHELF = wapo
                    INDEX_SHELF = index
                    QUERY_SHELF = query
                    app.run(debug=True, port=5000)
