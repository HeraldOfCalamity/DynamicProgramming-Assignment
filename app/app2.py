from flask import Flask, render_template, request
from models.Destino import Destino
from config import config

app = Flask(__name__)


@app.route('/')
def show_home_view():
    return render_template('home_view.html')

@app.route('/data/setUp', methods=['POST'])
def show_dataInput_view():
    data = request.form
    return render_template('dataInput_view.html', data=data)

@app.route('/data/benefit')
def show_benefitInput_view():
    pass

@app.route('/data/intervals')
def show_intervals_view():
    pass

@app.route('/sol')
def show_solution_view():
    pass

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()