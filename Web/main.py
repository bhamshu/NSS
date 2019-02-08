from flask import Flask, render_template, request
from passlib.hash import sha256_crypt
import json
from pyDes import triple_des
from admin import thedecrypt #, paddedkey

#from auxiliarymethods import validate
#from thedependencies import *

mydir = '/home/floorwell/nss_blood_operations'

debug = False

app = Flask(__name__)

@app.route('/')
def my_form():
	return render_template('home.html')

@app.route('/', methods=['POST'])
def my_form_post():
	uname = request.form['uname']
	pwrd = request.form['pwrd']
	u2p = {}
	with open(mydir+'/data/unametopwrd.json') as unametopwrd:
		u2p = json.loads(unametopwrd.read())
	if uname not in u2p.keys():
		return '<h1>Username Invalid</h1>'
	expected_password = u2p[uname]
	bullion = sha256_crypt.verify(uname+pwrd, expected_password)
	del u2p
	if not bullion:
		return '<h1>Intruder Alert!!!</h1>'
	if bullion==True:
		with open(mydir+'/data/unametopwrdencryptedkey.json') as unametopwrdencryptedkey:
			u2pk = json.loads(unametopwrdencryptedkey.read())
		encrypted_client_secret = eval(u2pk[uname]) #alternatively, first strip the "s and the b and then use .encode('utf-8')
		client_secret = thedecrypt(key = uname+pwrd, encmsg = encrypted_client_secret)
		#print(client_secret)#no longer secret
		return f'''<h1>Hello {uname}! You are successfully logged in :)</h1>'''
		            #<h2>Your client secret is {client_secret}</h2>'''


# # Display variable using <variable_name>
# @app.route('/user/<username>')
# def show_user_profile(username):
#	 return 'Hey there %s' % username

# # To use int or float <converter:variable_name>
# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#	 return 'Post id: %d' % post_id

if __name__ == "__main__":
	app.run(debug = debug)