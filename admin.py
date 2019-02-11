from passlib.hash import sha256_crypt
from pyDes import triple_des
import json

mydir = '/home/floorwell/NSS'
u2pjson = mydir+'/data/unametopwrd.json'
u2penckey = mydir+'/data/unametopwrdencryptedkey.json'

def initialise_records_donotdothisitwilldropallrecords():
	pass
	'''with open(u2pjson, mode='w', encoding='utf-8') as f:
		json.dump({}, f)
	with open(u2penckey, mode='w', encoding='utf-8') as f:
			json.dump({}, f)
		'''

def addvolunteer(uname, pwrd, csloc = None, client_secret = None):
	'''
	adds records to unametopwrd and to unametopwrdencryptedkey
	every volunteer has only read access of the sheet
	as of now
	arguments: uname, pwrd, csloc(optional), client_secret(optional) #give either of these two.
	csloc should be location to client_secret. if neither is given, csloc will be asked on terminal
	if type(client_secret)!=str, it'll be decoded to utf-8.
	(this is for when volunteer is added through webpage and client_secret file is uploaded)
	returns 0 if added successfully else None
	'''
	if client_secret==None:
		if csloc == None:
			csloc = input("Enter the location of client_secret: ")
			csloc = csloc.strip("'").strip('"')
		with open(csloc) as cs:
			client_secret = cs.read()

	elif type(client_secret)!=str:
		client_secret = client_secret.decode('utf-8')
	else:
		client_secret = client_secret #lol

	with open(u2pjson, 'r') as unametopwrd:
		diccu2p = json.loads(unametopwrd.read())
	#print(client_secret)
	with open(u2penckey, 'r') as unametopwrdencryptedkey:
		diccu2pkey = json.loads(unametopwrdencryptedkey.read())

	encpwrd = sha256_crypt.hash(uname+pwrd)
	diccu2p[uname] = encpwrd
	with open(u2pjson, 'w') as unametopwrd:
		json.dump(diccu2p, unametopwrd)

	encrypted_client_secret = triple_des(padded(uname+pwrd)).encrypt(client_secret, padmode=2)
	#print(encrypted_client_secret)
	encrypted_client_secret = ascii(encrypted_client_secret)
	diccu2pkey[uname] = encrypted_client_secret
	with open(u2penckey, 'w') as unametopwrdencryptedkey:
		json.dump(diccu2pkey, unametopwrdencryptedkey)
	print(f"The user {uname} was added successfully")
	return 0


def showallvolunteers():
	dicc={}
	with open(u2pjson, 'r') as unametopwrd:
		dicc = json.loads(unametopwrd.read())
	return dicc.keys()
	if __name__=="__main__":
		for i in dicc.keys():
			print(i)

def padded(key):
	if len(key)>24:
		return key[-24:] #to make sure it's not all uname
	else:
		return key+"X"*(24-len(key))

def thedecrypt(key, encmsg):
	'''
	thedecrypt(key, encmsg) = themsg
	theencrypt(key, themsg) = encmsg
	'''
	#I can use bitwise xor too for both the functions but that will
	#have some issues mainly in how to translate string to binary
	#plain ascii will not be entirely secure as many digits are predictible
	paddedkey = padded(key) #to make it 16 or 24 bytes long
	decrypted_client_secret = triple_des(paddedkey).decrypt(encmsg, padmode =2).decode("utf-8") #decode("utf-8") is to convert bytes literal to unicode
	return decrypted_client_secret

def dropvolunteer(uname):
	'''
	returns 0 if successfully deleted
	returns 1 if user doesn't exist
	returns -1 if data inconsistency is detected (should never return this)
	argument: uname
	'''
	with open(u2pjson, 'r') as unametopwrd:
		diccunametopwrd = json.loads(unametopwrd.read())
	if uname not in diccunametopwrd.keys():
		print(f"Attempt to delete {uname} failed, user does not exist")
		return 1
	else:
		del diccunametopwrd[uname]
		with open(u2penckey, 'r') as unametopwrdencryptedkey:
			diccunametopwrdencryptedkey = json.loads(unametopwrdencryptedkey.read())
		if uname not in diccunametopwrdencryptedkey.keys():
			print("Boy sound the alarms! the data is inconsistent")
			return -1
		else:
			del diccunametopwrdencryptedkey[uname]
		with open(u2penckey, 'w') as unametopwrdencryptedkey:
			json.dump(diccunametopwrdencryptedkey, unametopwrdencryptedkey)
		with open(u2pjson, 'w') as unametopwrd:
			 json.dump( diccunametopwrd, unametopwrd)
		print(f"successfully deleted user {uname}")
		return 0

def validatepwrd(uname, pwrd):
	'''
	returns sha256_crypt.verify(uname+pwrd, expected_password)
	where expected_password = u2p[uname]. the uname+pwrd is salted, hashed and stored
	returns bool value. True if pwrd matches. False if it doesn't.
	returns '1' if uname doesn't exist
	'''
	with open(u2pjson, 'r') as unametopwrd:
		u2p = json.loads(unametopwrd.read())
	if uname not in u2p:
		return '1'
	expected_password = u2p[uname]
	return sha256_crypt.verify(uname+pwrd, expected_password)

def getclientsecret(uname, pwrd):
	with open(u2penckey) as unametopwrdencryptedkey:
		u2pk = json.loads(unametopwrdencryptedkey.read())
	encrypted_client_secret = eval(u2pk[uname]) #alternatively, first strip the "s and the b and then use .encode('utf-8')
	client_secret = thedecrypt(key = uname+pwrd, encmsg = encrypted_client_secret)
	return client_secret

def changepassword(uname, existingpwrd, newpwrd):
	'''
	Arguments: uname, existingpwrd, newpwrd
	return 1 if user doesn't exist
	return 0 if successfully changed password
	return False if existingpwrd is wrong
	'''
	bullion = validatepwrd(uname, existingpwrd)
	if bullion=='1':
		#user doesn't exist
		return 1
	if bullion==False:
		#Wrong password
		return False

	client_secret = getclientsecret(uname, existingpwrd)

	print('''Hello future visitor who came to read the logs. The upcoming user add is not really an addition but just me\
		being lazy in implementing changepassword.
		''')
	addvolunteer(uname, newpwrd, client_secret = client_secret)
	return 0