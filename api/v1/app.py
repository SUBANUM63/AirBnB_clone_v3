#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    teardown function
    """
    storage.close()


if __name__ == "__main__":
    """ Main Function """
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)