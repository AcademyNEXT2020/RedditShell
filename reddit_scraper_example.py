# ---------------------------------------------------------------------------------------
# Package Imports
# (1) TODO: Install the "requests" package through the command line ("pip install requests")
# ---------------------------------------------------------------------------------------
import requests
from datetime import datetime
import os
import sys


# ---------------------------------------------------------------------------------------
# "multireddit" function that creates API calls for each subreddit in the string
# ---------------------------------------------------------------------------------------
def multireddit(subreddits, user, limit=5, orderby='score'):

    # Header information - Reddit username
    headers = {'user-agent': 'reddit-{}'.format(user)}


    ''' Displays an HTML listing of the top `limit` articles from the
    various `subreddits` specified by the user.  These articles will be
    sorted by the field specified by `orderby`

      - `subreddits` is a comma-separated list of subreddits (ie.
        `linux,linuxmasterrace`)

      - `orderby` is any field in the Reddit JSON data for a particular
        article (ie. `score`, `title`, `created_utc`, etc.)
    '''

    # Process function arguments
    # (2) TODO: split the string into a list, delimited by commas
    # Hint: you can use a loop OR a list comprehension. 
    # Hint: you'll want to call the .strip() method on each string to remove trailing whitespace




    # Create a list to hold URLs (API calls) and articles (within a given subreddit)
    urls = []
    articles = []
    for item in subreddits:
        URL = 'https://www.reddit.com/r/' + item + '/.json'
        urls.append(URL)
        #print(URL)

    # Fetch subreddit data
    for url in urls:
        # (3) TODO: use the "requests.get" method to make an API call
        # Hint: use the parameters "params" and "headers" after the URL
        
        # (4) TODO: retrieve the response as JSON format using the .json() method
        


        # access dictionary elements based on key
        subdata = data['data']
        children = subdata['children']
        #       print(type(children))
        for child in children:
            #            print('\n')
            childData = child['data']
            articles.append(child['data'])

    # Sort and limit data, and construct HTML results
    index = 0  # keep track of article number
    html = '<table><tbody>'
    for article in sorted(articles, reverse=True, key=lambda a: a[orderby])[:limit]:
        index += 1
        LN = article['url']  # link to article

        cmLN = 'https://www.reddit.com/'
        # (5) TODO: create a comment link using the article dictionary with key 'permalink'
        # your line should look like: cmLN += YOUR CODE HERE

      
        html += f'''
        <tr>
            <td>{str(index) + '.'}</td>
            <td style="text-align: left"><a href="{LN}">{article['title']}</td>
            <td style="text-align: right">Score: {article['score']}</td>
            <td><a href="{cmLN}">Comments</td>
        </tr>'''
    return html


if __name__ == '__main__':
    # GET COMMAND LINE SUBREDDITS
    if len(sys.argv)==1:
        print('Please enter one or more subreddits as command line arguments (separated with spaces)')
        exit()
    subs = ''

    # (6) TODO: use "sys.arv" to parse command-line arguments as space-separated strings
    # Hint: you'll want to construct one string with all of the subreddits, and store in the variable "subs"
    # Hint: use a loop (2 lines of code) or a list comprehension (1 line of code)!
    for sub in sys.argv[1:]:
        subs = subs + sub + ' '


    # DEFINE PROGRAM PARAMETERS
    NEW_PAGE_NAME = 'reddit_' + ('_'.join(item for item in str(datetime.now()).split(' '))).replace(':', '_').replace('.', '_') + '.html'
    USER = 'AcademyNEXT2020'
    ORDERBY = 'score'
    SUBREDDITS = subs

    # CALL "MULTIREDDIT" AND RETURN HTML-FORMATTED DATA
    generated_html = multireddit(SUBREDDITS, USER, limit=100, orderby=ORDERBY)

    # SAVE HTML WEB PAGE (default is current working directory based on user's operating system parameters)
    with open(os.path.join(sys.path[0], NEW_PAGE_NAME), "w+") as f:
        if f.write(generated_html):
            print('\nSuccessfully wrote ' + NEW_PAGE_NAME + ' to ' + sys.path[0] + '\n')
        else:
            print('Error: could not write file to ' + sys.path[0])


