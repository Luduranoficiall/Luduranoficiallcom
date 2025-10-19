from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ceo-premium-2025-ultra-seguro-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_professional.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ==================== MODELS ====================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(500))
    icon = db.Column(db.String(50), default='code')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SiteStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_contacts = db.Column(db.Integer, default=0)
    unread_contacts = db.Column(db.Integer, default=0)
    total_posts = db.Column(db.Integer, default=0)
    total_projects = db.Column(db.Integer, default=0)
    pending_appointments = db.Column(db.Integer, default=0)
    confirmed_appointments = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== ROUTES - PUBLIC ====================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()
        
        flash('Mensagem enviada com sucesso! Responderemos em breve.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/blog')
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('blog_post.html', post=post)

@app.route('/portfolio')
def portfolio():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('portfolio.html', projects=projects)

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date_str = request.form.get('date')
        time = request.form.get('time')
        message = request.form.get('message')
        
        # Converte a string de data para objeto date
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        new_appointment = Appointment(
            name=name,
            email=email,
            phone=phone,
            date=date_obj,
            time=time,
            message=message
        )
        db.session.add(new_appointment)
        db.session.commit()
        
        flash('Agendamento realizado com sucesso! Entraremos em contato para confirmar.', 'success')
        return redirect(url_for('schedule'))
    
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('schedule.html', today=today)

# ==================== ROUTES - AUTH (SÓ PARA CEO) ====================

@app.route('/ceo-login-ultra-secreto-2025', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Usuário ou senha inválidos!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('home'))

# ==================== ROUTES - ADMIN (SÓ CEO) ====================

@app.route('/admin')
@login_required
def admin_dashboard():
    # Calcula estatísticas em tempo real
    stats = {
        'total_contacts': Contact.query.count(),
        'unread_contacts': Contact.query.filter_by(read=False).count(),
        'total_posts': BlogPost.query.count(),
        'total_projects': Project.query.count(),
        'pending_appointments': Appointment.query.filter_by(status='pending').count(),
        'confirmed_appointments': Appointment.query.filter_by(status='confirmed').count()
    }
    
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    recent_appointments = Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc()).limit(5).all()
    
    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_contacts=recent_contacts,
        recent_appointments=recent_appointments
    )

@app.route('/admin/contacts')
@login_required
def admin_contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)

@app.route('/admin/contacts/<int:contact_id>/read', methods=['POST'])
@login_required
def mark_contact_read(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    contact.read = True
    db.session.commit()
    flash('Mensagem marcada como lida!', 'success')
    return redirect(url_for('admin_contacts'))

@app.route('/admin/contacts/<int:contact_id>/delete', methods=['POST'])
@login_required
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    flash('Mensagem excluída com sucesso!', 'success')
    return redirect(url_for('admin_contacts'))

@app.route('/admin/blog')
@login_required
def admin_blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blog.html', posts=posts)

@app.route('/admin/blog/new', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        new_post = BlogPost(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        
        flash('Post criado com sucesso!', 'success')
        return redirect(url_for('admin_blog'))
    
    return render_template('admin/blog_form.html', post=None)

@app.route('/admin/blog/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        db.session.commit()
        
        flash('Post atualizado com sucesso!', 'success')
        return redirect(url_for('admin_blog'))
    
    return render_template('admin/blog_form.html', post=post)

@app.route('/admin/blog/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post excluído com sucesso!', 'success')
    return redirect(url_for('admin_blog'))

@app.route('/admin/projects')
@login_required
def admin_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=projects)

@app.route('/admin/projects/new', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        tech_stack = request.form.get('tech_stack')
        icon = request.form.get('icon') or 'code'
        
        new_project = Project(
            title=title,
            description=description,
            tech_stack=tech_stack,
            icon=icon
        )
        db.session.add(new_project)
        db.session.commit()
        
        flash('Projeto adicionado com sucesso!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/project_form.html', project=None)

@app.route('/admin/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.tech_stack = request.form.get('tech_stack')
        project.icon = request.form.get('icon') or 'code'
        db.session.commit()
        
        flash('Projeto atualizado com sucesso!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/project_form.html', project=project)

@app.route('/admin/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Projeto excluído com sucesso!', 'success')
    return redirect(url_for('admin_projects'))

@app.route('/admin/appointments')
@login_required
def admin_appointments():
    appointments = Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    return render_template('admin/appointments.html', appointments=appointments)

@app.route('/admin/appointments/<int:appointment_id>/confirm', methods=['POST'])
@login_required
def confirm_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = 'confirmed'
    db.session.commit()
    flash('Agendamento confirmado!', 'success')
    return redirect(url_for('admin_appointments'))

@app.route('/admin/appointments/<int:appointment_id>/cancel', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = 'cancelled'
    db.session.commit()
    flash('Agendamento cancelado!', 'warning')
    return redirect(url_for('admin_appointments'))

@app.route('/admin/appointments/<int:appointment_id>/delete', methods=['POST'])
@login_required
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Agendamento excluído!', 'success')
    return redirect(url_for('admin_appointments'))

# ==================== INITIALIZE ====================

def init_db():
    with app.app_context():
        db.create_all()
        
        # Cria usuário CEO se não existir
        if not User.query.filter_by(username='CEO').first():
            ceo = User(username='CEO', email='ceo@seusite.com')
            ceo.set_password('CEO2025@Premium')
            db.session.add(ceo)
            db.session.commit()
            print('✅ USUÁRIO CEO CRIADO!')
            print('🔐 Username: CEO')
            print('🔑 Senha: CEO2025@Premium')
            print('⚠️  URL DE ACESSO: http://127.0.0.1:5000/ceo-login-ultra-secreto-2025')
            print('⚠️  ESTA URL É SECRETA! Não compartilhe com ninguém!')

if __name__ == '__main__':
    init_db()
    print('\n' + '='*70)
    print('🚀 SITE PROFISSIONAL PREMIUM - VERSÃO CEO')
    print('='*70)
    print('\n🌐 SITE PÚBLICO: http://127.0.0.1:5000')
    print('🔐 PAINEL CEO (SECRETO): http://127.0.0.1:5000/ceo-login-ultra-secreto-2025')
    print('\n📋 CREDENCIAIS DO CEO:')
    print('   👤 Username: CEO')
    print('   🔑 Senha: CEO2025@Premium')
    print('\n⚠️  O LINK DE LOGIN É SECRETO - Não aparece no menu público!')
    print('='*70 + '\n')
    app.run(debug=True, port=5000, host='127.0.0.1')
