from sqlalc import engine, Sql_connect
from pars_yar import Parser_yar
from config.config import yar_link

class Combine():
    def __init__(self, link:str):
        self.__main_parser = Parser_yar(link)
        self.__con = Sql_connect(engine)

    def db_filling(self):
        b:dict = self.__main_parser.get_data_mass()
        for key in b.keys():
            for fac_num in range(len(b[key][0])):
                for stud in b[key][1][fac_num]:
                    pr = stud[12].lower()=='да'
                    agr= stud[13].lower()=='да'
                    orig=stud[14].lower()=='да'
                    self.__con.insert_db(key,b[key][0][fac_num],int(stud[0]),int(stud[1]),int(stud[2]),int(stud[8]),int(stud[7]),pr,agr,orig)


if __name__ == "__main__":
    com = Combine(yar_link)
    com.db_filling()