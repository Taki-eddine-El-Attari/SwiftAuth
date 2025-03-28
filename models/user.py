from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  # Nom de la table en base de données
    
    # Définition des colonnes
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Initialise un nouvel utilisateur avec hachage du mot de passe
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.set_password(password)
    
    # Hache et stocke le mot de passe de l'utilisateur
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # Vérifie si le mot de passe fourni correspond au hachage stocké
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Met à jour la date de dernière connexion de l'utilisateur
    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()

    # Convertit l'objet User en chaîne JSON pour sérialisation    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'created_at': self.created_at,
            'last_login': self.last_login
        }
        
    @classmethod
    
    # Recherche un utilisateur par son ID (méthode de classe)
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
