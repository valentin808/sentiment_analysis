from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
def get_content( html):
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all('article', class_='sc-748e6672-1 gbDQbJ user-review-item')
        Data_list = []
        for item1 in items:
            item2 =  item1
            try:
               comment = item2.find('div',class_='ipc-html-content-inner-div').get_text()
            except:
                comment=''
            try:
                date = item2.find('li',class_='ipc-inline-list__item review-date').get_text()
            except:
                date=''
            try:
                rate = item2.find('span',class_='ipc-rating-star--rating').get_text()
            except:
                rate=''
            try:
                max_rate=item2.find('span',class_='ipc-rating-star--maxRating').get_text()
            except:
                max_rate=''
            

            Data_list.append({
                'comment': comment,
                'date' : date,
                'rate': rate,
                'max_rate':max_rate
                 })

        return Data_list



def save_to_csv(data, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data[0].keys())
        
        for row in data:
            writer.writerow(row.values())
    
    print(f"Data saved as  {filename} ({len(data)} reviews)")

    
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://www.imdb.com/title/tt0418279/reviews/?ref_=ttrt_sa_3"
driver.get(url)

time.sleep(3)

while True:
    try:
        load_more_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ipc-see-more__text"))
        )
        driver.execute_script("arguments[0].click();", load_more_button)
        print("Button 'Load More' clicked")
        time.sleep(2)
    except:
        print("Button 'Load More' dont found")
        break


page_html = driver.page_source
res = get_content(page_html)
print(f"Get {len(res)} reviews.")

save_to_csv(res, "imdb_reviews1.csv")
driver.quit()
