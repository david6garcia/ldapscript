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
user = 'cn=admin,dc=dgarcia,dc=gonzalonazareno,dc=org'
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
 
	dnusers = ('uid=%s,ou=People,dc=dgarcia,dc=gonzalonazareno,dc=org' % str(p["usuario"])
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
 
	l.add_s(dnusers,ldif)

	uidNumber = uidNumber + 1)
 
print "Usuarios añadidos correctamente"


# Importacion de maquinas

for c in todos["computers"]:
 
	dnusers2 = ('uid=%s,ou=Computers,dc=dgarcia,dc=gonzalonazareno,dc=org'%i["hostname"].encode('ascii','ignore'))
	dic2 = {}
	dic2['objectclass'] = ['top','organizationalUnit','ldapPublicKey']
	dic1['cn'] = str(c["hostname"])
	dic1['ipHostNumber'] = str(c["ipv4"])
	dic1['sshPublicKey'] = str(c["clave"])
 
	ldif2 = modlist.addModlist(dic2)
 
	l.add_s(dnusers2,ldif2)
 
print "Maquinas añadidas correctamente"

# Cerramos la conexión
l.unbind()

# Cerramos el fichero json
fichero_json.close()
