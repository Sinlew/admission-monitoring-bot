from sqlalchemy import create_engine, select, update

from sqlalchemy.orm import Session
import config.config as config 
from models.base import Base
from models.student import Student

engine=create_engine(config.SQLALCHEMY_url, echo=config.SQLALCHEMY_ECHO)

class Sql_connect():
    def __init__(self,engine) -> None:
        self.__engine=engine
        Base.metadata.create_all(bind=self.__engine)
    
    def addin_db(self,facultet:str,direction:str,rating:int,id_abit:int,snils:int,points:int, points_fin:int,priority:bool, agreement:bool, original:bool):
        with Session(self.__engine) as session:
            if self.is_copy(snils,direction):
                self.update_db(direction,snils,rating,points,points_fin,priority,agreement,original)
            else:
                student = Student(facultet=facultet,direction=direction,rating=rating,id_abitur=id_abit,snils=snils,points=points,points_fin=points_fin,priority=priority,agreement=agreement,original=original)
                session.add(student)
            session.commit()
    
    def search_db(self,snil:int)->list:
        with Session(self.__engine) as session:
            ans=select(Student).where(Student.snils == snil)
            res = session.scalars(ans).fetchall()
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

    
    

if __name__ == "__main__":
    a = Sql_connect(engine)
    print("DFf")
    
    # print(a.is_copy(15943353790,"04.03.01 Химия; Медицинская и фармацевтическая химия"))
    a.update_db("46.03.01 История; История",16548783416,1,299,300,True,True,True)
