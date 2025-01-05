from flask import Flask, request, jsonify
import json
import logging

app = Flask(__name__)
logging.basicConfig(filename='mixed_data.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

@app.route('/api/data', methods=['POST'])
def post_data():
    raw_data = request.get_data()

    try:
        # Find the start of the JSON data (assuming it starts with '{')
        json_start = raw_data.find(b'{')

        if json_start == -1:
            raise ValueError("No JSON data found")

        # Extract binary and JSON parts
        binary_part = raw_data[:json_start]
        json_part = raw_data[json_start:].decode('utf-8')

        # Log the binary part for inspection
        with open('binary_data.bin', 'wb') as f:
            f.write(binary_part)

        # Parse the JSON part
        parsed_json = json.loads(json_part)
        logging.info(f"Parsed JSON data: {parsed_json}")

        return jsonify({"status": "success", "parsed_json": parsed_json}), 200
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as e:
        logging.error(f"Failed to parse JSON: {e}")
        return jsonify({"error": "Malformed data"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

