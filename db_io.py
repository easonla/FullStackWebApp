from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem  # Import from setup

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def InsertRestaurant(name):
    tobeadded = Restaurant(name=name)
    session.add(tobeadded)
    session.commit()


def restaurant_name2id(name):
    doc = session.query(Restaurant).filter_by(name=name).first()
    return doc.id


def restaurant_id2name(_id):
    if isinstance(_id, str):
        _id = int(_id)

    doc = session.query(Restaurant).filter_by(id=_id).first()
    return doc.name


def RenameRestaurant(_id, new_name):
    doc = session.query(Restaurant).filter_by(id=int(_id)).first()
    doc.name = new_name
    session.add(doc)
    session.commit()


def DeleteRestaurant(_id):
    doc = session.query(Restaurant).filter_by(id=int(_id)).first()
    if doc != []:
        session.delete(doc)
        session.commit()


if __name__ == "__main__":
    doc = session.query(Restaurant).filter_by(id=1).first()
    print(doc.name)
