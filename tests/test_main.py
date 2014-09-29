import os
import pytest
from configreader import Config,load, ConfigException

TESTDATADIR = os.path.dirname(__file__)

def test_simple( ):
    f = open(os.path.join(TESTDATADIR,'profile.conf'),'r')
    c = Config(f,namespace={'os.getenv':os.getenv})
    assert isinstance(c,Config)

def test_simple_fail():
    f = open(os.path.join(TESTDATADIR,'profile.conf'),'r')
    with pytest.raises(ConfigException):
        c = Config(f)

def test_simple_hack_fail():
    f = open(os.path.join(TESTDATADIR,'profile_hack.conf'),'r')
    with pytest.raises(ConfigException):
        c = Config(f)

def test_hack():
    f = open(os.path.join(TESTDATADIR,'profile_hack.conf'),'r')
    c = Config(f,namespace={'os.getenv':os.getenv})
    with pytest.raises(KeyError):
        c['a']
