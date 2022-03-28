import requests
from bs4 import BeautifulSoup
import math
from multiprocessing import Pool, Manager

URL = "https://www.jobkorea.co.kr/"
HEADERS = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
PAGE_SIZE = 20


def get_last_page(word):
  job_url = URL + f"/Search/?stext={word}"
  
  request_result = requests.get(job_url, headers=HEADERS)
  soup = BeautifulSoup(request_result.text, "html.parser")
  total_jobs = soup.find("p", { "class": "filter-text" }).find("strong", {"class" : "dev_tot"}).get_text().replace(",", "")
  
  end = int(total_jobs)
  last_page = math.ceil(int(total_jobs) / PAGE_SIZE)

  return {"last_page":last_page, "end" : end}


def extract_job(result):
  result_company = result.find('div', {"class" : "post-list-corp"}).get_text(strip=True)

  result_title = result.find('a', {'class' : 'title'})
  if result_title is not None:
    result_title = result_title.get_text(strip=True)
  else:
    return None

  result_location =  result.find('p', {'class' : 'option'}).find("span", {"class" : "long"})
  if result_location is not None:
    result_location = result_location.get_text(strip=True)
  else:
    result_location = result.select(".option > span:nth-of-type(4)")[0].get_text(strip=True)
  result_href = result.find('a', {'class' : 'name'})['href']
  result_apply = URL + result_href
  
  return {'company' : result_company, 'title' : result_title, 'location' : result_location, 'apply_link' : result_apply}


def get_job_list(last_page, word):
  jobs = []
  
  for page in range(last_page):
    print(f"Scrapping Jobkorea Page : {page+1}")
    page_url = URL + f"/Search/?stext={word}&tabType=recruit&Page_No={page+1}"
    print(page_url)
    request_result = requests.get(page_url)
    soup = BeautifulSoup(request_result.text, 'html.parser')
    find_result = soup.find_all('li', {'class' : 'list-post'})

    count = 0
    for result in find_result:
      if count == 20:
        break
      job = extract_job(result)

      if job is not None:
        jobs.append(job)
        count += 1
      else:
        continue
  return jobs


def job_search(word):
  page_result = get_last_page(word)
  print(f"last_page : {page_result['last_page']}")

  jobs = get_job_list(page_result['last_page'], word)
  if __name__ == '__main__':
    pool = Pool(processes=10) #4개의 프로세스 동시에 작동
    pool.map(jobs, range(1,page_result['end'], 10))
  return jobs