import time
import subprocess
import re
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

    @classmethod
    def basic_tests_start_server(cls, test_method):

        test_method_name = test_method.__name__

        p = re.compile(r"\d\d")
        result = p.search(test_method_name)

        if result is not None:
            test_number = result.group(0)
        else: 
            test_number = "00"

        domain_files = [f"examples/basic/test_{test_number}/domain_file.lp"]

        ui_files = [f"examples/basic/test_{test_number}/ui.lp"]

        return cls.start_server(domain_files, ui_files)

    @classmethod
    def start_server(cls, domain_files, ui_files, optional = None):

        port = 8000
        url = "127.0.0.1"

        uvicorn_url = f"http://{url}:{port}"

        arguments = ["clinguin","server",f"--domain-files"]\
                    + domain_files\
                    + [f"--ui-files"]\
                    + ui_files
        
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


