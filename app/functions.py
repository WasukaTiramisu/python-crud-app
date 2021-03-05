import os
import sqlite3
import time
from datetime import datetime
from random import choices
import string
import random
from pprint import pprint

basedir = os.path.dirname(os.path.abspath(__file__))
notes_folder = os.path.join(basedir, "notes")
db = os.path.join(basedir, "folders.sqlite")


def create_filename(length: int = 16):
    """
    This function generates a new filename with .txt extension.
    It takes an input length, which is the length of the filename required
    """
    return "{}.txt".format("".join(choices(string.ascii_lowercase + string.digits, k=length)))

def check_filenames(filename: str):
    """
    This function will check if a filename is present in the database or not
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""
        SELECT preferredname FROM filenames
        """)
    res = c.fetchall()
    res = [i[0] for i in res]
    if filename in res:
        return True
    return False


def insert_filenames(preferredname, realname):
    """
    This function takes in a preferred name, and a real name, and enters it into database.
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""
        INSERT INTO filenames(preferredname, realname, created,
        edited, status, deleted) VALUES (?, ?, ?, ?, ?, ?)
        """, (preferredname, realname, str(time.time()), str(time.time()), 1, 0 ))
    conn.commit()
    conn.close()


def create_new_note(note: str, preferredname: str):
    """
    Creates a new note and enters the data in database
    """
    filename = create_filename()
    if os.path.isfile(os.path.join(notes_folder, filename)):
        # Checking if the file exists already
        filename = create_filename()
    if not check_filenames(preferredname):
        # Insert into database
        insert_filenames(preferredname, filename)
        # Writing to file
        with open(os.path.join(notes_folder, filename), "w+") as f:
            f.write(note)
        print("Written your note")
        print("Your filename is {}".format(filename))
    else:
        print("Filename already in use. Use a different filename")

def read_a_note(preferredname: str):
    """
    This function will take a preferredname and will return the contents of the file mapped to that filename
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""
        SELECT realname FROM filenames WHERE preferredname = ?
        """, (preferredname, ))
    res = c.fetchall()
    conn.close()
    if len(res) != 0:
        with open(os.path.join(notes_folder, res[0][0]), 'r') as f:
            print("\nContents of that file are: ")
            print("\n".join(f.readlines()))

    else:
        print("No such entry exists with that filename")


def update_a_note(note: str, preferredname: str):
    """
    Update an older note
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""
        SELECT realname FROM filenames WHERE preferredname = ?
        """, (preferredname, ))
    res = c.fetchall()
    if len(res) != 0:
        with open(os.path.join(notes_folder, res[0][0]), 'w') as f:
            f.write(note)
        c.execute("""
            UPDATE filenames SET edited = ? WHERE preferredname = ?
            """, (str(time.time()), preferredname))
        conn.commit()
        conn.close()

    else:
        conn.close()
        print("No such entry exists with that filename")

def deleting_a_note(preferredname: str):
    """
    Delete the file from system, and set the file as unavailable in database
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""
        SELECT realname FROM filenames WHERE preferredname = ?
        """, (preferredname, ))
    res = c.fetchall()
    if len(res) != 0:
        if os.path.isfile(os.path.join(notes_folder, res[0][0])):
            os.remove(os.path.join(notes_folder, res[0][0]))
            print("Deleted the note: {}. You cannot access it but you cannot use the filename until you delete it using delete_permanently function".format(preferredname))
        else:
            print("File is not present")
        c.execute("""
            UPDATE filenames SET deleted = ? WHERE preferredname = ?
            """, (1, preferredname))
        conn.commit()
        conn.close()

    else:
        conn.close()
        print("No such entry exists with that filename")

def delete_permanently(preferredname: str):
    """
    Delete from database
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("DELETE FROM filenames WHERE preferredname = ?", (preferredname, ))
    conn.commit()
    conn.close()
    print("Deleted the entry from database. You may use the name \"{}\" again.".format(preferredname))

def list_notes():
    """
    List all the notes in the database
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""
            SELECT preferredname, created, edited, deleted FROM filenames
        """)
    res = c.fetchall()
    conn.close()
    if len(res) == 0:
        print("No entries in database")
        return None
    files = {}
    for f in res:
        files[f[0]] = {
            "Created on": datetime.fromtimestamp(int(float(f[1]))).strftime("%c"),
            "Last modified on": datetime.fromtimestamp(int(float(f[2]))).strftime("%c"),
            "Available": bool(not f[3])
        }
    pprint(files)