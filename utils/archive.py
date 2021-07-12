from utils.dataset import Dataset
import zipfile
import os
import shutil


class Unpack(Dataset):

    def __init__(self, file):
        super().__init__()
        self.__file = file

    def unzip(self, ext=".zip", delete_after_unzip=False):

        if os.path.isfile(f'{self.tmp}/{self.__file}{ext}'):

            local_zip = f'{self.tmp}/{self.__file}{ext}'

            try:
                zip_ref = zipfile.ZipFile(local_zip, 'r')
                zip_ref.extractall(f'{self.tmp}/{self.__file}')
                print(f'Extract {self.__file}{ext} Successfully')

            except IOError as err:
                print(f'{self.tmp} is not accessible: ', err)

            finally:
                zip_ref.close()

            if delete_after_unzip:
                os.remove(f'{self.tmp}/{self.__file}{ext}')

        else:
            raise IOError(f"{self.__file}{ext} doesn't exists")


class Pack(Dataset):

    def __init__(self, file):
        super().__init__()
        self.__file = file

    def zip(self, ext=".zip", delete_folder_after_zip=False):

        ext = ext.replace(".", "")
        filepath = f'{self.tmp}/{self.__file}'

        if os.path.exists(filepath):

            try:
                shutil.make_archive(f"{self.tmp}/modified_{self.__file}",
                                    ext,
                                    filepath)
                print(f'Create modified_{self.__file}.{ext} Successfully')

            except IOError as err:
                print(f'{self.tmp} is not accessible: ', err)

            if delete_folder_after_zip:
                shutil.rmtree(filepath)

        else:
            raise IOError(f"{self.__file} doesn't exists")
