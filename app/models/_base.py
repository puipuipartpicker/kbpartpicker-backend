import sys
from enum import Enum
from datetime import datetime
from inflection import pluralize, underscore
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base, declared_attr
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, BigInteger


class BaseModel:

    @declared_attr
    def __tablename__(cls):
        return pluralize(underscore(cls.__name__))

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime,  default=datetime.now())
    updated_at = Column(DateTime,  default=datetime.now(),
                                   onupdate=datetime.now())

    @classmethod
    def get_or_create(cls, session, **kwargs):
        query = session.query(cls).filter_by(**kwargs).with_for_update()
        instance = query.one_or_none()
        if instance:
            session.commit()
            return instance, False
        else:
            params = dict(
                (k, v) for k, v in kwargs.items()
                if not isinstance(v, ClauseElement)
            )
            instance = cls(**params)
            try:
                session.add(instance)
                session.commit()
                return instance, True
            except IntegrityError as e:
                error_message = e.args[0]
                if "Duplicate entry" in error_message:
                    session.rollback()
                    print(error_message, file=sys.stderr)
                    return query.one(), False
                else:
                    raise e

    def populate(self, **kwargs):
        for key, val in kwargs.items():
            if getattr(self, key):
                continue
            setattr(self, key, val)

    def to_dict(self, **kwargs):
        res = dict()
        for c in self.__table__.columns:
            if c.name in ["created_at", "updated_at"]:
                continue
            val = getattr(self, c.name)
            if val is not None:
                if isinstance(val, Enum):
                    val = val.name
                res[c.name] = val
        if kwargs:
            for key, val in kwargs.items():
                res[key] = val
        return res

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.to_dict()}>"
    
    def __str__(self):
        return f"{self.__class__.__name__}"


BaseModel = declarative_base(cls=BaseModel)
