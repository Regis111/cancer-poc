from setuptools import setup

setup(
   name='DeepEcho',
   version='0.1',
   description='Beta version of DeepEcho',
   author='Robert Wcislo',
   packages=['esn'],  #same as name
   install_requires=['numpy', 'pandas', 'torch'], #external packages as dependencies
)
