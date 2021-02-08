import sys
from enum import Enum
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import ClauseElement
from config.database import db

# Define a base model for other database tables to inherit
class BaseModel(db.Model):

    __abstract__  = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                         onupdate=db.func.current_timestamp())

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
