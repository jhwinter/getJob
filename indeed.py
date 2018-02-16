#local python imports
from job import Job

#built-in python libraries
import argparse
from email.message import EmailMessage
from pprint import pformat
import re
import requests
import smtplib

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

#get dictionary object from command line arguments
args = vars(parser.parse_args())
#converts all of the command line arguments from lists to strings
for key in args.keys():
    if type(args[key]) is list:
        args[key] = ' '.join(args[key])

#initialize an empty list that will contain all the jobs found
job_list = []
#regular expression used to identify any html tags
html_tag_regex = re.compile('<*>')

### strings used for job query ###
search_url = 'https://www.indeed.com/jobs?q={}&l={}&jt={}&explvl={}'.format(args['job'], args['location'],
                                                                            args['jobtype'], args['experiencelevel'])
#get the initial search page
r = requests.get(search_url, allow_redirects=True)
while(True):
    #create beautiful soup out of the webpage
    soup = BeautifulSoup(r.content, 'html.parser')
    #get all of the job results on that particular page
    job_divs = soup.find_all('div', class_='row result')
    for div in job_divs:
        #get the a tag inside the job's div
        job_a_tag = div.find('a', class_='jobtitle turnstileLink')
        #link to that particular job's webpage
        job_link = 'https://indeed.com' + job_a_tag['href']
        #get the job title from the link to that job's webpage
        job_title = job_a_tag['title']
        #get the text of the span that contains the job's location and remove any whitespace
        job_location = div.find('span', class_='location').get_text().strip()
        #get the text of the span that contains the job's company and remove any whitespace
        job_company = div.find('span', class_='company').get_text().strip()
        #get the html page relating to that job
        job_page_request = requests.get(job_link, allow_redirects=True)
        #create a beautiful soup object out of the html of that job's page
        job_page_soup = BeautifulSoup(job_page_request.content, 'html.parser')
        #get the job summary
        job_summary = job_page_soup.find(id='job_summary').get_text()
        #remove any html tags from the job summary
        job_summary = re.sub(html_tag_regex, '', job_summary)
        #append the newly created job object to the list
        job_list.append(Job(job_title,job_location,job_company,job_link))
    #div that contains all of the links to additional pages such as next and previous
    page_selector_div = soup.find('div', class_='pagination')
    #try except is here because sometimes pagination div doesn't exist? on last page and results in none object
    try:
        next_page_span = page_selector_div.find_all('span', class_='np')[-1]
        if(next_page_span.get_text()[2:] == 'Previous'):
            break
    except Exception as e:
        print(e)
        break
    #get the a tag of the next page button
    next_page_a_tag = next_page_span.parent.parent
    #build the link to the next page from the href and data-pp attributes in the a tag
    next_page_link = 'https://indeed.com{}&pp={}'.format(next_page_a_tag['href'],
                                                        next_page_a_tag['data-pp'])
    #get the next page of results
    r = requests.get(next_page_link, allow_redirects=True)

#make the list of job objects into nicely formatted string
job_list_string = pformat(job_list)
#write all the jobs found out to a text file
with open('job_results.txt', 'w') as job_results_file:
    job_results_file.write(job_list_string)
