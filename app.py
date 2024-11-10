import sqlite3
from flask import Flask,redirect,render_template,url_for,request
#producto(id : integer, descripcion: texto, cantidad:integer, precio:float)
app=Flask(__name__)
def init_database():
    conn = sqlite3.connect("almacen.db")

    cursor=conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS producto(
        id INTEGER PRIMARY KEY,
        descripcion TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio DECIMAL(10,2) NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

init_database()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/productos")
def productos():
    conn=sqlite3.connect("almacen.db")
    conn.row_factory=sqlite3.Row

    cur=conn.cursor()
    cur.execute("SELECT * FROM producto")
    productos=cur.fetchall()
    return render_template("productos/index.html",productos=productos)

@app.route("/productos/crear")
def producto_crear():
    return render_template("productos/crear.html")

@app.route("/productos/crear/guarda",methods=['POST'])
def producto_sv():
    descripcion=request.form['descripcion']
    cantidad=request.form['cantidad']
    precio=request.form['precio']

    conn=sqlite3.connect("almacen.db")
    cur=conn.cursor()

    cur.execute("INSERT INTO producto (descripcion,cantidad,precio) VALUES (?,?,?)",(descripcion,cantidad,precio))

    conn.commit()
    conn.close()
    return redirect("/productos")

@app.route("/productos/edit/<int:id>")
def producto_edit(id):
    conn=sqlite3.connect("almacen.db")
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()

    cur.execute("SELECT * FROM producto WHERE id=?",(id,))
    producto=cur.fetchone()
    conn.close()
    return render_template("productos/editar.html",producto=producto)

@app.route("/productos/update",methods=['POST'])
def productos_update():
    id=request.form['id']
    descripcion=request.form['descripcion']
    cantidad=request.form['cantidad']
    precio=request.form['precio']

    conn=sqlite3.connect("almacen.db")
    cu=conn.cursor()

    cu.execute("UPDATE producto SET descripcion=?,cantidad=?,precio=? WHERE id=?",(descripcion,cantidad,precio,id))

    conn.commit()
    conn.close()
    return redirect("/productos")

@app.route("/productos/borrar/<int:id>")
def productos_del(id):
    conn=sqlite3.connect("almacen.db")
    cur=conn.cursor()

    cur.execute("DELETE FROM producto WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect("/productos")


if __name__=="__main__":
    app.run(debug=True)