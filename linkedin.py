import datetime
from time import sleep, time

from scrapers.linkedin.page import Page

if __name__ == '__main__':
    # set variables
    p = Page()
    if(p.login().connect('https://www.linkedin.com/login')):
        print('Logged')
        profile = p.profile()
        output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        output_filename = f'linkedin_{output_timestamp}.csv'

        p_url = 'https://vn.linkedin.com/in/hien-chau-8a4163141'
        if profile.connect(p_url):
            print (f'Profile {p_url} successed.')
            profile.write_to_file([profile.data], output_filename)
        
    else:
        print('Fail')
    print(f'Elapsed run time seconds')
