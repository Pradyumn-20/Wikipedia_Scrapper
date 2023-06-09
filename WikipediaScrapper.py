from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
from selenium import webdriver

class WikipediaScrapper:

    def __init__(self,executable_path,chrome_options):
        try:
            self.driver = webdriver.Chrome(executable_path=executable_path,chrome_options=chrome_options)
        except Exception as e:
            raise Exception("Issue in installing driver : " , str(e))

    def OpenUrl(self,url):
        try:
            self.driver.get(url)
        except Exception as e:
            raise Exception("issue while opening the URl : " ,str(e))

    def getSearchButton(self):
        try:
            x = self.driver.find_element_by_name(name="search")
            return x
        except Exception as e:
            raise Exception("Issue while getting search block :" , str(e))

    def searchData(self):
        try:
            self.driver.find_element_by_xpath(xpath="//*[@id='search-form']/fieldset/button/i").click()
        except Exception as e:
            raise Exception("Issue while clicking search button : " , str(e))

    def getPageData(self):
        try:
            data = self.driver.find_element_by_id("bodyContent").text
            return  data
        except Exception as e:
            raise Exception("Isssue while getting data : " , str(e))

    def getSummary(self,data):
        try:
            auto_abstractor = AutoAbstractor()
            # Set tokenizer.
            auto_abstractor.tokenizable_doc = SimpleTokenizer()
            # Set delimiter for making a list of sentence.
            auto_abstractor.delimiter_list = [".", "\n"]
            # Object of abstracting and filtering document.
            abstractable_doc = TopNRankAbstractor()
            # Summarize document.
            result_dict = auto_abstractor.summarize(data, abstractable_doc)
            return result_dict['summarize_result']
        except Exception as e:
            raise Exception("Issue while getting summary : " , str(e))

    def getLinks(self):
        try:
            tot_links = []
            links = self.driver.find_elements_by_css_selector("ol.references a")
            for link in links:
                if link.get_attribute("class") == "external text" and link.get_attribute("rel") == "nofollow":
                    tot_links.append(link.get_attribute('href'))
            return tot_links
        except Exception as e:
            raise Exception("Issue while getting links : ", str(e))

    def getImages(self):
        try:
            imgs = []
            images = self.driver.find_elements_by_tag_name("a.image img")
            for i in images:
                imgs.append(i.get_attribute("src"))
            return imgs
        except Exception as e:
            raise Exception("Issue while getting image links " , str(e))

    def closeDriver(self):
        try:
            self.driver.close()
        except Exception as e:
            raise Exception("Issue while closing driver : " , str(e))




