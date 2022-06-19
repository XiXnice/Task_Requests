from pprint import pp, pprint
import requests
import os

class YaUploader:
    host = 'https://cloud-api.yandex.net'

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Context-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _get_upload_link(self, file_path: str):
        url = f'{self.host}/v1/disk/resources/upload/'
        headers = self.get_headers()
        params = {'path': file_path, 'overwrite': True}
        response = requests.get(url, params = params, headers = headers)
        pprint(response.json())
        return response.json().get('href')

    def upload(self, file_path: str):
        headers = self.get_headers()
        file_name = os.path.basename(file_path)
        upload_link = self._get_upload_link('/' + file_name)
        response = requests.put(upload_link, data=open(file_name, 'rb'), headers = headers)
        response.raise_for_status()
        if response.status_code == 201:
            print('Success')

if __name__ == '__main__':
    path_to_file = input(str('Введите путь: '))
    token = input(str('Введите токен: '))
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)
    print(path_to_file)
