from selenium import webdriver
import requests
from lxml import html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pymysql
import time



db = pymysql.connect(host="localhost",  # your host
                     user="root",       # username
                     passwd="root",     # password
                     db="scrapjob")   # name of the database

cur = db.cursor()
cur.execute("""SELECT COUNT(*) FROM information_schema.tables WHERE table_name='careersjob'""")
exists = cur.fetchone()[0]
if(exists == 0):
    cur.execute(
        "CREATE TABLE careersjob (company VARCHAR(255), job_url VARCHAR(255), job_title VARCHAR(255), job_location VARCHAR(255), job_des VARCHAR(255), job_dept VARCHAR(255), job_date VARCHAR(255))")
url = 'https://careers.enterprise.com/search-jobs'
# resp = requests.get(url)
driver = webdriver.PhantomJS(executable_path='/home/universe/PycharmProjects/phantomjs/bin/phantomjs',
                   service_log_path='/home/universe/PycharmProjects/phantomjs/ghostdriver.log')
driver.get(url)
c = 1
print("start")
time.sleep(5)
while True:

    time.sleep(3)
    tree_html = html.fromstring(driver.page_source)
    link_list =  tree_html.xpath("//div[@id='search-results-list']//li//a/@href")
    title_list = tree_html.xpath("//div[@id='search-results-list']//li//a//h2/text()")
    location_list = tree_html.xpath("//div[@id='search-results-list']//li//a//span/text()")
    pager_num = tree_html.xpath("//input[@id='pagination-current-bottom']/@max")
    for index, link in enumerate(link_list):
        if (title_list.find("Remote") != -1):
            cur.execute("INSERT INTO careersjob (job_url, job_title, job_location) VALUE (%s, %s, %s)", (link_list[index], title_list[index],location_list[index]))
            db.commit()
    if pager_num == c:
        break;
    c = c + 1;
    driver.find_element_by_xpath('//a[contains(@class, "next")]').click()
print("finish")
