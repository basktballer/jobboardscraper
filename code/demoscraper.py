import requests
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import psycopg2
from psycopg2 import Error


URL = "https://ca.indeed.com/jobs?q=developer&l=Toronto%2C+ON"


firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference("headless.privatebrowsing.autostart", True)

# run firefox webdriver from executable path of your choice
# driver = webdriver.Firefox()
driver = webdriver.Firefox(firefox_profile=firefox_profile)
driver.get(URL)
# execute script to scroll down the page
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
# sleep for 30s
time.sleep(1)

soup = BeautifulSoup(driver.page_source, "html.parser")

def extract_posting_id(soup):
  ids = []
  divs = soup.findAll("div", attrs={"class": "jobsearch-SerpJobCard"})
  for div in divs:
    ids.append(div.get("data-jk"))
  return(ids)

# postingIDs = extract_posting_id(soup)
# print(postingIDs)
# print(len(postingIDs))

# for pID in postingIDs:
#   items = []
#   python_button = driver.find_element_by_xpath(f"//div[@data-jk='{pID}']")
#   python_button.click()
#   time.sleep(1)
#   jobdesc_elements = driver.find_elements_by_xpath('//*[@id="vjs-desc"]')

#   for itm in jobdesc_elements:
#     print(itm.get_attribute('innerText'))

#blank list
job_postings = []
for div in soup.findAll("div", attrs={"class": "jobsearch-SerpJobCard"}):
  #blank dictionary
  info = {
    'title':'',
    'company':'',
    'location':'',
    'salary':'',
    'description':''
  }
  #grab titles
  for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
    info['title']=a["title"]
  #grab company
  company = div.find_all(name="span", attrs={"class":"company"})
  if len(company) > 0:
    for b in company:
      info['company']=b.text.strip()
  else:
    sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
    for span in sec_try:
      info['company']=span.text.strip()
  #grab location
  for span in div.findAll("span", attrs={"class": "location"}):
    info['location']=span.text
  #grab description
  postingID = div.get("data-jk")
  python_button = driver.find_element_by_xpath(f"//div[@data-jk='{postingID}']")
  python_button.click()
  time.sleep(1)
  jobdesc_elements = driver.find_elements_by_xpath('//*[@id="vjs-desc"]')
  for itm in jobdesc_elements:
    info['description']+=itm.get_attribute('innerText')
  #grab URL
    #grab it later
  #append to job_postings
  job_postings.append(info)
print(job_postings)

try:
  connection = psycopg2.connect(user = "eden",
                                password = "Ed3nEd3nEd3n",
                                host = "127.0.0.1",
                                port = "5432",
                                database = "jobsdb")
  cursor = connection.cursor()

  postgres_insert_query = """ INSERT INTO jobs (DESCRIPTION, TITLE, COMPANY, LOCATION, SALARY) VALUES (%s,%s,%s,%s,%s)"""
  for jp in job_postings:
    record_to_insert = (jp['description'], jp['title'], jp['company'], jp['location'], '$9999.99')
    cursor.execute(postgres_insert_query, record_to_insert)

  connection.commit()
  count = cursor.rowcount
  print (count, "Record inserted successfully into jobs table")

except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to insert record into jobs table", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")    


# while True:
#     items = [itm.get_text(strip=True) for itm in soup.select('.lister-item-content a[href^="/title/"]')]
#     print(items)

#     try:
#         driver.find_element_by_xpath('//a[contains(.,"Next")]').click()
#         soup = BeautifulSoup(driver.page_source,"lxml")
#     except Exception: break

#printing soup in a more structured tree format that makes for easier reading
#print(soup.prettify())
# python_button = driver.find_element_by_xpath("//*[@id='p_e079b481b0f32776']") 
# python_button.click()

# driver.findElements(By.xpath(f"//div[@data-jk={'e079b481b0f32776'}]"))


#driver.quit()


# OG Code Testing
#conducting a request of the stated URL above:
#page = requests.get(URL)
#specifying a desired format of "page" using the html parser - 
# this allows python to read the various components of the page, rather than treating it as one long string.
#soup = BeautifulSoup(page.text, "html.parser")


def extract_job_title_from_result(soup): 
  jobs = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
      jobs.append(a["title"])
  return(jobs)
  
# jobspulled = extract_job_title_from_result(soup)
# print(jobspulled)
# print(len(jobspulled))

def extract_company_from_result(soup): 
  companies = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    company = div.find_all(name="span", attrs={"class":"company"})
    if len(company) > 0:
      for b in company:
        companies.append(b.text.strip())
    else:
      sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
      for span in sec_try:
        companies.append(span.text.strip())
  return(companies)
 
# companynames = extract_company_from_result(soup)
# print(companynames)
# print(len(companynames))

def extract_location_from_result(soup): 
  locations = []
  spans = soup.findAll("span", attrs={"class": "location"})
  for span in spans:
    locations.append(span.text)
  return(locations)

# joblocations = extract_location_from_result(soup)
# print(joblocations)
# print(len(joblocations))



# def extract_posting_description(soup)