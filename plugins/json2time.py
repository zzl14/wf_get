import time
from datetime import datetime
def epoch_to_date(_et):
    return datetime.fromtimestamp(_et)

def data2json(_dt):
	return time.mktime(_dt.utctimetuple())