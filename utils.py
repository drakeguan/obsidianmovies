import re
import unicodedata

from imdb import Cinemagoer
from mdutils.mdutils import MdUtils

# Maximum file name length of 255 characters for Mac: 255
# Make it 250 here for the extension part.
char_limit = 250

def clean_filename(filename, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.

    ref:
      - https://github.com/django/django/blob/main/django/utils/text.py
      - https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8
      - https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    """
    value = str(filename)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    
    value = re.sub(r"[^\w\s-]", "", value.lower())
    value = re.sub(r"[-\s]+", "-", value).strip("-_")

    if len(value)>char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return value[:char_limit]


# Write a function to get intended results given a movie title
def movie_search(my_title):
    """
    Given a string (movie title), find the metadata for that movie (or the closest
    one matching that name).

    Parameters
    ----------
    my_title : string

    returns a dictionary of metadata
    """
    # create a dictionary to store data
    information = dict()

    # create an instance of the IMDb class
    ia = Cinemagoer()

    # search for a movie
    lookups = ia.search_movie(my_title)

    # use the first search result to return the id
    try:
        # Test if any movies are found
        movie_id = lookups[0].movieID

        # get a movie
        movie = ia.get_movie(movie_id, info=('main', 'plot', 'akas'))

        # RETRIEVE DATA
        # Get the movie title searched for
        t = movie['title']
        information['title'] = t
        print(f'Retrieving data for {t}')

        # Get the title name in Taiwan
        try:
            information['ctitle'] = [string for string in movie['akas'] if string.endswith('Taiwan')][0][:-7]
        except:
            print('Title name in Taiwan not available')
            information['ctitle'] = ''

        # Get the plot outline
        try:
            information['plot'] = movie['plot outline']
        except:
            print('plot outline not available')
            try:
                information['plot'] = movie['plot'][0]
            except:
                print('plot also not available')
                information['plot'] = ''

        # Get the genre
        try:
            information['genre'] = ','.join(movie['genre'])
        except:
            print('no information on genre')
            information['genre'] = ''

        # Get the country
        try:
            information['country'] = ','.join(movie['countries'])
        except:
            print('no information on country')
            information['country'] = ''

        # Get the director
        # Extract the names in each Person object
        try:
            director_names = [d['name'] for d in movie['directors']]
            information['director'] = ','.join(director_names)
        except:
            print('director information not available')
            information['director'] = ''

        # Get the cast
        # Extract the top 5 names in cast (if it exists)
        try:
            cast_names = [d['name'] for d in movie['cast']]
            if len(cast_names) >5:
                cast_names = cast_names[0:5]
            information['cast'] = ','.join(cast_names)
        except:
            print('No information on cast')
            information['cast'] = ''
        
        # Get the rating
        try:
            information['rating'] = movie['rating']
        except:
            print('rating info is not available')
            information['rating'] = 'N/A'

        # Get the year
        try:
            information['year'] = movie['year']
        except:
            print('no information on year')
            information['year'] = ''

        # Get the type
        try:
            information['kind'] = movie['kind']
        except:
            print('type not available')
            information['kind'] = ''

        # Get the cover url
        try:
            information['cover url'] = movie['cover url']
        except:
            print('cover url not available')
            information['cover url'] = ''

        # Get sypnosis
        try:
            information['synopsis'] = movie['synopsis'][0]
        except:
            print('no synopsis')
            information['synopsis'] = ''
    except:
        print('NO RESULTS FOUND FOR {my_title}')
        information['title'] = my_title
        information['plot'] = ''
        information['genre'] = ''
        information['country'] = ''
        information['cover url'] = ''
        information['director'] = ''
        information['kind'] = ''
        information['rating'] = ''
        information['synopsis'] = ''
        information['year'] = ''

    return(information)

# Write a function to make a markdown page filled with information retrieved
def create_markdown_page(myresults):
    """
    Given a dataframe containing all the information about movies, 
    we can create individual pages

    Parameters
    ----------
    myresults : DataFrame
        Contains essential headers: title, year, rating, genre, country, director
        cast, synopsis and plot
    """
    # Create iterations
    for index, row in myresults.iterrows():
        # Create a file
        mdFile = MdUtils(file_name='notes/'+clean_filename(row['title']))
        mdFile.title = ''

        # Create a metadata section
        mdFile.write(text='---\n')
        mdFile.write(text='type: movie\n')
        facts = ['title', 'ctitle', 'year', 'rating','genre', 'country', 'director', 'cast', 'cover url']
        for f in facts:
            if f == 'cover url':
                mdFile.write(text='cover: ' + row[f] + '\n', wrap_width=0)
            elif f == 'title':
                mdFile.write(text='title: "' + row[f] + '"\n', wrap_width=0)
            elif f == 'ctitle':
                mdFile.write(text='ctitle: "' + row[f] + '"\n', wrap_width=0)
                mdFile.write(text='aliases: "' + row[f] + '"\n', wrap_width=0)
            else:
                mdFile.write(text=f'{f}: {row[f]}\n')
        mdFile.write(text='---\n')

        # Create a title
        mdFile.new_header(level=1, title=row['title'])

        # Create a Taiwanese title
        mdFile.new_header(level=1, title=row['ctitle'])

        # Create a cover
        # i could use new_inline_image but the text wraps at 20 characters
        # creating a break. Hence, I code my own image line and unwrap it
        cover_link = '!['+ row['title'] + '](' + row['cover url'] + ')'
        mdFile.new_line(text = cover_link, wrap_width=0)
        mdFile.write(text='\n')

        # Create a section for the plot
        mdFile.new_header(level=2, title="Plot")

        # Clean up plot text
        plot_text = row['plot']
        plot_text = ' '.join(plot_text.split())
        plot_text = plot_text.replace('\ ','')
        mdFile.new_line(text=plot_text, wrap_width=0)
        mdFile.write(text='\n')

        # Create my own review section
        mdFile.new_header(level=2, title="My own thoughts")

        # Create markdown
        mdFile.create_md_file()
