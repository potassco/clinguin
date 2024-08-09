import json

from reference_json_output import (
    BasicTest06,
    BasicTest07,
    BasicTest08,
    BasicTest09,
    BasicTest10,
    BasicTest11,
    BasicTest12,
)
from utils_test_utils import UtilsTestUtils


class TestBasic06_11:
    def setup_method(self, test_method):
        self.p, self.uvicorn_url = UtilsTestUtils.basic_tests_start_server(test_method)

    def teardown_method(self, test_method):
        UtilsTestUtils.shutdown_server(self.p)

    def test_basic_12(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest12.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_basic_11(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest11.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_basic_10(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest10.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_basic_09_order_02(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest09.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

        data = '{"function":"add_assumption(p(2),true)"}'
        uri = f"{self.uvicorn_url}/backend"
        received_by_postman = json.dumps(BasicTest09.post_p_1_reference_json())

        UtilsTestUtils.assert_post_request(uri, received_by_postman, data)

        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest09.get_p_2_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

        data = '{"function":"clear_assumptions"}'
        uri = f"{self.uvicorn_url}/backend"
        received_by_postman = json.dumps(BasicTest09.post_p_3_reference_json())

        UtilsTestUtils.assert_post_request(uri, received_by_postman, data)

        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest09.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_basic_09_order_01(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest09.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_basic_08(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest08.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_basic_07(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest07.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_basic_06(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest06.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)
