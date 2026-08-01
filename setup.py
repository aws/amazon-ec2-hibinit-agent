#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

hib_classifiers = [
    "Topic :: Utilities",
]

with open("README.md", "r") as fp:
    hib_long_description = fp.read()

setup(name="ec2_hibinit_agent",
      version='1.0.10',
      author="Jarred Desrosiers",
      author_email="jarredtd@amazon.com",
      packages=[],
      scripts=['agent/hibinit-agent'],
      data_files=[('/etc', ['etc/hibinit-config.cfg'])],
      description="Hibernation setup for EC2 Instances",
      long_description=hib_long_description,
      license="Apache-2.0",
      classifiers=hib_classifiers
)
