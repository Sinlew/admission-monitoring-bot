from sqlalchemy import create_engine, select, update

from sqlalchemy.orm import Session
import config.config as config 
from models.base import Base
from models.student import Student
import os

engine=create_engine(config.SQLALCHEMY_url, echo=config.SQLALCHEMY_ECHO)

class Sql_connect():
    def __init__(self,engine) -> None:
        self.__engine=engine
        Base.metadata.create_all(bind=self.__engine)
    
    def addin_db(self,facultet:str,direction:str,rating:int,id_abit:int,snils:int,points:int, points_fin:int,priority:bool, agreement:bool, original:bool):
        with Session(self.__engine) as session:
            student = Student(facultet=facultet,direction=direction,rating=rating,id_abitur=id_abit,snils=snils,points=points,points_fin=points_fin,priority=priority,agreement=agreement,original=original)
            session.add(student)
            session.commit()
    
    def search_db(self,snil:int)->list:
        with Session(self.__engine) as session:
            ans=select(Student.direction,Student.rating,Student.points_fin).where(Student.snils == snil)
            res = session.execute(ans).fetchall() 
            
        return res
    
    def is_copy(self, snil:int, fac_num:str)->bool:
        with Session(self.__engine) as session:
            a = select(Student).where(Student.direction==fac_num).where(Student.snils==snil)
            user = session.execute(a).all()
        if len(user)==0:
            return False
        else:
            return True
        
    def update_db(self,direction:str,snils:int,rating:int,points:int, points_fin:int,priority:bool, agreement:bool, original:bool):
        with Session(self.__engine) as session:
            # stud = session.query(Student).get(Student.direction==direction, Student.snils==snils)
            a = update(Student).where(Student.direction==direction).where(Student.snils==snils).values(rating=rating,points=points,points_fin=points_fin, priority=priority, agreement=agreement, original=original)
            session.execute(a)
            session.commit()

    def db_is_empty(self):
        with Session(self.__engine) as session:
            a = select(Student)
            
            user = session.execute(a).all()
            if len(user)==0:
                return True
            else:
                return False
            
    def search_db_as_dict(self,snil:int)->list:
        with Session(self.__engine) as session:
            dd=session.query(Student.direction,Student.rating,Student.points_fin).where(Student.snils == snil).distinct()
            a = [row._asdict() for row in dd]
        return a
            
    

    
    

if __name__ == "__main__":
    # a = Sql_connect(engine)
    pass
    
    # # print(a.is_copy(15943353790,"04.03.01 Химия; Медицинская и фармацевтическая химия"))
    # print(a.search_db2(16548783416))
    # a.db_delete()
    