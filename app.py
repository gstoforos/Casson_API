from flask import Flask, request, jsonify
from model_casson import fit_casson_model

app = Flask(__name__)

@app.route('/fit', methods=['POST'])
def fit():
    try:
        data = request.get_json()
        shear_rates = data.get("shear_rates", [])
        shear_stresses = data.get("shear_stresses", [])
        flow_rate = data.get("flow_rate", 1)
        diameter = data.get("diameter", 1)
        density = data.get("density", 1)

        result = fit_casson_model(shear_rates, shear_stresses, flow_rate, diameter, density)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
