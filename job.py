class Job:

    def __init__(self,title,location,company,link):
        self.title = title
        self.location = location
        self.company = company
        self.link = link

    def __repr__(self):
        return 'Title: {}\nLocation: {}\nCompany: {}\nLink: {}'.format(self.title, self.location,
                                                                        self.company, self.link)