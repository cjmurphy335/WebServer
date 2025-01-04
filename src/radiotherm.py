import logging
from flask import Flask, jsonify, request

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='api_requests.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

@app.route('/api/data', methods=['GET'])
def get_data():
    logging.info(f"GET request received")
    data = {"message": "Hello, Raspberry Pi!"}
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def post_data():
    new_data = request.json
    logging.info(f"POST request received with data: {new_data}")
    return jsonify({"received": new_data}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
