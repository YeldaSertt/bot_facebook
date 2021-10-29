"""This code is to open data from facebook with selenium"""
import logging
import sys
import os
import hashlib
from time import sleep
import selenium as se
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import dateparser


logging.basicConfig(stream=sys.stdout, format='%(message)s', level=logging.INFO)
logging.basicConfig(stream=sys.stdout, format='%(message)s', level=logging.CRITICAL)
class Facebook:
    """Class Facebook"""

    def __init__(self):
        """Code reads here first"""
        self.run()
    def control(self):
        """Code controls input format"""
        try:
            date_parsed = dateparser.parse(
            sys.argv[2], date_formats=["%Y%m"]
            )
            date_parsed.strftime("%Y%m")
        except:# pylint: disable=bare-except
            logging.critical(" CRITICAL : You entered a non-format input for example =>> python bot_facebook.py --month 202101")
            sys.exit()
    def set_driver(self):
        """Chrome settings are made"""
        driver_path = "c:\\chromedriver.exe"
        options = se.webdriver.ChromeOptions()
        options.add_argument('headless')

        opts = Options()
        opts.add_argument("--headless") #====> if you wanna close chrome open this comment
        opts.add_argument("start-maximized")
        opts.add_argument("--no-sandbox")
        opts.add_argument("disable-gpu")
        opts.add_argument("disable-infobars")
        opts.add_argument("--disable-extensions")
        opts.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 1
        })
        capabilities = webdriver.DesiredCapabilities.CHROME

        self.driver = se.webdriver.Chrome(executable_path=driver_path,options=opts)
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
        with open('URLS/url.lst', 'r+') as readurllist:
            urllist = readurllist.read().splitlines()
        md5_url = []
        for url in urllist:
            count = 1
            array = []
            templist = []
            self.driver.get(url)
            sleep(5)
            hash_url = self.hashurl(url)
            self.driver.save_screenshot(f"bot-facebook_{hash_url}.png")
            md5 = {}
            md5["url"] = url
            md5["hash_url"] = hash_url
            md5_url.append(md5)
            md5df = pd.DataFrame(md5_url)
            sleep(5)
            stop = True
            original_size = self.driver.get_window_size()
            while True:
                sleep(5)
                if stop:
                    for item in self.driver.find_elements_by_xpath("//div[contains(@class,'rq0escxv l9j0dhe7 du4w35lb fhuww2h9 hpfvmrgz gile2uim pwa15fzy g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5')]/div/div[not(contains(@class,'j83agx80 l9j0dhe7 k4urcfbm'))]/div/div"):
                        gonderi_no = count
                        self.driver.save_screenshot(f"ilkbot-facebook_{hash_url}.png")
                        try:
                            post_date = item.find_element_by_xpath("./div//div[@class='qzhwtbm6 knvmm38d']/span/span/span/span/a/span").text
                            date_parsed = dateparser.parse(
                                post_date, date_formats=["%m-%d-%Y"]
                            )
                            my_month = date_parsed.strftime("%Y%m")
                            post = item.find_element_by_xpath(".//div[contains(@class,'gmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql i')]/div").text
                        except: # pylint: disable=bare-except
                            continue

                        if post_date not in array or post not in array:
                            array.append(post_date)
                            array.append(post)
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

                            count = count+1
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", item)
                            Height = item.size["height"]
                            sleep(10)
                            if str(my_month) == str(sys.argv[2]):
                                csvdf.to_csv(f'./DOM/bot-facebook_{my_month}_{hash_url}.csv', index=False)
                                logging.info(csvdf)
                                #Image
                                path = os.path.join("./OCR")
                                try:
                                    os.makedirs(path, exist_ok=True)
                                except: # pylint: disable=bare-except
                                    pass
                                item.screenshot(f"./OCR/bot-facebook_{my_month}_{hash_url}_{str(gonderi_no).zfill(4)}.png")
                            else:
                                stop = False
                                break
                        else:
                            continue
                else:
                    break
            ele=self.driver.find_element("xpath", '//div[contains(@class,"rq0escxv l9j0dhe7 du4w35lb fhuww2h9 hpfvmrgz gile2uim pwa15fzy g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5")]')
            total_height = ele.size["height"]+1000
            self.driver.set_window_size(1920, total_height)
            sleep(5)
            self.driver.save_screenshot(f"bot-facebook_{str(sys.argv[2])}_{hash_url}.png")
            sleep(5)
            self.driver.set_window_size(original_size['width'], original_size['height'])
        md5df.to_csv("url-md5.csv", index=False)
        self.driver.quit()

    def run(self):
        """Selenium works in the order here"""
        self.control()
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
