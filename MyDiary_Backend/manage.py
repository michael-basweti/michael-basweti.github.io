"""
flask api
created by Michael Alex Basweti
"""
from _pytest.junitxml import unicode
from flask import Flask, jsonify, abort, request, url_for, redirect
from flasgger import Swagger
from flasgger import swag_from

app = Flask(__name__) #pylint: disable=invalid-name
swagger = Swagger(app) #pylint: disable=invalid-name

entries = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Buy from Gikomba',

    }
]


def make_public_entry(entry):
    """
    return url
    """
    new_entry = {}
    for field in entry:
        if field == 'id':
            new_entry['uri'] = url_for('get_entry', entry_id=entry['id'], _external=True)
        else:
            new_entry[field] = entry[field]
    return new_entry


@app.route('/mydiary/api/v1/entries/get', methods=['GET'])
@swag_from('colors.yml')
def get_entries():
    """
    get all the entries
    :return:
    """
    return jsonify({'entries': [make_public_entry(entry) for entry in entries]})


@app.route("/mydiary/api/v1/entries/get/<int:entry_id>")
def get_entry(entry_id):
    """
    get each entry by id
    ---
    tags:
      - get
    parameters:
      - name: entry_id
        in: path
        description: entry id
        required: true
        schema:
          properties:
            entry_id:
              type: integer
              format: int64
    responses:
      200:
        description: OK.
    """
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    return jsonify({'entry': make_public_entry(entry[0])})


@app.route("/mydiary/api/v1/entries/post", methods=['POST'])
def create_entry():
    """
    Echo back the name and any posted parameters.
    ---
    tags:
      - echo
    parameters:
      - in: body
        name: body
        description: JSON parameters.
        schema:
          properties:
            title:
              type: string
              description: sasa.
              example: Alice
            description:
              type: string
              description: hello.
              example: Smith
    responses:
      200:
        description: OK.
    """
    if not request.json or 'title' not in request.json:
        abort(400)
    entry = {
        'id': entries[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
    }

    entries.append(entry)
    return jsonify({'entry': make_public_entry(entry)}), 201


@app.route('/mydiary/api/v1/entries/edit/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """
    edit post by id.
    ---
    tags:
      - put
    parameters:
      - name: entry_id
        in: path
        description: entry id
        required: true
      - in: body
        name: body
        schema:
          properties:
            entry_id:
              type: integer
              format: int64
            title:
              type: string
              description: sasa.
              example: swam
            description:
              type: string
              description: hello.
              example: in the river
    responses:
      200:
        description: OK.
      example:
        {entry: {
        "description": "egg, Cheese, Pizza, Fruit, Hgahchjkadhjk",
        "title": "Buy lunch",
        "uri": "http://127.0.0.1:5000/mydiary/api/v1/entries/get/1"}
        }
    """
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json \
            and type(request.json['description']) is not unicode:
        abort(400)
    entry[0]['title'] = request.json.get('title', entry[0]['title'])
    entry[0]['description'] = request.json.get('description',
                                               entry[0]['description'])
    return jsonify({'entry': make_public_entry(entry[0])})


@app.route('/mydiary/api/v1/entries/delete/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """
    delete entry by id
    ---
    tags:
      - delete
    parameters:
      - name: entry_id
        in: path
        description: entry id
        required: true
        schema:
          properties:
            entry_id:
              type: integer
              format: int64
    responses:
      200:
        description: OK.
    """
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    entries.remove(entry[0])
    return jsonify({'result': True})


@app.route("/")
def index():
    """
    redirect the api to a swagger ui page
    :return:
    """
    return redirect("/apidocs")


if __name__ == '__main__':
    app.run(debug=True)
