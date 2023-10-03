import requests
from bs4 import BeautifulSoup as BS 
from config.config import yar_link
from pars_pdf import Pdf_work


class Parser_yar():
    
    def __init__(self,link:str) -> None:   
        self.__link=link
        self.__list_links=self.get_list_links()    
        
    def get_list_links(self)-> dict:
        r = requests.get(self.__link)
        html = BS(r.content, "html.parser")
        res = dict()
        for el in html.select("body > div.body-wrapper.clearfix > div.container.container-main.col-margin-top > div > div.col.col-mb-12.col-9.col-margin-bottom > table:nth-child(5) > tbody > tr > td "):
            a = el.find_all("a")
            if len(a)!=0:
                res[el.get_text("/", strip=True).split('/')[0]]=a[0].get('href')
        
        return res
    
    def get_data_mass(self)->dict:
        """
        Возвращает словарь вида "Название факультета":[[номера направлений],[массив из массивов для каждого направления]]
        """ 
        res = dict()
        for key in self.__list_links.keys():
            res[key]=Pdf_work(self.__list_links[key]).get_mass_con()
        return res
             
    
    
    def write_res(self):
        with open("ans.txt","w", encoding="utf-8") as f:
            f.write(str(self.__list_links.items()))

    @property
    def list_links(self):
        return self.__list_links

if __name__ == "__main__":
    a=Parser_yar(yar_link)
    b =a.get_data_mass()



# body > div.body-wrapper.clearfix > div.container.container-main.col-margin-top > div > div.col.col-mb-12.col-9.col-margin-bottom > table:nth-child(5) > tbody > tr:nth-child(11) > td > b > span > a
# body > div.body-wrapper.clearfix > div.container.container-main.col-margin-top > div > div.col.col-mb-12.col-9.col-margin-bottom > table:nth-child(5) > tbody > tr:nth-child(2) > td > span > b > a