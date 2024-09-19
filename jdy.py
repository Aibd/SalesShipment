import time
import requests
import json


class JDYApi:
    def __init__(self, api_key, app_id):
        self.api_key = api_key
        self.app_id = app_id
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json;charset=utf-8'
        }
        self.base_url = "https://api.jiandaoyun.com/api/v5/app/entry/data/"

    def _send_request(self, url, data):
        """ Helper function to send API requests and handle exceptions. """
        try:
            response = requests.post(url, data=json.dumps(data), headers=self.headers)
            return response.json()
        except requests.RequestException as e:
             raise f'Error during API request: {str(e)}'

    # 查询的数据条数，1~100，limit参数控制,30 次/秒
    def query_dataid(self, query_data):
        url = f"{self.base_url}list"
        try:
            result = self._send_request(url, query_data)
        except requests.RequestException as e:
            raise f'Error during query_dataid API request: {str(e)}'
        ids = [i['_id'] for i in result['data']]
        return ids


    # 删除多条数据接口一次最多支持删除 100 条数据, 10 次/秒
    def batch_delete(self,entry_id, ids):
        url = f"{self.base_url}batch_delete"
        query_data = {
            "app_id": self.app_id,
            "entry_id": entry_id,
            "data_ids": ids
        }
        try:
            result = self._send_request(url, query_data)
        except requests.RequestException as e:
            raise f'Error during API request: {str(e)}'
        return result


    def upload(self, data):
        url = f"{self.base_url}batch_create"
        return self._send_request(url, data)

    def get_usernumber(self):
        url = "https://api.jiandaoyun.com/api/v5/corp/department/user/list"
        data = {"dept_no": 1, "has_child": True}
        response_data = self._send_request(url, data)
        users = {i['name']: i['username'] for i in response_data['users']}
        return users



    def get_department_number(self, department_name):
        url = "https://api.jiandaoyun.com/api/v6/corp/department/list"
        data = {"dept_no": 1, "has_child": True}
        response_data = self._send_request(url, data)

        departments = response_data.get('departments', [])
        dept_no = next((dept['dept_no'] for dept in departments if dept['name'] == department_name), None)
        if not dept_no:
            return None
        return dept_no

