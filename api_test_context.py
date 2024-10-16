import uuid


class APITestContext:
    def __init__(self):
        self.session_id = str(uuid.uuid4())  # Generate a unique ID for each test run
        self.current_request = None
        self.current_response = None

    def set_current_request(self, method, url, headers, body):
        self.current_request = {
            'method': method,
            'url': url,
            'headers': headers,
            'body': body
        }

    def set_current_response(self, status_code, headers, body):
        self.current_response = {
            'status_code': status_code,
            'headers': headers,
            'body': body
        }