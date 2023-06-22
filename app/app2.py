from flask import Flask, render_template, request, make_response, redirect
import numpy as np
from models.Etapa import Etapa
from models.Destino import Destino
from models.Asignacion import Asignacion
from config import config
from models.Matrix import Matrix
from models.Solution import Solution
import json

app = Flask(__name__)

asig = Asignacion()
problemMatrix = Matrix()
sol = Solution()
def jinja_zip(*args):
    return zip(*args)

app.jinja_env.filters['zip'] = jinja_zip
@app.route('/')
def show_home_view():
    global asig, problemMatrix, sol
    asig = Asignacion()
    problemMatrix = Matrix()
    sol = Solution()
    return render_template('home_view.html', data=asig)

def generate_dest_list(num: int) -> list:
    dest_list = []
    for i in range(1, num+1):
        dest_list.append(Destino(request.form.get(f'dest_{i}')))
    return dest_list

def generate_op_list(num: int) -> list:
    op_list = []
    for i in range(1, num + 1):
        op_list.append(int(request.form.get(f'option_{i}')))
    return op_list

@app.route('/data/setUp', methods=['POST', 'GET'])
def show_dataInput_view():
    try:
        opNum = int(request.form.get('nud_options'))
        destNum = int(request.form.get('nud_dest'))
        resNum = int(request.form.get('nud_resAmount'))
        caso = str(request.form.get('slc_case'))

        asig.set_destinos(generate_dest_list(destNum))
        asig.set_opciones(generate_op_list(opNum))
        asig.set_caso(caso)
        asig.set_recurso(resNum)
        correct = True

    except Exception as ex:
        correct = False
        print(ex)
    finally:
        return render_template('dataInput_view.html', data=asig, correct=correct)
    
@app.route('/setCookie', methods=["POST"])
def setCookie():
    if request.method == 'POST':
        opNum = int(request.form.get('nud_options'))
        destNum = int(request.form.get('nud_dest'))
        resNum = int(request.form.get('nud_resAmount'))
        caso = str(request.form.get('slc_case'))



        asig.set_destinos(generate_dest_list(destNum))
        asig.set_opciones(generate_op_list(opNum))
        asig.set_caso(caso)
        asig.set_recurso(resNum)

        toCookie = {
            'opNum': asig.get_opciones(),
            'destNum': asig.get_destinos(),
            'resNum': asig.get_recurso(),
            'caso': asig.get_caso()
        }

        resp = make_response(render_template('dataInput_view.html', data=asig, correct=True))
        resp.set_cookie('asig', json.dumps(toCookie))
        return resp


@app.route('/data/etapas/<int:id>')
def getEtapas(id):
    print(asig.get_rangos())
    return render_template('etapas.html', data=asig, correct=True, id=id)

@app.route('/data/intervals', methods=['POST'])
def show_interval_view():
    try:
        
        for dest in asig.get_destinos():
            benefit = {}
            for op in asig.get_opciones():
                benefit[op] = int(request.form.get(f'{op}_{dest.get_nombre()}_value'))
            dest.set_benefit(benefit)

        asig.get_rangos()
        rangos = list(reversed(list(x.get_rango() for x in asig.get_destinos())))
        rangos = np.array([list(range(start, end + 1)) for start, end in rangos])
        rangos[-1] = [rangos[-1][-1]]
        asig.set_rangos(rangos)
        sol.rangos = rangos

        iterations, fs, d = get_Iteration()
        reformed_d = reformat(d)
        sol.d = reformed_d

        correct = True
        print([x.get_nombre() for x in asig.get_destinos()])

    except Exception as ex:
        correct = False
        print(ex)
        
    finally:
        return render_template('interval_view.html', correct=correct, data=asig, etapas=iterations, rangos=rangos.tolist(), fs=fs, d=reformed_d)


def get_Iteration():
    etapas = []
    fs = []
    ds = []
    problemMatrix.fill_Matrix(asig.get_matriz())
    rangos = list(reversed(list(x.get_rango() for x in asig.get_destinos())))
    f = [0] * len(asig.get_opciones())
    for index, (ra, i) in enumerate(zip(rangos, range(0, problemMatrix.matrix.shape[1]))):
        r = problemMatrix.getBenefits((problemMatrix.columns-1)-i)
        etapa = Etapa()
        if index == len(rangos)- 1:
            etapa.set_Size_of_Matrix(1, len(asig.get_opciones()))
            f = etapa.iterations(r, f, True, asig.get_caso())
            etapas.append(etapa)
            fs.append(f)
            etapa.get_destinations(asig.get_opciones(), f)
            ds.append(etapa.d)
        else:
            etapa.set_Size_of_Matrix(((ra[1] - ra[0]) + 1), len(asig.get_opciones()))
            f = etapa.iterations(r, f, False, asig.get_caso())
            etapas.append(etapa)
            fs.append(f)

            etapa.get_destinations(asig.get_opciones(), f)
            ds.append(etapa.d)
    asig.set_etapas(etapas)
    asig.set_fs(fs)
    asig.set_ds(ds)
    return (etapas, fs, ds)


def reformat(alist):
    nlist = []

    for row in alist:
        tlist = []
        for i in row:
            if len(i) > 1:
                tlist.append(i)
            else:
                tlist.append(i[0])
        nlist.append(tlist)
    return nlist


@app.route('/sol')
def show_solution_view():
    try:
        sol.createDictonaryPartialAnswer()
        asig.set_solution(sol.createSolutionMatrix())

        correct = True
        print(asig.get_solution())
    except Exception as ex:
        correct = False
        print(ex)
    finally:
        return render_template('solution_view.html',correct=correct, data=asig)

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True)