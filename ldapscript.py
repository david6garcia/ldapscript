# -*- coding: utf-8 -*-
 
import json 
import ldap
from ldap import modlist
import getpass
import sys
reload(sys)
sys.setdefaultencoding('utf8')
 
print "Conexión Servidor LDAP."
print""
 
# Conexion con ldap
 
servidor= 'ldap://localhost:389/'
l = ldap.initialize(servidor)
user = 'cn=admin,dc=barney,dc=dgarcia,dc=gonzalonazareno,dc=org'
pw = getpass.getpass('Introduzca password:')
try:
	l.simple_bind_s(user,pw)
except ldap.INVALID_CREDENTIALS:
    	print "Usuario o contraseña incorrecta"
    	sys.exit(0)

	
# Carga de datos
 
ruta=raw_input("Introduzca la ruta del fichero .json: ")

f=open(ruta,"r")
 
todos = json.load(f)
 
uidNumber = 2000
gidNumber = 2000
 
# Importacion de personas

for p in todos["personas"]:
	dnusers = 'uid=%s,ou=People,dc=barney,dc=dgarcia,dc=gonzalonazareno,dc=org' % str(p["usuario"])
	dic = {}
	dic['objectclass'] = ['top','posixAccount','inetOrgPerson','ldapPublicKey']
	dic['cn'] = str(p["nombre"])
	dic['sn'] = str(p["apellidos"])
	dic['uid'] = str(p["usuario"])
	dic['uidNumber'] = str(uidNumber)
	dic['gidNumber'] = str(gidNumber)
	dic['homeDirectory'] = ['/home/%s' % str(p["usuario"])]
	dic['mail'] = str(p["correo"])
	dic['sshPublicKey'] = str(p["clave"])
	dic['loginShell'] = '/bin/bash'
	ldif = modlist.addModlist(dic)
	try:
		l.add_s(dnusers,ldif)
		uidNumber = uidNumber + 1
	except:
               	print "Imposible añadir el usuario %s, ya se encuentra incluida" % str(p["usuario"]) 

print "Usuarios añadidos correctamente"


# Importacion de maquinas

for c in todos["computers"]:
	dnusers2 = 'uid=%s,ou=Computers,dc=barney,dc=dgarcia,dc=gonzalonazareno,dc=org' % str(c["hostname"])
	dic2 = {}
	dic2['objectclass'] = ['top','device','ldapPublicKey','ipHost']
	dic2['cn'] = str(c["hostname"])
	dic2['ipHostNumber'] = str(c["ipv4"])
	dic2['sshPublicKey'] = str(c["clave"])
	ldif2 = modlist.addModlist(dic2)
	try:
		l.add_s(dnusers2,ldif2)
        except:
                print "Imposible añadir la maquina %s,ya se encuentra incluida" % str(c["hostname"])	 

print "Maquinas añadidas correctamente"

# Cerramos la conexión
l.unbind()

# Cerramos el fichero json
f.close()
