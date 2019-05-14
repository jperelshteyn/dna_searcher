from setuptools import setup

setup(
    name = 'matchseq',
    version = '0.1.0',
    packages = ['matchseq'],
    entry_points = {
        'console_scripts': [
            'matchseq = matchseq.matchseq:main'
        ]
    })