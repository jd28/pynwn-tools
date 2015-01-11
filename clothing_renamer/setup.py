from setuptools import setup, find_packages
import os

stuff = {
    'name': 'clothing_renamer',
    'version': "0.1",
    'description': "Renames NWN clothing models",
    'packages': find_packages(),
    'author': 'jmd'
}

if os.name == 'nt':
    import py2exe
    stuff['console'] = [{
        "script": "clothing_renamer.py",
        "icon_resources" : [(1, os.path.join('../external/icons',"nwn1-toolset.ico"))]
    }]
    stuff['zipfile'] = None
    stuff['options']={"py2exe":{
             'compressed': 2,
             'optimize': 2,
             'bundle_files': 1}}


    setup(**stuff)
elif os.name == 'posix':
    stuff['scripts'] = ['clothing_renamer.py']
    setup(**stuff)
