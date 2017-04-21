from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='ddict',
    version='0.1.1',
    description='Dict class with dot notation (like attributes) for accessing nested values',
    long_description=long_description,
    url='https://github.com/rbehzadan/ddict',
    author='Reza Behzadan',
    author_email='rbehzadan@gmail.com',
    license='MIT',
    classifiers=[
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Build Tools',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='dict dot notation access',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    install_requires=[],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
        # 'dev': ['check-manifest'],
        # 'test': ['pytest', 'pytest-cov'],
    # },
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],
    # test_suite='pytest'
)

