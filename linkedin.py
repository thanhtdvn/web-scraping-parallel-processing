import datetime
from time import sleep, time

from scrapers.linkedin.page import Page

if __name__ == '__main__':
    # set variables
    p = Page()
    if(p.login().connect('https://www.linkedin.com/login')):
        print('Logged')

        """
        profile = p.profile()
        output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        output_filename = f'linkedin_{output_timestamp}.csv'
        """

        search_page = p.search()
        p_url = 'https://www.linkedin.com/search/results/people/?facetGeoUrn=%5B%22104195383%22%5D&keywords=angular&origin=FACETED_SEARCH'
        if search_page.connect(p_url):
            print (f'Search {p_url} successed.')
        else:
            print('Can not access search page')
    else:
        print('Fail')
    print(f'Elapsed run time seconds')
