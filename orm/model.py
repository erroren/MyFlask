from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, TEXT,ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+mysqlconnector://root:123456@localhost/goods", encoding="utf8", echo=True)
Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(20), nullable=False)
    password = Column(String(40), nullable=False)


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(10), nullable=False)
    content = Column(TEXT, nullable=False)
    userid = Column(Integer, ForeignKey('account.id'), nullable=False)


if __name__ == "__main__":
    Base.metadata.create_all(engine)



