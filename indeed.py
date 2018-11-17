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
cur.execute("""SELECT COUNT(*) FROM information_schema.tables WHERE table_name='indeedjob'""")
exists = cur.fetchone()[0]
if(exists == 0):
    cur.execute(
        "CREATE TABLE indeedjob (company VARCHAR(255), job_url VARCHAR(255), job_title VARCHAR(255), job_location VARCHAR(255), job_des VARCHAR(255), job_dept VARCHAR(255), job_date VARCHAR(255))")
# cur.execute("CREATE TABLE humanajob (company VARCHAR(255), job_url VARCHAR(255), job_title VARCHAR(255), job_location VARCHAR(255), job_des VARCHAR(255), job_dept VARCHAR(255), job_date VARCHAR(255))")
url = 'https://www.indeed.com/jobs?q=100+Remote&l='
# resp = requests.get(url)
driver = webdriver.PhantomJS(executable_path='/home/universe/PycharmProjects/phantomjs/bin/phantomjs',
                   service_log_path='/home/universe/PycharmProjects/phantomjs/ghostdriver.log')

c = 0
print("start")


while True:
    url = 'https://www.indeed.com/jobs?q=100+Remote&start='+str((c*10))
    driver.get(url)
    time.sleep(2)
    tree_html = html.fromstring(driver.page_source)
    title_list =  tree_html.xpath("//div[contains(@class,'jobsearch-SerpJobCard')]//a[@data-tn-element='jobTitle']/@title")
    link_list = tree_html.xpath("//div[contains(@class,'jobsearch-SerpJobCard')]//a[@data-tn-element='jobTitle']/@href")
    company_list = tree_html.xpath("//div[contains(@class,'jobsearch-SerpJobCard')]//span[@class='company']/text()")
    location_list = tree_html.xpath(
        "//div[contains(@class,'jobsearch-SerpJobCard')]//*[@class='location']/text()")
    # date_list = tree_html.xpath(
    #     "//div[contains(@class,'jobsearch-SerpJobCard')]//*[@class='date']/text()")
    for index, title in enumerate(title_list):
        cur.execute("INSERT INTO indeedjob (job_title, job_location, company, job_url) VALUE (%s, %s, %s, %s)",
                    (title_list[index], location_list[index],company_list[index], link_list[index]))
        db.commit()
    c += 1
    if(c == 100):
        break
print("finish")

