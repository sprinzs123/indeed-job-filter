from bs4 import BeautifulSoup
import requests
import json

url = "https://www.indeed.com/jobs?q=network&l=Marlton%2C+NJ"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
# get all tags info from this scrip, but need mode processing to be done
# find_all returns list and need to loop over to get data for each of the job position
# can make into list of json files for templates showing


def all_data(input_url):
    initial_page = requests.get(input_url, headers=headers)
    all_jobs = []
    soup = BeautifulSoup(initial_page.content, 'html.parser')
    for job in soup.find_all("div", {"class": "row"}):
        title = job.find("h2", {"class": "title"})
        date_posted = job.find("span", {"class": "date"})
        requirements = job.find("div", {"class": "jobCardReqList"})
        summary = job.find("div", {"class": "summary"})
        location = job.find("div", {"class": "location"})
        company = job.find("a", {"data-tn-element": "companyName"})
        application_link = 'https://www.indeed.com' + str(job.find("a", {"class": "jobtitle"})['href'])

        # verifying that data is present and then adding to it dictionary
        one_job = {}
        one_job.update({"title": data_testing.is_data_present(title)})
        one_job.update({"date_posted": data_testing.is_data_present(date_posted)})
        one_job.update({"requirements": data_testing.is_data_present(requirements)})
        one_job.update({"summary": data_testing.is_data_present(summary)})
        one_job.update({"location": data_testing.is_data_present(location)})
        one_job.update({"company": data_testing.is_data_present(company)})
        one_job.update({"application_link": data_testing.is_data_present(application_link)})
        print(one_job)
        json_job = json.loads(str(one_job))
        all_jobs.append(json_job)
    return all_jobs


# find how many pagination pages exist
# need to get valid urls
def get_page_numbers(initial_url):
    initial_page = requests.get(initial_url, headers=headers)
    soup = BeautifulSoup(initial_page.content, 'html.parser')
    page_count = 1
    for pagination_button in soup.find_all('span', {"class": "pn"}):
        current_pagination = pagination_button.text
        if current_pagination.isdigit():
            if int(current_pagination) > page_count:
                page_count = int(current_pagination)
    return page_count


# feed url with predefined filters and will find valid urls and make list that
# going to for loop later on
# assume that initial url is valid
def get_valid_urls(initial_url):
    url_list = []
    url_list.append(initial_url)
    pagination_count = 1
    pagination_limit = get_page_numbers(initial_url)
    for page_number in range(1, pagination_limit):
        url_list.append(initial_url + '&start' + '=' + str(pagination_count * 10))
        pagination_count += 1
    return url_list


class DataValidation:
    def is_data_present(self, data_scraped):
        if data_scraped is not None:
            return data_scraped.text
        else:
            return None

    # no longer need it, but keep just in case
    # use page number from scraping to determine how many pages exists on a page
    def page_exists(self, url):
        request = requests.get(str(url))
        if request.status_code == 200:
            return True
        else:
            return False


data_testing = DataValidation()
# print(get_valid_urls('https://www.indeed.com/jobs?q=network%2B&l=Marlton%2C+NJ&jt=parttime&fromage=last&start'))

# print(data_testing.page_exists('http://google.com'))

# all_data('https://www.indeed.com/jobs?q=software+developer&l=New+Jersey')
