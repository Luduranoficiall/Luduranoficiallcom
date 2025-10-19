from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'seu-secret-key-super-seguro-premium-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_professional.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ==================== MODELS ====================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
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
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(300))
    category = db.Column(db.String(50))
    tags = db.Column(db.String(200))
    image_url = db.Column(db.String(300))
    views = db.Column(db.Integer, default=0)
    published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(300))
    image_url = db.Column(db.String(300))
    project_url = db.Column(db.String(300))
    github_url = db.Column(db.String(300))
    featured = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    appointment_type = db.Column(db.String(50), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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
        
        flash('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/blog')
def blog():
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug).first_or_404()
    post.views += 1
    db.session.commit()
    return render_template('blog_post.html', post=post)

@app.route('/portfolio')
def portfolio():
    projects = Project.query.order_by(Project.order.asc()).all()
    return render_template('portfolio.html', projects=projects)

@app.route('/agendar', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        appointment_type = request.form.get('appointment_type')
        appointment_date = datetime.strptime(request.form.get('appointment_date'), '%Y-%m-%dT%H:%M')
        description = request.form.get('description')
        
        new_appointment = Appointment(
            name=name,
            email=email,
            phone=phone,
            appointment_type=appointment_type,
            appointment_date=appointment_date,
            description=description
        )
        db.session.add(new_appointment)
        db.session.commit()
        
        flash('Agendamento realizado com sucesso! Você receberá uma confirmação por email.', 'success')
        return redirect(url_for('schedule'))
    
    return render_template('schedule.html')

# ==================== ROUTES - AUTH ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Usuário ou senha inválidos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# ==================== ROUTES - ADMIN ====================

@app.route('/admin')
@login_required
def admin_dashboard():
    total_contacts = Contact.query.count()
    unread_contacts = Contact.query.filter_by(is_read=False).count()
    total_posts = BlogPost.query.count()
    total_appointments = Appointment.query.count()
    pending_appointments = Appointment.query.filter_by(status='pending').count()
    
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
        total_contacts=total_contacts,
        unread_contacts=unread_contacts,
        total_posts=total_posts,
        total_appointments=total_appointments,
        pending_appointments=pending_appointments,
        recent_contacts=recent_contacts,
        recent_appointments=recent_appointments
    )

@app.route('/admin/contacts')
@login_required
def admin_contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)

@app.route('/admin/contacts/<int:id>/read')
@login_required
def admin_contact_read(id):
    contact = Contact.query.get_or_404(id)
    contact.is_read = True
    db.session.commit()
    return redirect(url_for('admin_contacts'))

@app.route('/admin/blog')
@login_required
def admin_blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blog.html', posts=posts)

@app.route('/admin/blog/new', methods=['GET', 'POST'])
@login_required
def admin_blog_new():
    if request.method == 'POST':
        title = request.form.get('title')
        slug = request.form.get('slug')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        category = request.form.get('category')
        tags = request.form.get('tags')
        published = request.form.get('published') == 'on'
        
        new_post = BlogPost(
            title=title,
            slug=slug,
            content=content,
            excerpt=excerpt,
            category=category,
            tags=tags,
            published=published
        )
        db.session.add(new_post)
        db.session.commit()
        
        flash('Post criado com sucesso!', 'success')
        return redirect(url_for('admin_blog'))
    
    return render_template('admin/blog_form.html', post=None)

@app.route('/admin/blog/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_blog_edit(id):
    post = BlogPost.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.slug = request.form.get('slug')
        post.content = request.form.get('content')
        post.excerpt = request.form.get('excerpt')
        post.category = request.form.get('category')
        post.tags = request.form.get('tags')
        post.published = request.form.get('published') == 'on'
        
        db.session.commit()
        flash('Post atualizado com sucesso!', 'success')
        return redirect(url_for('admin_blog'))
    
    return render_template('admin/blog_form.html', post=post)

@app.route('/admin/projects')
@login_required
def admin_projects():
    projects = Project.query.order_by(Project.order.asc()).all()
    return render_template('admin/projects.html', projects=projects)

@app.route('/admin/projects/new', methods=['GET', 'POST'])
@login_required
def admin_project_new():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        technologies = request.form.get('technologies')
        project_url = request.form.get('project_url')
        github_url = request.form.get('github_url')
        featured = request.form.get('featured') == 'on'
        
        new_project = Project(
            title=title,
            description=description,
            technologies=technologies,
            project_url=project_url,
            github_url=github_url,
            featured=featured
        )
        db.session.add(new_project)
        db.session.commit()
        
        flash('Projeto adicionado com sucesso!', 'success')
        return redirect(url_for('admin_projects'))
    
    return render_template('admin/project_form.html', project=None)

@app.route('/admin/appointments')
@login_required
def admin_appointments():
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    return render_template('admin/appointments.html', appointments=appointments)

@app.route('/admin/appointments/<int:id>/confirm')
@login_required
def admin_appointment_confirm(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = 'confirmed'
    db.session.commit()
    flash('Agendamento confirmado!', 'success')
    return redirect(url_for('admin_appointments'))

@app.route('/admin/appointments/<int:id>/cancel')
@login_required
def admin_appointment_cancel(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = 'cancelled'
    db.session.commit()
    flash('Agendamento cancelado!', 'warning')
    return redirect(url_for('admin_appointments'))

# ==================== API ROUTES ====================

@app.route('/api/appointments/available', methods=['GET'])
def api_available_slots():
    date = request.args.get('date')
    available_slots = [
        '09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00'
    ]
    return jsonify(available_slots)

# ==================== INITIALIZE ====================

def init_db():
    with app.app_context():
        db.create_all()
        
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@seusite.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('✅ Usuário admin criado! Username: admin, Senha: admin123')
            print('⚠️  IMPORTANTE: Altere a senha após o primeiro login!')

if __name__ == '__main__':
    init_db()
    print('\n' + '='*60)
    print('🚀 SITE PROFISSIONAL PREMIUM INICIADO!')
    print('='*60)
    print('\n🌐 Acesso ao Site: http://127.0.0.1:5000')
    print('🔐 Acesso Admin: http://127.0.0.1:5000/login')
    print('\n📋 Credenciais Admin:')
    print('   Usuário: admin')
    print('   Senha: admin123')
    print('\n' + '='*60 + '\n')
    app.run(debug=True, port=5000)