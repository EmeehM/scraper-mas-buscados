import random
import time
from curl_cffi import requests
from lxml import html


import config
from logger import get_logger

logger = get_logger(__name__)

class Crawler:
    def __init__(self):
        self.HEADER_BROWSER = config.HEADER_BROWSER
        self.URL_BROWSER = config.URL_BROWSER
        self.HEADER_PAGE = config.HEADER_PAGE
        self.PROXIES = config.PROXIES
        self.most_wanted = []
        self.links = []

    def make_request(self, method,
                     url: str, headers: dict, payload, proxies: dict, mp=None,
                     max_retries=3) -> requests.Response | None:

        try_ = 0
        while try_ < max_retries:
            try:
                response = requests.request(method=method, url=url, headers=headers, data=payload,
                                            proxies=proxies, timeout=config.TIMEOUT, impersonate="chrome124",
                                            multipart=mp)
                status_code = response.status_code
                if status_code == 200 or status_code == 201:
                    return response
                else:
                    raise Exception(f"Bad requests status_code:{status_code}")
            except Exception as e:
                try_ += 1
                print(f"Trying to connect to: {url} - attempt: {try_} - {e}")
                time.sleep((random.randint(a=2, b=6)))
        print(f"Can't connect to: {url} - MAX RETRIES REACHED!")
        return None

    def data_parser(self, data) -> dict:
        try:
            name = data.xpath("normalize-space(//label[@for='Nombres']/following-sibling::text()[1])")
            name = name[2:]
            parts = name.split()
            if len(parts)>1:
                middle_name= parts[1]
                name = parts[0]
            else:
                middle_name =  ""
            print(name)
            print(middle_name)
        except Exception as e:
            logger.error(f"Can't extract names from the browsing page - Error: {e}")
            name = ""
            middle_name = ""

        try:
            last_name= data.xpath("//label[@id=Apellidos/following-sibling]")
            last_name = last_name[2:]
            if last_name.split[1]:
                second_last_name= last_name.split[1]
            else:
                second_last_name =  ""
        except Exception as e:
            logger.error(f"Can't extract names from the browsing page - Error: {e}")
            last_name = ""
            second_last_name = ""


        try:
            gender = data.xpath("//label[@id=GeneroId/following-sibling]")
            gender = gender[2:]
        except Exception as e:
            logger.error(f"Can't extract names from the browsing page - Error: {e}")
            gender=""

        try:
            DNI = data.xpath("//label[@id=Documento/following-sibling]")
            DNI = DNI[2:]
        except Exception as e:
            logger.error(f"Can't extract names from the browsing page - Error: {e}")
            DNI=""

        try:
            birth_date = data.xpath("//label[@id=FecNac/following-sibling]")
            birth_date = birth_date[2:]
        except Exception as e:
            logger.error(f"Can't extract names from the browsing page - Error: {e}")
            birth_date=""

        try:
            nationality = data.xpath("//label[@id=LugNac/following-sibling]")
            nationality = nationality[2:]
        except Exception as e:
            logger.error(f"Can't extract names from the browsing page - Error: {e}")
            nationality=""

        try:
            Age = data.xpath("//label[@id=EdadPresunta/following-sibling]")
            Age = Age[2:]
        except Exception as e:
            logger.error(f"Can't extract names from the browsing page - Error: {e}")
            Age=""

        person={
            "name":name,
            "middle_name": middle_name,
            "last_name":last_name,
            "second_last_name":second_last_name,
            "gender":gender,
            "DNI":DNI,
            "birth_date":birth_date,
            "nationality":nationality,
            "Age":Age,
        }
        print(person)




    def link_extraction(self):
        response = self.make_request(method="GET", url=self.URL_BROWSER,payload={}, proxies=self.PROXIES,headers=self.HEADER_BROWSER)
        tree = html.fromstring(response.content)
        panels = tree.xpath("//div[@class='panel-body']")
        for panel in panels:
            try:
                link = panel.xpath("./a/@href")
                if link:
                    self.links.append(link[0])
            except Exception as e:
                logger.error(f"Can't extract links from the browsing page - Error: {e}")

        self.info_extraction(links=self.links)

    def info_extraction(self, links):
        for link in links:
            #try:
            link = "https://www.dnrec.jus.gov.ar" + link
            print(link)
            unpolished_data = requests.get(url=link, headers=self.HEADER_PAGE,proxy=config.PROXY,timeout=config.TIMEOUT)
            tree = html.fromstring(unpolished_data.content)
            self.data_parser(tree)
            break

            #except Exception as e:
             #   logger.error(f"Can't extract links from the url: {link}   - Error: {e}")

    def crawl(self):
        logger.info("Extracting Links")
        self.link_extraction()
