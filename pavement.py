#!/usr/bin/python

from paver.easy import *
import paver.doctools
import os
import glob
import shutil

@task
def setup():
  sh('python3 setup.py -q install')
  pass

@task
def test():
  sh('nosetests test')
  pass

@task
def run():
  sh('python3 src/main.py')

@task
def clean():
  for pycfile in glob.glob("*/*/*.pyc"): os.remove(pycfile)
  for pycache in glob.glob("*/__pycache__"): os.removedirs(pycache)
  for pycache in glob.glob("./__pycache__"): shutil.rmtree(pycache)
  try:  
    shutil.rmtree(os.getcwd() + "/cover")
  except:
    pass
  pass

@task
@needs(['setup', 'clean', 'test'])
def default():
  pass
