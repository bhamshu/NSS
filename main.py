#SHOW MAP WITH HOSPITAL AND DIFFERENT DONORS
from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import sha256_crypt
import json
from pyDes import triple_des
from admin import thedecrypt #, paddedkey
from auxiliaries import buildpage
from records.main import main as rec

#CORRECT THIS THIS SHOULD NOT BE DONE
emergencymeasureses = ""

debug = False

if debug:
  mydir = 'E:/Desktop/30/CV/NSS Blood/Computations/blood donation project/Web'
else:
  mydir = '/home/floorwell/NSS'

from os import urandom
app = Flask(__name__)

if debug:
  app.secret_key = 'a_constant'
else:
  app.secret_key = urandom(24)

@app.route('/')
def my_form():
  return render_template('home.html')

@app.route('/', methods=['POST'])
def my_form_post():
  uname = request.form['uname']
  session['uname'] = uname
  pwrd = request.form['pwrd']
  if(uname == 'demo'):
    return redirect(url_for('demo'))
  from admin import validatepwrd
  bullion = validatepwrd(uname, pwrd)
  if bullion=='1':
    return render_template('failed.html', reason = 'invalid_username')

  if bullion==False:
    return render_template('failed.html', reason = 'wrong_password')
  # if bullion==True and uname=='admin':
  #   return admin()#redirect(url_for('admin'))
  session['admin'] = False
  if bullion==True:
    print(f"{uname} Successfully logged in")
    from admin import getclientsecret
    client_secret = getclientsecret(uname, pwrd)
    session['client_secret'] = client_secret
    global emergencymeasureses
    if uname=='admin':
      session['admin']=True
    emergencymeasureses = {k:v for k, v in session.items()}
    print("Here:", session)
    return render_template('logged_in.html', uname = uname)

@app.route('/googlesearch', methods = ['POST'])
def googlesearch():
  print("emergencymeasureses", emergencymeasureses)
  locname = request.form['locname']
  surl = f"https://www.google.com/search?q={locname}+coordinates"
  return redirect(surl)

@app.route('/demo')
def demo():
  return render_template('demo.html')

@app.route('/dummyrecord', methods=['POST'])
def showdummyrec():
  loc = request.form['loc'].strip()
  blood = request.form['blood'].strip() or None
  d, ids, coord_to_name = rec(target=loc, blood = blood, projectdirpath = mydir+"/records")
  pg = buildpage(d, ids, coord_to_name, blood)
  return pg

@app.route('/sortedrecords', methods = ['GET','POST'])
def showrecords():
  #print("and here: ", session)
  if 'client_secret' not in session:
      print('CORRECT THIS SESSION THING')
  print(f"{emergencymeasureses['client_secret']} wants to access records")
  client_secret = '"'+emergencymeasureses['client_secret']+'"'
  #print(client_secret)
  loc = request.form['loc'].strip()
  blood = request.form['blood'].strip() or None
  if blood!=None:
    blood = blood.split()
  d, ids, coord_to_name = rec(target=loc, blood = blood, projectdirpath = mydir+"/records", client_secret= client_secret)
  pg = buildpage(d, ids, coord_to_name, blood, num = 15)
  print(f"{emergencymeasureses['client_secret']} successfully accessed records")
  return pg

@app.route('/changepwrd', methods=['GET', 'POST'])
def changepwrd():
  from admin import changepassword
  try:
    uname = session['uname']
  except:
    print("Fix this shit")
    uname = emergencymeasureses['uname']

  existing_pwrd = request.form['existing_pwrd']
  new_pwrd = request.form['new_pwrd']
  confirm_new_pwrd = request.form['confirm_new_pwrd']
  if(new_pwrd!=confirm_new_pwrd):
    return render_template('failed.html', reason = 'Confirm New Password not same as New Password')
  nnn=changepassword(uname, existing_pwrd, new_pwrd)
  if nnn!=0:
    return render_template('failed.html', reason = 'Some error occured. It\'s not your fault. Please contact admin')
  return '''<h1>Password Successfully Changed. Please let chrome save the password or remember it carefully.
  There is no option of Forgot Password!</h1>'''


# def admin():
#   # uname = request.form['uname']
#   # pwrd = request.form['pwrd']
#   # if not (uname=='admin' and validatepwrd(uname, pwrd)):
#   #   print("THAT WAS AN ATTACK")
#   #   return "<h1>FRICK OFF</h1>"
#   # else:
#   #
#   session['admin'] = True
#   print("look: ", session)
#   return render_template('logged_in.html', uname = 'admin')

@app.route('/usermgmt', methods=['POST', 'GET'])
def adddeluser():
  if 'admin' not in session or not session['admin']:
    print("THAT WAS SOME COOL ATTACK")
    return "<h1>FRICK OFF</h1>"
  if 'deluname' in request.form.keys():
    deluname = request.form['deluname']
    if deluname=='admin':
      return f"<h1>Bwahahaha Nice ATTEMPT the admin cannot be deleted</h1>"
    from admin import dropvolunteer
    ret = dropvolunteer(deluname)
    if(ret==0):
      return f"<h1>Successfully Deleted {deluname}</h1>"
    elif (ret==1):
      return f"<h1>User Doesn't Exist</h1>"
    elif (ret==-1):
      return f"<h1>Sound the alarms! The data is inconsistent despite the best efforts by the benevolent admin :(</h1>"
    return f"<h1>Excuse me, wtf?</h1>"

  uname = request.form['uname']
  pwrd = request.form['pwrd']
  cls = request.files['client_secret'].read()
  u2p = {}
  with open(mydir+'/data/unametopwrd.json') as unametopwrd:
    u2p = json.loads(unametopwrd.read())
  if uname in u2p.keys():
    return render_template('failed.html', reason = 'user_exists')
  from admin import addvolunteer
  nn = addvolunteer(uname, pwrd, client_secret = cls)
  if nn==0:
    return f"<h1>User Successfully Added!</h1>"
  else:
    return f"<h1>Probably some error occured</h1>"

@app.route('/allvolunteers')
def showallvolunteers():
  '''no args. shows all volunteers'''
  if 'admin' not in session or not session['admin']:
    print("THAT WAS A COOL ATTEMPT")
    return f"403 Forbidden"
  from admin import showallvolunteers as s_a_v
  allvols = s_a_v()
  return f"<h1>{allvols}</h1>"

@app.errorhandler(405)
def method_not_allowed(e):
  print("Error response code: 405", e)
  return '''<h1>There is some error. Maybe you are logged out. Please <a href="/">log in</a></h1>'''



if __name__ == "__main__":
  app.run(debug = debug)