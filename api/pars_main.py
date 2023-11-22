from sqlalc import engine, Sql_connect
from pars_yar import Parser_yar
from config.config import yar_link
import os


class Combine:
    def __init__(self, link: str):
        self.__main_parser = Parser_yar(link)
        self.__con = Sql_connect(engine)

    def db_filling(self):
        b: dict = self.__main_parser.get_data_mass()
        print()
        if self.__con.db_is_empty():
            print("[info] database is empty")
            for key in b.keys():
                for fac_num in range(len(b[key][0])):
                    for stud in b[key][1][fac_num]:
                        "приведение к bool значению строковых данных о наличии приоритета, согласия, оригинала"
                        priority_confirmed, agreement_confirmed, original_confirmed = self.is_confirmed_list(
                            stud[12:15]
                        )
                        if stud[2] == "-":
                            stud[2] = 0

                        self.__con.addin_db(
                            facultet=key,
                            direction=b[key][0][fac_num],
                            rating=int(stud[0]),
                            id_abit=int(stud[1]),
                            snils=int(stud[2]),
                            points=int(stud[8]),
                            points_fin=int(stud[7]),
                            priority=priority_confirmed,
                            agreement=agreement_confirmed,
                            original=original_confirmed,
                        )
        else:
            print("[info] database is not empty")
            for key in b.keys():
                for fac_num in range(len(b[key][0])):
                    for stud in b[key][1][fac_num]:
                        "приведение к bool значению строковых данных о наличии приоритета, согласия, оригинала"
                        priority_confirmed, agreement_confirmed, original_confirmed = self.is_confirmed_list(
                            stud[12:15]
                        )
                        if stud[2] == "-":
                            stud[2] = 0
                        self.__con.update_db(
                            direction=b[key][0][fac_num],
                            snils=int(stud[2]),
                            rating=int(stud[0]),
                            points=int(stud[8]),
                            points_fin=int(stud[7]),
                            priority=priority_confirmed,
                            agreement=agreement_confirmed,
                            original=original_confirmed,
                        )
        self.delete_files_in_folder("pdf")

    def delete_files_in_folder(self, folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Ошибка при удалении файла {file_path}. {e}")

    def is_confirmed_list(self, text: list) -> list:
        """
        приведение к bool значению строковых данных из списка
        """
        res = [str(text[i]).lower() == "да" for i in range(len(text))]
        return res


if __name__ == "__main__":
    com = Combine(yar_link)
   