import threading

class RemoteFile2:
    def __init__(self, request, path, type):
        self.request = request
        self.path = path
        self.type = type
        
    def receive(self):
        import os
        from xt import settings
        
        file = self.request.FILES.get('file', '')
        filename = file.name
        
        fname = os.path.join(settings.MEDIA_ROOT, 'file/', filename)
        
        if os.path.exists(fname):
            os.remove(fname)
            
        dirs = os.path.dirname(fname)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
            
        fp = open(fname, 'wb')
        for content in file.chunks():
            fp.write(content)
        fp.close()
        
        #call handle process
        info = {}
        info['type'] = self.type
        info['path'] = fname
        info['position'] = self.request.POST.get('position', '')
        info['label'] = self.request.POST.get('label', '')
        info['option'] = 'watermark'
        
        import socket
        import pickle
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8091))
        sock.send(pickle.dumps(info))
        sock.close()

class RemoteFile(threading.Thread):
    
    def __init__(self, request, path, type):
        threading.Thread.__init__(self)
        self.request = request
        self.path = path
        self.type = type
    
    def run(self):
        import os
        from xt import settings
        
        file = self.request.FILES.get('file', '')
        filename = file.name
        
        fname = os.path.join(settings.MEDIA_ROOT, 'file/', filename)
        
        if os.path.exists(fname):
            os.remove(fname)
            
        dirs = os.path.dirname(fname)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
            
        fp = open(fname, 'wb')
        for content in file.chunks():
            fp.write(content)
        fp.close()
        
        #call handle process
        info = {}
        info['type'] = self.type
        info['path'] = fname
        info['position'] = self.request.POST.get('position', '')
        info['label'] = self.request.POST.get('label', '')
        info['option'] = 'watermark'
        
        import socket
        import pickle
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8091))
        sock.send(pickle.dumps(info))
        