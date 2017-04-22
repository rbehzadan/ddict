from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='ddict',
    version='0.1.3',
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

    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    packages=['ddict'],
    py_modules=['ddict'],

    install_requires=[],

    # $ pip install -e .[dev]
    extras_require={
        'dev': ['pytest-cov'],
    },
    setup_requires=[
        'pytest-runner',
        'pytest-cov'
    ],
)

