from reference_json_output import Elevator
from utils_test_utils import UtilsTestUtils


class TestTemporal:
    def setup_method(self, test_method):
        domain_files = ["examples/temporal/elevator/encoding.lp"]
        ui_files = ["examples/temporal/elevator/ui.lp"]

        temporal = ["--backend", "TemporalBackend"]

        self.p, self.uvicorn_url = UtilsTestUtils.start_server(
            domain_files, ui_files, optional=temporal
        )

    def teardown_method(self, test_method):
        UtilsTestUtils.shutdown_server(self.p)

    def test_startup_get(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = str(Elevator.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_find_plan(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = str(Elevator.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

        post_calls = [
            ("find_plan", Elevator.post_find_plan),
        ]

        for post_call in post_calls:
            data = '{"function":"' + post_call[0] + '"}'
            uri = f"{self.uvicorn_url}/backend"
            received_by_postman = str(post_call[1]())

            UtilsTestUtils.assert_post_request(uri, received_by_postman, data)
