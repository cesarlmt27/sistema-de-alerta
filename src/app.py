from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_login import LoginManager, current_user
from datetime import datetime
from sqlalchemy import literal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:N1d44@localhost/Proyectos en Tic'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = app.config['SECRET_KEY']
app.debug = True
db = SQLAlchemy(app)
login_manager = LoginManager()

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    arduino_asignado = db.Column(db.String(255), db.ForeignKey('arduino.name'))

#sensor asignado a un Arduino
#completar arduino

class Arduino(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
def __init__(self, name, description):
    self.name = name
    self.description = description

class Sensor1(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fecha = db.Column(db.DateTime())
    temperatura = db.Column(db.Float())
    arduino_asignado = db.Column(db.String(255), db.ForeignKey('arduino.name'))
def __init__(self, fecha, temperatura, arduino_asignado):
    self.fecha = fecha
    self.temperatura = temperatura
    self.arduino_asignado = arduino_asignado
class Sensor2(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fecha = db.Column(db.DateTime())
    humedad = db.Column(db.Float())
    arduino_asignado = db.Column(db.String(255), db.ForeignKey('arduino.name'))
def __init__(self, fecha, humedad, arduino_asignado):
    self.fecha = fecha
    self.humedad = humedad
    self.arduino_asignado = arduino_asignado
    

#FALTAN SENSORES
new_sensor1 = Sensor1(fecha=datetime.now(), temperatura=25.5, arduino_asignado='Arduino1')
# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

#create a user to test with


@app.route('/')
def index():
    
    return render_template('index.html')


@app.route('/test_add_values', methods=['GET', 'POST'])
@login_required
def test_add_values():
    return render_template('test_add_values.html')

@app.route('/test_add_data', methods=['POST'])
@login_required
def test_add_data():
    if request.form['num']== '1':

        data2 = request.form['temp']
        fecha = datetime.now()
        arduino_asignado = request.form['arduino_asignado']
        new_sensor1 = Sensor1(fecha=fecha, temperatura=data2, arduino_asignado= arduino_asignado)
        db.session.add(new_sensor1)
        db.session.commit()

        return render_template('index.html')
        
    if request.form['num']== '2':

        data2 = request.form['temp']
        fecha = datetime.now()
        arduino_asignado = request.form['arduino_asignado']
        new_sensor2 = Sensor2(fecha=fecha, humedad=data2, arduino_asignado= arduino_asignado)
        db.session.add(new_sensor2)
        db.session.commit()

        return render_template('index.html')

    return render_template('index.html')


    
           

#EL EN FUTURO RENDERIZAR OTRA DIRECCION HTML EN LA QUE DIGA SE HAN ENCONTRADO X ALERTAS 


#OBSOLETO - FLASK TIENE UNO MEJOR
@app.route('/adduser', methods=['GET','POST'])
def add_user():
    return render_template('adduser.html')



@app.route('/ver_datos', methods=['GET','POST'])
@login_required
def ver_datos(arduino_actual):
    
    sensortemp = Sensor1.query.filter_by(arduino_asignado=arduino_actual).all()
    sensorhumedad = Sensor2.query.filter_by(arduino_asignado=arduino_actual).all()

    #agregar los demas sensores
    return render_template('ver_datos.html', sensortemp=sensortemp,sensorhumedad=sensorhumedad, arduino_actual=arduino_actual) 


@app.route('/verificación_arduino', methods=['GET','POST'])
@login_required
def checkeo_datos():
    user = User.query.filter_by(email=current_user.email).first()
    if user.arduino_asignado == None:
        return render_template('add_arduino.html')
    else:

        #se entregan datos de sensores
        arduino_actual = user.arduino_asignado
        return ver_datos(arduino_actual)
    
   
@app.route('/new_arduino', methods=['POST'])
@login_required
def asignar_arduino():
    #se comprueba si existe el arduino y se asigna al usuario
    nuevoarduino=request.form['arduino']
    arduino = Arduino.query.filter_by(name=nuevoarduino).first()
    
    if arduino == None:
        myUser = User.query.filter_by(email=current_user.email).first()
        myUser.arduino_asignado = nuevoarduino
        new_arduino = Arduino(name=nuevoarduino, description= "Arduino asignado a " + current_user.email)
        db.session.add(new_arduino)
        db.session.commit()
           
    
    return render_template('index.html')

#info de usuario -NO TERMINADO-
@app.route('/profile/<string:email>')
@login_required
def profile(email):
    user = User.query.filter_by(email=email).first()
    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.run()
