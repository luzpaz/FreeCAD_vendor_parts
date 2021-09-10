from setuptools import setup
import os
# from freecad.workbench_starterkit.version import __version__
# name: this is the name of the distribution.
# Packages using the same name here cannot be installed together

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            "freecad", "mcm_addon", "version.py")
with open(version_path) as fp:
    exec(fp.read())

setup(name='freecad.mcm_addon',
      version=str(__version__),
      packages=['freecad',
                'freecad.mcm_addon'],
      maintainer="alexneufeld",
      maintainer_email="alex.d.neufeld@gmail.com",
      url="https://github.com/alexneufeld/FreeCAD_mcm_addon",
      description="freecad module for mcmaster-carr support, installable with pip",
      install_requires=[],
      include_package_data=True)
