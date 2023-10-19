import requests
import os
import pdfplumber
import os.path


class Pdf_work:
    def __init__(self, link: str) -> None:
        self._dir = ".\pdf"
        self.__link = link
        self.download_pdf()
        self.__list_incoming = self.set_atr_list()
        self.__list_directions = self.set_fac_number()

    def download_pdf(self) -> None:
        """
        функция скачивает файл пдф с сайта яргу и отправляет в папку pdf
        """
        link_fin = f"https://www.uniyar.ac.ru{self.__link}"
        file_path = os.path.join(self._dir, f"{self.__link.split('/')[-1]}")
        if not os.path.exists(file_path):
            r = requests.get(link_fin)
            if r.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(r.content)
                print("file download")
        else:
            print("file exist")

    def set_atr_list(self) -> list:
        """
        возвращает список списков по каждому отдельному направлению
        """
        path_pdf = f'pdf\{self.__link.split("/")[-1]}'
        list_ = []
        with pdfplumber.open(path_pdf) as pdf:
            temp_list = list()
            for page in pdf.pages:
                table = page.extract_table()
                if table[0][0] == "N\nп/п":
                    if not temp_list == []:
                        list_.append(temp_list)
                        temp_list = []
                    temp_list += table[1:]
                else:
                    temp_list += table
            list_.append(temp_list)

        print("list of applicants was created")
        return list_

    def set_fac_number(self) -> list:
        """
        Возвращает список id факультетов в правильном порядке
        """
        path_pdf = f'pdf\{self.__link.split("/")[-1]}'
        list_ = []
        with pdfplumber.open(path_pdf) as pdf:
            for page in pdf.pages:
                table = page.extract_text().split("\n")
                # При длине table <=3 возникают ошибки с последними полупустыми страницами без данных
                if len(table) > 3:
                    if len(table[2].split(".")) > 2:
                        list_.append(table[2])
        print("faculty id was created")
        return list_

    def get_mass_con(self) -> list:
        return [self.list_directions, self.list_incoming]

    @property
    def list_incoming(self) -> list:
        return self.__list_incoming

    @property
    def list_directions(self) -> list:
        return self.__list_directions


if __name__ == "__main__":
    a = Pdf_work("/Abitur/abiturientu-2022/reytingovyy-spiski-2022/Reiting_sait_biofak.pdf%20(53).pdf")
    # print(a.get_atr_list("/Abitur/abiturientu-2022/reytingovyy-spiski-2022/Reiting_sait_urfak.pdf%20(53).pdf"))
    # print(a.set_atr_list())
    # print(a.set_fac_number())

    print(a.list_directions)
