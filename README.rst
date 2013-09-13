A simple but still powerfull Configuration Parser
#################################################

There are quite many Configuration Parsers for Python out there, but well, they
all kind of suck in there own way. Let me point out what I dislike:

* `configparser`_: which is the de facto standard, has it's ini like language, in
  my opionion quite awful, difficult and limited

* Configuration through yaml: is beautiful, but how about intergration of
  simple environment variables or interpolation of already defined values

* How about just execution a python module, very unsafe (but who cares), but it
  also pollutes the namespace with all sort of builtins and whatsoever

So I was looking once again and found `python-config`_, which looked really
exactly what I wanted, but well, I had my problems with it, since I wanted to
have acces to stuff like `os.getenv('HOME')` and similar, which was not really
possible since it was forbidden to call a function, though you could still
evaluate stuff and so on. I looke into the source and thought well how can I
allow also calling functions? But I realized they are defining there own
parsing grammar, which seemed kind of reinventing the wheel since I already
knew the `ast`_ module. 

Finally I wrote a very simple Configuration Parser which lets `ast`_ and
`operator`_ do most of the work. It has of course its own problems, and is hack
of half an hour so don't expect much. For me it is still usefull, and maybe we
can improve it.

Usage 
*******
As a simple example of what is possible and how to use the module, see the
following config file which is by the way completely valid python::

    home = os.getenv('HOME')
    aster_root = home+"/data/opt/aster"
    project = "bikeframe-test"
    version = "testing"
    # source directory for all files if relative path
    srcdir = "."
    # output directory for all stuff
    outdir = "results"
    # input mesh file
    meshfile = "mesh.med"
    logfile = "asterclient.log"
    workdir = "/data/tmp"
    # define the studies
    calculations = [
        {"name":"main",
          "commandfile": "main.comm",
          "resultfiles":{
                "bikeframe.rmed":80,
                "bikeframe.msh": 81,
                "buckling.rmed": 82,
                "bikeframe.table": 39,
                "bikeframe.resu": 38,
                "buckling.resu": 37,
                },
          "inputfiles":["parameters.py"],
          },
        {"name": "post",
          "commandfile":"post.comm",
          "poursuite": "main",
          "resultfiles":{
            "vmises.table": 40,
            "protocol": "protocol*.rst",
            }
          }]

Suppose we have this saved as `profile.conf` we could read it like::

    import os
    from configreader import Config

    c = Config(open('profile.conf','r'),namespace={'os.getenv':os.getenv})

which would give as all the values specified and evaluated as a python `dict`.
If we wouldn't have provided the namespace with `os.getenv` the parsing would
have failed since it only allows functions mapped in the namespace, so you have
completele fine grained possibility on what to allow. 
As input the `Config` class expects any file like object which is an object
with a read method.


.. _python-config: https://github.com/Inkvi/python-config
.. _ast: http://docs.python.org/3.3/library/ast.html
.. _operator: http://docs.python.org/3.3/library/operator.html
.. _configparser: http://docs.python.org/3.3/library/configparser.html
