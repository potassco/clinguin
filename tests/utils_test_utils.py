
import httpx


class UtilsTestUtils:

    @classmethod
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

    @classmethod
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