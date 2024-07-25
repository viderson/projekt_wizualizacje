from flask import Flask, request, render_template, redirect, url_for, flash, send_file
import os, sys
import subprocess
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'

main_dir = os.path.dirname(os.path.abspath(__file__)) + '/'
UPLOAD_FOLDER = main_dir + 'uploads/'
GENERATED_FOLDER = main_dir + 'generated/'
os.makedirs(GENERATED_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = ['xlsx']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nie znaleziono części pliku')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Nie wybrano pliku')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = UPLOAD_FOLDER + filename
            file.save(file_path)
            return redirect(url_for('file_selected', filename=filename))
        else:
            flash('Nieprawidłowy format pliku. Dozwolone są tylko pliki .xlsx')
            return redirect(request.url)
    return render_template('index.html')

@app.route('/file_selected/<filename>')
def file_selected(filename):
    file_path   = UPLOAD_FOLDER + filename
    output_file = GENERATED_FOLDER + 'fedropol_map.html'
    
    # Uruchamiamy skrypt generate_map.py z przekazanym plikiem
    subprocess.run([sys.executable, main_dir + 'generate_map.py',
				file_path, # argv 1
			        output_file]) # argv 2
    return send_file(output_file)

@app.route('/unload', methods=['POST'])
def tab_closed():
        os._exit(0)
        return '', 204

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=False)
