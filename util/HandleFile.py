import os
import picture
        
if __name__ == '__main__':
    import socket
    import pickle
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 8091))
        server.listen(5)
        
        while (True):
            connection, address = server.accept()
            info = pickle.loads(connection.recv(1024))
            
            try:
                if info.get('type', '') == u'picture':
                    im = info['path']
                    if info.get('option', '') == u'watermark':
                        picture.watermark(im, info['label'], info['position'])
                    else:
                        print info['option']
                else:
                    print info['type']
            except Exception, e:
                print 'in while' + e
    except Exception, e:
        print 'HandleFile in main' + e