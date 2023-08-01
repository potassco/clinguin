import time
import subprocess
import datetime
import httpx

import re
import json

from reference_json_output import *

class Test:

    def setup_method(self, test_method):

        test_method_name = test_method.__name__

        p = re.compile(r"\d\d")
        result = p.search(test_method_name)

        if result is not None:
            test_number = result.group(0)
        else: 
            test_number = "00"

        self.port = 8000
        self.url = "127.0.0.1"

        self.uvicorn_url = f"http://{self.url}:{self.port}"

        arguments = ["clinguin","server",f"--domain-files=examples/basic/test_{test_number}/domain_file.lp", f"--ui-files=examples/basic/test_{test_number}/ui.lp"]
        self.p = subprocess.Popen(arguments)       

        time.sleep(3)  # time for the server to start

        print("SETUP COMPLETE")

    def teardown_method(self, test_method):
        self.p.kill()
        print(datetime.datetime.now())
        print("TEARDOWN COMPLETE")

    def test_health(self):

        uri = f"{self.uvicorn_url}/health"
        received_by_postman = str(Health.get_reference_json())

        self.assert_get_request(uri, received_by_postman)


    def test_basic_00(self):

        uri = f"{self.uvicorn_url}"
        received_by_postman = str(BasicTest00.get_reference_json())

        self.assert_get_request(uri, received_by_postman)

    def test_basic_01_order_01(self):

        uri = f"{self.uvicorn_url}"
        received_by_postman = str(BasicTest01.get_reference_json())

        self.assert_get_request(uri, received_by_postman)

        data = '{"function":"add_assumption(p(1))"}'
        uri = f"{self.uvicorn_url}/backend"
        received_by_postman = str(BasicTest01.post_p_1_reference_json())

        self.assert_post_request(uri, received_by_postman, data)

        uri = f"{self.uvicorn_url}"
        received_by_postman = str(BasicTest01.get_p_1_reference_json())

        self.assert_get_request(uri, received_by_postman)

    def test_basic_01_order_02(self):

        uri = f"{self.uvicorn_url}"
        received_by_postman = str(BasicTest01.get_reference_json())

        self.assert_get_request(uri, received_by_postman)

        data = '{"function":"add_assumption(p(2))"}'
        uri = f"{self.uvicorn_url}/backend"
        received_by_postman = str(BasicTest01.post_p_2_reference_json())

        self.assert_post_request(uri, received_by_postman, data)

        uri = f"{self.uvicorn_url}"
        received_by_postman = str(BasicTest01.get_p_2_reference_json())

        self.assert_get_request(uri, received_by_postman)

    def assert_get_request(self, uri, should_output, should_status_code = 200):

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

    def assert_post_request(self, uri, should_output, data, should_status_code = 200):
        try:


            r = httpx.post(uri, content = data, timeout=1000)

            assert r.status_code == should_status_code

            received_by_request = str(r.json())

            assert received_by_request == should_output

        except httpx.ConnectError:
            assert False
        except Exception as ex:
            print(ex)
            assert False


