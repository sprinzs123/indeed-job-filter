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
            all_results = []
            current_node = self.head
            count = 0
            while current_node:
                one_job = {'title': current_node.title, 'date': current_node.date,
                           'requirements': current_node.requirements, 'summary': current_node.summary,
                           'location': current_node.location, 'company': current_node.company,
                           'link': current_node.link}
                all_results.append(one_job)
                count += 1
                current_node = current_node.next
            return all_results

    # FILTERS ###
    # iterate through nodes to filter by category
    def filter_titles(self, filter_list):
        current = self.head
        previous = None
        while current:

            if current.title in filter_list:
                previous.next = current.next
                current = current.next
            else:
                previous = current
                current = current.next

    def filter_requirements(self, filter_list):
        current = self.head
        previous = None
        while current:
            if current.requirements in filter_list:
                previous.next = current.next
                current = current.next
            else:
                previous = current
                current = current.next

    def filter_summary(self, filter_list):
        current = self.head
        previous = None
        while current:
            if current.summary in filter_list:
                previous.next = current.next
                current = current.next
            else:
                previous = current
                current = current.next

    def date_filter(self, filter_date):
        current = self.head
        previous = None
        while current:
            if current.date <= filter_date:
                previous.next = current.next
                current = current.next
            else:
                previous = current
                current = current.next

    def filter_any(self, filter_list):
        current = self.head
        previous = None
        while current:
            if current.title in filter_list or current.summary in filter_list or current.requirements in filter_list:
                previous.next = current.next
                current = current.next
            else:
                previous = current
                current = current.next


# unit testing for some of the data
class DataValidation:
    def is_data_present(self, data_scraped):
        if data_scraped is not None:
            if type(data_scraped) == str:
                return data_scraped
            else:
                text_only = data_scraped.text
                text_only = text_only.replace('\n', '')
                return text_only
        else:
            return None

    # use page number from scraping to determine how many pages exists on a page
    def page_exists(self, url):
        request = requests.get(str(url))
        if request.status_code == 200:
            return True
        else:
            return False


# class that stores all function that need to change data types or change data
# need for recording correct time and filter objects by time
class DataTransformation:
    # data scraped is in 'x days ago' format and need to make it to int so can filter
    def str_day_to_int(self, str_time):
        str_int = ''
        for i in str_time:
            if i.isaplpha():
                str_int += i
        return int(str_int)


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}


# main function that is used to record items and is used on flask file
def all_data(input_url, title_filters, requirements_filters, summary_filters):
    all_pages = urls_from_total(input_url)
    data_transform = DataTransformation()
    for one_page in all_pages:
        initial_page = requests.get(one_page, headers=headers)
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
            str_date = data_testing.is_data_present(date_posted)
            ind_date = data_transform.str_day_to_int(str_date)
            requirements = data_testing.is_data_present(requirements)
            summary = data_testing.is_data_present(summary)
            location = data_testing.is_data_present(location)
            company = data_testing.is_data_present(company)
            link = data_testing.is_data_present(application_link)

            # adding item to linked list with rest of items
            item_list.insert_start(title, ind_date, requirements, summary, location, company, link)

        # filtering items/getting final result of the that is going to be passed into flask for display
        # final output is lists of lists
        # print(item_list.item_count())
        return item_list.final_results()


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


# make valid list of url by scraping first job of each page
# get first job from each page and compare if this job posting already exists
# if not it is a valid new page
def valid_scare_url(initial_url):
    check_string = ''
    unique_page = True
    pagination_count = 1
    url_list = []
    url_list.append(initial_url)
    while unique_page:
        print(pagination_count)
        new_url = initial_url + '&start' + '=' + str(pagination_count * 10)
        initial_page = requests.get(new_url, headers=headers)
        soup = BeautifulSoup(initial_page.content, 'html.parser')
        title = soup.find("h2", {"class": "title"})
        requirements = soup.find("div", {"class": "jobCardReqList"})
        summary = soup.find("div", {"class": "summary"})
        location = soup.find("div", {"class": "location"})
        company = soup.find("a", {"data-tn-element": "companyName"})
        new_check = str(title) + str(requirements) + str(summary) + str(location) + str(company)
        if new_check == check_string:
            unique_page = False
        else:
            url_list.append(new_url)
            pagination_count += 1
            check_string = new_check
    return url_list


# get how many jobs are totally detected
def urls_from_total(initial_url):
    url_list = []
    url_list.append(initial_url)
    initial_page = requests.get(initial_url, headers=headers)
    soup = BeautifulSoup(initial_page.content, 'html.parser')
    results_count = soup.find("div", {"id": "searchCountPages"}).text
    int_results = int(results_count.split()[-2])
    pagination_count = int(int_results/15)
    for i in range(1, pagination_count + 1):
        new_url = initial_url + '&start' + '=' + str(i * 10)
        url_list.append(new_url)
    return url_list


# testing items to validate data
test_url = 'https://www.indeed.com/jobs?q=computer+science+internship&l=Marlton,+NJ&ts=1607291973924&rq=1&rsIdx=0'
urls_from_total(test_url)

# print(all_data(test_url, None, None, None))

# test data that is pulled up with script
# need for flask template testing
dummy_items = [{'title': 'Guest Advocate (Cashier or Front of Store Attendant/ Cart At...', 'date': '30+ days ago', 'requirements': None, 'summary': 'Advocates of guest experience who welcome, thank, and exceed guest service expectations by focusing on guest interaction and recovery.', 'location': None, 'company': 'TARGET', 'link': 'https://www.indeed.com/rc/clk?jk=cf52b8bd0296e902&fccid=15f43d82dc901ff2&vjs=3'}, {'title': 'File Clerk, Per Diem - FLOAT DEPT - Various NJ Locations', 'date': '9 days ago', 'requirements': None, 'summary': 'Ability to use computer systems; ability to interact with registration staff to resolve issues.Prepares charts and paperwork packets for new patients.', 'location': None, 'company': 'Jefferson - Camden County, NJ', 'link': 'https://www.indeed.com/rc/clk?jk=c8bb4eb33d1bb4ea&fccid=cce48ad42816872f&vjs=3'}, {'title': 'Telemedicine Patient Registration Specialist - Full or Part...new', 'date': '7 days ago', 'requirements': None, 'summary': 'Medical billing - ensure all billing codes are entered correctly and accurately.Southern Jersey Family Medical Centers, Inc. is looking for a talented…', 'location': None, 'company': 'Southern Jersey Family Medical Centers', 'link': 'https://www.indeed.com/rc/clk?jk=539d96a1b7a174a2&fccid=92c7b089e7df7bc6&vjs=3'}]


# DEBUGGING ###
# getting all titles for debugging
def get_titles(self):
    if self.head is None:
        return False
    else:
        all_items = []
        current_node = self.head
        while current_node:
            all_items.append(current_node.title)
            current_node = current_node.next
        return all_items


# how many items
def item_count(self):
    if self.head is None:
        return False
    else:
        current_node = self.head
        count = 0
        while current_node:
            current_node = current_node.next
            count += 1
        return count