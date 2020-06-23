# Gleb Koval's Reddit scrapper
#
# This does not use the example file
# I tried making it in a function programming style
# because I like it more than object-oriented
# and am currently trying to switch to it

def combine_arrays(*arrays):
    target = []
    for array in arrays:
        target += array
    return target

def subreddit_to_api_url(subreddit):
    return f"https://www.reddit.com/r/{subreddit}/.json"

def get_reddit_headers(user):
    return {"user-agent": f"reddit-{user}"}

def get_subreddit_data(subreddit_api_url, headers, params={}):
    import requests

    return requests.get(
        url = subreddit_api_url,
        params = params,
        headers = headers
    ).json()["data"]

def get_subreddit_articles(subreddit_data):
    return [ article["data"] for article in subreddit_data["children"] ]

def sort_subreddit_articles(subreddit_articles, order_by, limit):
    return sorted(subreddit_articles, reverse=True, key=lambda article: article[order_by])[:limit]

def get_subreddit_article_comments_url(subreddit_article):
    return f"https://www.reddit.com/{subreddit_article['permalink']}"

def generate_articles_html(subreddit_articles):
    return "".join([
        f"""
        <tr>
            <td>{index}.</td>
            <td style="text-align: left"><a href="{article["url"]}">{article["title"]}</a></td>
            <td style="text-align: right">Score: {article["score"]}</td>
            <td><a href="{get_subreddit_article_comments_url(article)}">Comments</a></td>
        </tr>
        """
        for (index, article) in enumerate(subreddit_articles)
    ])

def save_html_file(filename, content):
    import os, sys

    with open(os.path.join(sys.path[0], filename), "w+") as html_file:
        html_file.write(content)

def create_html_file(page_name, html):
    save_html_file(page_name+".html",
        f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>{page_name}</title>
            </head>
            <body>
                <table>
                    <tbody>
                        {html}
                    </tbody>
                </table>
            </body>
        </html>
        """
    )

def main():
    import sys
    from datetime import datetime

    if len(sys.argv)==1:
        print('Please enter one or more subreddits as command line arguments (separated with spaces)')
        return

    page_name = 'reddit_' + ('_'.join(item for item in str(datetime.now()).split(' '))).replace(':', '_').replace('.', '_')
    user = "AcademyNEXT2020"
    order_by = "score"
    limit = 5
    subreddits = sys.argv[1:]

    print("Subreddit(s):", ", ".join(subreddits))

    headers = get_reddit_headers(user)
    subreddit_api_urls = [ subreddit_to_api_url(subreddit) for subreddit in subreddits ]
    subreddit_datas = [ get_subreddit_data(subreddit_api_url, headers) for subreddit_api_url in subreddit_api_urls ]
    subreddit_articles = sort_subreddit_articles(combine_arrays(
        *[
            get_subreddit_articles(subreddit_data)
            for subreddit_data in subreddit_datas
        ]
    ), order_by, limit)
    articles_html = generate_articles_html(subreddit_articles)
    create_html_file(page_name, articles_html)

    print(f"Created {page_name}.html")

if __name__ == "__main__":
    main()