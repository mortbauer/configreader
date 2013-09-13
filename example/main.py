import os
from configreader import Config

c = Config(open('profile.conf','r'),namespace={'os.getenv':os.getenv})
