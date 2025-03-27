from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controllers.auth_controller import AuthController
from utils.decorators import login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('auth.profile'))
        
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
def login():
    if 'user_id' in session:
        return redirect(url_for('auth.profile'))
        
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
def logout():
    AuthController.logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    user_data = AuthController.get_current_user()
    return render_template('profile.html', user=user_data)
