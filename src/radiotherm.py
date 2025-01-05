from flask import Flask, request, jsonify
import json
import logging

app = Flask(__name__)
logging.basicConfig(filename='mixed_data.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

@app.route('/api/data', methods=['POST'])
def post_data():
    # Get the raw binary data from the request
    raw_data = request.get_data()

    try:
        # Assume the first 10 bytes are binary, and the rest is JSON
        binary_part = raw_data[:10]
        json_part = raw_data[10:].decode('utf-8')

        # Log or save the binary part
        with open('binary_data.bin', 'wb') as f:
            f.write(binary_part)

        # Parse the JSON part
        parsed_json = json.loads(json_part)

        # Log or process the parsed JSON
        logging.info(f"Parsed JSON data: {parsed_json}")

        return jsonify({"status": "success", "parsed_json": parsed_json}), 200
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logging.error(f"Failed to parse JSON: {e}")
        return jsonify({"error": "Malformed data"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
