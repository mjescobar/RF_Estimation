try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'RT Estimation',
    'author': 'Maria Jose Escobar',
    'url': 'https://github.com/mjescobar/RF_Estimation',
    'download_url': 'https://github.com/mjescobar/RF_Estimation.git',
    'author_email': 'mariajose.escobar@usm.cl',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['Clustering,STA'],
    'scripts': [],
    'name': 'RT Estimation'
}

setup(**config)
