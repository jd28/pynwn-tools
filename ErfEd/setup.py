# setup.py for neverrun

from distutils.core import setup
import os

data_files = [('', ["ErfEd.ini"])]

if os.name == 'nt':
    import py2exe
    setup(name="ErfEd",
          version="0.1",
          description="ERF file format editor.",
          author="jmd",
          data_files = data_files,
          windows = [ {
              "script": "ErfEd.py",
              "icon_resources" : [(1, os.path.join('../icons',"nwn1-toolset.ico"))]}],
              options={"py2exe":{"includes":["sip"]}})

elif os.name == 'posix':
    setup(name="ErfEd",
          version="0.1",
          description="ERF file format editor.",
          author="jmd",
          packages = ['widgets'],
          data_files = data_files,
          scripts = ['ErfEd.py'])
