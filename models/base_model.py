from db import db
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()

    def restore(self):
        self.deleted_at = None
        self.updated_at = datetime.utcnow()
        db.session.commit()


    @classmethod
    def get(cls, ident, with_deleted=False):
        if with_deleted:
            return cls.query.get(ident)
        return cls.query.filter(cls.id == ident, cls.deleted_at.is_(None)).first()

    @classmethod
    def get_or_404(cls, ident, with_deleted=False):
        if with_deleted:
            return cls.query.filter_by(id=ident).first_or_404()
        return cls.query.filter(cls.deleted_at.is_(None)).filter_by(id=ident).first_or_404()
   
    @classmethod
    def filter(cls, *args, with_deleted=False, **kwargs):
        if with_deleted is True:
            return cls.query.filter(*args, **kwargs)
        return cls.query.filter(*args, **kwargs).filter(cls.deleted_at.is_(None))
    
    @classmethod
    def filter_by(cls, *args, with_deleted=False, **kwargs):
        query = cls.query.filter(*args).filter_by(**kwargs)
        if not with_deleted:
            query = query.filter(cls.deleted_at.is_(None))
        return query
    
    @classmethod
    def all(cls, with_deleted=False):
        if with_deleted is True:
            return cls.query.all()
        return cls.query.filter(cls.deleted_at.is_(None)).all()

