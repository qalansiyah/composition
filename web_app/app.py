from flask import Flask, request, render_template
import pickle
import tensorflow as tf
from catboost import CatBoostRegressor

cat = CatBoostRegressor()

app = Flask(__name__)

@app.route('/')
def choose_prediction_method():
    return render_template('main.html')


def matrix_fill_prediction(params):
    model = tf.keras.models.load_model('models/matrix_fill/')
    pred = model.predict(params)
    return pred

def strength_prediction(params):
    model = cat.load_model('models/strength.cbm',format='cbm')
    pred = model.predict([params])
    return pred

def elasticy_prediction(params):
    model = cat.load_model('models/elasticity.cbm',format='cbm')
    pred = model.predict([params])
    return pred 


@app.route('/matrix_fill/', methods=['POST', 'GET'])
def matrix_fill():
    message = ''
    if request.method == 'POST':
        param_list = ('density', 'elast', 'hardener', 'ep_group', 'temp', 'surf_density', 'elast_tension', 'st_tension', 'resin', 'angle', 'step', 'patch')
        params = []
        for i in param_list:
            param = request.form.get(i)
            params.append(param)
        params = [float(i.replace(',', '.')) for i in params]

        message = f'Спрогнозированное Соотношение матрица-наполнитель для введенных параметров: {matrix_fill_prediction(params)}'
    return render_template('matrix_fill.html', message=message)

@app.route('/strength/', methods=['POST', 'GET'])
def strength():
    message = ''
    if request.method == 'POST':
        param_list = ('matrix', 'density', 'elast', 'hardener', 'ep_group', 'temp', 'surf_density',  'resin', 'angle', 'step', 'patch')
        params = []
        for i in param_list:
            param = request.form.get(i)
            params.append(param)
        params = [float(i.replace(',', '.')) for i in params]

        message = f'Спрогнозированное значение Прочности при растяжении для введенных параметров: {strength_prediction(params)} МПа'
    return render_template('strength.html', message=message)

@app.route('/elasticy/', methods=['POST', 'GET'])
def elasticy():
    message = ''
    if request.method == 'POST':
        param_list = ('matrix', 'density', 'elast', 'hardener', 'ep_group', 'temp', 'surf_density',  'resin', 'angle', 'step', 'patch')
        params = []
        for i in param_list:
            param = request.form.get(i)
            params.append(param)
        params = [float(i.replace(',', '.')) for i in params]
        
        message = f'Спрогнозированное значение Модуля упругости при растяжении для введенных параметров: {elasticy_prediction(params)} ГПа'
    return render_template('elasticy.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
