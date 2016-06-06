"""Setup file to automate the install of sdic in the Python environment."""
from setuptools import setup
from sdic.constants import VERSION


setup(
    name='sdic',
    version=VERSION,
    author='Laurent Raufaste',
    author_email='analogue@glop.org',
    url='https://github.com/percolate/sdic',
    description='Asynchronous soft constraints executed against you databases',
    keywords='sdic sql mysql postgresql sqlalchemy data integrity constraints',
    license='GPLv3',
    packages=['sdic'],
    install_requires=['docopt', 'prettytable'],
    entry_points={
        'console_scripts': [
            'sdic=sdic.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)
