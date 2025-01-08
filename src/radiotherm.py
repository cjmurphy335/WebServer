from flask import Flask, request, jsonify
import json
import logging

app = Flask(__name__)
logging.basicConfig(filename='mixed_data.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

@app.route('/api/data', methods=['POST'])
def post_data():
    raw_data = request.get_data()

    with open('raw_payload.bin', 'wb') as f:
        f.write(raw_data)

    logging.info(f"Received {len(raw_data)} bytes")

    return jsonify({"status": "received"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

