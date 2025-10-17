from app._core.database import Base
from sqlalchemy import Column, String

class Lab(Base):
    __tablename__ = "labs"
    id = Column(String, primary_key=True)