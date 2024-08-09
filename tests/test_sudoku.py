from utils_test_utils import UtilsTestUtils


class TestSudoku:
    def setup_method(self, test_method):
        domain_files = [
            "examples/clingo/sudoku/instance.lp",
            "examples/clingo/sudoku/encoding.lp",
        ]
        ui_files = ["examples/clingo/sudoku/ui.lp"]

        self.p, self.uvicorn_url = UtilsTestUtils.start_server(domain_files, ui_files)

    def teardown_method(self, test_method):
        UtilsTestUtils.shutdown_server(self.p)

    # TODO -> Update tests according to ''DO' syntax (or use sudoku_2)
    """
    def test_startup_get(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = str(Sudoku.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)


    def test_startup_next(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = str(Sudoku.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

        data = '{"function":"next_solution"}'
        uri = f"{self.uvicorn_url}/backend"
        received_by_postman = str(Sudoku.post_p_1())

        UtilsTestUtils.assert_post_request(uri, received_by_postman, data)

        data = '{"function":"next_solution"}'
        uri = f"{self.uvicorn_url}/backend"
        received_by_postman = str(Sudoku.post_p_2())

        UtilsTestUtils.assert_post_request(uri, received_by_postman, data)

        data = '{"function":"clear_assumptions"}'
        uri = f"{self.uvicorn_url}/backend"
        received_by_postman = str(Sudoku.post_p_3())

        UtilsTestUtils.assert_post_request(uri, received_by_postman, data)

        uri = f"{self.uvicorn_url}"
        received_by_postman = str(Sudoku.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

    def test_assumptions(self):
        uri = f"{self.uvicorn_url}"
        received_by_postman = str(Sudoku.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)

        post_calls = [
            ("add_assumption(sudoku(2,2,5),true)", Sudoku.post_assumption_1),
            ("add_assumption(sudoku(5,8,9),true)", Sudoku.post_assumption_2),
            ("add_assumption(sudoku(8,8,8),true)", Sudoku.post_assumption_3),
            ("add_assumption(sudoku(2,8,7),true)", Sudoku.post_assumption_4),
            ("add_assumption(sudoku(6,8,4),true)", Sudoku.post_assumption_5),
            ("add_assumption(sudoku(3,8,3),true)", Sudoku.post_assumption_6),
            ("next_solution", Sudoku.post_assumption_7),
            ("next_solution", Sudoku.post_assumption_8),
            ("clear_assumptions", Sudoku.post_assumption_9),
        ]

        for post_call in post_calls:
            data = '{"function":"' + post_call[0] + '"}'
            uri = f"{self.uvicorn_url}/backend"
            received_by_postman = str(post_call[1]())

            UtilsTestUtils.assert_post_request(uri, received_by_postman, data)

        uri = f"{self.uvicorn_url}"
        received_by_postman = str(Sudoku.get_reference_json())

        UtilsTestUtils.assert_get_request(uri, received_by_postman)
    """
