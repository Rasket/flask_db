from flask import Flask, request, render_template, flash, send_file
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as lite
import base64
import sys
import os

def readImage(filename):
	fin = open(filename, "rb")
	img = fin.read()
	return img
        
#, static_folder = 'templates'
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(120))
    file = db.Column(db.LargeBinary)

    def __repr__(self):
        return '<User %r>' % self.username





@app.route('/', methods=['post', 'get'])
def login():
	message = 'sasa'
	if request.method == 'POST':
		username = request.form.get('username')  # запрос к данным формы
		password = request.form.get('password')
		file = request.files['file']
		file.save('file.jpg')
		if username != '':
			data = readImage("file.jpg")
			    # Конвертируем данные
			binary = lite.Binary(data)
			temp = User(username = username, password = password, file = data)
			db.session.add(temp)
			db.session.commit()
			os.remove('file.jpg')

	return render_template('index.html', message=message)


@app.route('/<thing>/')
def echo(thing):
	user = User.query.filter_by(username = thing).first()
	image = None
	if user.file != None:
		image = base64.b64encode(user.file).decode('ascii')
	return render_template('profile.html', user = user, image = image)




if __name__ == '__main__':

	app.run(port = 9999, debug = True)
