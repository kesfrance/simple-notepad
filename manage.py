# manage.py - controller

# imports
from flask import Flask, render_template, request, session, \
flash, redirect, url_for, g
import sqlite3
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbase_setup import Base, Notes
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///notepad.db')
Session = sessionmaker(bind=engine)
DBsession = Session()

# configuration
DATABASE = './notepad.db'
app = Flask(__name__)
USERNAME = 'user'
PASSWORD = 'user'
SECRET_KEY = '\x83\xc0\x08\xcd\xe3\x12\xa8'

# pulls in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

# function used for connecting to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

#user cannot access main page except firts logged in
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

#check for credentials and login
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
            request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error)

@app.route('/add', methods=['POST'])
@login_required
def add():
    titles = request.form['title']
    contents = request.form['content']
    if not titles or not contents:
        flash("All fields are required. Please try again.")
        return redirect(url_for('main'))  
    else:   
        addedNote = Notes(title=request.form['title'], content=request.form['content'])
        DBsession.add(addedNote)
        DBsession.commit()
    flash('New entry was successfully made!')
    return redirect(url_for('main'))

@app.route('/main')
@login_required
def main():
    allNotes = DBsession.query(Notes).order_by(Notes.id.desc())
    return render_template('main.html', allnotes=allNotes)

@app.route('/note/<int:note_id>')
@login_required
def singleNote(note_id):
    oneNote = DBsession.query(Notes).filter_by(id=note_id).one()
    return render_template('singleNote.html', note_id=note_id, oneNote=oneNote)

  
@app.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required  
def editNote(note_id):
    allnotes = DBsession.query(Notes)
    editedNote = allnotes.filter_by(id=note_id).one()    
    if request.method == 'POST':
        if request.form['title']:
	        editedNote.title = request.form['title']
	        editedNote.content = request.form['content']
	        DBsession.add(editedNote)
	        DBsession.commit()
        flash("Note has been edited")
        return redirect(url_for('main'))
    else:
        return render_template('editedNote.html', note_id=note_id, i=editedNote)

    
    
@app.route('/note/<int:note_id>/delete', methods= ['GET', 'POST'])
@login_required  
def deleteNote(note_id):
    deletedNote = DBsession.query(Notes).filter_by(id=note_id).one()       
    if request.method == 'POST':
        DBsession.delete(deletedNote)
        DBsession.commit()
        flash("Note has been deleted")
        return redirect(url_for('main'))
    else:
        return render_template('deleteNote.html', note_id=note_id, i=deletedNote)


#logout and flash a message
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
