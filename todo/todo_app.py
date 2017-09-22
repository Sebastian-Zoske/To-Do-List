# To-Do-List-Project
# 15.07.2017
#
# Author: Sebastian Zoske
# Matr-Nr: 554384
# Informatics3
# HTW Berlin
# s0554384@htw-berlin.de

from flask import Flask, request, session, g, redirect, url_for, render_template
from sqlalchemy import create_engine, or_
from models import Entry, Base
from sqlalchemy.orm import sessionmaker

# creating the Flask app to use the functionalities.
app = Flask(__name__)
# creates the engine as a starting point for the SQLAlchemy functionalities.
# Here it is tailored towards SQLite.
engine = create_engine('sqlite:///database.db')

# creating a new session for adding, deleting or modifying data in the Database (e.g. session.add(item)).
db_session = sessionmaker(bind=engine)
session = db_session()


# initalizes the database.
def init_db():
    Base.metadata.create_all(engine)
    print("Database created.")


# init the db over Console Command: python -m flask initdb.
@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')


# app.route defines the Path to the function from the url. Here "/" means it's e.g. www.url.de/
@app.route('/')
def show_entries():
    # gets all entries from the database
    result_entries = session.query(Entry).all()
    # renders the html-template
    return render_template('to-do-list.html', entries=result_entries)


# adds a new entry to the database.
# gets data from the formula via POST.
@app.route('/add', methods=['POST'])
def add_item():
    # gets the different data from the form.
    title = request.form['title']
    descr = request.form['descr']
    new_entry = Entry(title=title, descr=descr)
    # adding Entry to the session.
    session.add(new_entry)
    # commit flushes the session and finalize all changes.
    session.commit()
    return redirect(url_for('show_entries'))

# gets the ID of the Item, looks for it in the database and deletes it.
@app.route('/delete/<int:e_id>')
def delete_item(e_id):
    session.query(Entry).filter_by(id=e_id).delete()
    session.commit()
    return redirect(url_for('show_entries'))

# if you click on a Entry, the text will be striked in HTML
# changing the state from new to finished or vice versa
@app.route('/changestate/<int:e_id>')
def change_state(e_id):
    entry = session.query(Entry).filter_by(id=e_id).first()

    if (entry.state == 'finished'):
        entry.state = 'new'
    else:
        entry.state = 'finished'

    session.commit();
    return redirect(url_for('show_entries'))


@app.route('/', methods=['POST'])
def search_item():
    search_text = request.form['search_text']

    # gets all Entrys that contains the searched text in the Title or Description.
    result_entries = session.query(Entry).filter(
        or_(Entry.title.like('%' + search_text + '%'), Entry.descr.like('%' + search_text + '%'))).all()

    return render_template('to-do-list.html', entries=result_entries)


# closes the database/session after the request.
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
