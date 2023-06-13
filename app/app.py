from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

initial_data = {
    'destinations':['M1', 'M2', 'M3'],
    'asig_options': [1, 2, 3],
    'min_asig': {'M1': 1, 'M2': 1, 'M3': 1},
    'available_res': 6,
    'optimizer': 'max'
}

# benefits = {}
# rangos = {}
@app.route('/')
def index():
    data = {
        'title': 'Pruebitas'
    }
    return render_template('layout.html', data=data)

@app.route('/data')
def show_load_data():
    return render_template('load_data.html', initial_data=initial_data)

@app.route('/sol', methods=['POST'])
def show_loaded_data():
    loaded_data = get_benefits()
    ranges = get_rangos()
    return render_template('loaded_data.html', loaded_data=loaded_data, initial_data=initial_data, ranges=ranges)

def get_benefits():
    benefits = {}
    for dest in initial_data['destinations']:
        _dest = {}
        for op in initial_data['asig_options']:
            _dest[op] = int(request.form.get(f'{op}_{dest}_value'))
        benefits[dest] = _dest
    return benefits

def get_left_sum():
    left = 0
    for dest in initial_data['destinations']:
        left += initial_data['min_asig'][dest]
    return left

def get_rangos():
    rangos = {}
    right_sum = 0
    left_sum = get_left_sum()

    for dest in reversed(initial_data['destinations']):
        min_asig_val = initial_data['min_asig'][dest]
        right_sum += min_asig_val
        left_sum -= min_asig_val

        rangos[dest] = (right_sum, initial_data['available_res'] - left_sum)
    return rangos



if __name__ == "__main__":
    app.run(debug=True, port=5000)