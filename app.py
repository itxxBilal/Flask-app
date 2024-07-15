from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=True)

@app.before_request
def create_tables():
    if not hasattr(app, 'has_created_tables'):
        db.create_all()
        app.has_created_tables = True

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_message = Message(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/about')
def about():
    projects = Project.query.all()
    return render_template('about.html', projects=projects)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    projects = Project.query.all()
    return render_template('dashboard.html', messages=messages, projects=projects)

@app.route('/add_project', methods=['POST'])
def add_project():
    name = request.form['name']
    link = request.form['link']
    description = request.form['description']
    image = request.files.get('image', None)
    
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        image_url = os.path.join('uploads', filename)
    else:
        image_url = None
    
    new_project = Project(name=name, link=link, description=description, image=image_url)
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], project.image.split('/')[-1])
        if os.path.exists(image_path):
            os.remove(image_path)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/update_project/<int:project_id>', methods=['POST'])
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    project.name = request.form['name']
    project.link = request.form['link']
    project.description = request.form['description']
    image = request.files.get('image', None)
    
    if image:
        if project.image:
            old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], project.image.split('/')[-1])
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        project.image = os.path.join('uploads', filename)
    
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
