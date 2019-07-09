""" app runner """
from logging.config import fileConfig

from fields_service import APP

if __name__ == '__main__':

    fileConfig('logging.config')

    APP.run()
