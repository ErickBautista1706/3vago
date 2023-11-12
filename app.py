from flask import Flask, url_for, render_template

app = Flask(__name__, static_folder='static')

@app.route("/")
def hello_world():
    return render_template('temp.html')

@app.route("/inicio")
def login():
    return render_template('inicio.html')

@app.route("/admin")
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)