"""Contains all functions for the Web Scraper Project on Jetbrains Academy"""
import json.decoder
import os
import re
import string

import requests

from bs4 import BeautifulSoup

# constant URL for step 4 + 5 of the project
nature_page_url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page="

# Step 1:
# Requirements:
# 1.    Send an HTTP request to a URL received from the user input.
# 2.    Print out the Quote content extracted from the json body response.
# 3.    Print out the Invalid quote resource! error message if there's no quote or something goes wrong.


def get_user_url():
    """
    Return a command prompt provided URL without validation(schema, response, etc.)

    :return: user provided URL without validation
    """
    print("Input the URL:")
    url = input()
    print()
    return url


def get_quote(url):
    """
    Return operation success and the content or a error message

    :param url: URL, which delivers a json answer with a content field
    :return: Tuple (bool, string) which contains the information about the success of the method
             and the requested content or an error message.
    """
    try:
        response = requests.get(url)
        # Status with #2xx or #3xx
        if response:
            return True, response.json()['content']
        return False, "Invalid quote resource!"
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
        return False, "Invalid URL"
    except (json.decoder.JSONDecodeError, KeyError):
        return False, "Invalid quote resource!"


def step_1():
    """
    Solution for step 1

    :return: None
    """
    _, message = get_quote(get_user_url())
    print(message)


# Step 2:
# Requirements:
# 1.    Feed your program a link to a movie or a TV series description. ex. https://www.imdb.com/title/tt0080684/
#       Only imdb-URLs with title in their path are valid
# 2.    Inspect the page and find out how the movie's or a series' title and description are stored in the source code.
# 3.    Download the webpage content, parse it using the beautifulsoup library,
#       and print out the movie's original title and description in a dictionary.
# 4.    Respond with "Invalid movie page!" if the the page doesn't have a description or isn't a imdb page.

def get_movie(url):
    """
    Return a dictionary with the title and description of the provided imdb movie/series page

    :param url: URL to an imdb movie or series webpage
    :return: True and a dictionary with the title and description or False and an error message
    """
    # Define error_return for reusability
    error_return = False, "Invalid movie page!"
    if "imdb" not in url or "title" not in url:
        return error_return
    try:
        # Accept-Language required by exercise
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        soup = BeautifulSoup(response.content, "html.parser")
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
        return error_return

    title = soup.find("title").text
    # get attribute content in the meta tag containing the description
    description = soup.find('meta', {'name': 'description'}).get("content")
    if description is None:
        return error_return
    return True, {"title": title, "description": description}


def step_2():
    """
    Solution for step 2

    :return: None
    """
    # Reuse get_user_url() from step 1
    _, content = get_movie(get_user_url())
    print(content)

# Step 3:
# Requirements:
# 1.    Create a program that retrieves the page's source code from a user input URL.
#       Please, don't decode the page's content.
# 2.    Save the page's content to the 'source.html' file. Please, write the file in binary mode.
# 3.    Print the Content saved. message if everything is OK (Don't forget to add a check for the status_code).
# 4.    If something is wrong, print the message The URL returned X, where X is the received error code.


def save_web_page(url, location="source.html"):
    """
    Saves the content of a web page as binary file

    :param url: URL for the web page
    :param location: save location/file_name
    :return: (True, None) for a successful execution or False with the response status of the web page
            for an invalid URL (False, "Invalid URL")
    """
    try:
        response = requests.get(url)
        if not response:
            return False, response.status_code
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
        return False, "Invalid URL"

    with open(location, "wb") as file:
        file.write(response.content)
        return True, None


def step_3():
    """
    Solution for step 3

    :return: None
    """
    success, message = save_web_page(get_user_url())
    if success:
        print("Content saved")
    else:
        print(f"The URL returned {message}!")

# Step 4:
# Requirements:
# 1.    Create a program that takes the https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3 URL
#       and then goes over the page source code searching for articles.
# 2.    Detect the article type and the link to view the article tags and their attributes.
# 3.    Save the contents of each article of the type "News", that is, the text from the article body without the tags,
#       to a separate file named %article_title%.txt. When saving the file, replace
#       the whitespaces in the name of the article with underscores and remove punctuation marks in the filename.
#       Also, strip all trailing whitespaces in the article body and title.


def generate_file_name(title):
    """
    Generates a file name for a nature title

    :param title: Title string
    :return: File name as string
    """
    title = title.strip()
    # Replaces white spaces with underscores and removes all punctuation
    translation_table = title.maketrans(" ", "_", string.punctuation)
    return title.translate(translation_table) + ".txt"


def get_nature_article_content(url):
    """
    Fetches the text content from an article on nature.com

    :param url: URL to a nature article
    :return: Written content of the article without tags
    """
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    # use .text.strip() for the body of the article, otherwise the tests will fail.
    return soup.find("div", attrs={"class": re.compile(".*article.*body")}).text.strip()


def write_text_file(content, destination, mode="wb"):
    """
    (Over-)Writes a binary UTF-8 encoded file

    Mode "wb" was given by the exercise, mode as parameter could lead to errors and should be improved or removed

    :param content: content to be saved
    :param destination: save file location
    :param mode: write mode [default="wb"]
    :return: None
    """
    with open(destination, mode=mode) as file:
        file.write(content.encode("UTF-8"))


def step_4():
    """
    Solution for step 4

    :return: None
    """
    # previous code rewritten for step 5
    save_nature_articles(1, "News", starting_page=3, gen_dirs=False)

# Step 5:
# Requirements:
# 1.    Improve your code so that the function can take two parameters from the user input:
#       the number of pages (an integer) and the type of articles (a string). The integer with the number of pages
#       specifies the number of pages on which the program should look for the articles.
# 2.    Go back to the https://www.nature.com/nature/articles?sort=PubDate&year=2020 website
#       and find out how to navigate between the pages with the requests module changing the URL.
# 3.    Create a directory named Page_N (where N is the page number corresponding to the number input by the user)
#       for each page.
#       Search and collect all articles page by page; filter all the articles by the article type
#       and put all the articles that are found on the page with the matched type to the directory Page_N.
#       Mind that when the user enters some number, for example, 4, the program should search all pages
#       up to that number and the respective folders (Folder 1, Folder 2, Folder 3, Folder 4) should be created.
#       Mind also that in articles of different types the content is contained in different tags.
# 5.    Save the articles to separate *.txt files. Keep the same processing of the titles for the filenames
#       as in the previous stage. You can give users some feedback on completion, but it is not required.


# starting_page and gen_dirs for compatibility with step 4
def save_nature_articles(num_pages, article_type, starting_page=1, gen_dirs=True):
    """
    Find and save articles from nature.com with a specific article type on a specific amount of pages.

    :param num_pages: Number of pages to be read
    :param article_type: Requested article type as string
    :param starting_page: First page to be searched
    :param gen_dirs: Boolean value whether to create directories for the search results
    :return: None
    """
    for page_number in range(starting_page, num_pages + starting_page):
        dir_name = "Page_" + str(page_number)
        if gen_dirs and not os.access(dir_name, os.F_OK):
            os.mkdir(dir_name)

        soup = BeautifulSoup(requests.get(nature_page_url + str(page_number)).content, "html.parser")
        articles = soup.findAll("article")
        for article in articles:
            # Filter articles for the requested type
            if article.find("span", attrs={"class": "c-meta__type"}).text == article_type:
                hyperref = article.find("a", attrs={"data-track-action": "view article"})
                file_name = generate_file_name(hyperref.text)
                if gen_dirs:
                    file_name = dir_name + "/" + file_name
                content = get_nature_article_content("https://www.nature.com" + hyperref.get("href"))
                write_text_file(content, file_name)


def step_5():
    """
    Solution for step 5

    :return: None
    """
    num_pages = int(input())
    article_type = input()
    save_nature_articles(num_pages, article_type)


if __name__ == "__main__":
    # Main routine to call the different steps
    # step_1()
    # step_2()
    # step_3()
    # step_4()
    step_5()
