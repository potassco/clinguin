from clinguin.client import AbstractFrontend
import subprocess
import os
import inspect
import pathlib
class AngularFrontend(AbstractFrontend):

  def __init__(self, args, base_engine):
    super().__init__(base_engine, args)
    path = pathlib.Path(inspect.getfile(AngularFrontend)).parent
    print(pathlib.Path(inspect.getfile(AngularFrontend)).parent)
    self.process = subprocess.Popen(["ng", "serve"], shell=True, cwd=path)
    self.process.communicate()



