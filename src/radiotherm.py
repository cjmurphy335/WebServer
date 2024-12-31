from flask import Flask, jsonify, request

app = Flask(__name__)

# Example endpoint
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello, Raspberry Pi!"}
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def post_data():
    new_data = request.json
    return jsonify({"received": new_data}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
