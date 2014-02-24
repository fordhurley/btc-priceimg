"""
Copyright (C) 2013 Ford Hurley

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
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
