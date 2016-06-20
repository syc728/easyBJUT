from distutils.core import setup  
import py2exe  
  
options = {"py2exe":  {"compressed": 1,"optimize": 2,"bundle_files": 1}}     
setup(
       version = "1.0.0",
       description = "yoho",
       name = "EasyBjut",
       options = options,
       zipfile = None,
       console = [{"script": "v1.2.py" }]
       )
