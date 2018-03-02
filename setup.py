from setuptools import setup

setup(
    name='boxrec',
    version='0.1',
    packages=[
        'boxrec'
    ],
    url='https://github.com/FutureFacts/boxrec',
    license='MIT',
    author='Floris Hoogenboom, Tom Rijntjes',
    author_email='floris.hoogenboom@futurefacts.nl, tom.rijntjes@futurefacts.nl',
    description='A wrapper around the Boxrec.com website to facilitate easy scraping.',
    install_requires = [
        'requests>=2.12',
        'lxml>=3.7',
        'lazy-object-proxy>=1.2'
    ]
)