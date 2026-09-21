print ("estoy ejecutando app.py")

from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

#inicializamos nuestra app

app=Flask(__name__)


#para enlazar la app con la base de datos //localhost que es mi servidor local

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bd_pagina'


mysql=MySQL(app)


@app.route("/")
def index(): #LEER
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user") #ejecutara la consulta de mysql
    data = cur.fetchall() #para recuperar la informacion de nuestra base de datos
    cur.close()
    
    return render_template('index.html', user=data)


@app.route('/add', methods=['POST'])
def add_user():  #CREAR
    
    if request.method == 'POST':
        
        name = request.form ['name']
        email = request.form ['email']
        
        cur=mysql.connection.cursor()
        
        cur.execute("INSERT INTO user (name, email) VALUES (%s, %s)", (name, email))
        
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('index'))
    
    #CREATE  CREAR
    #READ     LEER
    #UPDATE   ACTUALIZAR
    #DELETE   ELIMINAR
@app.route('/edit/<int:id>',  methods=['POST', 'GET'])
def edit_user(id):   #edit
        
    if request.method == 'POST':
            
        name = request.form['name']
        email = request.form['email']
            
        cur = mysql.connection.cursor()
            
            #se agrega where id=%s para que coincida con la dupla (id,name, email)
        cur.execute("UPDATE user SET name = %s, email = %s WHERE id = %s", (name, email, id))
            
        mysql.connection.commit()
        cur.close()
            
        return redirect (url_for('index'))
        
    else: 
            
        cur = mysql.connection.cursor()
            
        cur.execute("SELECT * FROM user WHERE id = %s", (id,))
            
        data = cur.fetchone()
        cur.close()
        
        return render_template('edit.html', user=data)
    
@app.route('/delete/<int:id>')
def delete_user(id):
        
    cur = mysql.connection.cursor()
        
    cur.execute("DELETE FROM user WHERE id = %s",(id,))
        
    mysql.connection.commit()
    cur.close()
        
    return redirect(url_for('index'))
    
@app.route('/search')
def buscar():
    #1. capturamos lo que el usuario escribio en el buscador
    busqueda = request.args.get('q', '').strip()
    
    #2. conextamos con la base de datos
    cursor = mysql.connection.cursor()
    
    #3. si escribio LGO, BUSCAMOS COINCIDENCIAS EN NOMBRE O CORREO
    if busqueda:
        sql = "SELECT * FROM user WHERE name LIKE %s OR email LIKE %s"
        texto_busqueda = f"%{busqueda}%"
        cursor.execute(sql, (texto_busqueda, texto_busqueda))
    #sino escribio nada, traemos todos los usuarios
    else:
        cursor.execute("SELECT * FROM user")
        
    #4. guardamos los resultados y cerramos la conexion del cursor
    usuarios = cursor.fetchall()
    cursor.close()
    
    #5. enviamos la informacion a la pagina html
    return render_template('index.html', user=usuarios, busqueda=busqueda)
        
    

if __name__== '__main__':
    print("Mi programa se esta ejecutando")
    app.run(debug=True)