from reference_json_output import (
    BasicTest00,
    BasicTest01,
    BasicTest02,
    BasicTest03,
    BasicTest04,
    BasicTest05,
)
from utils_test_utils import UtilsTestUtils


class TestBackendUnit_00_05:
    def setup_method(self, test_method):
        self.backend = UtilsTestUtils.instantiate_backend(test_method)

    def teardown_method(self, test_method):
        pass

    def test_basic_05(self):
        should_output = BasicTest05.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_04(self):
        should_output = BasicTest04.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_03_order_04(self):
        should_output = BasicTest03.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

        self.backend.add_assumption("p(1)", "true")
        received_by_backend = self.backend.get()
        should_output = BasicTest03.post_p_1_reference_json()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

        self.backend.clear_assumptions()
        received_by_backend = self.backend.get()
        should_output = BasicTest03.post_p_3_reference_json()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_03_order_03(self):
        should_output = BasicTest03.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

        self.backend.clear_assumptions()
        received_by_backend = self.backend.get()
        should_output = BasicTest03.post_p_2_reference_json()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_03_order_02(self):
        should_output = BasicTest03.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

        self.backend.add_assumption("p(1)", "true")
        received_by_backend = self.backend.get()
        should_output = BasicTest03.post_p_1_reference_json()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_03_order_01(self):
        should_output = BasicTest03.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_02(self):
        should_output = BasicTest02.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_01_order_02(self):
        should_output = BasicTest01.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

        self.backend.add_assumption("p(2)", "true")
        received_by_backend = self.backend.get()
        should_output = BasicTest01.post_p_2_reference_json()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

        should_output = BasicTest01.get_p_2_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_basic_01_order_01(self):
        should_output = BasicTest01.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

        self.backend.add_assumption("p(1)", "true")
        received_by_backend = self.backend.get()
        should_output = BasicTest01.post_p_1_reference_json()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

        should_output = BasicTest01.get_p_1_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)

    def test_get_method(self):
        should_output = BasicTest00.get_reference_json()
        received_by_backend = self.backend.get()
        UtilsTestUtils.assert_result(should_output, received_by_backend)
