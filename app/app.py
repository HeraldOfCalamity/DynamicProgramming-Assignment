from flask import Flask, render_template, request, make_response, redirect, send_file, jsonify
import numpy as np
from models.Etapa import Etapa
from models.Destino import Destino
from models.Asignacion import Asignacion
from config import config
from models.Matrix import Matrix
from models.Solution import Solution
from models.exportToPdf import create_pdf
from models.Grafo import *
import json
from flask_cors import *
app = Flask(__name__)
asig = Asignacion()
problemMatrix = Matrix()
sol = Solution()
cors = CORS(app, resources={r"/create_graph": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


def jinja_zip(*args):
    return zip(*args)


app.jinja_env.filters['zip'] = jinja_zip


@app.route('/')
def show_home():
    return render_template('true_home_view.html', data=asig)


@app.route('/graph')
def show_graph_view():
    return render_template('graph_view.html', data=None)


@app.route('/asignacion')
def show_asig_view():
    global asig, problemMatrix, sol
    load_cookie()
    loadMatrixCookie()
    asig = Asignacion()
    problemMatrix = Matrix()
    sol = Solution()
    return render_template('asig_view.html', data=asig)


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


def generateRanges(i):
    rangos = None
    if i:
        rangos = list(reversed(list(x.get_rango()
                      for x in asig.get_destinos())))
        rangos = np.array([list(range(start, end + 1))
                          for start, end in rangos])
        rangos[-1] = [rangos[-1][-1]]
    else:
        rangos = list(reversed(list(x.get_rango()
                      for x in asig.get_destinos())))
    return rangos


def destParser(datos):
    dset = []
    for d in datos:
        nombre = d['name']
        beneficio = d['benefits']
        range = d['range']
        if d['benefits'] is not None:
            try:
                beneficios = {int(k): v for k, v in d['benefits'].items()}
                beneficio = beneficios
            except ValueError:
                beneficios = None
        dset.append(Destino(nombre, benefit=beneficio, rango=range))
    return dset


def load_cookie():
    if request.cookies.get('asig') == None:
        pass
    else:
        asig_data = json.loads(request.cookies.get('asig'))
        opNum = asig_data['opNum']
        destNum = asig_data['destNum']
        resNum = int(asig_data['resNum'])
        caso = str(asig_data['caso'])

        asig.set_destinos(destParser(destNum))
        asig.set_opciones(opNum)
        asig.set_caso(caso)
        asig.set_recurso(resNum)


@app.route('/data/setUp', methods=['POST', 'GET'])
def show_dataInput_view():
    error = ''
    try:
        load_cookie()
        correct = True

    except Exception as ex:
        correct = False
        error = ex
    finally:
        return render_template('dataInput_view.html', data=asig, correct=correct, error=error)


@app.route('/setCookie', methods=["POST"])
def setCookie():
    if request.method == 'POST':
        opNum = int(request.form.get('nud_options'))
        destNum = int(request.form.get('nud_dest'))
        resNum = int(request.form.get('nud_resAmount'))
        caso = str(request.form.get('slc_case'))

        dst = generate_dest_list(destNum)
        toCookie = {
            'opNum': generate_op_list(opNum),
            'destNum': [x.__dict__() for x in dst],
            'resNum': resNum,
            'caso': caso
        }

        resp = make_response(redirect('/data/setUp'))
        resp.set_cookie('asig', json.dumps(toCookie))
        return resp


@app.route('/graph/sol', methods=["POST"])
def get_graph_sol():
    new_graph()
    graph = {}

    nud_nodes = int(request.form.get('nud_nodes'))
    for i in range(1, nud_nodes+1):
        dests = request.form.getlist(f'dests_{i}')
        weights = []
        for dest in dests:
            weights.append(request.form.get(f'costo_{i}_{dest}'))
        graph[i] = {'name': request.form.get(
            f'desde_{i}'), 'sig': dests, 'weights': weights}

    fillNodes(graph)
    fill_edges(graph)
    saveGraph('temp.jpg')
    return render_template('graph_solution.html', graph=graph)
    # return nud_nodes


@app.route('/data/etapas/<int:id>')
def getEtapas(id):
    load_cookie()
    loadMatrixCookie()
    error = None
    try:
        asig.get_etapas()[id]
        correct = True
    except Exception as ex:
        correct = False
        error = ex
    return render_template('etapas.html', data=asig, correct=correct, id=id, error=error)


@app.route('/setCookie/matrix', methods=['POST'])
def createMatrixCookie():

    for dest in asig.get_destinos():
        benefit = {}
        for op in asig.get_opciones():
            benefit[op] = float(request.form.get(
                f'{op}_{dest.get_nombre()}_value'))
        dest.set_benefit(benefit)

    asig.get_rangos()
    toCookie = {
        "dests": [x.__dict__() for x in asig.get_destinos()]
    }
    resp = make_response(redirect('/data/intervals'))
    resp.set_cookie('matrix', json.dumps(toCookie))
    return resp


def loadMatrixCookie():
    if request.cookies.get('matrix') == None:
        pass
    else:
        matrix_data = json.loads(request.cookies.get('matrix'))
        # print(f"data matrix -> {matrix_data}")
        asig.set_destinos(destParser(matrix_data['dests']))


@app.route('/data/intervals', methods=['POST', 'GET'])
def show_interval_view():
    error = ''
    try:
        load_cookie()
        loadMatrixCookie()
        print([x.get_benefit()[1] for x in asig.get_destinos()])
        rangos = generateRanges(True)
        asig.set_rangos(rangos)
        sol.rangos = rangos

        _, _, sol.d = get_Iteration()
        # print(asig.get_etapas())
        correct = True

    except Exception as ex:
        correct = False
        error = ex
        print(ex)

    finally:
        return render_template('interval_view.html', correct=correct, data=asig, error=error)


def get_Iteration():
    asig.set_etapas([])
    problemMatrix.fill_Matrix(asig.get_matriz())
    rangos = generateRanges(False)
    f = [0] * len(asig.get_opciones())
    for index, (ra, i) in enumerate(zip(rangos, range(0, problemMatrix.matrix.shape[1]))):
        r = problemMatrix.getBenefits((problemMatrix.columns-1)-i)
        etapa = Etapa()
        if index == len(rangos) - 1:
            etapa.set_Size_of_Matrix(1, len(asig.get_opciones()))
            f = etapa.iterations(r, f, True, asig.get_caso())
            asig.get_etapas().append(etapa)
            asig.get_fs().append(f)
            etapa.get_destinations(asig.get_opciones(), f)
            asig.get_ds().append(etapa.d)
        else:
            etapa.set_Size_of_Matrix(
                ((ra[1] - ra[0]) + 1), len(asig.get_opciones()))
            f = etapa.iterations(r, f, False, asig.get_caso())
            asig.get_etapas().append(etapa)
            asig.get_fs().append(f)

            etapa.get_destinations(asig.get_opciones(), f)
            asig.get_ds().append(etapa.d)

    return (
        asig.get_etapas(),
        asig.get_fs(),
        asig.get_formated_ds()
    )


@app.route('/sol')
def show_solution_view():
    error = ''
    try:
        sol.createDictonaryPartialAnswer()
        asig.set_solution(sol.createSolutionMatrix())

        correct = True
        # print(asig.get_solution())
    except Exception as ex:
        correct = False
        error = ex
    finally:
        print(error)
        return render_template('solution_view.html', correct=correct, data=asig, error=error)


@app.route("/toPdf")
def toPdfo():
    create_pdf("./app/temp/temp.pdf", asig)
    nombre = 'Solucion.pdf'
    return send_file('./temp/temp.pdf', as_attachment=True, download_name=nombre)
    # return "Creado!"


@app.route('/manual')
def manual():
    return render_template('manual_usuario.html', data=asig)


@app.route('/create_graph', methods=["POST"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def c_graph():
    new_graph()
    json = request.get_json()

    if json is None:
        return jsonify({'error': 'Invalid JSON data'}), 400
    # print(json['1'])
    fillNodes(json)
    fill_edges(json)

    response = {"Message": f"Number of nodes: ",
                "Message2": f"Number of Edges "}
    # response = {"Message": f"test"}
    print(json)
    return jsonify(response)


@app.route('/get_imageGraph')
def getImageGraph():
    saveGraph('temp.jpg')
    return send_file('./temp/temp.jpg', as_attachment=True, download_name="grafo.jpg")


@app.route("/get_shortest_path")
def get_shorttestPath():
    r = request.get_json()
    if r is None:
        return jsonify({"error": "Invalid"}), 400

    source = r["source"]
    dst = r["target"]
    path = find_shortest_path(source, dst)
    distance = find_shortest_distance(source, dst)

    print(path, distance)
    return "Get"


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True)
