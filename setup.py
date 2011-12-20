from setuptools import setup, find_packages
import os

version = '1.1.5'

setup(name='younglives.content',
      version=version,
      description="Young Lives content package",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['younglives'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'younglives.content',
          'archetypes.markerfield',
          'archetypes.referencebrowserwidget',
          'archetypes.schemaextender',
          'archetypes.schematuning',
          'collective.autopermission',
          'collective.flowplayer',
          'collective.interfaces',
          'collective.monkeypatcher',
          'plone.app.redirector',
          'plone.app.registry',
          'Products.AdvancedQuery',
          'Products.RedirectionTool',
          'Products.OrderableReferenceField',
          'Products.PloneFormGen',
          'Products.PloneKeywordManager',
          'setuptools',
          'z3c.jbot',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
