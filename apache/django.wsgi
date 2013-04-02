import os
import sys
 
path = '/home/xinting/Documents/workspace/xt'
if path not in sys.path:
    sys.path.insert(0, '/home/xinting/Documents/workspace/xt')

os.environ['DJANGO_SETTINGS_MODULE'] = 'xt.settings'
	 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
