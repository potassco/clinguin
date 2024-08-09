import json

from reference_json_output import (
    BasicTest00,
    BasicTest01,
    BasicTest02,
    BasicTest03,
    BasicTest04,
    BasicTest05,
    Health,
)
from utils_test_utils import UtilsTestUtils


class TestBasic00_05:
    def setup_method(self, test_method):
        self.p, self.uvicorn_url = UtilsTestUtils.basic_tests_start_server(test_method)

    def teardown_method(self, test_method):
        UtilsTestUtils.shutdown_server(self.p)

    def test_health(self):
        uri = f"{self.uvicorn_url}/health"
        received_by_postman = json.dumps(Health.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_basic_05(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest05.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_basic_04(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest04.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_basic_03_order_04(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest03.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

        data = '{"function":"add_assumption(p(1),true)"}'
        uri = f"{self.uvicorn_url}/backend"
        received_by_postman = json.dumps(BasicTest03.post_p_1_reference_json())

        UtilsTestUtils.assert_post_request(uri, received_by_postman, data)

        data = '{"function":"clear_assumptions"}'
        uri = f"{self.uvicorn_url}/backend"
        received_by_postman = json.dumps(BasicTest03.post_p_3_reference_json())

        UtilsTestUtils.assert_post_request(uri, received_by_postman, data)

    def test_basic_03_order_03(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest03.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

        data = '{"function":"clear_assumptions"}'
        uri = f"{self.uvicorn_url}/backend"
        received_by_postman = json.dumps(BasicTest03.post_p_2_reference_json())

        UtilsTestUtils.assert_post_request(uri, received_by_postman, data)

    def test_basic_03_order_02(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest03.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

        data = '{"function":"add_assumption(p(1),true)"}'
        uri = f"{self.uvicorn_url}/backend"
        received_by_postman = json.dumps(BasicTest03.post_p_1_reference_json())

        UtilsTestUtils.assert_post_request(uri, received_by_postman, data)

    def test_basic_03_order_01(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest03.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_basic_02(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest02.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_basic_01_order_02(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest01.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

        data = '{"function":"add_assumption(p(2),true)"}'
        uri = f"{self.uvicorn_url}/backend"
        received_by_postman = json.dumps(BasicTest01.post_p_2_reference_json())

        UtilsTestUtils.assert_post_request(uri, received_by_postman, data)

        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest01.get_p_2_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_basic_01_order_01(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest01.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

        data = '{"function":"add_assumption(p(1),true)"}'
        uri = f"{self.uvicorn_url}/backend"
        received_by_postman = json.dumps(BasicTest01.post_p_1_reference_json())

        UtilsTestUtils.assert_post_request(uri, received_by_postman, data)

        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest01.get_p_1_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_basic_00(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = json.dumps(BasicTest00.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)
