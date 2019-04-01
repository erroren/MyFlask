from orm import model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine("mysql+mysqlconnector://root:123456@localhost/goods", encoding="utf8", echo=True)
session = sessionmaker()()


def insertUser(username, password):
    session.add(model.User(name=username, password=password))
    session.commit()
    session.close()


def selectuser(username, password):
    res = session.query(model.User).filter(model.User.name == username).filter(model.User.password == password).first()
    # print(res)
    return res


def selectuserbyid(num):
    res = session.query(model.User).filter(model.User.id == num).first()
    return res


def selectarticle():
    res = session.query(model.Project)
    return res


def selectmyself(userid):
    res = session.query(model.Project).filter(model.Project.userid == userid)
    return res


def selectone(id):
    res = session.query(model.Project).filter(model.Project.id == id).first()
    return res


def addarticle(title, content, userid):
    session.add(model.Project(title=title, content=content, userid=userid))
    session.commit()


def updatearticle(id, title, content):
    session.query(model.Project).filter(model.Project.id == id).update({model.Project.title: title,
                                                                        model.Project.content: content})
    session.commit()


def deletearticle(id):
    session.query(model.Project).filter(model.Project.id == id).delete()
    session.commit()

