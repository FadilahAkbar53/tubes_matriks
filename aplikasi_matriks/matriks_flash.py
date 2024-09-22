# aplikasi_matriks_flask.py
from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            a = np.array([[float(request.form['a11']), float(request.form['a12'])],
                           [float(request.form['a21']), float(request.form['a22'])]])
            b = np.array([[float(request.form['b11']), float(request.form['b12'])],
                           [float(request.form['b21']), float(request.form['b22'])]])
            result = a + b
            return render_template('index.html', result=result)
        except ValueError:
            return "Error: Pastikan semua nilai adalah angka."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
