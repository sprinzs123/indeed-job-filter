from bs4 import BeautifulSoup
import requests
import json

# functions to connect to flask


# use link list to track what objects are recorded and filter them
class Node(object):
    def __init__(self, title=None, date=None, requirements=None,
                 summary=None, location=None, company=None, link=None):
        self.title = title
        self.date = date
        self.requirements = requirements
        self.summary = summary
        self.location = location
        self.company = company
        self.link = link
        self.next = None


class LinkedList(object):
    def __init__(self):
        self.head = None

    def insert_start(self, title, date, requirements, summary, location, company, link):
        new_node = Node(title, date, requirements, summary, location, company, link)
        if self.head is None:
            self.head = new_node
        else:
            old_head = self.head
            new_node.next = old_head
            self.head = new_node

    def final_results(self):
        if self.head is None:
            return False
        else:
            all_results = {}
            current_node = self.head
            while current_node:
                one_job = {'title': current_node.title, 'date': current_node.date,
                           'requirements': current_node.requirements, 'summary': current_node.summary,
                           'location': current_node.location, 'company': current_node.company,
                           'link': current_node.link}
                all_results.update({1: one_job})
                current_node = current_node.next
            return all_results

    # iterate through nodes to filter by category
    def filter_titles(self, titles_list):
        current = self.head
        previous = None
        while current:
            # print(current.title)
            if current.title in titles_list:
                previous.next = current.next
                current = current.next
            else:
                previous = current
                current = current.next


class DataValidation:
    def is_data_present(self, data_scraped):
        print(data_scraped)
        if data_scraped is not None:
            return data_scraped
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


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}


# main function that is used to record items and is used on flask file
def all_data(input_url, title_filters, requirements_filters, summary_filters):
    initial_page = requests.get(input_url, headers=headers)
    all_jobs = []
    item_list = LinkedList()

    soup = BeautifulSoup(initial_page.content, 'html.parser')
    for job in soup.find_all("div", {"class": "row"}):
        title = job.find("h2", {"class": "title"})
        date_posted = job.find("span", {"class": "date"})
        requirements = job.find("div", {"class": "jobCardReqList"})
        summary = job.find("div", {"class": "summary"})
        location = job.find("div", {"class": "location"})
        company = job.find("a", {"data-tn-element": "companyName"})
        application_link = 'https://www.indeed.com' + str(job.find("a", {"class": "jobtitle"})['href'])

        # veryfying that is data is present
        data_testing = DataValidation()
        title = data_testing.is_data_present(title)
        date = data_testing.is_data_present(date_posted)
        requirements = data_testing.is_data_present(requirements)
        summary = data_testing.is_data_present(summary)
        location = data_testing.is_data_present(location)
        company = data_testing.is_data_present(company)
        link = data_testing.is_data_present(application_link)

        # adding item to linked list with rest of items
        item_list.insert_start(title, date, requirements, summary, location, company, link)

    # filtering items by
    return item_list.final_results()


# testing items to validate data
test_url = 'https://www.indeed.com/jobs?q=computer&l=Marlton%2C+NJ&jt=parttime'
(all_data(test_url, None, None, None))
