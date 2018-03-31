from setuptools import find_packages, setup, Command

setup(
    name='europa',
    version='0.1',
    description='The Europa project',
    author='Peter Adkins',
    author_email='peter.adkins@kernelpicnic.net',
    url='https://www.github.com/darkarnium/europa',
    packages=find_packages('src'),
    package_dir={
        'europa': 'src/europa',
    },
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
    install_requires=[
        'flask==0.12.2',
        'flask_migrate==2.1.1',
        'flask_sqlalchemy==2.3.2',
        'psycopg2==2.7.3.2',
    ]
)
