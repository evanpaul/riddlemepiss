# from beautifulsoup4 import BeautifulSoup
from bs4 import BeautifulSoup
import urllib3
import time

def get_riddle_page_html(num):
    '''Capture the HTML from riddles.com'''
    url = 'https://riddles.com/' + str(num)
    response = http.request('GET', url)

    return BeautifulSoup(response.data, 'html.parser')

def get_text_from_css(soup, css_class):
    '''Grab text from specified CSS class. Structure is inconsistent'''
    grabbed_text = soup.select(css_class + " > p")
    if grabbed_text:
        grabbed_text = grabbed_text[0].text
    else: # The site switches how it structures these
        grabbed_text = soup.select(css_class)[0].text

    return grabbed_text

def parse_riddle(soup):
    '''Parse riddle and answer from captured HTML'''
    riddle_class = ".orange_dk_blockquote"
    answer_class = ".dark_purple_blockquote"

    riddle = get_text_from_css(soup, riddle_class).replace("\r\n", "")
    answer = get_text_from_css(soup, answer_class).replace("\r\n", "")

    return riddle, answer

def write_data(riddle, answer):
    '''Save riddles in case of connection issues and for convenience'''
    RIDDLE_FP.write(riddle + "\n")
    ANSWER_FP.write(answer + "\n")
    COMBINED_FP.write(riddle + " " + answer + "\n")

if __name__ == "__main__":
    http = urllib3.PoolManager()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    RIDDLE_FP = open("riddles.txt", "w")
    ANSWER_FP = open("answer.txt", "w")
    COMBINED_FP = open("combined.txt", "w")
    MISS_LIMIT = 25 # May need to be tweaked, haven't tested
    
    rid_num = 1
    misses = 0
    while misses < MISS_LIMIT: # Many consecutive misses is a sign we've probably hit the end
        soup = get_riddle_page_html(rid_num)
        exists = not bool(soup.select(".label-danger")) and not bool(soup.select(".headline"))
        
        if exists:
            riddle, answer = parse_riddle(soup)
            print("RIDDLE", rid_num)
            write_data(riddle, answer)

        else:
            print("RIDDLE", rid_num, "does not exist")

        rid_num += 1
        time.sleep(1) # Be kind to the site since it doesn't appear to have rate-limiting.
