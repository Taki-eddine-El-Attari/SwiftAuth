from flask import session, flash, redirect, url_for
from models.user import User, db
from utils.cache import cache

class AuthController:
    @staticmethod
    def register_user(email, username, password, confirm_password):
        # Validate input
        if not email or not username or not password or not confirm_password:
            return False, "All fields are required"
            
        if password != confirm_password:
            return False, "Passwords do not match"
            
        # Check if user already exists
        existing_user = User.find_by_email(email)
        if existing_user:
            return False, "Email already registered"
            
        # Create new user
        try:
            new_user = User(email=email, username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return True, "Registration successful! Please login."
        except Exception as e:
            db.session.rollback()
            return False, f"Registration failed: {str(e)}"
    
    @staticmethod
    def login_user(email, password, remember=False):
        # Validate input
        if not email or not password:
            return False, "Email and password are required"
            
        # Check if user exists
        user = User.find_by_email(email)
        if not user or not user.check_password(password):
            return False, "Invalid email or password"
            
        # Update login timestamp
        user.update_last_login()
        
        # Set session
        session['user_id'] = user.id
        session['username'] = user.username
        session.permanent = remember
        
        # Cache user data
        cache.set(f'user_{user.id}', user.to_dict(), timeout=300)
        
        return True, "Login successful!"
    
    @staticmethod
    def logout_user():
        # Clear cache
        if 'user_id' in session:
            cache.delete(f'user_{session["user_id"]}')
            
        # Clear session
        session.clear()
        return True, "Logged out successfully"
    
    @staticmethod
    def get_current_user():
        if 'user_id' not in session:
            return None
            
        user_id = session['user_id']
        
        # Try to get user from cache
        cached_user = cache.get(f'user_{user_id}')
        if cached_user:
            return cached_user
            
        # Get from database if not in cache
        user = User.query.get(user_id)
        if user:
            user_data = user.to_dict()
            cache.set(f'user_{user_id}', user_data, timeout=300)
            return user_data
            
        return None
