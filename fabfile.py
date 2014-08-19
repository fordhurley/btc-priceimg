from fabric.api import local, shell_env


def test():
    """
    Run test suite.
    """
    with shell_env(FLASK_ENV='test'):
        local('nosetests')


def serve():
    """
    Run the development server.
    """
    local('./serve.py')


def deploy():
    """
    Deploy app to Heroku.
    """
    test()
    local('git push heroku master')
