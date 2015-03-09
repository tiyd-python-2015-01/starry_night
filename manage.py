#!/usr/bin/env python
import os

from flask.ext.script import Manager, Shell, Server
from flask.ext.script.commands import ShowUrls, Clean

from starry_night import create_app


app = create_app()
manager = Manager(app)
manager.add_command('server', Server())
manager.add_command('show-urls', ShowUrls())
manager.add_command('clean', Clean())


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app)


if __name__ == '__main__':
    manager.run()
