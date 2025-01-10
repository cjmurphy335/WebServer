from flask import Flask, request, jsonify
import json
import logging

app = Flask(__name__)
logging.basicConfig(filename='mixed_data.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

import os
import json
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def post_data():
    try:
        # Get the raw POST data
        raw_data = request.get_data()

        # Find the end of the JSON segment
        json_end_index = raw_data.find(b'}') + 1
        if json_end_index == 0:
            raise ValueError("No valid JSON segment found")

        # Extract and decode the JSON part
        json_part = raw_data[:json_end_index]
        parsed_json = json.loads(json_part.decode('utf-8'))

        # Extract the binary part
        binary_part = raw_data[json_end_index:]

        # Extract the eiv from the JSON
        eiv = parsed_json.get('eiv', 'unknown_eiv')

        # Prepare the output JSON structure for binary data
        binary_output = {
            "eiv": eiv,
            "binary_data": binary_part.hex()  # Hex encoding for JSON compatibility
        }

        # Create a timestamped filename for the binary data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        binary_filename = f"binary_data_{timestamp}.json"

        # Save the binary data to a file
        with open(binary_filename, 'w') as f:
            json.dump(binary_output, f, indent=4)

        # Log the successful parsing and file creation
        app.logger.info(f"Parsed JSON: {parsed_json}")
        app.logger.info(f"Binary data saved to {binary_filename}")

        return jsonify({"status": "success", "message": "Data received and processed"}), 200

    except (json.JSONDecodeError, ValueError) as e:
        app.logger.error(f"Failed to parse JSON: {e}")
        return jsonify({"status": "error", "message": "Failed to parse JSON"}), 400

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

