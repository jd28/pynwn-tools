from setuptools import setup, find_packages
import os

areag = [os.path.join('areag', i) for i in os.listdir('areag')]

data_files = [('examples/areag', areag)]

stuff = {
    'name': 'areaglob',
    'version': "0.1",
    'description': "Combines areag.ini files.",
    'packages': find_packages(),
    'data_files': data_files,
    'author': 'jmd'
}

if os.name == 'nt':
    import py2exe
    stuff['console'] = [{
        "script": "areaglob.py",
        "icon_resources" : [(1, os.path.join('../external/icons',"nwn1-toolset.ico"))]
    }]
    stuff['zipfile'] = None
    stuff['options']={"py2exe":{
             'compressed': 2,
             'optimize': 2,
             'bundle_files': 1}}

    setup(**stuff)
elif os.name == 'posix':
    stuff['scripts'] = ['areaglob.py']
    setup(**stuff)
