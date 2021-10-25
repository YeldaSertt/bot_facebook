"""This code is to open data from facebook with selenium"""
import logging
import sys
import csv
import os
import hashlib
from time import sleep
import selenium as se
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import dateparser



logging.basicConfig(stream=sys.stdout, format='%(message)s', level=logging.INFO)
class Facebook:
    """Class Facebook"""
    def __init__(self):
        """Code reads here first"""
        self.run()

    def set_driver(self):
        """Chrome settings are made"""
        options = se.webdriver.ChromeOptions()
        options.add_argument('headless')

        opts = Options()
        opts.add_argument(f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36")
        opts.add_argument("--headless") #====> if you wanna close chrome open this comment
        opts.add_argument("window-size=1920,1080")
        opts.add_argument("start-maximized")
        opts.add_argument("--no-sandbox")
        opts.add_argument("disable-gpu")
        opts.add_argument("disable-infobars")
        opts.add_argument("--disable-extensions")
        opts.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 1
        })

        capabilities = webdriver.DesiredCapabilities.CHROME

        self.driver = se.webdriver.Chrome(options=opts)
        sleep(2)

    def login(self):
        """login from facebook"""
        self.driver.get("https://tr-tr.facebook.com/")
        sleep(5)
        self.driver.find_element_by_name("email").send_keys("erefett_sert@hotmail.com")
        sleep(5)
        self.driver.find_element_by_name("pass").send_keys("Erefet12345")
        sleep(5)
        self.driver.find_element_by_name("login").click()
        sleep(7)

    def login_profil(self):
        """data is pulled here"""
        urllist = []
        urls = open("URLS/url.lst", "r")
        for url in urls:
            urllist.append(url)

        count = 1
        with open('url-md5.csv', 'w', encoding='UTF8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = ['url', 'md5']
            writer.writerow(header)
            for url in urllist:
                self.driver.get(url)
                sleep(5)

                hash_url = self.hashurl(url)
                sleep(5)
                gonderi_no = count
                sleep(5)
                data = [url, hash_url]
                writer.writerow(data)
                dizi = []
                templist = []
                sleep(7)
            while True:
                sleep(5)
                if self.driver.find_elements_by_xpath("//div[contains(@class,'rq0escxv l9j0dhe7 du4w35lb fhuww2h9 hpfvmrgz gile2uim pwa15fzy g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5')]/div//div[@class='j83agx80 l9j0dhe7 k4urcfbm']"):
                    for item in self.driver.find_elements_by_xpath("//div[contains(@class,'rq0escxv l9j0dhe7 du4w35lb fhuww2h9 hpfvmrgz gile2uim pwa15fzy g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5')]/div//div[@class='j83agx80 l9j0dhe7 k4urcfbm']"):
                        gonderi_no = count
                        try:
                            post_date = item.find_element_by_xpath("./div//div[@class='qzhwtbm6 knvmm38d']/span/span/span/span/a/span").text
                            date_parsed = dateparser.parse(
                                post_date, date_formats=["%m-%d-%Y"]
                            )
                            my_month = date_parsed.strftime("%Y%m")
                            post = item.find_element_by_xpath(".//div[contains(@class,'gmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql i')]/div").text
                        except: # pylint: disable=bare-except
                            continue

                        if post_date not in dizi or post not in dizi:
                            dizi.append(post_date)
                            dizi.append(post)
                            like = item.find_element_by_xpath(".//div[@class='l9j0dhe7']/div[contains(@class,'s1tcr66n')]//span[@class='pcp91wgn']").text
                            try:
                                share = item.find_element_by_xpath(".//div[@class='l9j0dhe7']/div[contains(@class,'s1tcr66n')]/div/div/span/div/span[contains(.,'Pay')]").text.replace("Paylaşım", "")
                            except: # pylint: disable=bare-except
                                share = "0"
                            try:
                                comment = item.find_element_by_xpath(".//div[@class='l9j0dhe7']/div[contains(@class,'s1tcr66n')]/div/div/div/span[contains(.,'Yorum')]").text.replace("Yorum", "")
                            except: # pylint: disable=bare-except
                                comment = "0"


                            table_dict = {
                                "Begeni":like,
                                'Yorum':comment,
                                'Paylasım':share,
                            }
                            templist.append(table_dict)
                            csvdf = pd.DataFrame(templist)

                            #CSV
                            path = os.path.join("./DOM")
                            try:
                                os.makedirs(path, exist_ok=True)
                            except: # pylint: disable=bare-except
                                pass

                            csvdf.to_csv(f'./DOM/bot-facebook_fulldata.csv', index=False)

                            count = count+1
                            self.driver.execute_script("window.scrollTo(0, window.scrollY + 1100)")
                            if str(my_month) == str(sys.argv[2]):
                                csvdf.to_csv(f'./DOM/bot-facebook_{my_month}_{hash_url}.csv', index=False)
                                logging.info(csvdf)
                                self.driver.execute_script("document.body.style.zoom='110%'")
                                #Image
                                path = os.path.join("./OCR")
                                try:
                                    os.makedirs(path, exist_ok=True)
                                except: # pylint: disable=bare-except
                                    pass
                                self.driver.save_screenshot(f"./OCR/bot-facebook_{my_month}_{hash_url}_000{gonderi_no}.png")
                            else:
                                break
                        else:
                            continue
                else:break


    def run(self):
        """Selenium works in the order here"""
        self.set_driver()
        self.login()
        self.login_profil()

    def hashurl(self, url):
        """Url hashes come from here"""
        str2hash = url
        result = hashlib.md5(str2hash.encode())
        return result.hexdigest()

def main():
    """"Main"""
    Facebook()

if __name__ == "__main__":
    main()
