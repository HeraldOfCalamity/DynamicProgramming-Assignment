from flask import Flask, request
from models.Matrix import Matrix
from models.Etapa import Etapa
app = Flask(__name__)


ProblemMatrix = Matrix()
cost = None

initial_data = {
    "min_asig": None,
    "available_res": None,
    "optimizer": None,
    "Matrix": None
}

@app.route("/", methods=['POST', 'GET'])
def hello_function():
    return {"message": "Hello World"}


@app.route("/initial_data", methods=["POST"])
def get_Initial_Data():
    requested_data = request.json
    size = requested_data.get('size')
    initial_data["Matrix"] = ProblemMatrix.set_Size_of_Matrix(size[0], size[1]).tolist()
    initial_data["min_asig"] = {f'M{x}': 1 for x in range(1, size[0]+1)}
    initial_data["available_res"] = requested_data.get("available_res")
    initial_data["optimizer"] = requested_data.get("optimizer")
    print(ProblemMatrix.matrix)
    return initial_data


@app.route("/fill_matrix", methods=['POST'])
def show_loaded_data():
    global cost
    requested_data = request.json
    matrixLocaly = requested_data.get("matrix")
    ProblemMatrix.fill_Matrix(matrixLocaly)
    cost = ProblemMatrix.getBenefits(2)
    print(ProblemMatrix.matrix)
    return {"matrix": ProblemMatrix.matrix.tolist(), "r": cost}

@app.route("/solution", methods=["POST"])
def make_Solution():
    global cost
    requested_data = request.json
    f = requested_data.get('f')
    etapa = Etapa()
    etapa.set_Size_of_Matrix(requested_data.get("range"), len(requested_data.get("nro")))
    etapa.iterations(cost, f)
    print(etapa.matrix)
    return {"r": cost}

if __name__ == '__main__':
    app.run(debug=True)