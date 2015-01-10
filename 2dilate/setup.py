from distutils.core import setup
import os

samples = [os.path.join('samples', i) for i in os.listdir('samples')]
twodxs = [os.path.join('2dx', i) for i in os.listdir('2dx')]

data_files = [('examples/2dilate/samples', samples),
              ('examples/2dilate/2dx', twodxs),
              ('', ['2dasource.zip'])]

from setuptools import setup, find_packages
import os

stuff = {
    'name': '2dilate',
    'version': "0.3",
    'description': "A slightly different kind of 2da merger",
    'packages': find_packages(),
    'author': 'jmd',
    'data_files': data_files,
}

if os.name == 'nt':
    import py2exe
    stuff['console'] = [{
        "script": "2dilate.py",
        "icon_resources" : [(1, os.path.join('../external/icons',"nwn1-toolset.ico"))]
    }]
    stuff['zipfile'] = None
    stuff['options']={"py2exe":{
             'compressed': 2,
             'optimize': 2,
             'bundle_files': 1}}


    setup(**stuff)
elif os.name == 'posix':
    stuff['scripts'] = ['2dilate.py']
    setup(**stuff)
