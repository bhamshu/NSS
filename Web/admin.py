from passlib.hash import sha256_crypt
from pyDes import triple_des
import json

u2pjson = 'data/unametopwrd.json'
u2penckey = 'data/unametopwrdencryptedkey.json'

def initialise_records_donotdothisitwilldropallrecords():
	pass
	'''with open(u2pjson, mode='w', encoding='utf-8') as f:
		json.dump({}, f)
	with open(u2penckey, mode='w', encoding='utf-8') as f:
			json.dump({}, f)
		'''

def addvolunteer(uname, pwrd):
	'''IF FAILED AT ANY STEP, SHOW ADDING USER FAILED AND MAKE SURE 
	WHOLE TRANSACTION GETS CANCELLED
	add records to unametopwrd and to unametopwrdencryptedkey
	every volunteer has only read access of the sheet
	as of now
	'''
	client_secret = ""
	print("copy paste the client secret here:")
	while(True):
		line = input()
		if line=="":
			client_secret = client_secret.strip()
			break
		client_secret+=line+"\n"

	with open(u2pjson, 'r') as unametopwrd:
		dicc = json.loads(unametopwrd.read())

	encpwrd = sha256_crypt.hash(uname+pwrd)
	dicc[uname] = encpwrd
	with open(u2pjson, 'w') as unametopwrd:
		json.dump(dicc, unametopwrd)
	del dicc

	with open(u2penckey, 'r') as unametopwrdencryptedkey:
		dicc = json.loads(unametopwrdencryptedkey.read())

	encrypted_client_secret = triple_des(padded(uname+pwrd)).encrypt(client_secret, padmode=2)
	#print(encrypted_client_secret)
	encrypted_client_secret = ascii(encrypted_client_secret)
	dicc[uname] = encrypted_client_secret
	with open(u2penckey, 'w') as unametopwrdencryptedkey:
		json.dump(dicc, unametopwrdencryptedkey)


def showallvolunteers():
	dicc={}
	with open(u2pjson, 'r') as unametopwrd:
		dicc = json.loads(unametopwrd.read())
	for i in dicc.keys():
		print(i)

def padded(key):
	if len(key)>24:
		return key[-24:] #to make sure it's not all uname
	else:
		return key+"X"*(24-len(key))

def thedecrypt(key, encmsg):
	'''a stub. 
	this will be in a separate module and 
	decrypt encrypted_client_secret
	thedecrypt(key, encmsg) = themsg
	theencrypt(key, themsg) = encmsg
	'''
	#I can use bitwise xor too for both the functions but that will
	#have some issues mainly in how to translate string to binary
	#plain ascii will not be entirely secure as many digits are predictible
	paddedkey = padded(key) #to make it 16 or 24 bytes long
	decrypted_client_secret = triple_des(paddedkey).decrypt(encmsg, padmode =2).decode("utf-8") #decode("utf-8") is to convert bytes literal to unicode
	return decrypted_client_secret
