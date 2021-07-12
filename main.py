# flake8: noqa

from utils.download import KaggleDownloader
from utils.download import GoogleDriveDownloader
from utils.download import webDownloader
from utils.archive import Unpack
from utils.archive import Pack


if __name__ == '__main__':

    #type = 'Google Drive'
    #type = 'web'
    type = 'Kaggle'

    if type in ['html', 'htmls', 'HTML', 'HTMLS', 'web', 'Web', 'WEB']:
        url = "your url here"
        d = webDownloader(url)
        filename = d.download_file()

    elif type in ['Google Drive', 'GoogleDrive', 'googledrive', 'google drive']: 
        url = "your url here"
        g = GoogleDriveDownloader(url)
        filename = g.download_file()
        unpack = True
        if unpack:
            Unpack(file=filename).unzip(delete_after_unzip=True)
    
    elif type in ['kaggle', 'Kaggle']:
        data = 'kaggle competitions download -c titanic'
        data = ' '.join([data]).split()
        if data[1] == 'datasets':
            filename = (" ".join([data[4].replace("/", " ")]).split())[1]
        else:
            filename = data[4]        
        KaggleDownloader().download_files(dataset=data[4], method=data[1], quiet=True)      
        unpack = True
        pack = True
        if unpack:
            Unpack(file=filename).unzip(delete_after_unzip=True)
        if pack:
            Pack(file=filename).zip(delete_folder_after_zip=True)
        
