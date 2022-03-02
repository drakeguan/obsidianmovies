This repo was forked from https://github.com/wjivan/obsidianmovies.
So if you like to check out the initial idea and codebase, go check [Wen Jian](https://github.com/wjivan/obsidianmovies) there :)

# Motivation
[Obsidian](https://obsidian.md/) is a great note-taking and productivity tool. One area I want to log and review are movies.
When I sat down and listed all my favourite movies, it came down to a list of more than 100 movies!
Trying to search through the cast and directors for all these movies is time consuming and I just want to get a quick summary of the movie before trying to write my own thoughts on them. So I decided to use Python to automate this for me. 

# Requirements
You need to install Python and its required packages for this to work. 
Python 3 and [Pipenv](https://pipenv.pypa.io/en/latest/) are assumed to be installed (or just Pipenv might be enough).

```shell
pipenv install
```

# How this works
1. Input all the movies to search into the csv `movies_to_search.md`. 
2. The script makes use of the [`Cinemagoer` package](https://cinemagoer.github.io/) to download the metadata from IMDB. 
This does not require you to have an IMDB api account. You can check out their documentations on what data is available to adjust as required. 
I created a function that allows me to down the information regarding:
- title
- plot
- genre
- country
- cover url
- director
- kind
- rating
- synopsis
- year
3. Obsidian reads markdown pages so I automate the creation of markdown pages using python using [mdutils](https://pypi.org/project/mdutils/). 
I create a function to automate the creation of a standard template filled in with the new metadata:
4. You can drag and drop these newly created markdown sheets into Obsidian. 
