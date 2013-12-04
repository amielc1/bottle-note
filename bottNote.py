import sqlite3
from bottle import route ,run ,debug , template , request ,static_file 

@route('/make_db')
def make_db():
    con = sqlite3.connect('notes.db') # Warning: This file is created in the current directory
    con.execute("CREATE TABLE notes (tel char(15) NOT NULL, name char(20) NOT NULL, note char(500) NOT NULL)")
    con.commit()
    return """<p>make db</p>"""

@route('/new', method='GET')
def new_item():
    if request.GET.get('save','').strip():
        name = request.GET.get('_name','').strip()
        tel =request.GET.get('tel','').strip()
        note =request.GET.get('_note','').strip()
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute("INSERT INTO notes (tel,name,note) VALUES (?,?,?)", (tel,name,note))
        own = c.lastrowid
        conn.commit()
        c.close()

        return '<p>The new note was inserted into the database, the owner  is %s</p>' % own
    else:
        return template('new_note.tpl')

@route('/show')
def show_list():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT name ,tel ,note FROM notes ;")
    result = c.fetchall()
    c.close()
    output = template('make_table', rows=result)
    return output

@route('/check')
def check():
    con = sqlite3.connect('notes.db')
    if con.cursor() : 
        return con.cursor().execute("select * from notes").fetchone()
    else : 
        return """False"""

@route('/del')
def delNote():
    conn = sqlite3.connect('notes.db')
    c =conn.cursor()
    c.execute("delete * from notes")
    conn.commite()
    c.close()

run(host='localhost', port=8080,
    debug=True, reloader=True)
