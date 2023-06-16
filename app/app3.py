from flask import Flask, request
from models.Matrix import Matrix
app = Flask(__name__)


matrix = Matrix()

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
    initial_data["Matrix"] = matrix.set_Size_of_Matrix(size[0], size[1]).tolist()
    initial_data["min_asig"] = {f'M{x}': 1 for x in range(1, size[0]+1)}
    initial_data["available_res"] = requested_data.get("available_res")
    initial_data["optimizer"] = requested_data.get("optimizer")
    return initial_data


@app.route("/fill_matrix", methods=['POST'])
def show_loaded_data():
    requested_data = request.json
    matrixLocaly = requested_data.get("matrix")
    matrix.fill_Matrix(matrixLocaly)
    r = matrix.getBenefits(0)
    return {"matrix": matrix.matrix.tolist(), "r": r}

@app.route("/solution", methods=["POST"])
def make_Solution():
    requested_data = request.json
    return requested_data


if __name__ == '__main__':
    app.run(debug=True)