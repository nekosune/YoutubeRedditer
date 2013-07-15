from yrconfigparser import MyConfigParser
import os
import sys
import praw
from datetime import datetime
import pickle

cfg_file=MyConfigParser()
path_to_cfg = os.path.abspath(os.path.dirname(sys.argv[0]))
path_to_cfg = os.path.join(path_to_cfg, 'ytconfig.cfg')
cfg_file.read(path_to_cfg)

r = praw.Reddit(user_agent=cfg_file.get('reddit', 'user_agent'))
print 'Logging in as '+ cfg_file.get('reddit', 'username')
r.login(cfg_file.get('reddit', 'username'),
            cfg_file.get('reddit', 'password'))

youtubes=cfg_file.getlist("youtube", "channels")

with open("lastCheck","r") as f:
    lastUpdate=pickle.load(f)

print "Checking youtube for updates since %s" % lastUpdate

for youtube in youtubes:
    print "Checking "+youtube
    
    
    
with open("lastCheck","w") as f:
    pickle.dump(datetime.now(),f)