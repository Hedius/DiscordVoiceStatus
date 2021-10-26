__author__ = 'Hedius'
__license__ = 'GPLv3'

from flask import Flask, request
from StatusBot.SharedStorage import SharedStorage

app = Flask(__name__)
# shared storage with discord bot
storage = SharedStorage()


@app.route('/api/servers/<server_id>/widget.json')
@app.route('/<server_id>')
@app.route('/')
def get_widget_data(server_id=None):
    """
    Return the cached data or an error if the given server_id is invalid.
    Calls:
    /api/servers/<server_id>/widget.json
    /<server_id>
    /?id=<server_id>
    :param server_id: optional server_id (requires HTTP URL param if not set)
    :return:
    """
    if server_id is None:
        server_id = request.args.get('id')
    if server_id is None:
        return 'Server ID not given!', 400
    try:
        server_id = int(server_id)
    except ValueError:
        return 'Invalid server ID given!', 400

    with storage.lock:
        if server_id not in storage.data:
            return (
                'Server not cached by this bot! Add the bot to the server!',
                400
            )
        # return cached entry
        return storage.data[server_id]
