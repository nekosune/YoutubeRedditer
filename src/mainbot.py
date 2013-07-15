from yrconfigparser import MyConfigParser
import os
import sys
import praw
from datetime import datetime
import pickle
import gdata
from gdata.youtube.service import YouTubeService

def PrintEntryDetails(entry):
  print 'Video title: %s' % entry.media.title.text
  print 'Video published on: %s ' % entry.published.text
  print 'Video description: %s' % entry.media.description.text
  print 'Video category: %s' % entry.media.category[0].text
  print 'Video tags: %s' % entry.media.keywords.text
  print 'Video watch page: %s' % entry.media.player.url
  print 'Video flash player URL: %s' % entry.GetSwfUrl()
  print 'Video duration: %s' % entry.media.duration.seconds

  # non entry.media attributes
  print 'Video view count: %s' % entry.statistics.view_count
  if not entry.rating is None:
      print 'Video rating: %s' % entry.rating.average

  # show alternate formats
  for alternate_format in entry.media.content:
    if 'isDefault' not in alternate_format.extension_attributes:
      print 'Alternate format: %s | url: %s ' % (alternate_format.type,
                                                 alternate_format.url)

  # show thumbnails
  for thumbnail in entry.media.thumbnail:
    print 'Thumbnail url: %s' % thumbnail.url
    
def PrintVideoFeed(feed):
  for entry in feed.entry:
    PrintEntryDetails(entry)
    

def GetAndPrintUserUploads(username):
  yt_service = YouTubeService()
  uri = 'http://gdata.youtube.com/feeds/api/users/%s/uploads' % username
  PrintVideoFeed(yt_service.GetYouTubeVideoFeed(uri))
  
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
    GetAndPrintUserUploads(youtube)
    
 
    
with open("lastCheck","w") as f:
    pickle.dump(datetime.now(),f)