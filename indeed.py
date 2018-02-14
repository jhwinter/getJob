#local python imports
from job import Job

#built-in python libraries
import argparse
import requests

#3rd party python libraries
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Help find jobs from Indeed, LinkedIn, ZipRecruiter.')
required = parser.add_argument_group('required arguments:')
required.add_argument('-j', '--job', type=str, nargs=1, required=True,
                    help='Job or keyword to search for (Web Developer, Python, Software Engineer)')
parser.add_argument('-l', '--location', type=str, nargs=1, default='',
                    help='Location to search for jobs in (City, State, Zip Code, State)')
parser.add_argument('-jt', '--jobtype', type=str, nargs=1, default='',
                    help='Type of employment you are seeking (fulltime, parttime, contract, temporary, commission, internship)')
parser.add_argument('-explvl', '--experiencelevel', type=str, nargs=1, default='',
                    help='Level of experience you are seeking (entry_level, mid_level, senior_level)')

args = vars(parser.parse_args())
for key in args.keys():
    if type(args[key]) is list:
        args[key] = ' '.join(args[key])

job_list = []

### strings used for job query ###
search_url = 'https://www.indeed.com/jobs?q={}&l={}&jt={}&explvl={}'.format(args['job'], args['location'],
                                                                            args['jobtype'], args['experiencelevel'])
r = requests.get(search_url, allow_redirects=True)
soup = BeautifulSoup(r.content, 'html.parser')
job_divs = soup.find_all('div', class_='row result')
for div in job_divs:
    job_a_tag = div.find('a', class_='jobtitle turnstileLink')
    job_link = 'https://indeed.com' + job_a_tag['href']
    job_title = job_a_tag['title']
    job_location = div.find('span', class_='location').get_text().strip()
    job_company = div.find('span', class_='company').get_text().strip()
    job_list.append(Job(job_title,job_location,job_company,job_link))
page_selector_div = soup.find('div', class_='pagination')
page_selections = page_selector_div.find_all('a')
last_page_option = page_selections[-1]
print(last_page_option)