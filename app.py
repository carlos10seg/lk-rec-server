from flask import Flask, jsonify, abort, make_response, request
from controller import Controller
#from recommender import Recommender

app = Flask(__name__)

@app.route('/lkpy/create_structure', methods=['GET'])
def create_structure():
    ctrl = Controller()
    ctrl.create_db_structure_with_data()
    return jsonify({"result": 'ok'})

# Save all the algo models to disk
# http://127.0.0.1:5001/lkpy/save_models/popular,bias
@app.route('/lkpy/save_models/<algos>', methods=['GET'])
def save_models(algos):
    ctrl = Controller()
    ctrl.save_models(algos)
    return jsonify({"result": 'ok'})

# Test local urls:
# http://127.0.0.1:5001/lkpy/recommend/popular/30/10
@app.route('/lkpy/recommend/<algo>/<int:user_id>/<int:num_recs>', methods=['GET'])
def recommend(algo, user_id, num_recs):
    ctrl = Controller()
    recs = ctrl.get_recs_using_model(user_id, num_recs, algo, None)
    return jsonify({'recommendations': recs})
 
 # Test local urls:
 # http://127.0.0.1:5001/lkpy/predict/bias/22/10/5,102,203,304,400
@app.route('/lkpy/predict/<algo>/<int:user_id>/<int:num_recs>/<items>', methods=['GET'])
def predict(algo, user_id, num_recs, items):
    ctrl = Controller()
    items = list(map(int, items.split(',')))
    recs = ctrl.get_recs(user_id, num_recs, algo, items)
    return jsonify({'predictions': recs})

if __name__ == '__main__':
    app.run(debug=True, port=5001)