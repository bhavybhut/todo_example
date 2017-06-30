import sqlite3
from bottle import route, run, debug, template, request, redirect, get, static_file

@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='./static/')

@route('/')
@route('/todo')
def todo():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task, status FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    c.execute("SELECT id, task, status FROM todo WHERE status LIKE '0'")
    res_closed = c.fetchall()
    c.close()
    output = template('make_table', rows=result, closed=res_closed)
    return output

@route('/new', method='POST')
def new_item():
    new = request.POST.task.strip()
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new, 1))
    new_id = c.lastrowid
    conn.commit()
    c.close()
    return redirect("/")

@route('/search', method='POST')
def new_item():
    item = request.POST.searchtxt.strip()
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    item = "%" + item + "%"
    c.execute("SELECT id, task, status FROM todo WHERE task LIKE ? AND status LIKE '1'", (str(item),))
    result = c.fetchall()
    c.execute("SELECT id, task, status FROM todo WHERE task LIKE ? AND status LIKE '0'", (str(item),))
    res_closed = c.fetchall()
    c.close()
    if not result:
        output = template('make_table', rows=result, closed=res_closed)
        return output
    else:
        output = template('make_table', rows=result, closed=res_closed)
        return output
        #return 'Task ID: '+str(result[0][0])+'and Task: '+str(result[0][1])

@route('/edit/<no:int>', method='GET')
def edit_item(no):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no),))
    cur_data = c.fetchone()
    return template('edit_task', old=cur_data, no=no)

@route('/edit/<no:int>', method='POST')
def edit_item(no):
    edit = request.POST.task.strip()
    status = request.POST.status.strip()
    if status == 'open':
        status = 1
    else:
        status = 0
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit, status, no))
    conn.commit()
    return redirect("/")

@route('/delete/<i:int>', method='GET')
def delete_item(i):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM todo WHERE id = ?", (str(i),))
    conn.commit()
    return redirect("/")

debug(True)
run(reloader=True)