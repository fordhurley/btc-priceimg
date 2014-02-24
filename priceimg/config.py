import os

from priceimg import app
import util

try:
    ENV = os.environ['FLASK_ENV']
except KeyError:
    ENV = 'dev'

CONFIG_FILE = os.path.abspath(os.path.join('config', '%s.cfg' % ENV))

app.config.from_pyfile(CONFIG_FILE)

ENV_VARS = [
    'FONT_URL'
]
for var in ENV_VARS:
    app.config[var] = os.environ.get(var)

app.config['FONT_PATH'] = util.download_asset(app.config['FONT_URL'])
