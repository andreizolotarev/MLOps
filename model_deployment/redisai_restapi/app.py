from redisai import Client
import sys
import traceback
from flask import Flask, request, jsonify
import ast

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# connect to RedisAI
con = Client(host='redisai', port=6379)
# load the model
con.modelset(key='iris_model',
             backend='ONNX',
             device='CPU',
             data=open('iris.onnx', 'rb').read(),
             outputs=['classes', 'confidence'])
             
# iris features: sepal_length, sepal_width, petal_length, petal_width
# labels: 0-'iris_setosa', 1-'iris_versicolor', 2-'iris_virginica'

def flower_label(class_int):
    '''Convert class integer to the text label'''
    if class_int == 0:
        prediction = 'iris_setosa'
    if class_int == 1:
        prediction = 'iris_versicolor'
    if class_int == 2:
        prediction = 'iris_virginica'
    return prediction

@app.route('/predict', methods=['POST'])
def predict():
    try:
        dic = request.get_data().decode('ISO-8859-1')
        dic = ast.literal_eval(dic)
        print('input:\n', dic)
        con.tensorset(key='to_predict', tensor=dic['features'], shape=[1,4], dtype='float')
        con.modelrun(key='iris_model', inputs='to_predict', outputs=['class', 'confidence'])
        return jsonify({'prediction': flower_label(class_int=con.tensorget(key='class')[0])})
    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()})

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except Exception as e:
        port = 80
    app.run(host='0.0.0.0', port=port, debug=True)
