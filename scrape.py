# from beautifulsoup4 import BeautifulSoup
from bs4 import BeautifulSoup
import urllib3
import time

def get_riddle_page(num):
    url = 'https://riddles.com/' + str(num)
    response = http.request('GET', url)

    return BeautifulSoup(response.data, 'html.parser')

def parse_riddle(soup):
    riddle = soup.select(".orange_dk_blockquote > p")
    if riddle:
        riddle = riddle[0].text
    else: # Okay yeah let's just change structure for no reason
        riddle = soup.select(".orange_dk_blockquote")[0].text

    answer = soup.select(".dark_purple_blockquote > p")
    if answer:
        answer = answer[0].text
    else:
        answer = soup.select(".dark_purple_blockquote")[0].text

    return riddle.replace("\r\n", ""), answer.replace("\r\n", "")

def write_data(riddle, answer):
    RIDDLE_F.write(riddle + "\n")
    ANSWER_F.write(answer + "\n")
    COMBINED_F.write(riddle + " " + answer + "\n")


http = urllib3.PoolManager()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

RIDDLE_F = open("riddles_3.txt", "w")
ANSWER_F = open("answers_3.txt", "w")
COMBINED_F = open("combined_3.txt", "w")

rid_num = 1
while True:
    soup = get_riddle_page(rid_num)
    exists = not bool(soup.select(".label-danger")) and not bool(soup.select(".headline"))
    
    if exists:
        riddle, answer = parse_riddle(soup)
        print("RIDDLE", rid_num)
        write_data(riddle, answer)

    else:
        print("RIDDLE", rid_num, "does not exist")

    rid_num += 1
    # time.sleep(0.5)
    # break