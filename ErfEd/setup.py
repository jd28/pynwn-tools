from setuptools import setup, find_packages

import os

platforms = [os.path.join('../external/platforms', i) for i in os.listdir('../external/platforms')]
data_files = []

if os.name == 'nt':
    import py2exe
    data_files.append(('platforms', platforms))
    setup(name="ErfEd",
          version="0.1",
          description="ERF file format editor.",
          author="jmd",
          data_files = data_files,
          windows = [{
              "script": "ErfEd.py",
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
    setup(name="ErfEd",
          version="0.1",
          description="ERF file format editor.",
          author="jmd",
          packages = ['widgets'],
          data_files = data_files,
          scripts = ['ErfEd.py'])
