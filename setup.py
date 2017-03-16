from setuptools import setup


setup(name = 'dunendggd',
      version = '1.0.0',
      description = 'DUNE Near Detector based on General Geometry Description',
      author = 'Jose Palomino and Guang Yang',
      author_email = 'gyang@nngroup.physics.sunysb.edu',
      license = 'GPLv2',
      url = 'https://github.com/gyang9/GuJo',
      package_dir = {},
      packages = ['ndggd', 'ndggd.Det', 'ndggd.Module', 'ndggd.Component', 'ndggd.Active'],
      install_requires = [
        "gegede >= 0.4",
        "pint >= 0.5.1",      # for units
        "lxml >= 3.3.5",      # for GDML export],
      ],
  )

