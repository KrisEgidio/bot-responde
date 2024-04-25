import requests


class APIRequests:
    def __init__(self):
        self.base_url = 'http://localhost:8000'

    def send_question(self, question):
        url = f'{self.base_url}/questions/respond'
        headers = {'Content-Type': 'application/json'}
        data = {'question': question}

        response = requests.post(url, json=data, headers=headers)
        return response.json()