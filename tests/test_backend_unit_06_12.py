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


class TestBackendUnit_06_11:
    def setup_method(self, test_method):
        self.backend = UtilsTestUtils.instantiate_backend(test_method)

    def teardown_method(self, test_method):
        pass

    def test_basic_12(self):
        should_output = BasicTest12.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_11(self):
        should_output = BasicTest11.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_10(self):
        should_output = BasicTest10.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_09_order_02(self):
        should_output = BasicTest09.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

        self.backend.add_assumption("p(2)", "true")
        received_by_backend = self.backend.get()
        should_output = BasicTest09.post_p_1_reference_json()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

        should_output = BasicTest09.get_p_2_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

        should_output = BasicTest09.post_p_3_reference_json()
        self.backend.clear_assumptions()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

        should_output = BasicTest09.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_09_order_01(self):
        should_output = BasicTest09.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_08(self):
        should_output = BasicTest08.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_07(self):
        should_output = BasicTest07.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_06(self):
        should_output = BasicTest06.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)
