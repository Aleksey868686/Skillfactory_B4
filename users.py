from __future__ import annotations
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

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

def connect_db() -> sessionmaker:
    """
    Устанавливает соединение к БД, создает таблицы, если их еще нет и возвращает объект сессии
    """

    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data() -> User:
    """
    Запрашивает данные нового пользователя
    """

    first_name = input("Please enter your name: ")
    last_name = input("Please enter your surname: ")
    gender = input("Please enter your gender(Male or Female): ")
    email = input("Please enter your email: ")
    birthdate = input("Please enter your birthdate (YYYY-MM-DD): ")
    height = input("Please enter your height (in m). Please use '.' for decimal point: ")
    obj = User(
        first_name = first_name, 
        last_name = last_name,
        gender = gender,
        email = email,
        birthdate = birthdate,
        height = height,
    ) 
    return obj

def main() -> None:
    """
    Исполняет ход основной программы
    """

    session = connect_db()
    obj = request_data()
    session.add(obj)
    session.commit()
    print("Your personal data were saved. Thanks!")

if __name__ == "__main__":
    main()
