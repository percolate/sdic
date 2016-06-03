"""Setup file to automate the install of Mackup in the Python environment."""
from setuptools import setup
from sdic.constants import VERSION


setup(
    name='sql-data-integrity-checker',
    version=VERSION,
    author='Laurent Raufaste',
    author_email='analogue@glop.org',
    url='https://github.com/percolate/sql-data-integrity-checker',
    description='Asynchronous soft constraints executed against you databases',
    keywords='sql mysql postgresql sqlalchemy data integrity constraints',
    license='GPLv3',
    packages=['sdic'],
    install_requires=['docopt'],
    entry_points={
        'console_scripts': [
            'sql-data-integrity-checker=sdic.main:main',
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
