from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.auth_controller import AuthController
from utils.decorators import login_required

# Création du Blueprint pour les routes d'authentification
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])

# Gère l'inscription des utilisateurs
def register():
    # Si l'utilisateur est déjà connecté, redirection vers le profil
    if 'user_id' in session:
        return redirect(url_for('auth.profile'))
        
    # Traitement du formulaire d'inscription
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        success, message = AuthController.register_user(
            email, username, password, confirm_password
        )
        
        flash(message, 'success' if success else 'danger')
        
        if success:
            return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])

# Gère la connexion des utilisateurs
def login():
    # Si l'utilisateur est déjà connecté, redirection vers le profil
    if 'user_id' in session:
        return redirect(url_for('auth.profile'))
        
    # Traitement du formulaire de connexion
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        success, message = AuthController.login_user(email, password, remember)
        
        flash(message, 'success' if success else 'danger')
        
        if success:
            return redirect(url_for('auth.profile'))
    
    return render_template('login.html')

@auth_bp.route('/logout')

# Gère la déconnexion des utilisateurs
def logout():
    AuthController.logout_user()
    flash('Vous avez été déconnecté avec succès', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required

# Gère l'affichage du profil de l'utilisateur connecté
def profile():
    user_data = AuthController.get_current_user()
    return render_template('profile.html', user=user_data)
