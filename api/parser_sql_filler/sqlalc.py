from sqlalchemy import create_engine, select

from sqlalchemy.orm import Session
import config.config as config 
from models.base import Base
from models.student import Student

engine=create_engine(config.SQLALCHEMY_url, echo=config.SQLALCHEMY_ECHO)

class Sql_connect():
    def __init__(self,engine) -> None:
        self.__engine=engine
        Base.metadata.create_all(bind=self.__engine)
    
    def insert_db(self,facultet:str,direction:str,rating:int,id_abit:int,snils:int,points:int, points_fin:int,priority:bool, agreement:bool, original:bool):
        with Session(self.__engine) as session:
            student = Student(facultet=facultet,direction=direction,rating=rating,id_abitur=id_abit,snils=snils,points=points,points_fin=points_fin,priority=priority,agreement=agreement,original=original)
            session.add(student)
            session.commit()
    
    def search_db(self,snil:int)->list:
        with Session(self.__engine) as session:
            ans=select(Student).where(Student.snils == snil)
            res = session.scalars(ans).fetchall()
        return res


    
    

if __name__ == "__main__":
    a = Sql_connect(engine)
    print("DFf")
    b= a.search_db(23)[0]
    print(b.get_list())
