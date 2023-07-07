from flask import Blueprint, request, render_template, redirect

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.form.get('email')
    if not email:
        return redirect('/login')
    
    
    return redirect('/')

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    #clear cookies and session
    return redirect('/')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    email = request.form.get('email')
    
    
    return redirect('/')