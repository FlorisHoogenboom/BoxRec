from setuptools import setup

setup(
    name='boxrec',
    version='0.1',
    packages=[
        'boxrec'
    ],
    url='https://github.com/FutureFacts/boxrec',
    license='WTFPL',
    author='Floris Hoogenboom',
    author_email='floris.hoogenboom@futurefacts.nl',
    description='A wrapper around the Boxrec.com website to facilitate easy scraping.',
    install_requires = [
        'requests',
        'lxml',
        'lazy-object-proxy'
    ],
    test_requires = [
        'nose'
    ]
)