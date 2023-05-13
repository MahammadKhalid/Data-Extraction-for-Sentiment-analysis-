# Importing packages
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time
import math
from tqdm.auto import tqdm
from random import choice
import sys
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

# to ignore SSL certificate errors
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# random user-agent
from fake_useragent import UserAgent
ua = UserAgent()



HEADERS = {
    'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'rtt': '50',
    'downlink': '6.65',
    'ect': '4g',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.amazon.com/Heat-Storm-HS-1500-PHX-WIFI-Infrared-Heater/dp/B07JXRWJ8D/ref=cm_cr_arp_d_pl_foot_top?ie=UTF8&th=1',
    'accept-language': 'en-US,en;q=0.9,la;q=0.8',
    'cookie': 'ubid-main=133-9061931-0297943; sid="u39jVVzRWP15jSjEJsTdwA==|9ucGRH1SUgtb9e1e982gkm5/DayNcyYRTYXgNPZNa+g="; x-main="mE3y@VSbrs7MHrVVNnP1GN@GVZOaUJqe"; at-main=Atza|IwEBIEv12ButU1VeMnrsclL17GM9BJ-80JPgG6TYbBZbAXZckOoe9wa7IyBNlbjEK-8F1AIpcMN4VR2tIGeWA0vdJ4PpvJA1R0N5Qn0zMsC4B6Y4megebgi3Jvq2BJ1g0jZRL9j9iYhPHFSdTUesgv9Q7p_PRb4dNNjnfnUGDeVxZHaCdWr-Iqatk6j8KcKYkusa9mKmGsz-2x_KF6xgU6Nx7QFE2yxAbegk8SnGIFiys8r99A; sess-at-main="NNbbNBJIIdO6ZUsf30V6vNV2aj2QETHGwAkzG3gX4ZE="; sst-main=Sst1|PQE1PjQcFvrt9Y3KNw8yA3eLEIpcrmUeovHZU8z9TftQ5cSjvbwa41EIkU6fNZnswQN4ItbnsOHE1dW6jzxtQ5W5bIW0nVNoX1SqhosV1IFUTgrfEJwe91NBnbMk4QMpfHZzjnBCtuP1l57JiSOetaBnrD4WZxe2IlQpTxhK57-mFsDAyjjPTpdWIsZFwK9KLFywkHaoJvVh6onccpXzMt_dEhnmwr3OeBWfFPagGojOYGpcnso44cDXzkLBMph3j_EnVk0ms-t-HRbuo64GAJ0O-Gc0e6o3D4JVCIy3pd9tERCyOn9iggvsICLQ5NDuq3IPop8KSk3xevMVZoEEucCO11ml7yWYg_Yo9wAlBGqRX9C4697s9qyM_llnAG0nn1KGTS-2BGyGl_7W47MtvpGTCtRdTp9jIJMFiwFPjUQ6h9to0Hligj45NYrF0p1JtCsH; i18n-prefs=USD; lc-main=en_US; aws-ubid-main=176-3363682-5411304; aws-session-id=140-0883594-3508442; aws-session-id-time=2232452694l; aws-session-token="4AcXH13Lb7gLaLAbVWxzhrnUWw5VZWqZi720/Dto7jgpDRcELFSp5rdL/70JOV/CzC3Q7NX5fwXr1hOyO1SGinrTZ2/mJwX9JI22zhbAj64paG31aDmWkELeUqOO9jxn87nBCHKuubVjDeLMfQoBykloAFSaSt6E/K+EiIG2dMyk5aC6G1Icjvrl1bdKmSGt3a+v4I/vPmozdi8jzhcihQnIA5aY3o5i/8p+kzEfCSQ="; sess-aws-at-main="OAo44oXc4/XY6EgTI5DzZjccXmr3Pf10LEqvTiATPBk="; regStatus=registered; aws_lang=en; s_fid=54929DF7E2EC5594-1DEC0D72EFDC6854; s_vn=1633268724773%26vn%3D1; s_invisit=true; s_cc=true; aws-target-visitor-id=1601732725193-893467; aws-target-data=%7B%22support%22%3A%221%22%7D; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A231071709544%3Aroot%22%2C%22alias%22%3A%22%22%2C%22username%22%3A%22jeff%2520james%22%2C%22keybase%22%3A%22%22%2C%22issuer%22%3A%22https%3A%2F%2Fwww.amazon.com%2Fap%2Fsignin%22%2C%22signinType%22%3A%22PUBLIC%22%7D; skin=noskin; csd-key=eyJ2IjoxLCJraWQiOiIzZTQwMDciLCJrZXkiOiJFTGpoTmpBeGhmNjgvTGdKQVNuTDBUcWx0a2JYaHRQdkVLRTRienk0bmVUM2Jnd0pHTHVlUlBjYkxya0RQVVRWMlV1YWI5WWZBMkZXTG93c1BxUUNtM21BL2RCbitJVkVuSmhFZkRqY2JUWEQrTllWbGlQSkhDeU9QYkpKa0RkYmNQRWtvOXNZa0VzU3hOZXFEbkZkUkk4b3FzY0dNZUU3MWFEVHcrRlNFVCtZYmd3amc3V0YyNjBoK29qQ0p6cVhkRDJzUVJBeVFtNmJxZG1TdXkzS092YkRIM293amNseTZVa0tKeGYzLzE5enA4OG10VWM2UG53clVvelQxMzdSbVpkVnlsZisvbjdSTGI0WkUzbjMzWDlEL1lsbmxhK0duLytlaU9qTjMzQUd3NG1NRC9oOTc0dFlqdmFQWnJDT2xKTk1RNmFVY3FpTDhReWQ0TUxwVFE9PSJ9; session-id-apay=143-6467005-0669008; session-id-time=2082787201l; session-id=146-2689202-9572416; s_dslv_s=More%20than%2030%20days; s_depth=2; s_dslv=1606267728256; s_nr=1606267728265-Repeat; session-token="gg4ozkVpSmo/CMUdJGU4vWV1Ap01LEGeSpGlQkj7ZEa3VEBeb+7xCHNDf8DV2y2tr45chYDEFySwu8cJx7Y1FN6QdAhBjINCqmSudE2ms/C0+61bcVE1sGzdOXLfxh57MgpZuzU1Xi/z3o8TsWfewFly/Kl6Aq0tKSWEPXT08CejwjX16Neh+Q00ofyScckwc/Qv/Q0oYIUysh3th6kRYg=="; csm-hit=tb:RP2649Z9F69V9KV5A8BV+sa-738Q8AECSK2TQNV33QMY-2WTAQEBB75E5T1SDK1R6|1606489267955&adb:adblk_yes&t:1606489267955',
}

class amazon_product_review_scraper:
    
    def __init__(self, product_asin,amazon_site="amazon.com", sleep_time=1, start_page=1, end_page=2):
        
        # url
        self.url = "https://www." + amazon_site + "/product-reviews/" + product_asin + "?pageNumber={}"
        self.sleep_time = sleep_time
        self.reviews_dict = {"Date Info":[], "Country Info":[], "Name":[], "Review Title":[], "Content":[], "Rating":[], "Link":[], "Product Title":[]}
        
        self.proxies = self.proxy_generator()        
        self.max_try = 10
        self.ua = ua.random
        self.proxy = choice(self.proxies)
        
        self.start_page = start_page
        if (end_page == None):
            self.end_page = self.total_pages()-1
        else:
            self.end_page = min(end_page, self.total_pages())


    def total_pages(self):
        
        response = self.request_wrapper(self.url.format(1))
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ## TODO if else        
        content = soup.find("div", {"data-hook": "cr-filter-info-review-rating-count"})
        total_reviews = int(content.text.replace("\n","").split()[3].replace(",",""))
    
        print ("Total reviews (all pages): {}".format(total_reviews), flush=True)
        
        total_pages = math.ceil(total_reviews/10)
        return total_pages
    

    # page scrapper
    def helper(self, content, tag, parameter_key, parameter_value):
        attribute_lst = []
        attributes = content.find_all(tag, {parameter_key: parameter_value})
        for attribute in attributes:
            attribute_lst.append(attribute.contents[0])
        return attribute_lst

    # MAIN FUNCTION
    def scrape(self):

        
        print ("Total pages: {}".format(self.end_page - self.start_page+1), flush=True)
        print ("Start page: {}; End page: {}".format(self.start_page, self.end_page))
        print ()
        print ("Started!", flush=True)

        for page in tqdm(range(self.start_page, self.end_page+1)):
            res = self.page_scraper(page)
            # print(self.reviews_dict)
            #
            if res == None:
                time.sleep(self.sleep_time)
            else:
                print ("Not able to scrape page {} Waiting for 10 sec more to bypassed CAPTCHA".format(page))
                time.sleep(3)
                res = self.page_scraper(page)
                


        print ("Completed!")
        
        # returning df
        print(len(self.reviews_dict["Date Info"]))
        print(len(self.reviews_dict["Country Info"]))
        print(len(self.reviews_dict["Name"]))
        print(len(self.reviews_dict["Review Title"]))
        print(len(self.reviews_dict["Content"]))
        print(len(self.reviews_dict["Link"]))
        print(len(self.reviews_dict["Product Title"]))
        print(len(self.reviews_dict["Rating"]))
        
        return self.reviews_dict



    def page_scraper(self, page):
        
        # try:

        response = self.request_wrapper(self.url.format(page))   

        # parsing content
        soup = BeautifulSoup(response.text, 'html.parser')
        ## reviews section
        reviews = soup.findAll("div", {"class":"a-section review aok-relative"})
        ## parsing reviews section
        reviews = BeautifulSoup('<br/>'.join([str(tag) for tag in reviews]), 'html.parser')

        ## 1. title
        title_lst = []
        try:
            titles = reviews.find_all("a", class_="review-title")
            # print(titles)
            if titles == []:
                titles = reviews.find_all("a", {"data-hook":"review-title"})
            # print(titles)
            if titles == []:
                titles = reviews.find_all("span", class_="review-title")
            # print(titles)
        except:
            titles=["",""]
        
        for title in titles:
            try:
                title_lst.append(title.find_all("span")[0].contents[0])
            except:
                title_lst.append("")

        ## 2. name
        name_lst = self.helper(reviews, "span", "class", "a-profile-name")

        ## 3. rating
        rating_lst = []
        try:
            ratings = reviews.find_all("i", {"data-hook":"review-star-rating"})
            if ratings == []:
                ratings = reviews.find_all("i", {"data-hook":"cmps-review-star-rating"})
                # print(ratings)
        except:
            
            ratings = ["",""]
        
        for rating in ratings:
            try:
                rating_lst.append(rating.find_all("span")[0].contents[0])
            except:
                rating_lst.append("")

        ## 4. date
        date_lst = [i.split("on")[1] for i in self.helper(reviews, "span", "data-hook", "review-date")]   
        ## 5. country
        country_lst = [i.split("on")[0] for i in self.helper(reviews, "span", "data-hook", "review-date")]

        ## 6. content
        contents = reviews.find_all("span", {"data-hook":"review-body"})
        content_lst = []
        for content in contents:
            try:
                text_ = content.find_all("span")[0].get_text("\n").strip()
                text_ = ". ".join(text_.splitlines())
                text_ = re.sub(' +', ' ', text_)
                content_lst.append(text_)
            except:
                content_lst.append("")

        ## 7. Link
        product_link =  "https://www.amazon.com"+soup.find_all("a", {"data-hook":"product-link"})[0]["href"]
        product_link = [product_link for i in range(int(len(content_lst)))]

        ## 8. title
        product_title = soup.find_all("a", {"data-hook":"product-link"})[0].text
        product_title = [product_title for i in range(int(len(content_lst)))]


        # adding to the main list
        self.reviews_dict['Date Info'].extend(date_lst)
        self.reviews_dict['Country Info'].extend(country_lst)
        self.reviews_dict['Name'].extend(name_lst)
        self.reviews_dict['Review Title'].extend(title_lst)
        self.reviews_dict['Content'].extend(content_lst)
        self.reviews_dict['Rating'].extend(rating_lst)
        self.reviews_dict['Link'].extend(product_link)
        self.reviews_dict['Product Title'].extend(product_title)

        return None

        # except:
        #     print ("Not able to scrape page {} (CAPTCHA is not bypassed)".format(page), flush=True)
        #     return "Proxy Update"


    # wrapper around request package to make it resilient
    def request_wrapper(self, url):
        
        while (True):
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            # amazon blocks requests that does not come from browser, therefore need to mention user-agent
            # response = requests.get(url, verify=False, headers={'User-Agent': self.ua}, proxies=self.proxy)
            SESSION = requests.Session() 
            # print(url) 
            response = SESSION.get(url, headers=HEADERS)
            # print(response.status_code)
            # checking the response code
            if (response.status_code != 200):
                pass
                # raise Exception(response.raise_for_status())
            
            # checking whether capcha is bypassed or not (status code is 200 in case it displays the capcha image)
            if "api-services-support@amazon.com" in response.text:
                
                if (self.max_try == 0):
                    raise Exception("CAPTCHA is not bypassed")
                else:
                    time.sleep(self.sleep_time)
                    self.max_try -= 1
                    self.ua = ua.random
                    self.proxy = choice(self.proxies)
                    continue
                
            self.max_try = 5
            break
            
        return response



    # random proxy generator
    def proxy_generator(self):
        proxies = []
        response = requests.get("https://sslproxies.org/")
        soup = BeautifulSoup(response.content, 'html.parser')
        proxys = pd.read_html(response.text)[0][["IP Address","Port"]]
        proxies= list(proxys["IP Address"].astype(str)+":"+proxys["Port"].astype(str))
        proxies_lst = [{'http':'http://'+proxy} for proxy in proxies]
        return proxies_lst

# helps scrape data 
def onehelper( content, tag, parameter_key, parameter_value):
    attribute_lst = []
    attributes = content.find_all(tag, {parameter_key: parameter_value})
    for attribute in attributes:
        attribute_lst.append(attribute.contents[0])
    return attribute_lst

# get ASIN number from keyword search
def get_ASIN_LST(Key_word):
    key_url="https://www.amazon.com/s?k="+str(Key_word)
    print(Key_word)

    
    s = requests.Session()            
    response = s.get(key_url,headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    reviewsASIN = soup.findAll("div", {"data-component-type":"s-search-result"})
    
    ASIN_lst=[]
    for i in reviewsASIN:
        ASIN_lst.append(i["data-asin"])
    # print(ASIN_lst)
    return ASIN_lst


def main(ASIN,Path_name):

    CSV_PATH = os.path.join(os.path.dirname(os.path.join(os.getcwd(),__file__)),Path_name)
    asinlst = get_ASIN_LST(ASIN)
    final_df =[]
    for ASIN in asinlst:
        scrap = amazon_product_review_scraper(product_asin=ASIN)
        print(ASIN)
        reviews_df = scrap.scrape()
        reviews_df = pd.DataFrame.from_dict(reviews_df, orient='index')
        reviews_df = reviews_df.transpose()
        final_df.append(reviews_df)
        print(reviews_df)
    review_df_final = pd.concat(final_df)
    review_df_final.to_csv(CSV_PATH,index=False)

if __name__ == "__main__":
    # Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-k", "--keyword", default="iphone",type=str, help="Keywords")
    parser.add_argument("-p", "--Path", default="Reviews.csv", type=str, help="Full path where you need to save the reviews")
    args = vars(parser.parse_args())
    key = args["keyword"]
    Path_name = args["Path"]
    
    main(key,Path_name)