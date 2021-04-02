#Names: Chris Hudson, Ethan Perlmutter

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    #Get titles code start
    with open(filename) as a:
        soup = BeautifulSoup(a, 'html.parser')
    
    #For books and authors
    bk = soup.find_all('a', class_='bookTitle')
    bk_lst = []
    athr_nme = soup.find_all('a', class_='authorName')
    nme_lst = []
    
    #For loops
    for b in bk:
        bk_lst.append(b.text.strip())
    for b in athr_nme:
        nme_lst.append(b.text.strip())
    
    #Return statement - commenting out code for part 1
    return list(zip(bk_lst, nme_lst))
    
    #Get titles from results completion

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    #Parser/retrieve object creation
    web_link = requests.get('https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc')
    soup = BeautifulSoup(web_link.text, 'html.parser')
    
    #Adding URL/link to new list
    bks = soup.find_all('tr')
    link_lst = []

    #For loop and return created list
    for b in bks:
        c = b.find('a')
        complete = c['href']
        url = "https://goodreads.com" + str(complete)
    link_lst.append(url)
    return link_lst[:10]
   
   #Get search part completion

def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    #Get book summary through url
    web_link = requests.get(book_url)
    soup = BeautifulSoup(web_link.text, 'html.parser')

    #Capture book title and info (header of pages)
    bk_title = soup.find('h1').text
    athr = soup.find('a', class_='authorName').text
    web_pgs = soup.find('span', itemprop = 'numberOfPages').text
    web_pgs = web_pgs.strip()
    web_pgs = web_pgs[:-5]

    #Return book, title, page number
    return (str(bk_title.strip()), str(athr), int(web_pgs))

    #Get book search completion


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    #Summarize best book function list creation
    file_1 = filepath
    
    #Open file/close file
    d = open(file_1)
    soup = BeautifulSoup(d.read(), 'html.parser')
    d.close()

    #List category creation
    anc = soup.find_all('div', class_='category clearFix')
    total_lst = []

    #For loop progression (displayed is variable progression through alphabet)
    for b in anc:
        e = b.find('a')
        f = b.find('img', class_='category__winnerImage')
        bk_ctg = e.find('h4').text
        bk_html = e['href']
        bk_title = f['alt']

        total_lst.append((str(bk_ctg.strip()), str(bk_html), str(bk_title)))

    #Return total_lst and three elements within it
    return total_lst

    #Summarize best book section completion
def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    #Take list of tuples, write and save to file
    with open(filename, 'w', newline = '') as file:
        f_write = csv.writer(file)
        f_write.writerow(["Book Title", "Author Name"])
        for b in data:
            f_write.writerow(b)
    
    #Completed csv section

def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        l_var = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(l_var), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(l_var), list)
        # check that each item in the list is a tuple
        for b in l_var:
            self.assertEqual(type(b), tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(l_var[0], ("Harry Potter and the Deathly Hallows (Harry Potter, #7)", "J.K. Rowling"))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(l_var[-1], ("Harry Potter: The Prequel (Harry Potter, #0.5)", "Julian Harrison"))
    
    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 1)

        # check that each URL in the TestCases.search_urls is a string
        for b in TestCases.search_urls:
            self.assertEqual(type(b), str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
            self.assertTrue('https://goodreads.com/book/show/' in b)

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        b_sum = []
        # for each URL in TestCases.search_urls (should be a list of tuples)
        for b in get_search_links():
            b_sum.append(get_book_summary(b))
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(b_sum), 1)
            # check that each item in the list is a tuple
        for b in b_sum:
            self.assertEqual(type(b), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(b), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(b[0]), str)
            self.assertEqual(type(b[1]), str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(b[2]), int)
            # check that the first book in the search has 337 pages
        self.assertEqual(b_sum[0][2], 274)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        l_var = summarize_best_books('best_books_2020.htm')
        # check that we have the right number of best books (20)
        self.assertEqual(len(l_var), 20)
            # assert each item in the list of best books is a tuple
        for b in l_var:
            # check that each tuple has a length of 3
            self.assertEqual(type(b), tuple)
            self.assertEqual(len(b), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(l_var[0], ('Fiction', 'https://www.goodreads.com/choiceawards/best-fiction-books-2020', "The Midnight Library"))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(l_var[-1], ('Picture Books', 'https://www.goodreads.com/choiceawards/best-picture-books-2020', "Antiracist Baby"))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        l_var = get_titles_from_search_results("search_results.htm")
        # call write csv on the variable you saved and 'test.csv'
        write_csv(l_var, 'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        
        with open('test.csv', newline='') as var1:
            r_csv = csv.reader(var1)
            csv_l = list(r_csv)
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_l), 21)
        # check that the header row is correct
        self.assertEqual(csv_l[0], ['Book Title', 'Author Name'])
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_l[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)' , 'J.K. Rowling'])
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_l[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)' , 'Julian Harrison']) 


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



