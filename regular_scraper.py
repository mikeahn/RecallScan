from bs4 import BeautifulSoup
import requests
import time
import calendar
# This will run as a cron job daily to get the latest recall information and add to the database.

# constants
COI = "Food & Beverages"


# remove fda.gov/about url which is at the top of this aspx page.
def extract_about(link_list):
    for link in link_list:
        if "www.fda.gov/about" in link:
            link_list.remove(link)

    return link_list


recall_gov_aspx = "https://www.recalls.gov/rrfda.aspx"
r = requests.get(recall_gov_aspx)

data = r.text
soup = BeautifulSoup(data,  "html.parser")
all_links = soup.find_all('a')

# extract list from the aspx
recall_gov_urls = [x.get('href') for x in all_links]
extract_about(recall_gov_urls)

for url in recall_gov_urls:
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    # check if this information is category of interest
    product_type = soup.find(text="Product Type:")
    if product_type is not None:
        product_type_value = str(product_type.findNext("dd").contents[0])

        if COI in product_type_value:
            # first, find inset column that contains our summary information
            announcement_date_label = soup.find(text="Company Announcement Date:")
            announcement_date_value = announcement_date_label.findNext("dd").contents[0].contents[0]
            announcement_date_timestamp = calendar.timegm(time.strptime(announcement_date_value, '%B %d, %Y'))

            # des_date_label = soup.find(text="Brand Name:")
            # des_val = des_date_label.findNext("dd").find(class_="field--item").contents[0]
            # print(des_val)
            # print(product_type_value.strip())
