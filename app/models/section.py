from app import db
from datetime import datetime

class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    level = db.relationship('Level', back_populates='sections')
    questions = db.relationship('Question', back_populates='section', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'level_id': self.level_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 