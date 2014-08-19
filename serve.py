#!/usr/bin/env python
import os
import re


def get_env(path):
    """
    Return environment variables from a file as a dict. File should be
    formatted like:

    FLASK_ENV=test
    FONT_URL=http://example.com
    """
    env = {}

    if not os.path.exists(path):
        return env

    with open(path) as f:
        for line in f:
            if re.search(r'^\s#', line):
                continue
            key, value = line.split('=', 1)
            env[key] = value

    return env


if __name__ == '__main__':
    # Set environment variables before importing
    os.environ.update(get_env('.env'))

    from priceimg import app
    app.run(debug=True, port=5002)
