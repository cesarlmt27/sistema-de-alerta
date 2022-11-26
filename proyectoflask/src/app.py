from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_login import LoginManager, current_user
from datetime import datetime, timezone
from sqlalchemy import literal
import pytz
from flask_mail import Mail, Message

#HAY QUE:
#1.- asignar todos los nuevos sensores y poder graficarlos + sus datos de distribucion
#2.- poder ver con admin los datos de todos los sensores (crear una pagina que imprima todos los sensores que solo pueda accederse con rol de admin)
#3.- parametros estandar de cada sensor (nueva base de datos)
#4.- agregar alerta de sensores al correo 
#5.- hacer posible que se asigne mas de un arduino a un usuario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:N1d44@localhost/Proyecto en Tic'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = app.config['SECRET_KEY']
app.debug = True
db = SQLAlchemy(app)
login_manager = LoginManager()


#configuracion del mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'proyectosenticcct1@gmail.com'
app.config['MAIL_PASSWORD'] = 'jmxrmrnltxyfhgqo'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

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

#sensor asignado a un Arduino
#completar arduino

class Arduino(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
def __init__(self, name, description):
    self.name = name
    self.description = description

#SENSOR TEMPERATURA
class Sensor1(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fecha = db.Column(db.DateTime())
    temperatura = db.Column(db.Float())
    arduino_asignado = db.Column(db.String(255), db.ForeignKey('arduino.name'))
def __init__(self, fecha, temperatura, arduino_asignado):
    self.fecha = fecha
    self.temperatura = temperatura
    self.arduino_asignado = arduino_asignado

#SENSOR LUMINOSIDAD
class Sensor2(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fecha = db.Column(db.DateTime())
    luminosidad = db.Column(db.Float())
    arduino_asignado = db.Column(db.String(255), db.ForeignKey('arduino.name'))
def __init__(self, fecha, luminosidad, arduino_asignado):
    self.fecha = fecha
    self.luminosidad = luminosidad
    self.arduino_asignado = arduino_asignado

#SENSOR MOVIMIENTO
class Sensor3(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fecha = db.Column(db.DateTime())
    movimiento = db.Column(db.Boolean())
    arduino_asignado = db.Column(db.String(255), db.ForeignKey('arduino.name'))
def __init__(self, fecha, movimiento, arduino_asignado):
    self.fecha = fecha
    self.movimiento = movimiento
    self.arduino_asignado = arduino_asignado

#SENSOR GAS
class Sensor4(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fecha = db.Column(db.DateTime())
    gas = db.Column(db.Float())
    arduino_asignado = db.Column(db.String(255), db.ForeignKey('arduino.name'))
def __init__(self, fecha, gas, arduino_asignado):
    self.fecha = fecha
    self.gas = gas
    self.arduino_asignado = arduino_asignado



#Dueños de arduino
class Owner(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    arduino_asignado = db.Column(db.String(255), db.ForeignKey('arduino.name'))
def __init__(self, owner_id, arduino_asignado):
    self.owner_id = owner_id
    self.arduino_asignado = arduino_asignado


class parametrosalerta(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    temperaturamin = db.Column(db.Float())
    temperaturamax = db.Column(db.Float())
    gasminimo = db.Column(db.Float())
    gasmaximo = db.Column(db.Float())
    movimiento = db.Column(db.Boolean())
    luminosidadmax = db.Column(db.Float())
    luminosidadmin = db.Column(db.Float())
    arduino_asignado = db.Column(db.String(255), db.ForeignKey('arduino.name'))
def __init__(self, temperaturamin, temperaturamax, gasminimo, gasmaximo, movimiento, luminosidadmax, luminosidadmin, arduino_asignado):
    self.temperaturamin = temperaturamin
    self.temperaturamax = temperaturamax
    self.gasminimo = gasminimo
    self.gasmaximo = gasmaximo
    self.movimiento = movimiento
    self.luminosidadmax = luminosidadmax
    self.luminosidadmin = luminosidadmin
    self.arduino_asignado = arduino_asignado



#FALTAN SENSORES
# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


local_tz = pytz.timezone('America/Santiago')
def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)
    
#create a user to test with

    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verificación_arduino_graficos', methods=['GET','POST'])
@login_required
def checkeo_datos_graficos():
    user = User.query.filter_by(email=current_user.email).first()
    owner = Owner.query.filter_by(owner_id=user.id).first()

    if owner == None:
        return render_template('add_arduino.html')
    else:

        #se entregan datos de sensores
        arduino_actual = owner.arduino_asignado
        return ver_graficos(arduino_actual)
    
 
@app.route('/ver_graficos', methods=['GET', 'POST'])
@login_required
def ver_graficos(arduino_actual):
    all_arduinos_From_user = Owner.query.filter_by(owner_id=current_user.id).all()
    user = User.query.filter_by(email=current_user.email).first()
    sensortemp = Sensor1.query.filter_by(arduino_asignado=arduino_actual).all()
    sensorluminosidad = Sensor2.query.filter_by(arduino_asignado=arduino_actual).all()
    sensormovimiento = Sensor3.query.filter_by(arduino_asignado=arduino_actual).all()
    sensorgas = Sensor4.query.filter_by(arduino_asignado=arduino_actual).all()
    labels1 = []
    values1 = []
    for i in sensortemp:
        labels1.append(str(i.fecha))
        values1.append((i.temperatura))
    labels2 = []
    values2 = []
    for i in sensorluminosidad:
        labels2.append(str(i.fecha))
        values2.append((i.luminosidad))
    #agregar los demas sensores
    labels3 = []
    values3 = []
    for i in sensormovimiento:
        labels3.append(str(i.fecha))
        values3.append((i.movimiento))
    labels4 = []
    values4 = []
    for i in sensorgas:
        labels4.append(str(i.fecha))
        values4.append((i.gas))

    return render_template('ver_graficos.html', labels1=labels1, values1=values1, labels2=labels2, values2=values2, labels3=labels3, values3=values3, labels4=labels4, values4=values4, all_arduinos_From_user=all_arduinos_From_user, arduino_actual=arduino_actual)

@app.route('/ver_mas_graficos', methods=['GET','POST'])
@login_required
def sellecionararduino_graficos():
    arduino_actual = request.form['arduinos']
    
    return ver_graficos(arduino_actual)


@app.route('/test_add_values', methods=['GET', 'POST'])
@login_required
def test_add_values():
    return render_template('test_add_values.html')

@app.route('/errorpage', methods=['GET', 'POST'])
@login_required
def errorpage(descripcionerror):
    return render_template('error.html', descripcionerror=descripcionerror)


#POSIBLEMENTE HAY QUE ELIMINAR ESTA FUNCION
@app.route('/test_add_data', methods=['POST'])
@login_required
def test_add_data():
    if request.form['num']== '1':
        
        data2 = request.form['temp']
        fecha = datetime.utcnow()
        arduino_asignado = request.form['arduino_asignado']
        new_sensor1 = Sensor1(fecha=fecha, temperatura=data2, arduino_asignado= arduino_asignado)
        db.session.add(new_sensor1)
        db.session.commit()

        return render_template('index.html')
        
    if request.form['num']== '2':

        data2 = request.form['temp']
        fecha = datetime.utcnow()
        arduino_asignado = request.form['arduino_asignado']
        new_sensor2 = Sensor2(fecha=fecha, luminosidad=data2, arduino_asignado= arduino_asignado)
        db.session.add(new_sensor2)
        db.session.commit()

        return render_template('index.html')

    return render_template('index.html')

#ENVIO DE CORREO
@app.route('/alerta_mail', methods=['GET', 'POST'])
@login_required
def alerta_mail():
    if request.method == 'POST':
        msg = Message('Alerta de temperatura', sender = 'noreply@demo.com', recipients = [current_user.email])
        msg.body = "La temperatura ha superado el limite establecido"
        mail.send(msg)
        return "Mail enviado"
    return render_template('index.html')
        

#EL EN FUTURO RENDERIZAR OTRA DIRECCION HTML EN LA QUE DIGA SE HAN ENCONTRADO X ALERTAS 


@app.route('/adduser', methods=['GET','POST'])
def add_user():
    return render_template('adduser.html')



@app.route('/ver_mas', methods=['GET','POST'])
@login_required
def seleccionararduino():
    arduino_actual = request.form['arduinos']
    
    return ver_datos(arduino_actual)



@app.route('/ver_datos', methods=['GET','POST'])
@login_required
def ver_datos(arduino_actual):
    
    all_arduinos_From_user = Owner.query.filter_by(owner_id=current_user.id).all()

    sensortemp = Sensor1.query.filter_by(arduino_asignado=arduino_actual).all()
    sensorluminosidad = Sensor2.query.filter_by(arduino_asignado=arduino_actual).all()
    sensormovimiento = Sensor3.query.filter_by(arduino_asignado=arduino_actual).all()
    sensorgas = Sensor4.query.filter_by(arduino_asignado=arduino_actual).all()

    #agregar los demas sensores
    return render_template('ver_datos.html', sensortemp=sensortemp,sensorluminosidad=sensorluminosidad, arduino_actual=arduino_actual, sensormovimiento=sensormovimiento, sensorgas=sensorgas,all_arduinos_From_user=all_arduinos_From_user) 


@app.route('/verificación_arduino', methods=['GET','POST'])
@login_required
def checkeo_datos():
    user = User.query.filter_by(email=current_user.email).first()
    owner = Owner.query.filter_by(owner_id=user.id).first()

    if owner == None:
        return render_template('add_arduino.html')
    else:

        #se entregan datos de sensores
        arduino_actual = owner.arduino_asignado
        return ver_datos(arduino_actual)
    
   
@app.route('/add_arduino', methods=['GET','POST'])
@login_required
def add_arduino():
    user = User.query.filter_by(email=current_user.email).first()
    
    if user.roles != 1:
        errorpage("No tiene permisos para agregar arduinos")

    return render_template('add_arduino.html')

@app.route('/new_arduino', methods=['POST'])
@login_required
def asignar_arduino():
    #se comprueba si existe el arduino y se asigna al usuario
    nuevoarduino=request.form['arduino']
    arduino = Arduino.query.filter_by(name=nuevoarduino).first()
    
    if arduino == None:        
        new_arduino = Arduino(name=nuevoarduino, description= "Arduino asignado a " + current_user.email)
        db.session.add(new_arduino)
        db.session.commit()
        user = User.query.filter_by(email=current_user.email).first()
        new_owner = Owner(owner_id=user.id, arduino_asignado=nuevoarduino)
        db.session.add(new_owner)
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
