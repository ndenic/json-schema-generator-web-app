import json
from flask import Flask, render_template, request, jsonify
from genson import SchemaBuilder

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_schema', methods=['POST'])
def generate_schema():
    json_data = request.json.get('json_data')

    if not json_data:
        return jsonify({'error': 'Please enter JSON data.'}), 400

    try:
        datastore = json.loads(json_data)
    except json.JSONDecodeError as e:
        return jsonify({'error': f'Invalid JSON format: {e.msg} at position {e.pos}.'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid JSON format.'}), 400

    try:
        builder = SchemaBuilder()
        builder.add_object(datastore)
        schema = builder.to_schema()
    except Exception as e:
        return jsonify({'error': f'Error generating schema: {str(e)}'}), 500

    formatted_schema = json.dumps(schema, indent=4)
    return jsonify({'schema': formatted_schema})


if __name__ == "__main__":
    app.run(debug=True)
