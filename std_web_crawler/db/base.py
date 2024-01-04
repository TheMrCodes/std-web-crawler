from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr


class BaseModel(DeclarativeBase):

    __abstract__ = True
    _the_prefix = 'swc_'
    
    @declared_attr
    def __tablename__(cls):
        return cls._the_prefix + cls.__incomplete_tablename__
