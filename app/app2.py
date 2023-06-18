from flask import Flask, render_template, request
from models.Destino import Destino
from models.Aignacion import Asignacion
from config import config

app = Flask(__name__)
asig = Asignacion()

@app.route('/')
def show_home_view():
    return render_template('home_view.html')

def generate_dest_list(num: int) -> list:
    dest_list = []
    for i in range(1, num+1):
        dest_list.append(Destino(request.form.get(f'dest_{i}_name')))
    return dest_list

def generate_op_list(num: int) -> list:
    op_list = []
    for i in range(1, num + 1):
        op_list.append(int(request.form.get(f'option_{i}')))
    return op_list

@app.route('/data/setUp', methods=['POST'])
def show_dataInput_view():
    
    try:
        opNum = int(request.form.get('nud_options'))
        destNum = int(request.form.get('nud_dest'))

        asig.set_destinos(generate_dest_list(destNum))
        asig.set_opciones(generate_op_list(opNum))

        data = asig
        correct = True

    except Exception as ex:
        correct = False
        data = None
    finally:
        return render_template('dataInput_view.html', data=data, correct=correct)
    

@app.route('/data/intervals', methods=['POST'])
def show_interval_view():
    try:
        
        for dest in asig.get_destinos():
            benefit = {}
            for op in asig.get_opciones():
                benefit[op] = request.form.get(f'{op}_{dest.get_nombre()}_value')
            dest.set_benefit(benefit)
        
        correct = True
    except Exception as ex:
        data = None
        correct = False
        print(ex.with_traceback())
    finally:
        return render_template('interval_view.html', correct=correct, data = data)

@app.route('/sol')
def show_solution_view():
    pass

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()