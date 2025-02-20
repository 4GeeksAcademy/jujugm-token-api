from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites: Mapped[List["Favorite"]] = relationship()


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    favorites: Mapped[List["Favorite"]] = relationship()


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    

class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))


    def serialize(self):
#     Esto de abajo consulta la base de datos para encontrar un planeta (Planets) cuyo id coincida con self.planet_id.
# scalar_one() devuelve un único resultado (o lanza un error si no encuentra nada).
        planet = db.session.execute(db.select(Planets).filter_by(id=self.planet_id)).scalar_one()
       
       
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": planet.serialize()
   
        }