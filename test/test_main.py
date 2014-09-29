import os
import pytest
from configreader import Config,load, ConfigException

def test_simple( ):
    c = Config(open('profile.conf','r'),namespace={'os.getenv':os.getenv})
    assert isinstance(c,Config)

def test_simple_fail():
    with pytest.raises(ConfigException):
        c = Config(open('profile.conf','r'))

def test_simple_hack_fail():
    with pytest.raises(ConfigException):
        c = Config(open('profile_hack.conf','r'))

def test_hack():
    c = Config(open('profile_hack.conf','r'),
                namespace={'os.getenv':os.getenv})
    with pytest.raises(KeyError):
        c['a']
