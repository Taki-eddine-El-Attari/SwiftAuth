from functools import wraps
from flask import session, redirect, url_for, flash

# Décorateur pour vérifier si l'utilisateur est connecté
def login_required(f):
   
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Veuillez vous connecter pour accéder à cette page', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
