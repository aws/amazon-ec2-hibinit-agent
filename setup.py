#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

hib_classifiers = [
    "License :: OSI Approved :: APACHE SOFTWARE LICENSE",
    "Topic :: Utilities",
]

with open("README.md", "r") as fp:
    hib_long_description = fp.read()

setup(name="ec2-hibinit-agent",
      version='1.0.0',
      author="Anchal Agarwal",
      author_email="anchalag@amazon.com",
      tests_require=["pytest"],	
      scripts=['agent/hibinit-agent'],
      data_files=[('/etc', ['etc/hibinit-config.cfg'])],
      description="Hibernation setup for EC2 Instances",
      long_description=hib_long_description,
      license="Apache 2.0",
      classifiers=hib_classifiers
)
