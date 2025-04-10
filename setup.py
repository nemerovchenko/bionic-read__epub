from setuptools import setup, find_packages

setup(
    name='bionic-read',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A project to convert EPUB files to Bionic Reading format',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'beautifulsoup4',
        'lxml',
        'regex',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'bionic-read=converter:main',
        ],
    },
)