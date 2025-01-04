from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Set up logging to capture raw request data
logging.basicConfig(filename='thermostat_post.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

@app.route('/api/data', methods=['POST'])
def post_data():
    # Capture raw data
    raw_data = request.get_data(as_text=True)
    logging.info(f"POST request received with data: {raw_data}")

    # Optionally, return a simple response to acknowledge the request
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
