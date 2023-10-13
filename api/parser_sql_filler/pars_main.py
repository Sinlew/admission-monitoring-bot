from sqlalc import engine, Sql_connect
from pars_yar import Parser_yar
from config.config import yar_link
import os

class Combine():
    def __init__(self, link:str):
        self.__main_parser = Parser_yar(link)
        self.__con = Sql_connect(engine)

    def db_filling(self):
        b:dict = self.__main_parser.get_data_mass()
        if self.__con.db_is_empty():
            print("[info] database is empty")
            for key in b.keys():
                for fac_num in range(len(b[key][0])):
                    for stud in b[key][1][fac_num]:
                        pr = stud[12].lower()=='да'
                        agr= stud[13].lower()=='да'
                        orig=stud[14].lower()=='да'
                        if stud[2]=='-':
                            stud[2]=0
                        self.__con.addin_db(key,b[key][0][fac_num],int(stud[0]),int(stud[1]),int(stud[2]),int(stud[8]),int(stud[7]),pr,agr,orig)
        else:
            print("[info] database is not empty")
            for key in b.keys():
                for fac_num in range(len(b[key][0])):
                    for stud in b[key][1][fac_num]:
                        pr = stud[12].lower()=='да'
                        agr= stud[13].lower()=='да'
                        orig=stud[14].lower()=='да'
                        if stud[2]=='-':
                            stud[2]=0
                        self.__con.update_db(b[key][0][fac_num],int(stud[2]),int(stud[0]),int(stud[8]),int(stud[7]),pr,agr,orig)
        self.delete_files_in_folder("pdf")

    def delete_files_in_folder(self,folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f'Ошибка при удалении файла {file_path}. {e}')


if __name__ == "__main__":
    com = Combine(yar_link)
    com.db_filling()