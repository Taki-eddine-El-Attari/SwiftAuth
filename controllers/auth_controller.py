from flask import session, flash, redirect, url_for
from models.user import User, db
from utils.cache import cache

class AuthController:
    @staticmethod
    # Gère l'inscription d'un nouvel utilisateur
    def register_user(email, username, password, confirm_password):
        # Validation des champs obligatoires
        if not email or not username or not password or not confirm_password:
            return False, "Tous les champs sont obligatoires"
            
        # Vérification de la correspondance des mots de passe
        if password != confirm_password:
            return False, "Les mots de passe ne correspondent pas"
            
        # Vérification de l'unicité de l'email
        existing_user = User.find_by_email(email)
        if existing_user:
            return False, "Cet email est déjà enregistré"
            
        # Création du nouvel utilisateur
        try:
            new_user = User(email=email, username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return True, "Inscription réussie ! Veuillez vous connecter."
        except Exception as e:
            db.session.rollback()
            return False, f"Échec de l'inscription : {str(e)}"
    
    @staticmethod
    
    # Gère la connexion d'un utilisateur
    def login_user(email, password, remember=False):
        # Validation des champs obligatoires
        if not email or not password:
            return False, "Email et mot de passe requis"
            
        # Vérification des identifiants
        user = User.find_by_email(email)
        if not user or not user.check_password(password):
            return False, "Email ou mot de passe invalide"
            
        # Mise à jour de la date de dernière connexion
        user.update_last_login()
        
        # Configuration de la session
        session['user_id'] = user.id
        session['username'] = user.username
        session.permanent = remember
        
        # Mise en cache des données utilisateur
        cache.set(f'user_{user.id}', user.to_dict(), timeout=300)
        
        return True, "Connexion réussie !"
    
    @staticmethod

    # Gère la déconnexion d'un utilisateur
    def logout_user():
        # Nettoyage du cache
        if 'user_id' in session:
            cache.delete(f'user_{session["user_id"]}')
            
        # Nettoyage de la session
        session.clear()
        return True, "Déconnexion réussie"
    
    @staticmethod

    # Vérifie si l'utilisateur est connecté
    def get_current_user():
        if 'user_id' not in session:
            return None
            
        user_id = session['user_id']
        
        # Tentative de récupération depuis le cache
        cached_user = cache.get(f'user_{user_id}')
        if cached_user:
            return cached_user
            
        # Récupération depuis la base de données si absent du cache
        user = User.query.get(user_id)
        if user:
            user_data = user.to_dict()
            cache.set(f'user_{user_id}', user_data, timeout=300)
            return user_data
            
        return None
