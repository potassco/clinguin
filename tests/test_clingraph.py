from utils_test_utils import UtilsTestUtils


class TestClingraph:
    def setup_method(self, test_method):
        domain_files = ["examples/clingraph/coloring/encoding.lp"]
        ui_files = ["examples/clingraph/coloring/ui.lp"]

        clingraph = [
            "--backend",
            "ClingraphBackend",
            "--clingraph-files",
            "examples/clingraph/coloring/viz.lp",
            "--engine",
            "neato",
        ]

        self.p, self.uvicorn_url = UtilsTestUtils.start_server(
            domain_files, ui_files, optional=clingraph
        )

    def teardown_method(self, test_method):
        UtilsTestUtils.shutdown_server(self.p)

    # TODO -> Fix non-determinism of clingraph/graphviz!
    # Not working due to non-deterministic nature of graphviz
    # Maybe further investigation in the future ...
    """
    def test_startup_get(self):

        uri = f"{self.uvicorn_url}"
        received_by_postman = str(Coloring.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_assumptions(self):

        uri = f"{self.uvicorn_url}"
        received_by_postman = str(Coloring.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

        post_calls = [
            ("add_assumption(assign(1,blue),true)", Coloring.post_assumption_1),
            ("add_assumption(assign(2,green),true)", Coloring.post_assumption_2),
            ("add_assumption(assign(5,blue),true)", Coloring.post_assumption_3)
        ]

        for post_call in post_calls:

            data = '{"function":"' + post_call[0] + '"}'
            uri = f"{self.uvicorn_url}/backend"
            received_by_postman = str(post_call[1]())

            UtilsTestUtils.assert_post_request(uri, received_by_postman, data)
    """
