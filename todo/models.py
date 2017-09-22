# To-Do-List-Project
# 15.07.2017
#
# Author: Sebastian Zoske
# Matr-Nr: 554384
# Informatics3
# HTW Berlin
# s0554384@htw-berlin.de

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# this class defines the Table that will be created in the database.
class Entry(Base):
    __tablename__ = 'entries'
    # defining the different Columns.
    # ID is the primary_key with autoincrement which will
    # be used to identify the objects for e.g deleting, editing.
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    descr = Column(String(300))
    state = Column(String(15))


    def __init__(self, title, descr):
        self.title = title
        self.descr = descr
        self.state = "new"

    def __repr__(self):
        return "Title: " + self.text + \
               "Description: " + self.descr + \
               "State: " + self.state
