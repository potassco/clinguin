import copy
import json
import re
import subprocess
import time
from datetime import datetime

import httpx

from clinguin import args_to_dict_converter
from clinguin.parse_input import ArgumentParser
from clinguin.server.application.backends.clingo_multishot_backend import (
    ClingoMultishotBackend,
)


class UtilsTestUtils:
    @classmethod
    def assert_get_request(self, uri, should_output, should_status_code=200):
        try:
            r = httpx.get(uri, timeout=1000)
            assert r.status_code == should_status_code

            received_by_request = str(r.json())

            assert received_by_request == should_output

        except httpx.ConnectError:
            assert False
        except Exception as ex:
            print(ex)
            assert False

    @classmethod
    def assert_post_request(self, uri, should_output, data, should_status_code=200):
        try:
            r = httpx.post(uri, content=data, timeout=1000)

            assert r.status_code == should_status_code

            received_by_request = str(r.json())

            assert received_by_request == should_output

        except httpx.ConnectError:
            assert False
        except Exception as ex:
            print(ex)
            assert False

    @classmethod
    def basic_tests_start_server(cls, test_method):
        test_method_name = test_method.__name__

        p = re.compile(r"\d\d")
        result = p.search(test_method_name)

        if result is not None:
            test_number = result.group(0)
        else:
            test_number = "00"

        domain_files = [f"examples/test/test_{test_number}/domain_file.lp"]

        ui_files = [f"examples/test/test_{test_number}/ui.lp"]

        return cls.start_server(domain_files, ui_files)

    @classmethod
    def start_server(cls, domain_files, ui_files, optional=None):
        port = 8000
        url = "127.0.0.1"

        uvicorn_url = f"http://{url}:{port}"

        arguments = (
            ["clinguin", "server", "--domain-files"]
            + domain_files
            + ["--ui-files"]
            + ui_files
        )

        if optional is not None:
            arguments += optional

        p = subprocess.Popen(arguments)

        time.sleep(3)  # time for the server to start

        print("SERVER SETUP COMPLETE")

        return (p, uvicorn_url)

    @classmethod
    def shutdown_server(cls, server_process):
        server_process.kill()

        print("SERVER SHUTDOWN COMPLETE")

    @classmethod
    def instantiate_backend(self, test_method):
        test_method_name = test_method.__name__

        p = re.compile(r"\d\d")
        result = p.search(test_method_name)

        if result is not None:
            test_number = result.group(0)
        else:
            test_number = "00"

        domain_files = [f"examples/test/test_{test_number}/domain_file.lp"]

        ui_files = [f"examples/test/test_{test_number}/ui.lp"]

        parser = ArgumentParser()

        arguments = (
            ["server", "--domain-files"] + domain_files + ["--ui-files"] + ui_files
        )

        args = parser.parse("server", arguments)

        args_dict = vars(args)

        timestamp = datetime.now().strftime("%Y-%m-%d::%H:%M:%S")

        log_dict = args_to_dict_converter(args_dict, timestamp)

        args_copy = copy.deepcopy(args)
        args_copy.log_args = log_dict

        self.args = args_copy

        return ClingoMultishotBackend(args_copy)

    @classmethod
    def assert_result(self, should_output, received_by_request):
        received_by_request = json.loads(
            json.dumps(received_by_request, default=lambda o: o.__dict__)
        )
        print(received_by_request)
        print(should_output)
        assert str(received_by_request) == str(should_output)
