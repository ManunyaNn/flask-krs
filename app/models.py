from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app import db
from app.utils import get_youtube_thumbnail


class User(UserMixin, db.Model):
    """Модель пользователя"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' или 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связь с видео (один ко многим)
    videos = db.relationship('Video', backref='author', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Map(db.Model):
    """Модель карты CS2"""
    __tablename__ = 'maps'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    display_name = db.Column(db.String(64), nullable=False)
    
    # Связь с видео (один ко многим)
    videos = db.relationship('Video', backref='map', lazy=True)
    
    def __repr__(self):
        return f'<Map {self.display_name}>'

class Grenade(db.Model):
    """Модель типа гранаты"""
    __tablename__ = 'grenades'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    display_name = db.Column(db.String(64), nullable=False)
    color = db.Column(db.String(20))  # для визуального отличия
    
    # Связь с видео (один ко многим)
    videos = db.relationship('Video', backref='grenade', lazy=True)
    
    def __repr__(self):
        return f'<Grenade {self.display_name}>'

class Video(db.Model):
    """Модель видео с раскидкой гранаты"""
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(500), nullable=False)  # ссылка на YouTube и т.д.
    thumbnail_url = db.Column(db.String(500))  # превью видео
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Внешние ключи
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    map_id = db.Column(db.Integer, db.ForeignKey('maps.id'), nullable=False)
    grenade_id = db.Column(db.Integer, db.ForeignKey('grenades.id'), nullable=False)
    
    def __repr__(self):
        return f'<Video {self.title}>'
    
    def __init__(self, **kwargs):
        super(Video, self).__init__(**kwargs)
        # АВТОМАТИЧЕСКИ ГЕНЕРИРУЕМ ПРЕВЬЮ ПРИ СОЗДАНИИ ОБЪЕКТА
        if self.video_url and not self.thumbnail_url:
            self.thumbnail_url = get_youtube_thumbnail(self.video_url, quality='hqdefault')