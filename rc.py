from simplecrypt import encrypt, decrypt
from binascii import hexlify, unhexlify

import threading
import requests
import os.path
import getpass
import ctypes
import sys
import re
import os

requests.packages.urllib3.disable_warnings()

def argumentos():
  if len(sys.argv) == 1:
    open_rc('5')
    open_rc('6')
    open_rc('7')
    open_rc('8')
  if len(sys.argv) > 1:
    na = False
    for i in sys.argv:
      if i != '-na':
        b = False
      if i == '-na':
        na = True
      if i == '-rc5':
        b = True
        open_rc('5')
      if i == '-rc6':
        b = True
        open_rc('6')
      if i == '-rc7':
        b = True
        open_rc('7')
      if i == '-rc8':
        b = True
        open_rc('8')
    if b == False and na == False:
      print('Parametro incorrecto')
    if b == False and na == True:
      open_rc('5')
      open_rc('6')
      open_rc('7')
      open_rc('8')

def argumento_na():
  if len(sys.argv) > 1:
    for i in sys.argv:
      if i == '-na':
        if not os.path.exists('configuracion.ini'):
          configurar_regionales(True)
        print('Procesando...')
        return True
  return False

def mensaje_error(rc, style):
  ctypes.windll.user32.MessageBoxW(0, 'Login y/o Pass rc'+rc+' incorrecto' , 'Error', style)

def Mbox(title, text, style):
  return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def configurar_regionales(error=False):
  if error == True:
    print('No ha configurado el acceso al regional 5/6/7/8.\nDebe realizarlo para poder abrirlos!!!\n')
  if os.path.exists('configuracion.ini'):
    os.remove('configuracion.ini')
  login_name = input('Login name: ')
  pass_rc5 = getpass.getpass("Password RC5: ")
  pass_rc6 = getpass.getpass("Password RC6: ")
  pass_rc7 = getpass.getpass("Password RC7: ")
  pass_rc8 = getpass.getpass("Password RC8: ")
  print('Encriptando datos...')
  f = open('configuracion.ini', 'a')
  f.write('login name:'+login_name+'\n')
  try:
    f.write('pass rc5:'+str(hexlify(encrypt('contra', pass_rc5.encode('utf8'))))[2:-1]+'\n')
  except:
    f.write('pass rc5:'+str(hexlify(encrypt('contra', 'cualquiera'.encode('utf8'))))[2:-1]+'\n')
  try:
    f.write('pass rc6:'+str(hexlify(encrypt('contra', pass_rc6.encode('utf8'))))[2:-1]+'\n')
  except:
    f.write('pass rc6:'+str(hexlify(encrypt('contra', 'cualquiera'.encode('utf8'))))[2:-1]+'\n')
  try:
    f.write('pass rc7:'+str(hexlify(encrypt('contra', pass_rc7.encode('utf8'))))[2:-1]+'\n')
  except:
    f.write('pass rc7:'+str(hexlify(encrypt('contra', 'cualquiera'.encode('utf8'))))[2:-1]+'\n')
  try:
    f.write('pass rc8:'+str(hexlify(encrypt('contra', pass_rc8.encode('utf8'))))[2:-1]+'\n')
  except:
    f.write('pass rc8:'+str(hexlify(encrypt('contra', 'cualquiera'.encode('utf8'))))[2:-1]+'\n')
  f.write('\n\n\n\nCreado por Marco Weihmüller')
  f.close()

def open_rc(rc):
  if not os.path.exists('configuracion.ini'):
    return False
  f = open('configuracion.ini', 'r')
  datos = f.read()
  f.close()
  login = re.search('login name:(.*?)\s', datos)
  if login:
    login = login.group(1)
  else:
    print('No se puede extraer el Login. Debera realizar la configuracion del Login')
    sys.exit()
  if rc == '5':
    password = re.search('pass rc5:(.*?)\s', datos)
    if password:
      password = decrypt('contra', unhexlify(password.group(1)))
    else:
      print('No se puede extraer la Password. Debera realizar la configuracion del RC'+rc)
      return False
  if rc == '6':
    password = re.search('pass rc6:(.*?)\s', datos)
    if password:
      password = decrypt('contra', unhexlify(password.group(1)))
    else:
      print('No se puede extraer la Password. Debera realizar la configuracion del RC'+rc)
      return False
  if rc == '7':
    password = re.search('pass rc7:(.*?)\s', datos)
    if password:
      password = decrypt('contra', unhexlify(password.group(1)))
    else:
      print('No se puede extraer la Password. Debera realizar la configuracion del RC'+rc)
      return False
  if rc == '8':
    password = re.search('pass rc8:(.*?)\s', datos)
    if password:
      password = decrypt('contra', unhexlify(password.group(1)))
    else:
      print('No se puede extraer la Password. Debera realizar la configuracion del RC'+rc)
      return False
  firma = re.search('Creado por Marco Weihmüller', datos)
  if not firma:
    os.remove('configuracion.ini')
    f = open('configuracion.ini', 'a')
    login = re.search('login name:(.*?)\s', datos)
    if login:
      f.write('login name:'+login[1]+'\n')
    password_l = re.search('pass rc5:(.*?)\s', datos)
    if password_l:
      f.write('pass rc5:' + re.search('pass rc5:(.*?)\s', datos).group(1)+'\n')
    password_l = re.search('pass rc6:(.*?)\s', datos)
    if password_l:
      f.write('pass rc6:' + re.search('pass rc6:(.*?)\s', datos).group(1)+'\n')
    password_l = re.search('pass rc7:(.*?)\s', datos)
    if password_l:
      f.write('pass rc7:' + re.search('pass rc7:(.*?)\s', datos).group(1)+'\n')
    password_l = re.search('pass rc8:(.*?)\s', datos)
    if password_l:
      f.write('pass rc8:' + re.search('pass rc8:(.*?)\s', datos).group(1)+'\n')
    f.write('\n\n\n\nCreado por Marco Weihmüller')
    f.close()
  s =  requests.Session()
  try:
    a = s.get(urlRC, verify = False)
  except:
    print('URL del RC'+rc+' no funciona.')
    return False

  viewstate = re.search('javax.faces.ViewState.{1,4}\svalue=\"(.*?)\"', a.text, re.IGNORECASE)

  if viewstate:
    a = s.post(urlRC, verify = False, \
               data = {'login:username' : login, 'login:password' : password, 'login:loginButton' : 'Log In', 'login_SUBMIT' : '1', 'javax.faces.ViewState' : viewstate.group(1)})

    if not re.search('Your last successful login was', a.text, re.IGNORECASE):
      t = threading.Thread(target=mensaje_error, args = (rc, 0,))
      t.start()
      return False

    viewstate = re.search('javax.faces.ViewState.{1,4}\svalue=\"(.*?)\"', a.text, re.IGNORECASE)

    if viewstate:
      s.post(urlRC, verify = False,
             data = {'login:legalPanelCloseButton' : 'OK', 'login_SUBMIT' : '1', 'javax.faces.ViewState' : viewstate.group(1)})

      r = s.get(urlRC, verify = False, stream=True)

      f = open('start'+rc+'.jnlp', 'wb')
      f.write(r.content)
      f.close()
      f = open('start'+rc+'.jnlp', 'rb')
      os.startfile('start'+rc+'.jnlp')
      f.close()

  else:
    print('URL del RC'+rc+' no funciona.')
    return False


if __name__ == '__main__':
  if not argumento_na():
    result = Mbox('Configuración', '¿Desea configurar el acceso al regional 5/6/7/8?', 4)
    if result == 6:
      configurar_regionales()
      print('Procesando...')
      argumentos()
    if result == 7:
      if not os.path.exists('configuracion.ini'):
        configurar_regionales(True)
      print('Procesando...')
      argumentos()
  else:
      argumentos()
