from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from database import db
from forms import PersonasForm
from models import Persona

app = Flask(__name__)

#Configuracion de nuestra base de datos:
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'personas_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'


app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

#Flask migrate

migrate = Migrate()
migrate.init_app(app, db)

app.config['SECRET_KEY'] = 'mi_llave'




@app.route('/home')
def home ():
    personas = Persona.query.all()
    count = Persona.query.count()
    app.logger.debug(f'Cantidad de personas: {count}')
    app.logger.debug(f'Personas: {personas}')
    return render_template('home.html', personas=personas, count=count)


@app.route('/details/<int:id>')
def details(id):
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Details: {persona.id}')
    return render_template('details.html', persona=persona)

@app.route('/add', methods=['GET', 'POST'])
def add ():
    persona = Persona()
    form_persona = PersonasForm(obj=persona)
    if request.method  == 'POST':
        if form_persona.validate_on_submit():
            form_persona.populate_obj(persona)
            db.session.add(persona)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('add.html', persona = form_persona)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    persona = Persona.query.get_or_404(id)
    form_persona = PersonasForm(obj=persona)
    if request.method == 'POST':
        form_persona.validate_on_submit()
        form_persona.populate_obj(persona)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('update.html', persona=form_persona)


@app.route('/delete/<int:id>', methods=['GET', 'POST' ])
def delete(id):
    persona = Persona.query.get_or_404(id)
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('home'))