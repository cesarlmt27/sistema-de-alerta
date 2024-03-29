from flask import Flask, render_template, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_login import LoginManager, current_user
from datetime import datetime
from sqlalchemy import literal
import time
from flask_mail import Mail, Message 
from datetime import timedelta

#HAY QUE:
#1.- asignar todos los nuevos sensores y poder graficarlos + sus datos de distribucion
#2.- poder ver con admin los datos de todos los sensores (crear una pagina que imprima todos los sensores que solo pueda accederse con rol de admin)
#3.- parametros estandar de cada sensor (nueva base de datos)
#4.- agregar alerta de sensores al correo 
#5.- hacer posible que se asigne mas de un arduino a un usuario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:anakin@localhost/tic123'
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

#esta tabla al final se usa para tener un control de datos
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
    fecha_ultimo_mensaje = db.Column(db.DateTime())
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


#create a user to test with

#before first req
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verificación_arduino_graficos', methods=['GET','POST'])
@login_required
def checkeo_datos_graficos():
    user = User.query.filter_by(email=current_user.email).first()
    owner = Owner.query.filter_by(owner_id=user.id).first()

    if owner == None:
        return errorpage("No tiene un arduino que analizar")

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


    last_24_hours_temps = []

    #save temperatures from last 24hours
    for i in sensortemp:
        #check if i.fecha is from last 24 hours and then append to list with utc +3
        if i.fecha > datetime.now() - timedelta(hours=24):
            last_24_hours_temps.append(i.temperatura)
    daytype = ""
    if len(last_24_hours_temps) > 0:
        if sum(last_24_hours_temps)/len(last_24_hours_temps) > 25:
            daytype = "por los datos se desprende que en las ultimas 24 horas la temperatura alta y ha estado caluroso"
        #normal 
        if sum(last_24_hours_temps)/len(last_24_hours_temps) < 25 and sum(last_24_hours_temps)/len(last_24_hours_temps) > 15:
            daytype = "por los datos se desprende que en las ultimas 24 horas la temperatura ha estado normal y ha estado fresco"
        #cold day
        if sum(last_24_hours_temps)/len(last_24_hours_temps) < 15:
            daytype = "por los datos se desprende que en las ultimas 24 horas la temperatura ha estado baja y ha estado frio"
    else:
        daytype = "no se han registrado datos de temperatura en las ultimas 24 horas para tener una idea de como ha estado el clima"
    
    return render_template('ver_graficos.html', labels1=labels1, values1=values1, labels2=labels2, values2=values2, labels3=labels3, values3=values3, labels4=labels4, values4=values4, all_arduinos_From_user=all_arduinos_From_user, arduino_actual=arduino_actual, daytype=daytype)

@app.route('/ver_mas_graficos', methods=['GET','POST'])
@login_required
def seleccionararduino_graficos():
    arduino_actual = request.form['arduinos']
    
    return ver_graficos(arduino_actual)

@app.route('/control', methods=['GET', 'POST'])
@login_required
def control():
    #check if user does not has role admin
    if not current_user.has_role('admin'):
        return errorpage("No tiene permiso para acceder a esta página")



    

    
    all_users = User.query.all()
    all_arduinos = Arduino.query.all()
    return render_template('control_de_datos.html', all_users=all_users, all_arduinos=all_arduinos)

@app.route('/administrar', methods=['GET','POST'])
@login_required
def administrar():
    if not current_user.has_role('admin'):
        return errorpage("No tiene permiso para acceder a esta página")    


    seleccion = request.form['seleccion']

    if seleccion == "1":
        todoslosparametros = parametrosalerta.query.all()
        return render_template('cambiarparametro1.html', todoslosparametros=todoslosparametros)
    
    if seleccion == "2":
        todoslosroles = Role.query.all()
        all_users = User.query.all()
    return render_template('cambiarroles.html', todoslosroles=todoslosroles, all_users=all_users)
    

@app.route('/cambiarparametroespecifico', methods=['GET','POST'])
@login_required
def cambiarparametrosesp():
   

    seleccion = request.form['seleccion']
    seleccionpar = request.form['seleccionpar']
    if seleccionpar == "1":
        if request.form['parmin'] == "" or request.form['parmax'] == "":
            return errorpage("Los valores ingresados no son válidos")        
        newMin = float(request.form['parmin'])
        newMax = float(request.form['parmax'])
        #if newmin or newmax are not positive numbers return errorpage()


            
        #if new min or max are not numbers return errorpage()
        if newMin == "" or newMax == "":
            return errorpage("Los valores ingresados no son válidos")
        if newMin == None:
            return errorpage("Los valores ingresados no son válidos")
        
        parametro = parametrosalerta.query.filter_by(arduino_asignado=seleccion).first()
        parametro.temperaturamin = newMin
        parametro.temperaturamax = newMax
        db.session.commit()
        all_users = User.query.all()
        all_arduinos = Arduino.query.all()
        return render_template('control_de_datos.html', all_users=all_users, all_arduinos=all_arduinos)
    
    if seleccionpar == "2":
        if request.form['parmin'] == "" or request.form['parmax'] == "":
            return errorpage("Los valores ingresados no son válidos")        
        newMin = float(request.form['parmin'])
        newMax = float(request.form['parmax'])

        if float(newMin) < 0 or float(newMax) < 0:
            return errorpage("Los valores ingresados no son válidos")
        if newMin == "" or newMax == "":
            return errorpage("Los valores ingresados no son válidos")        

        if newMin == None:
            return errorpage("Los valores ingresados no son válidos")
        parametro = parametrosalerta.query.filter_by(arduino_asignado=seleccion).first()
        parametro.gasminimo = newMin
        parametro.gasmaximo = newMax
        db.session.commit()
        all_users = User.query.all()
        all_arduinos = Arduino.query.all()
        return render_template('control_de_datos.html', all_users=all_users, all_arduinos=all_arduinos)
    
    if seleccionpar == "3":
        if request.form['parmin'] == "" or request.form['parmax'] == "":
            return errorpage("Los valores ingresados no son válidos")        
        newMin = float(request.form['parmin'])
        newMax = float(request.form['parmax'])

        if float(newMin) < 0 or float(newMax) < 0:
            return errorpage("Los valores ingresados no son válidos")

        #if "" error

        if newMin == None:
            return errorpage("Los valores ingresados no son válidos")
        parametro = parametrosalerta.query.filter_by(arduino_asignado=seleccion).first()
        parametro.luminosidadmin = newMin
        parametro.luminosidadmax = newMax
        db.session.commit()
        all_users = User.query.all()
        all_arduinos = Arduino.query.all()
        return render_template('control_de_datos.html', all_users=all_users, all_arduinos=all_arduinos)

@app.route('/cambiarrolesp', methods=['GET','POST'])
@login_required
def cambiarrolesp():

    if not current_user.has_role('admin'):
        return errorpage("No tiene permiso para acceder a esta página")

    userselect = request.form['userselect']
    seleccionrol = request.form['seleccionrol']
    
    if seleccionrol == "a":
        user = User.query.filter_by(email=userselect).first()
        user.roles = list(Role.query.filter(Role.name == 'cliente'))
        db.session.commit()
        todoslosroles = Role.query.all()
        all_users = User.query.all()
        return render_template('cambiarroles.html', todoslosroles=todoslosroles, all_users=all_users)
    
    if seleccionrol == "b":
        user = User.query.filter_by(email=userselect).first()
        user.roles = list(Role.query.filter(Role.name == 'admin'))
        db.session.commit()
        todoslosroles = Role.query.all()
        all_users = User.query.all()
        return render_template('cambiarroles.html', todoslosroles=todoslosroles, all_users=all_users)
    
   
    



@app.route('/errorpage', methods=['GET', 'POST'])
@login_required
def errorpage(descripcionerror):
    return render_template('error.html', descripcionerror=descripcionerror)



def alerta_mail(mailtargetlist, descripcionalerta):

    msg = Message("ALERTA",sender = 'noreply@demo.com', recipients = mailtargetlist)
    msg.body = descripcionalerta
    mail.send(msg)

        

#EL EN FUTURO RENDERIZAR OTRA DIRECCION HTML EN LA QUE DIGA SE HAN ENCONTRADO X ALERTAS 


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
        return errorpage("No tiene arduinos asignados")
    else:

        #se entregan datos de sensores
        arduino_actual = owner.arduino_asignado
        return ver_datos(arduino_actual)
    
   
@app.route('/add_arduino', methods=['GET','POST'])
@login_required
def add_arduino():
    if not current_user.has_role('admin'):
        return errorpage("No tiene permiso para acceder a esta página")    
    user = User.query.filter_by(email=current_user.email).first()

    all_owner_without_user = Owner.query.filter_by(owner_id=None).all()

    

    if all_owner_without_user == None:
        return errorpage("No hay arduinos disponibles")
    return render_template('add_arduino.html', all_owner_without_user=all_owner_without_user)

@app.route('/update_asignacion', methods=['GET','POST'])
@login_required
def update_asignacion():
    arduino_actual = request.form['arduinos sin dueño']
    selected_arduino = Owner.query.filter_by(arduino_asignado=arduino_actual).first()
    #cambiar el id de selected_arduino a usuario actual
    selected_arduino.owner_id = current_user.id

    
    db.session.commit()

    #crear parametros de alerta estandar
    new_parametrosalerta = parametrosalerta(temperaturamin=0,temperaturamax=40,gasminimo=0,gasmaximo=600,movimiento=True,luminosidadmax=1000,luminosidadmin=100,arduino_asignado=arduino_actual)
    db.session.add(new_parametrosalerta)
    db.session.commit()

    #cambiar nombre de descripcion del arduino a "arduino asignado a " + email
    arduino = Arduino.query.filter_by(name=arduino_actual).first()
    arduino.description = "Arduino asignado a " + current_user.email
    db.session.commit()

    return render_template('/index.html')



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

#POST ARDUINO ENVIANDO SEÑAL
@app.route('/arduinosignal', methods=['POST'])
def arduinosignal():
    if request.method == 'POST':



        data = request.form
        arduino_asignado = data['serialInput']
        #se revisa si el arduino tiene dueño si no, se va a la pagina de asignacion
        arduino = Arduino.query.filter_by(name=arduino_asignado).first()
        
        if arduino == None:
            #crear arduino sin dueño
            new_arduino = Arduino(name=arduino_asignado, description= "Arduino sin dueño")
            db.session.add(new_arduino)
            db.session.commit()
            new_owner = Owner(arduino_asignado=arduino_asignado)
            db.session.add(new_owner)
            db.session.commit()


        temp = data['tempInput']
        
        fecha = datetime.now()
        new_sensor1 = Sensor1(fecha=fecha, temperatura=temp, arduino_asignado= arduino_asignado)
        db.session.add(new_sensor1)
        db.session.commit()
        #
        ldr = data['ldrInput']
        fecha = datetime.now()
        new_sensor2 = Sensor2(fecha=fecha, luminosidad=ldr, arduino_asignado= arduino_asignado)
        db.session.add(new_sensor2)
        db.session.commit()
        #
        pir = data['pirInput']
        if pir == "1.00":
            pir = True
        else:
            pir = False
        fecha = datetime.now()
        new_sensor3 = Sensor3(fecha=fecha, movimiento=pir, arduino_asignado= arduino_asignado)
        db.session.add(new_sensor3)
        db.session.commit()
        #
        gas = data['gasInput']

        fecha = datetime.now()
        new_sensor4 = Sensor4(fecha=fecha, gas=gas, arduino_asignado= arduino_asignado)
        db.session.add(new_sensor4)
        db.session.commit()
        




        #search in parametrosalerta
        parametros = parametrosalerta.query.filter_by(arduino_asignado=arduino_asignado).first()
        owner = Owner.query.filter_by(arduino_asignado=arduino_asignado).first()
        mensaje = ""
        if parametros == None:
            return jsonify(data)       
        else:
            #se revisa si hay alertas
            if float(temp) > parametros.temperaturamax or float(temp) < parametros.temperaturamin:
                mensaje = mensaje + "Temperatura No ideal, "
            if float(ldr) > parametros.luminosidadmax or float(ldr) < parametros.luminosidadmin:
                mensaje = mensaje + "Luminosidad No ideal, "
            if pir == parametros.movimiento:
                search_usermov = User.query.filter_by(id=owner.owner_id).first()
                mailtargetlistmov = [search_usermov.email]
                alerta_mail(mailtargetlistmov, "Movimiento detectado en el dispositivo " + arduino_asignado)
                mailtargetlistmov = []
            if float(gas) > parametros.gasmaximo or float(gas) < parametros.gasminimo:
                mensaje = mensaje + "Gas No ideal "
            if mensaje != "":
                mensaje = mensaje + "en el dispositivo " + arduino_asignado
                #si no se ha mandado un correo en los ultimos 5 minutos envia
                if owner.fecha_ultimo_mensaje == None or owner.fecha_ultimo_mensaje < datetime.now() - timedelta(minutes=1):
                    
                    #se manda correo
                    search_user = User.query.filter_by(id=owner.owner_id).first()
                    mailtargetlist = [search_user.email]
                    alerta_mail(mailtargetlist, mensaje)
                    mailtargetlist = []
                    owner.fecha_ultimo_mensaje = datetime.now()
                    db.session.commit()
                    mensaje=""


                

    return jsonify(data)
#info de usuario -NO TERMINADO-

if __name__ == '__main__':
    app.run(host='0.0.0.0')
