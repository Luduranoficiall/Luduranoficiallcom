from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
    jsonify,
    make_response
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from datetime import datetime, date
from sqlalchemy import func
from io import StringIO
import csv
import json
import os

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = 'ceo-premium-2025-ultra-seguro-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_professional.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', '')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])
app.config['CEO_EMAIL'] = os.getenv('CEO_EMAIL', 'contato@luduranoficiall.com')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

MONTHS_PT = [
    'janeiro',
    'fevereiro',
    'março',
    'abril',
    'maio',
    'junho',
    'julho',
    'agosto',
    'setembro',
    'outubro',
    'novembro',
    'dezembro'
]


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def save_uploaded_file(file_storage, subfolder: str) -> str | None:
    if not file_storage or file_storage.filename == '' or not allowed_file(file_storage.filename):
        return None

    filename = secure_filename(file_storage.filename)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    new_filename = f"{timestamp}_{filename}"
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(folder_path, exist_ok=True)
    full_path = os.path.join(folder_path, new_filename)
    file_storage.save(full_path)
    static_folder = os.path.join(app.root_path, 'static')
    relative_path = os.path.relpath(full_path, static_folder)
    return relative_path.replace('\\', '/')


def export_csv(filename: str, headers: list[str], rows: list[list[str]]):
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(headers)
    writer.writerows(rows)
    response = make_response(buffer.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    return response


@app.template_filter('data_extenso_pt')
def data_extenso_pt(value: datetime | date | None) -> str:
    if not value:
        return ''
    if isinstance(value, datetime):
        base_date = value.date()
    else:
        base_date = value
    month_name = MONTHS_PT[base_date.month - 1]
    return f"{base_date.day:02d} de {month_name} de {base_date.year}"


@app.template_filter('data_hora_pt')
def data_hora_pt(value: datetime | None) -> str:
    if not value:
        return ''
    return value.strftime('%d/%m/%Y às %H:%M')

# ==================== MODELOS ====================

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
    excerpt = db.Column(db.String(400))
    cover_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(500))
    icon = db.Column(db.String(50), default='code')
    image_path = db.Column(db.String(255))
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


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=True)

    post = db.relationship('BlogPost', backref=db.backref('comments', lazy=True))

class SiteStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_contacts = db.Column(db.Integer, default=0)
    unread_contacts = db.Column(db.Integer, default=0)
    total_posts = db.Column(db.Integer, default=0)
    total_projects = db.Column(db.Integer, default=0)
    pending_appointments = db.Column(db.Integer, default=0)
    confirmed_appointments = db.Column(db.Integer, default=0)


class SiteMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, default=date.today)
    page_views = db.Column(db.Integer, default=0)
    contact_submissions = db.Column(db.Integer, default=0)
    appointments_created = db.Column(db.Integer, default=0)
    blog_comments = db.Column(db.Integer, default=0)


def get_or_create_metric(target_date: date | None = None) -> SiteMetric:
    if target_date is None:
        target_date = date.today()
    metric = SiteMetric.query.filter_by(date=target_date).first()
    if not metric:
        metric = SiteMetric(date=target_date)
        db.session.add(metric)
        db.session.commit()
    return metric


def send_notification_email(subject: str, body: str) -> None:
    if not app.config['MAIL_SERVER'] or not app.config['MAIL_USERNAME']:
        app.logger.info('[EMAIL MOCK] %s -> %s\n%s', subject, app.config['CEO_EMAIL'], body)
        return

    try:
        msg = Message(subject=subject, recipients=[app.config['CEO_EMAIL']])
        msg.body = body
        mail.send(msg)
    except Exception as exc:  # pylint: disable=broad-except
        app.logger.error('Falha ao enviar email: %s', exc)


@app.before_request
def track_metrics():
    if request.endpoint in ('static', None):
        return
    if request.path.startswith('/admin') or request.path.startswith('/ceo-login'):
        return
    if request.method == 'GET':
        metric = get_or_create_metric()
        metric.page_views += 1
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== ROTAS - PÚBLICO ====================

@app.route('/')
def home():
    projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(3).all()
    return render_template('index.html', projects=projects, posts=posts)

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        message = (request.form.get('message') or '').strip()

        if not all([name, email, message]):
            flash('Preencha todos os campos antes de enviar sua mensagem.', 'error')
            return redirect(url_for('contact'))
        
        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()

        metric = get_or_create_metric()
        metric.contact_submissions += 1
        db.session.commit()

        email_body = (
            f"Nova mensagem recebida no site profissional:\n\n"
            f"Nome: {name}\n"
            f"Email: {email}\n"
            f"Mensagem:\n{message}\n\n"
            f"Data: {datetime.utcnow().strftime('%d/%m/%Y %H:%M')}"
        )
        send_notification_email('Novo contato no site', email_body)
        
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
    comments = Comment.query.filter_by(post_id=post_id, approved=True).order_by(Comment.created_at.desc()).all()
    return render_template('blog_post.html', post=post, comments=comments)


@app.route('/blog/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    post = BlogPost.query.get_or_404(post_id)
    name = (request.form.get('name') or '').strip()
    email = (request.form.get('email') or '').strip()
    message = (request.form.get('message') or '').strip()

    if not all([name, email, message]):
        flash('Preencha todos os campos para enviar seu comentário.', 'error')
        return redirect(url_for('blog_post', post_id=post.id))

    comment = Comment(post_id=post.id, name=name, email=email, message=message)
    db.session.add(comment)
    db.session.commit()

    metric = get_or_create_metric()
    metric.blog_comments += 1
    db.session.commit()

    email_body = (
        f"Novo comentário no blog:\n\n"
        f"Post: {post.title}\n"
        f"Nome: {name}\n"
        f"Email: {email}\n\n"
        f"Mensagem:\n{message}\n"
    )
    send_notification_email('Novo comentário no blog', email_body)

    flash('Comentário enviado com sucesso! Obrigado por participar da conversa.', 'success')
    return redirect(url_for('blog_post', post_id=post.id) + '#comentarios')

@app.route('/portfolio')
def portfolio():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('portfolio.html', projects=projects)

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        phone = (request.form.get('phone') or '').strip()
        date_str = (request.form.get('date') or '').strip()
        time = (request.form.get('time') or '').strip()
        message = (request.form.get('message') or '').strip()

        if not all([name, email, phone, date_str, time, message]):
            flash('Preencha todos os campos para concluir o agendamento.', 'error')
            return redirect(url_for('schedule'))
        
        # Converte a string de data para objeto date
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Informe uma data válida para o agendamento.', 'error')
            return redirect(url_for('schedule'))
        
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

        metric = get_or_create_metric()
        metric.appointments_created += 1
        db.session.commit()

        email_body = (
            f"Novo agendamento recebido no site profissional:\n\n"
            f"Nome: {name}\n"
            f"Email: {email}\n"
            f"Telefone: {phone}\n"
            f"Data: {date_obj.strftime('%d/%m/%Y')}\n"
            f"Horário: {time}\n\n"
            f"Mensagem:\n{message}"
        )
        send_notification_email('Novo agendamento no site', email_body)
        
        flash('Agendamento realizado com sucesso! Entraremos em contato para confirmar.', 'success')
        return redirect(url_for('schedule'))
    
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('schedule.html', today=today)

# ==================== ROTAS - AUTENTICAÇÃO (APENAS CEO) ====================

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

# ==================== ROTAS - ÁREA ADMINISTRATIVA (APENAS CEO) ====================

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

    metrics = SiteMetric.query.order_by(SiteMetric.date.desc()).limit(14).all()
    metrics.reverse()
    chart_labels = [m.date.strftime('%d/%m') for m in metrics]
    chart_page_views = [m.page_views for m in metrics]
    chart_contacts = [m.contact_submissions for m in metrics]
    chart_appointments = [m.appointments_created for m in metrics]
    chart_comments = [m.blog_comments for m in metrics]

    popular_posts = (
        db.session.query(BlogPost, func.count(Comment.id).label('comment_total'))
        .outerjoin(Comment)
        .group_by(BlogPost.id)
        .order_by(func.count(Comment.id).desc())
        .limit(5)
        .all()
    )

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_contacts=recent_contacts,
        recent_appointments=recent_appointments,
        chart_labels=json.dumps(chart_labels, ensure_ascii=False),
        chart_page_views=json.dumps(chart_page_views),
        chart_contacts=json.dumps(chart_contacts),
        chart_appointments=json.dumps(chart_appointments),
        chart_comments=json.dumps(chart_comments),
        popular_posts=popular_posts
    )

@app.route('/admin/contacts')
@login_required
def admin_contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)


@app.route('/admin/export/contacts')
@login_required
def export_contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    rows = [
        [
            contact.id,
            contact.name,
            contact.email,
            contact.message,
            'Sim' if contact.read else 'Não',
            contact.created_at.strftime('%d/%m/%Y %H:%M')
        ]
        for contact in contacts
    ]
    headers = ['ID', 'Nome', 'Email', 'Mensagem', 'Lida', 'Recebida em']
    return export_csv('contatos.csv', headers, rows)

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
        excerpt = request.form.get('excerpt') or content[:180]
        cover_image = save_uploaded_file(request.files.get('cover_image'), 'blog')
        
        new_post = BlogPost(title=title, content=content, excerpt=excerpt)
        if cover_image:
            new_post.cover_image = cover_image
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
        post.excerpt = request.form.get('excerpt') or post.content[:180]
        new_cover = save_uploaded_file(request.files.get('cover_image'), 'blog')
        if new_cover:
            post.cover_image = new_cover
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


@app.route('/admin/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comentário removido com sucesso!', 'success')
    return redirect(request.referrer or url_for('admin_blog'))

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
        image = save_uploaded_file(request.files.get('image'), 'projects')
        
        new_project = Project(
            title=title,
            description=description,
            tech_stack=tech_stack,
            icon=icon
        )
        if image:
            new_project.image_path = image
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
        new_image = save_uploaded_file(request.files.get('image'), 'projects')
        if new_image:
            project.image_path = new_image
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
    appointments_events = [
        {
            'title': appointment.name,
            'start': datetime.combine(appointment.date, datetime.strptime(appointment.time, '%H:%M').time()).isoformat(),
            'extendedProps': {
                'email': appointment.email,
                'phone': appointment.phone,
                'message': appointment.message,
                'status': appointment.status
            }
        }
        for appointment in appointments
    ]
    return render_template('admin/appointments.html', appointments=appointments, appointments_events=json.dumps(appointments_events))

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


@app.route('/admin/export/appointments')
@login_required
def export_appointments():
    appointments = Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    rows = [
        [
            appointment.id,
            appointment.name,
            appointment.email,
            appointment.phone,
            appointment.date.strftime('%d/%m/%Y'),
            appointment.time,
            appointment.status,
            appointment.message
        ]
        for appointment in appointments
    ]
    headers = ['ID', 'Nome', 'Email', 'Telefone', 'Data', 'Hora', 'Status', 'Mensagem']
    return export_csv('agendamentos.csv', headers, rows)

# ==================== INICIALIZAÇÃO ====================

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
