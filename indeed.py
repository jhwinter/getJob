#built-in python libraries
import argparse

parser = argparse.ArgumentParser(description='Help find jobs from Indeed, LinkedIn, ZipRecruiter.')
required = parser.add_argument_group('required arguments:')
required.add_argument('-j', '--job', type=str, nargs=1, required=True,
                    help='Job or keyword to search for (Web Developer, Python, Software Engineer)')
parser.add_argument('-l', '--location', type=str, nargs=1,
                    help='Location to search for jobs in (City, State, Zip Code, State)')
parser.add_argument('-jt', '--jobtype', type=str, nargs=1,
                    help='Type of employment you are seeking (fulltime, parttime, contract, temporary, commission, internship)')
parser.add_argument('-explvl', '--experiencelevel', type=str, nargs=1,
                    help='Level of experience you are seeking (entry_level, mid_level, senior_level)')

args = parser.parse_args()
print(args['job'])
for arg in vars(args):
    print(getattr(args, arg))
    if arg is None:
        print(args[arg])

### strings used for job query ###

#job keyword to look for/what field
q = 'software developer'
#location keyword/where field
l = ''
#Job Type Choices/jt field
jt = ['fulltime', 'parttime', 'contract', 'temporary', 'commission', 'internship']
#Experience Level choices/explvl field
explvl = ['entry_level', 'mid_level', 'senior_level']

search_url = 'https://www.indeed.com/jobs?q={}'.format(q)

