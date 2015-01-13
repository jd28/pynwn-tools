from setuptools import setup, find_packages
import os

head2da = [os.path.join('heads', i) for i in os.listdir('heads')]
data_files = [
    ('examples/heads/', head2da),
    ('', ['head_renamer.ini']),
]

stuff = {
    'name': 'head_renamer',
    'version': "0.1",
    'description': "Renames NWN head models",
    'packages': find_packages(),
    'author': 'jmd',
    'data_files': data_files,
}

if os.name == 'nt':
    import py2exe
    stuff['console'] = [{
        "script": "head_renamer.py",
        "icon_resources" : [(1, os.path.join('../external/icons',"nwn1-toolset.ico"))]
    }]
    stuff['zipfile'] = None
    stuff['options']={"py2exe":{
             'compressed': 2,
             'optimize': 2,
             'bundle_files': 1}}


    setup(**stuff)
elif os.name == 'posix':
    stuff['scripts'] = ['head_renamer.py']
    setup(**stuff)
