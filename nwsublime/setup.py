from setuptools import setup, find_packages

import os

data_files = [
    ('', ['nwsublime.ini']),
    ('', ['CTAGS_COPYING']),
    ('', ['ctags.exe']),
]

description="Sublime Text tools."
version="0.1",
author="jmd",

if os.name == 'nt':
    import py2exe
    setup(name="nwsublime",
          description=description,
          data_files = data_files,
          version=version,
          author=author,
          windows = [{
              "script": "nwsublime.py",
              "icon_resources" : [(1, os.path.join('../external/icons',"nwn1-toolset.ico"))]
          }],
          zipfile=None,
          options={"py2exe":{
              'compressed': 2,
              'optimize': 2,
              'includes': ["sip"],
              'bundle_files': 1}
          })

elif os.name == 'posix':
    setup(name="nwsublime",
          version=version,
          author=author,
          description=description,
          data_files = data_files,
          scripts = ['nwsublime.py'])
