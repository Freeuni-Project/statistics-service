# run.py

from application import create_app, db
from flask_migrate import Migrate  # for migrations
from flask_cors import CORS, cross_origin

app = create_app()
app.app_context().push()
cors = CORS(app)
migrate = Migrate(app, db)
app.config['CORS_HEADERS'] = 'Content-Type'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
