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

import os
import json
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

import os
import json
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Define log file paths
LOG_FILE = "parsed_json.log"
BINARY_FILE = "binary_data.json"

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

        # Append parsed JSON to the log file
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(json.dumps(parsed_json) + '\n')

        # Extract the binary part
        binary_part = raw_data[json_end_index:]

        # Extract the eiv from the JSON
        eiv = parsed_json.get('eiv', 'unknown_eiv')

        # Prepare the output JSON structure for binary data
        binary_output = {
            "eiv": eiv,
            "binary_data": binary_part.hex()  # Hex encoding for JSON compatibility
        }

        # Append the binary data to the binary file
        if not os.path.exists(BINARY_FILE):
            # Create a new file with an empty list if it doesn't exist
            with open(BINARY_FILE, 'w') as binary_file:
                json.dump([], binary_file)

        # Load existing data, append the new record, and save
        with open(BINARY_FILE, 'r+') as binary_file:
            data = json.load(binary_file)
            data.append(binary_output)
            binary_file.seek(0)
            json.dump(data, binary_file, indent=4)

        app.logger.info(f"Received and processed data from {request.remote_addr}")

        return jsonify({"status": "success", "message": "Data received and processed"}), 200

    except (json.JSONDecodeError, ValueError) as e:
        app.logger.error(f"Failed to parse JSON: {e}")
        return jsonify({"status": "error", "message": "Failed to parse JSON"}), 400

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



