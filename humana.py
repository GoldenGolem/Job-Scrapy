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
cur.execute("""SELECT COUNT(*) FROM information_schema.tables WHERE table_name='humanajob'""")
exists = cur.fetchone()[0]
if(exists == 0):
    cur.execute(
        "CREATE TABLE humanajob (company VARCHAR(255), job_url VARCHAR(255), job_title VARCHAR(255), job_location VARCHAR(255), job_des VARCHAR(255), job_dept VARCHAR(255), job_date VARCHAR(255))")
# cur.execute("CREATE TABLE humanajob (company VARCHAR(255), job_url VARCHAR(255), job_title VARCHAR(255), job_location VARCHAR(255), job_des VARCHAR(255), job_dept VARCHAR(255), job_date VARCHAR(255))")
url = 'https://humana.wd5.myworkdayjobs.com/humana_External_career_Site'
# resp = requests.get(url)
driver = webdriver.PhantomJS(executable_path='/home/universe/PycharmProjects/phantomjs/bin/phantomjs',
                   service_log_path='/home/universe/PycharmProjects/phantomjs/ghostdriver.log')
driver.get(url)
c = 1
print("start")
time.sleep(5)

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    tree_html = html.fromstring(driver.page_source)
    title_list =  tree_html.xpath("//li[@data-automation-id='compositeContainer']//div[@id='monikerList']//div[@data-automation-id='promptOption']/text()")
    length = tree_html.xpath("//span[@id='wd-FacetedSearchResultList-PaginationText-facetSearchResultList.newFacetSearch.Report_Entry']/text()")
    if(int(length[0].split(' ')[0]) <= len(title_list)):
        break;
date_location_list = tree_html.xpath("//span[@data-automation-id='compositeSubHeaderOne']/text()")
for index, title in enumerate(title_list):
    date_location = date_location_list[index];
    location = date_location.split('|')[0];
    location = location.split(',')[0]
    date = date_location.split('|')[2]
    if (title_list.find("Remote") != -1):
        cur.execute("INSERT INTO humanajob (job_title, job_location, job_date) VALUE (%s, %s, %s)",
                (title_list[index], location, date))
        db.commit()
print("finish")

