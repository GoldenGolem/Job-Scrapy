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
cur.execute("""SELECT COUNT(*) FROM information_schema.tables WHERE table_name='accenturejob'""")
exists = cur.fetchone()[0]
if(exists == 0):
    cur.execute(
        "CREATE TABLE accenturejob (company VARCHAR(255), job_url VARCHAR(255), job_title VARCHAR(255), job_location VARCHAR(255), job_des VARCHAR(255), job_dept VARCHAR(255), job_date VARCHAR(255))")
# cur.execute("CREATE TABLE accenturejob (company VARCHAR(255), job_url VARCHAR(255), job_title VARCHAR(255), job_location VARCHAR(255), job_des VARCHAR(255), job_dept VARCHAR(255), job_date VARCHAR(255))")
url = 'https://www.accenture.com/us-en/careers/jobsearch'
# resp = requests.get(url)
driver = webdriver.PhantomJS(executable_path='/home/universe/PycharmProjects/phantomjs/bin/phantomjs',
                   service_log_path='/home/universe/PycharmProjects/phantomjs/ghostdriver.log')
driver.get(url)
c = 1
print("start")
time.sleep(8)

while True:
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element_by_id('load-more').click()

    time.sleep(5)


    tree_html = html.fromstring(driver.page_source)
    title_list =  tree_html.xpath("//div[@id='job-seach-results']//div[contains(@class,'job')]//a[@class='job-title']/text()")
    length = tree_html.xpath("//span[contains(@class,'total-jobs-count')]/text()")

    if(int(length[0][1:-1]) <= len(title_list)):
        break;
link_list =  tree_html.xpath("//div[@id='job-seach-results']//div[contains(@class,'job')]//a[@class='job-title']/href()")
location_list =  tree_html.xpath("//div[@id='job-seach-results']//div[contains(@class,'job')]//a[@class='loc']/text()")
date_list =  tree_html.xpath("//div[@id='job-seach-results']//div[contains(@class,'job')]//p[@class='job-post-date']/text()")

for index, title in enumerate(title_list):
    if (title_list.find("Remote") != -1):
        cur.execute("INSERT INTO accenturejob (job_title,job_link, job_location, job_date) VALUE (%s, %s, %s, %s)",
                (title_list[index], link_list[index], location_list[index], date_list[index]))
        db.commit()
print("finish")

