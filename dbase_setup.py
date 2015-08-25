from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///notepad.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Notes(Base):
   __tablename__= 'notes'
   
   id = Column(Integer, primary_key = True)
   title = Column(String(80), nullable =False )
   content = Column(String(2040), nullable= False)

   @property
   def serialize(self):
        """
        serialize function to be able to send JSON objects in a
        serializable format
        """
        return {
        'title': self.title,
        'content' : self.content,
        'id': self.id,
        }

#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


                