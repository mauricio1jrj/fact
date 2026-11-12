from src import create_app

app = create_app('development')

if __name__ == '__main__':
    print("T frontend iniciando en http://localhost:5000")
    app.run(debug=True,port=5000)


"""@app.route("/")
def index():
    return render_template("index.html")


@app.route("/lista-clientes")
def listaClientes():
    return render_template("Lista_Clientes.html")

@app.route("/nuevo-cliente")
def nuevoCliente():
    return render_template("Nuevo_Cliente.html")

@app.route("/lista-facturas")
def listafact():
    return render_template("Lista_facturas.html")

@app.route("/nueva-factura")
def nuevafact():
    return render_template("Nueva_factura.html")

@app.route("/eli-factura")
def Elifact():
    return render_template("Eli_Factura.html")

@app.route("/lista-vendedor")
def listvende():
    return render_template("Lista_vendedor.html")

@app.route("/nuevo-vendedor")
def nuevovende():
    return render_template("Nuevo_vendedor.html")

@app.route("/nuevo-producto")
def nuevoproduc():
    return render_template("Nuevo_producto.html")

@app.route("/lista-producto")
def listproduc():
    return render_template("Lista_productos.html")



if __name__ == '__main__':
    app.run(debug=True)"""