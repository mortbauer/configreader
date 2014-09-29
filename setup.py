from setuptools import setup

setup(name="configreader",
    description="An easy-to-use, powerful configuration module for Python",
    long_description = open('README.rst','r').read(),
    license="""MIT""",
    version = "0.0.2",
    author = "Martin Ortbauer",
    author_email = "mortbauer@gmail.com",
    url = "https://github.com/mortbauer/configreader",
    py_modules = ["configreader"],
    classifiers=[
          "Development Status :: Alpha",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python",
          "Topic :: Utilities",
    ],
    )
