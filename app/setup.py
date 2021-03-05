import os
import sqlite3


#This is the directory of this file
basedir = os.path.dirname(os.path.abspath(__file__))

# Checking if the folder exists
def create_folder():
	if not os.path.isdir(os.path.join(basedir, 'notes')):
		print('creating a new folder')
		os.mkdir(os.path.join(basedir, 'notes'))
	else:
		# print("folder already present")
		pass

# Creating the database
def create_database():
	"""
	This function creates a database incase it does not exist
	"""
	filename = os.path.join(basedir, "folders.sqlite")
	if not os.path.isfile(filename):
		print("Database is not present. Creating a new database")
		connection = sqlite3.connect(filename)
		cursor = connection.cursor()
		statement = """
		CREATE TABLE "filenames" (
			"preferredname"	TEXT,
			"realname"  TEXT,
			"created"	TEXT,
			"edited"	TEXT,
			"status"	NUMERIC,
			"deleted"	NUMERIC
		);
		"""
		cursor.execute(statement)
		connection.commit()
		connection.close()

	else:
		# print("Database exists!")
		pass

create_folder()
create_database()
