from app.setup import create_folder, create_database
from app.functions import create_new_note, check_filenames, read_a_note, update_a_note, deleting_a_note, list_notes, delete_permanently
from sys import exit


if __name__ == "__main__":
	print("Welcome to the notepad CLI")
	print("Developed by @WasukaTiramisu")
	print("Follow me on github :) ")
	while True:
		resp = input("\nEnter h for help: ")
		if resp.lower() == "h":
			print("Enter ls to list the notes")
			print("Enter c to create a new note")
			print("Enter r to read a note")
			print("Enter u to update a note")
			print("Enter d to delete a note")
			print("Enter i to delete an entry")
			print("Enter q to exit")
		if resp.lower() == "ls":
			list_notes()
		if resp.lower() == "c":
			filename = input("Enter the name: ")
			note = input("Enter your note: ")
			create_new_note(note, filename)
		if resp.lower() == "r":
			filename = input("Enter the name of the note: ")
			read_a_note(filename)
		if resp.lower() == "u":
			filename = input("Enter the name of the note you want to update: ")
			note = input("Enter the new note: ")
			update_a_note(note, filename)
		if resp.lower() == "d":
			filename = input("Enter the name you of the note you want to delete: ")
			deleting_a_note(filename)
			perm = ("Do you want to delete it permanently? (Enter y to confirm) ")
			if perm.lower() == "y":
				delete_permanently(filename)
		if resp.lower() == "i":
			filename = input("Enter the name you of the note you want to delete: ")
			delete_permanently(filename)
		if resp.lower() == "q":
			print("Exiting!")
			exit()

