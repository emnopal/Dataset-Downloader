import os


class Dataset:

    def __init__(self):

        tmp = f'{os.getcwd()}/downloaded_dataset'

        if not os.path.exists(tmp):
            try:
                os.mkdir(tmp)
            except IOError as err:
                print(f'cannot access {tmp}: ', err)
        else:
            pass
        self.tmp = tmp
