from datetime import datetime
import pickle
import dateutil.parser

local_time = datetime.now().replace(tzinfo=dateutil.tz.tzlocal())
with open("lastCheck","w") as f:
    pickle.dump(local_time,f)