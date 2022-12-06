import json
from typing import Any
from urllib.request import Request, urlopen


class Client:
    """Use this Client class to send information and check for a valid response."""
    FAILED_REQUEST = object()  # Look below to see how this sentinel is used.

    @classmethod
    def send_json(cls, url, python_obj) -> Any:
        """Converts the python_obj parameter into a JSON string and sends that JSON to the server.
        Returns server's response converted back from JSON to a Python object."""
        json_string = json.dumps(python_obj)
        json_bytes = json_string.encode('utf-8')
        request = Request(  # instantiation of an object representing a url/http request
            url=url,
            method='GET',  # get request here is the client getting info from a server
            headers={
                'Content-Length': len(json_bytes),
                'Content-Type': 'application/json',
            },
            data=json_bytes  # this is the message body with whatever data python_obj parameter held
        )
        response = urlopen(request)
        if 200 <= response.status <= 299:
            # Any status in the 200 range is considered a successful response.
            response_data_bytes = response.read()
            response_data_string = response_data_bytes.decode('utf-8')
            reconstituted_python_object = json.loads(response_data_string)
            request_result = reconstituted_python_object
        else:
            request_result = cls.FAILED_REQUEST
        return request_result


if __name__ == '__main__':
    """
    THIS IS HOW YOU TEST YOUR MICROSERVICE
    """

    # TODO: Set your base server url according to how you are running your server.
    base_server_url = "https://flaskserver.jasonavina.repl.co"
    intended_path = "/alltimeseries"
    # querystring = "?ticker=msft"
    full_server_url = base_server_url + intended_path  # + querystring

    # TODO: Create the data you want to send.

    sample_data_to_send = json.dumps('MSFT')  # Any combination of JSON-compatible Python objects: int, float, str, list, dict, True/False/None

    result = Client.send_json(full_server_url, sample_data_to_send)

    if result is Client.FAILED_REQUEST:
        print(f"REQUEST FAILED for {sample_data_to_send=}")
    else:
        print(f"REQUEST SUCCEEDED:")
        if type(result) is dict:
            pretty = json.dumps(result, indent=4)
            print(pretty)
        else:
            print(result)
