
from setuptools import setup
from setuptools import find_packages


setup(name='BinanceFuturesPy',
      version='1.0',
      description='Python library for Binance Futures and Binance Futures Testnet',
      author='morozdima',
      url='https://github.com/morozdima/BinanceFuturesPy',
      download_url='https://github.com/morozdima/BinanceFuturesPy/archive/master.zip',
      license='MIT',
      install_requires=['websocket-client', 'pandas'],
      packages=find_packages()
      )
