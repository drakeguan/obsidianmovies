import importlib
import multiprocessing
import pickle

import pandas as pd
from pqdm.processes import pqdm
# If you want threads instead:
# from pqdm.threads import pqdm

import utils

def main():
    # Import a list of movie names to search
    to_search = pd.read_csv('movies_to_search.md', sep='\t')

    # query to IMDB to fill up the csv
    my_search = to_search['Movies'].tolist()
    results = pqdm(my_search, movie_search, n_jobs=multiprocessing.cpu_count())
    myresults = pd.DataFrame(results)

    # Save a copy of myresults
    myresults.to_pickle('download_results.pkl')
    myresults.to_csv('myresult.csv')

    ## OPTION1: CREATING INDIVIDUAL MARKDOWN FILES
    # Create small markdown pages
    create_markdown_page(myresults)

    ## OPTION 2: CREATE A MAIN MARKDOWN PAGE
    # Add obsidian links to the title
    myresults['title'] = '[['+myresults['title']+']]'

    ## OPTION 3: FILTER OUT JUST THE FACTS
    facts = ['title', 'year', 'rating','genre', 'country', 'director', 'cast']
    simpleresults = myresults[facts]

    ## SAVE OUT AS TEXT
    with open('movie_main.txt','w') as file_out:
        simpleresults.to_markdown(buf=file_out)

if __name__ == '__main__':
    # %load_ext autoreload
    # %autoreload 2
    importlib.reload(utils)
    from utils import movie_search, create_markdown_page

    main()
