# Jo and Ju project

## Description of folders and files

* `Notebooks`        - contains all the Jupyter Notebooks
* `data`             - contains all the `.csv` files
* `pictures`         - contains useful pictures
* `scripts`          - contains python code for GitHub workflows
* `startupjh`        - actual Python package
* `tests`            - contains tests to be performed on the package 
* `.gitignore`       - contains all the file and folder names to be ignored by git when committing/pushing
* `Makefile`         - contains make commands (e.g. make tests)
* `requirements.txt` - list of required python packages for the package to be installed and run
* `setup.py`         - Python code that installs and sets up the package

## Description of `startupjh`

**Prefer using `serpapi.py` over `scraperapi.py` for data collection**

### `serpapi.py`

Python script containing 4 methods:

(1) `get_user_input()` - asks user for a search input

(2) `serpapi_og_results()` - scrapes Google Scholar organic results using SerpAPI
                             output - dataframe with following columns: 
                             paper_id, title, result_id, link, snippet, resources_title,
                             resources_link, citation_count, cites_id, versions, cluster_id
                                              
(3) `serpapi_full_cite(df)` - scrapes the full MLA citation from Google Scholar by iterating on the `df["result_id"]`
                              input: the Pandas dataframe generated by `serpapi_og_results()`
                              output: same dataframe as input but with an extra `full_citation` column
    
(4) `serpapi_cited_by_list(df)` - iterates on `df["cites_id"]` to scrape the list of papers citing each paper in `df`
                                  input: dataframe generated by `serpapi_og_results()`
                                  output: new dataframe of citing papers with citing_paper_id corresponging to paper_id if `df`

### `data_preprocess.py`

Python script containing the methods used to preprocess the data collected from `serpapi.py`or `scraperapi-py`

(1) `extract_key_words(df)` - method to extract key words from paper titles
                              input - dataframe that MUST have a `["title"]` column 
                              output - dataframe with an extra `["key_words"]` column

(2) `extract_pub_info(df)` - method to extract author(s), year, and pub_info from full_citation
                             input - dataframe that MUST have a `["full_citation"]` column
                                     only works for primaryResults - will be updated for citingPapers
                             output - dataframe with three extra columns `["authors", "pub_info", "year"]`
