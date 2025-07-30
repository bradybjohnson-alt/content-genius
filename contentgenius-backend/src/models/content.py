from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ContentRequest(db.Model):
    __tablename__ = 'content_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(100), nullable=True)
    content_type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    keywords = db.Column(db.String(500), nullable=True)
    tone = db.Column(db.String(50), nullable=True)
    target_audience = db.Column(db.String(200), nullable=True)
    word_count = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, review, completed, delivered
    ai_generated_content = db.Column(db.Text, nullable=True)
    final_content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_name': self.client_name,
            'client_email': self.client_email,
            'company': self.company,
            'content_type': self.content_type,
            'title': self.title,
            'description': self.description,
            'keywords': self.keywords,
            'tone': self.tone,
            'target_audience': self.target_audience,
            'word_count': self.word_count,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    company = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    subscription_plan = db.Column(db.String(20), default='starter')  # starter, professional, enterprise
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'company': self.company,
            'phone': self.phone,
            'subscription_plan': self.subscription_plan,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

