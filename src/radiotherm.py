@app.route('/api/data', methods=['POST'])
def post_data():
    raw_data = request.get_data()

    with open('raw_payload.bin', 'wb') as f:
        f.write(raw_data)

    logging.info(f"Received {len(raw_data)} bytes")

    return jsonify({"status": "received"}), 200
