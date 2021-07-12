'''

Purposed of this code is for downloading Dataset
through API and requests in Kaggle, Google Drive and HTTP

'''

import time
import requests

from kaggle.api.kaggle_api_extended import KaggleApi
from utils.dataset import Dataset


class KaggleDownloader(Dataset):

    def __init__(self):

        super().__init__()
        api = KaggleApi()
        self.__api = api

    def download_files(self, dataset, method, quiet=False):

        try:

            self.__api.authenticate()
            print('auth success')

            print(f'Downloading {dataset}.zip')

            if method == 'datasets':

                self.__api.dataset_download_files(
                    dataset=dataset,
                    path=self.tmp,
                    quiet=quiet)

                print(f'Download {dataset}.zip Successfully')

            elif method == 'competitions':

                self.__api.competition_download_files(
                    competition=dataset,
                    path=self.tmp,
                    quiet=quiet)

                print(f'Downloading {dataset}.zip Successfully')

            else:
                raise ValueError(f'{method} is not dataset nor competition')

        except ValueError as err:
            raise ValueError('Kaggle.json invalid: ', err)

        except OSError as err:
            raise OSError('Kaggle.json not found: ', err)

    def download_file(self, dataset, method, filename, quiet=False):

        try:

            self.__api.authenticate()
            print('auth success')

            print(f'Downloading {dataset}/{filename}')

            if method == 'datasets':

                self.__api.dataset_download_file(
                    dataset=dataset,
                    file_name=filename,
                    path=self.tmp,
                    quiet=quiet)

                print(f'Download {dataset}/{filename} Successfully')

            elif method == 'competitions':

                self.__api.competition_download_file(
                    competition=dataset,
                    file_name=filename,
                    path=self.tmp,
                    quiet=quiet)

                print(f'Downloading {dataset}/{filename} Successfully')

            else:
                raise ValueError(f'{method} is not dataset nor competition')

        except ValueError as err:
            raise ValueError('Kaggle.json invalid: ', err)

        except OSError as err:
            raise OSError('Kaggle.json not found: ', err)


class GoogleDriveDownloader(Dataset):

    def __init__(self, url):

        super().__init__()
        self.__url_raw = 'https://docs.google.com/uc?export=download'
        self.__chunk_size = 32768

        if 'view' not in url:
            self.__file_id = url.split('/')[-1]

        else:
            self.__file_id = url.split('/')[-2]

    def __get_confirm_token(self, response):

        for key, value in response.cookies.items():

            if key.startswith('download_warning'):
                return value

        return None

    def download_file(self, ext='.zip', namefile=time.strftime("%Y%m%d-%H%M%S")): # noqa

        print(f'Downloading {namefile}{ext} with id {self.__file_id}')

        try:

            session = requests.Session()
            response = session.get(self.__url_raw,
                                   params={'id': self.__file_id},
                                   stream=True,
                                   timeout=100)

            token = self.__get_confirm_token(response)

            if token:
                response = session.get(self.__url_raw,
                                       params={'id': self.__file_id,
                                               'confirm': token},
                                       stream=True,
                                       timeout=100)

            with open(f'{self.tmp}/{namefile}{ext}', 'wb') as file:
                for chunk in response.iter_content(self.__chunk_size):
                    if chunk:
                        try:
                            file.write(chunk)
                        except requests.exceptions.HTTPError as errh:
                            print("Http Error:", errh)
                        except requests.exceptions.ConnectionError as errc:
                            print("Error Connecting:", errc)
                        except requests.exceptions.Timeout as errt:
                            print("Timeout Error:", errt)
                        except requests.exceptions.RequestException as err:
                            print("OOps: Something Else", err)
                        except OSError as errd:
                            print("File cannot accessible", errd)

            print(f'Download {namefile}{ext} with id {self.__file_id} Successfully') # noqa

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)

        return namefile


class webDownloader(Dataset):

    def __init__(self, url):

        super().__init__()
        self.__url = url
        self.__file_name = url.split("/")[-1]
        self.__chunk_size = 1024

    def download_file(self):

        print(f'Downloading {self.__file_name}')

        try:
            with requests.Session() as session:
                response = session.get(self.__url, stream=True, timeout=100)

            with open(f'{self.tmp}/{self.__file_name}', 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.__chunk_size): # noqa
                    if chunk:
                        try:
                            f.write(chunk)
                        except requests.exceptions.HTTPError as errh:
                            print("Http Error:", errh)
                        except requests.exceptions.ConnectionError as errc:
                            print("Error Connecting:", errc)
                        except requests.exceptions.Timeout as errt:
                            print("Timeout Error:", errt)
                        except requests.exceptions.RequestException as err:
                            print("OOps: Something Else", err)
                        except OSError as err:
                            print("File cannot accessible", err)

            print(f'Download {self.__file_name} successfully')

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)

        return self.__file_name
