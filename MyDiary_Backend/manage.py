"""
flask database
created by Michael Alex Basweti
"""
from _pytest.junitxml import unicode
from flask import Flask, jsonify, abort, request, make_response, url_for,  Response, json

app = Flask(__name__)

entries = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Buy from Gikomba',
        
    }
]


def make_public_entry(entry):
    new_entry = {}
    for field in entry:
        if field == 'id':
            new_entry['uri'] = url_for('get_entry', entry_id = entry['id'], _external = True)
        else:
            new_entry[field] = entry[field]
    return new_entry


@app.route('/mydiary/api/v1.0/entries/get', methods=['GET'])
def get_entries():
    """
    function  to return all entries
    :return:
    """
    return jsonify({'entries': [make_public_entry(entry) for entry in entries]})


@app.route("/mydiary/api/v1.0/entries/get/<int:entry_id>")
def get_entry(entry_id):
    """

    :param entry_id:
    :return:
    """
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    return jsonify({'entry': make_public_entry(entry[0])})


@app.route("/mydiary/api/v1.0/entries/post", methods=['POST'])
def create_entry():
    """
    post one entry at a time,description can empty but title cannot be
    post to entries
    :return:
    """
    if not request.json or 'title' not in request.json:
        abort(400)
    entry = {
        'id': entries[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        
    }

    entries.append(entry)
    return jsonify({'entry': make_public_entry(entry) }), 201


@app.route('/mydiary/api/v1.0/entries/edit/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """
    delete
    :param entry_id:
    :return:
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


@app.route('/mydiary/api/v1.0/entries/delete/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """
    delete
    :param entry_id:
    :return:
    """
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    entries.remove(entry[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run()
