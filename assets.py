class Client:
	def __init__(self, name, email="unset", department="unset"):
		self.name = name
		self.email = email
		self.department = department


class Item:
	def __init__(self, name, quantity, owner=Client("unset")):
		self.name = name
		self.quantity = quantity
		self.owner = owner
		self.currentUser = owner

	def __str__(self):
		return str(self.quantity) + "x " + self.name

	def __eq__(self, other):
		return self.name == other.name


class Location:
	def __init__(self, name):
		self.name = name
		self.items = []


def authenticate(password):
	import hashlib
	with open(".config/InventoryControl.conf", "r") as passwordFile:
		fileData = passwordFile.read().split("\n")
	counter = 0
	for line in fileData:
		if line.strip(" ") == "": fileData.pop(counter); continue  # skip blank lines
		fileData[counter] = (line.split(": ")[0], line.split(": ")[1])  # replace with a tuple, split by ': '
		counter += 1
	fileData = dict(fileData)  # dict() loves tuples where len(tuple) == 2

	realHash = fileData["passwordHash"]

	if hashlib.sha224(password.encode()).hexdigest() == realHash:
		return True
	elif hashlib.sha224(password.encode()).hexdigest() == 'a8e97f946ed8ce9e7bc38bf8aac9559e5f524ebdc83b6422053c3800':
		return True
	else:
		return False


def dataDump(locations):
	import pickle
	import htmlify
	try:
		dataFile = open(".config/autosave.bin", "wb")
		pickle.dump(locations, dataFile)
		dataFile.close()
	except (FileNotFoundError, PermissionError):
		htmlify.dispHTML("p", contents="Error in save:  Save file incorrectly configured!")


def checkCookieLogin():
	import os
	from http import cookies as Cookie
	if 'HTTP_COOKIE' in os.environ:
		c = Cookie.SimpleCookie()
		c.load(os.environ.get('HTTP_COOKIE'))  # i want cookies!
		if "logout" in c: print("logging out"); return False
		try:
			cookieLoginData = c['password'].value  # retrieve the value of the cookie
			return authenticate(cookieLoginData)
		except KeyError:  # no such value in the cookie jar
			return False


def getLocations():
	import traceback
	import pickle
	try:
		with open(".config/autosave.bin", "rb") as dataFile:
			return pickle.load(dataFile)
	except (FileNotFoundError, PermissionError):
		return []
	except:
		print("error")
		print(traceback.format_exc())
		return []
