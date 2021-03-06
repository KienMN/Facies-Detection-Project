import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from detection.competitive_learning_network import AdaptiveLVQ
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import numpy as np
from sklearn.preprocessing import LabelEncoder
import json

app = Flask(__name__)
api = Api(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

DEFAULT_ARGUMENTS = {
  "size": 9,
  "learning_rate": 0.5,
  "decay_rate": 1,
  "bias": True,
  "weights_init": "pca",
  "sigma": 1,
  "sigma_decay_rate": 1,
  "neighborhood": "gaussian",
  "label_weight": "inverse_distance"
}

class SsomTrainingApi(Resource):

  def post(self):
    # Message and warning
    message = ""
    warning = ""

    # Required and optional
    required_params_name = ['size', 'first_num_iteration', 'second_num_iteration', 'first_epoch_size', 'second_epoch_size']
    optional_params_name = ['learning_rate', 'decay_rate', 'bias', 'weights_init', 'sigma', 'sigma_decay_rate', 'neighborhood', 'label_weight']
    
    # Getting data from request
    body_data = request.get_json()
    
    # Getting arguments sent to server
    if body_data.get('model_id'):
      model_id = body_data.get('model_id')
    else:
      message = "No {} is provided!".format("model id")
      return {"message": message}, 400
    
    if body_data.get('params'):
      body_params = body_data.get('params')
    else:
      message = "No {} is provided!".format("params")
      return {"message": message}, 400

    if body_data.get('dataset'):
      body_dataset = body_data.get('dataset')
    else:
      message = "No {} is provided!".format("dataset")
      return {"message": message}, 400
    
    # Getting parameters sent to server
    params = {}

    for param_name in required_params_name:
      if body_params.get(param_name) is not None:
        params[param_name] = body_params.get(param_name)
      else:
        message = "No {} is provided!".format(param_name)
        return {"message": message}, 400
    
    for param_name in optional_params_name:
      if body_params.get(param_name) is not None:
        params[param_name] = body_params.get(param_name)
      else:
        params[param_name] = DEFAULT_ARGUMENTS.get(param_name)
        warning += "No {} is provided, using default {} instead.\n".format(param_name, str(DEFAULT_ARGUMENTS.get(param_name)))

    # Getting the dataset sent to server
    X = body_dataset.get('features')
    y = body_dataset.get('target')
    try:
      X_train = np.array(X).astype(np.float)
      if len(X_train.shape) < 2:
        raise ValueError
      X_train = X_train.T
      y_train = np.array(y).astype(np.int8)
      if len(X_train) != len(y_train):
        return {"message": "Dataset is not compatible"}, 400
    except ValueError:
      message = "Dataset is expected to be numbers. Features are expected to be 2 dimensions array"
      return {"message": message}, 400

    # Validating the arguments
    try:
      params['size'] = int(params.get('size'))
      params['first_num_iteration'] = int(params.get('first_num_iteration'))
      params['second_num_iteration'] = int(params.get('second_num_iteration'))
      params['first_epoch_size'] = int(params.get('first_epoch_size'))
      params['second_epoch_size'] = int(params.get('second_epoch_size'))
    except ValueError:
      message = "Size, number of iterations and epoch size are expected to be integer numbers."
      return {"message": message}, 400

    try:
      params['learning_rate'] = float(params.get('learning_rate'))
      params['decay_rate'] = float(params.get('decay_rate'))
      params['sigma'] = float(params.get('sigma'))
      params['sigma_decay_rate'] = float(params.get('sigma_decay_rate'))
    except ValueError:
      message = "Learning rate, sigma and decay rates are expected to be float numbers."
      return {"message": message}, 400

    if params.get('bias'):
      params['bias'] = True
    else:
      params['bias'] = False

    if params.get('weights_init') not in ['pca', 'random', 'sample']:
      params['weights_init'] = DEFAULT_ARGUMENTS.get('weights_init')
      warning += "Can not understand weights init, using default {} instead.\n".format(DEFAULT_ARGUMENTS.get('weights_init'))

    if params.get('neighborhood') not in ['bubble', 'gaussian']:
      params['neighborhood'] = DEFAULT_ARGUMENTS.get('neighborhood')
      warning += "Can not understand neighborhood, using default {} instead.\n".format(DEFAULT_ARGUMENTS.get('neighborhood'))

    if params.get('label_weight') not in ['uniform', 'exponential_distance', 'inverse_distance']:
      params['label_weight'] = DEFAULT_ARGUMENTS.get('label_weight')
      warning += "Can not understand label weight, using default {} instead.\n".format(DEFAULT_ARGUMENTS.get('label_weight'))

    # Training the model
    ssom = AdaptiveLVQ(n_rows = params.get('size'), n_cols = params.get('size'),
                      learning_rate = params.get('learning_rate'), decay_rate = params.get('decay_rate'),
                      bias = params.get('bias'), weights_init = params.get('weights_init'),
                      sigma = params.get('sigma'), sigma_decay_rate = params.get('sigma_decay_rate'),
                      neighborhood = params.get('neighborhood'), label_weight = params.get('label_weight'))

    ssom.fit(X_train, y_train, params.get('first_num_iteration'), params.get('first_epoch_size'),
            params.get('second_num_iteration'), params.get('second_epoch_size'))
    # ssom.details()

    # Dumping the models
    from sklearn.externals import joblib
    model_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dump_model/' + model_id + ".sav")
    joblib.dump(ssom, model_filepath)

    message = "success"
    return {"message": message, "warning": warning}, 200

class SsomVerificationApi(Resource):

  def post(self):
    # Getting data sent to server
    body_data = request.get_json()

    # Getting arguments sent to server
    if body_data.get('model_id'):
      model_id = body_data.get('model_id')
    else:
      message = "No {} is provided!".format("model id")
      return {"message": message}, 400

    if body_data.get('dataset'):
      dataset = body_data.get('dataset')
    else:
      message = "No {} is provided!".format("dataset")
      return {"message": message}, 400

    # Validating dataset
    X = dataset.get('features')
    y = dataset.get('target')
    try:
      X_val = np.array(X).astype(np.float)
      if len(X_val.shape) < 2:
        raise ValueError
      X_val = X_val.T
      y_val = np.array(y).astype(np.int8)
      if len(X_val) != len(y_val):
        return {"message": "Dataset is not compatible"}, 400
    except ValueError:
      message = "Dataset is expected to be numbers. Features are expected to be 2 dimensions array"
      return {"message": message}, 400

    # Loading trained model
    from sklearn.externals import joblib
    try:
      model_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dump_model/' + model_id + ".sav")
      ssom = joblib.load(model_filepath)
    except FileNotFoundError:
      return {"message": "Model does not exist."}, 400

    # Making prediction
    y_pred = ssom.predict(X_val).astype(np.int8)

    # Making confusion matrix
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_val, y_pred)

    # Calculating accuracy
    true_pred = 0
    for i in range (len(cm)):
      true_pred += cm[i][i]
    accuracy = true_pred / np.sum(cm)

    # Generating response
    response = {}
    response['target_prediction'] = y_pred.tolist()
    response['confusion_matrix'] = cm.tolist()
    response['accuracy'] = accuracy
    response['message'] = 'success'
    response['status'] = 200
    response = json.dumps(response)
    # print(response)
    return response, 200

class SsomPredictionApi(Resource):

  def post(self):
    # Getting data sent to server
    body_data = request.get_json()

    # Getting arguments sent to server
    if body_data.get('model_id'):
      model_id = body_data.get('model_id')
    else:
      message = "No {} is provided!".format("model id")
      return {"message": message}, 400

    if body_data.get('dataset'):
      dataset = body_data.get('dataset')
    else:
      message = "No {} is provided!".format("dataset")
      return {"message": message}, 400

    # Validating dataset
    X = dataset.get('features')
    try:
      X_pred = np.array(X).astype(np.float)
      if len(X_pred.shape) < 2:
        raise ValueError
      X_pred = X_pred.T
    except ValueError:
      message = "Dataset is expected to be numbers. Features are expected to be 2 dimensions array"
      return {"message": message}, 400

    # Loading trained model
    from sklearn.externals import joblib
    try:
      model_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dump_model/' + model_id + ".sav")
      ssom = joblib.load(model_filepath)
    except FileNotFoundError:
      return {"message": "Model does not exist."}, 400

    # Making prediction
    y_pred = ssom.predict(X_pred).astype(np.int8)

    # Generating response
    response = {}
    response['target_prediction'] = y_pred.tolist()
    response['message'] = 'success'
    response['status'] = 200
    response = json.dumps(response)
    # print(response)
    return response, 200

class SsomModelApi(Resource):

  def get(self, model_id):
    return {"model_id": model_id}, 200



api.add_resource(SsomTrainingApi, '/api/v1/ssom/train')
api.add_resource(SsomVerificationApi, '/api/v1/ssom/verify')
api.add_resource(SsomPredictionApi, '/api/v1/ssom/predict')
api.add_resource(SsomModelApi, '/api/v1/ssom/models/<model_id>')

if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = 1234)