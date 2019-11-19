
import setuptools


with open("README.md", "r") as fh:
      long_description = fh.read()

setuptools.setup(
                 name='BinanceFuturesPy',
                 version='1.1',
                 scripts=['futurespy'],
                 author='morozdima',
                 author_email="dmytro@black-box.ai",
                 description='Python library for Binance Futures and Binance Futures Testnet',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url='https://github.com/morozdima/BinanceFuturesPy',
                 download_url='https://github.com/morozdima/BinanceFuturesPy/archive/master.zip',
                 packages=setuptools.find_packages()
)
