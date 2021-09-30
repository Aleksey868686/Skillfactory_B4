from __future__ import annotations
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time
import datetime

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class Athelete(Base):
    """
    Описывает структуру таблицы athelete, содержащую данные об атлетах
    """
    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

    def __str__(self):
        return (f" id:{self.id} - {self.name} - {self.gender} - Рост: {self.height} - Дата рождения: {self.birthdate}")

class User(Base):
    """
    Описывает структуру таблицы user
    """
    
    __tablename__ = "user"
    id = sa.Column(sa.INTEGER, primary_key=True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.INTEGER)

    def __str__(self):
        return (f"{self.id} - {self.first_name}-{self.last_name}")

def connect_db() -> sessionmaker:
    """
    Устанавливает соединение к БД, создает таблицы, если их еще нет и возвращает объект сессии
    """

    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find_same_height(id: int, session: sessionmaker) -> None:
    """
    Ищет ближайшего по росту атлета
    """

    dict_delta_height = {}
    flag_height = True
    query_height = session.query(Athelete).filter(Athelete.height != None).all()
    for obj in query_height:
        delta_in_height = abs(id.height - obj.height)
        if delta_in_height == 0:
            flag_height = False
            print(f"Athlet similar by height: {obj}")
            break
        else:
            dict_delta_height[obj] = delta_in_height
    if flag_height:
        print(f"Athlet similar by height: {min(dict_delta_height, key=dict_delta_height.get)}")

def find_same_birthdate(id: int, session) -> None: 
    """
    Ищет атлета с ближайшим днем рождения
    """

    dict_delta_birthdate = {}
    flag_birthdate = True
    query_birthdate = session.query(Athelete).filter(Athelete.birthdate).all()
    for obj in query_birthdate:
        birthdate_stamp_id = time.mktime(datetime.datetime.strptime(id.birthdate, "%Y-%m-%d").timetuple())
        birthdate_stamp_obj = time.mktime(datetime.datetime.strptime(obj.birthdate, "%Y-%m-%d").timetuple())
        delta_in_birthdate = abs(birthdate_stamp_obj - birthdate_stamp_id)
        if delta_in_birthdate == 0:
            flag_birthdate = False
            print(f"Athlet similar by birthdate: {obj}")
            break
        else:
            dict_delta_birthdate[obj] = delta_in_birthdate
    if flag_birthdate:
        print(f"Athlet similar by birthdate: {min(dict_delta_birthdate, key=dict_delta_birthdate.get)}")


def main() -> None:
    """
    Исполняет ход основной программы
    """

    print("Let's look for athletes similar to one of the users")
    id_req = int(input("Please enter user ID: "))
    session = connect_db()
    query_id = session.query(User).filter(User.id == id_req).first()
    if query_id:
        find_same_height(query_id, session)
        find_same_birthdate(query_id, session)
    else:
        print("Пользователя с таким идентификатором нет")

if __name__ == "__main__":
    main()