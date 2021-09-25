from setuptools import setup
import os
# from freecad.workbench_starterkit.version import __version__
# name: this is the name of the distribution.
# Packages using the same name here cannot be installed together

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            "freecad", "vendor_parts", "version.py")
with open(version_path) as fp:
    exec(fp.read())

setup(name='freecad.vendor_parts',
      version=str(__version__),
      packages=['freecad',
                'freecad.vendor_parts'],
      maintainer="alexneufeld",
      maintainer_email="alex.d.neufeld@gmail.com",
      url="https://github.com/alexneufeld/FreeCAD_vendor_parts",
      description="freecad module for vendor part downloading support, installable with pip",
      install_requires=[],
      include_package_data=True)
