from setuptools import setup, find_packages
import os

stuff = {
    'name': 'tlkie',
    'version': "0.1",
    'description': "Converts/Merges TLK and Meaglyn's TLS",
    'packages': find_packages(),
    'author': 'jmd'
}

if os.name == 'nt':
    import py2exe
    stuff['console'] = [{
        "script": "tlkie.py",
        "icon_resources" : [(1, os.path.join('../external/icons',"nwn1-toolset.ico"))]
    }]
    stuff['zipfile'] = None
    stuff['options']={"py2exe":{
             'compressed': 2,
             'optimize': 2,
             'bundle_files': 1}}


    setup(**stuff)
elif os.name == 'posix':
    stuff['scripts'] = ['tlkie.py']
    setup(**stuff)
