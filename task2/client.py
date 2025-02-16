import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_item(self, data):
        url = f"{self.base_url}/item"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        return requests.post(url, json=data, headers=headers)

    def get_item_by_id(self, item_id):
        url = f"{self.base_url}/item/{item_id}"
        headers = {'Accept': 'application/json'}
        return requests.get(url, headers=headers)

    def get_statistics(self, item_id):
        url = f"{self.base_url}/statistic/{item_id}"
        headers = {'Accept': 'application/json'}
        return requests.get(url, headers=headers)

    def get_items_by_seller(self, seller_id):
        url = f"{self.base_url}/{seller_id}/item"
        headers = {'Accept': 'application/json'}
        return requests.get(url, headers=headers)
