from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import deque
from bs4 import BeautifulSoup
from datetime import date
import calendar
import csv

driver = webdriver.Chrome()
base_url = 'https://www.nytimes.com'
archive_dict = ['2016/01', '2016/02', '2016/03', '2016/04', '2016/05', '2016/06', '2016/07', '2016/08', '2016/09', '2016/10', '2016/11', '2016/12',
                '2017/01', '2017/02', '2017/03', '2017/04', '2017/05', '2017/06', '2017/07', '2017/08', '2017/09', '2017/10', '2017/11', '2017/12',
                '2018/01', '2018/02', '2018/03', '2018/04', '2018/05', '2018/06', '2018/07', '2018/08', '2018/09', '2018/10', '2018/11', '2018/12',
                '2019/01', '2019/02']
data = []

def nyt_login():
    driver.get('https://myaccount.nytimes.com/auth/login?URI=https%3A%2F%2Fwww.nytimes.com%2Fcrosswords%2Farchive')
    driver.find_element_by_id('username').send_keys('spine101@mac.com')
    driver.find_element_by_id ('password').send_keys('csidallas')
    driver.find_element_by_id('submitButton').click()

def get_day_of_week(puzzle_uri):
    year = int(puzzle_uri[23:27])
    month = int(puzzle_uri[28:30])
    day = int(puzzle_uri[31:33])
    return calendar.day_name[date(year, month, day).weekday()]

def get_last_row(csv_file):
    with open(csv_file, 'r') as f:
        try:
            lastrow = deque(csv.reader(f), 1)[0]
        except IndexError:  # empty file
            return None
        return lastrow[0]

date_last_pulled = get_last_row('xword_stats.csv')
nyt_login()
element = WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.ID, "TopAd")))
counter = 0

# Run if first time scraping
# while counter < 38:
#    driver.get('https://www.nytimes.com/crosswords/archive/daily/' + archive_dict[counter])
#    soup = BeautifulSoup(driver.page_source, 'html.parser')
#    for completed in soup.find_all('div', attrs={'class': 'index-hasGoldStar--2l2J1'}):
#        puz_uri = str(list(completed.children)[0])[43:76]
#        driver.get(base_url + puz_uri)
#        puz_soup = BeautifulSoup(driver.page_source, 'html.parser')
#        time_div = puz_soup.find('div', attrs={'class': 'timer-count'})
#        time = time_div.text.strip()
#        data.append((puz_uri, time))

#    counter += 1

# Run for subsequent scrapes
soup = BeautifulSoup(driver.page_source, 'html.parser')
for completed in soup.find_all('div', attrs={'class': 'index-hasGoldStar--2l2J1'}):
    puz_uri = str(list(completed.children)[0])[43:76]
    driver.get(base_url + puz_uri)
    puz_soup = BeautifulSoup(driver.page_source, 'html.parser')
    time_div = puz_soup.find('div', attrs={'class': 'timer-count'})
    time = time_div.text.strip()
    data.append((puz_uri, time))

with open('xword_stats.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    for puz_uri, time in data:
        if puz_uri[23:33] > date_last_pulled: # Comment out if first time scraping
            writer.writerow([puz_uri[23:33], get_day_of_week(puz_uri), time])
