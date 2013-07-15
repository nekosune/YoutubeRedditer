from yrconfigparser import MyConfigParser
import os
import sys
import praw
from datetime import datetime
import pickle
import gdata
from gdata.youtube.service import YouTubeService
import dateutil.parser


def GetAndPrintUserUploads(username,date):
    yt_service = YouTubeService()
    uri = 'http://gdata.youtube.com/feeds/api/users/%s/uploads' % username
    feed=yt_service.GetYouTubeVideoFeed(uri)
    entries=[]
    for entry in feed.entry:
        published= dateutil.parser.parse(entry.published.text).astimezone(dateutil.tz.tzlocal())
        if published > date:
            entries+=[entry]
    return entries
      
  
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
    results=GetAndPrintUserUploads(youtube,lastUpdate)
    for result in results:
        submission=r.submit(cfg_file.get('reddit', 'postSubreddit'), result.media.title.text, url=result.media.player.url)
        if result.media.description.text:
            submission.add_comment(result.media.description.text.replace("\r\n","\r\n\r\n"))
    

local_time = datetime.now().replace(tzinfo=dateutil.tz.tzlocal())
with open("lastCheck","w") as f:
    pickle.dump(local_time,f)

    
