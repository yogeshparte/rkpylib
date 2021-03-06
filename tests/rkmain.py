from rkpylib.rkhttp import RKHTTPGlobals, RKHTTP
from rkpylib.rkdatasource import RKDataSource
from rkpylib.rkutils import trace_memory_leaks
from rktest import *
from test import *

import gc
import tracemalloc
import pprint
import socket


if __name__ == '__main__':    

    ''' Function to get a free datasource object from pool ''' 
    def dspool_func(pool):
        for idx, ds in enumerate(pool):
            if ds.lock.acquire(False):
                return ds
            else:
                continue
        return None


    tracemalloc.start()
    try:
        #gc.set_debug(gc.DEBUG_LEAK)
        ipaddr = socket.gethostname()
        port = 8282

    
        ''' Creating pool of Datasource and locks to enable thread-safe processing '''
        dspool = list()
        for i in range(5):
            ds = RKDataSource(server='127.0.0.1', port=27017, database='test')
            dspool.append(ds)

        server = RKHTTP.server((ipaddr, port), "rkmain_testapp", "/var/log/rkhttp.log")
        print (f'listening on address {ipaddr} and port {port}')
            
        ''' Adding datasource and lock to globally accessing variables list '''
        server.globals.register('dspool', dspool)
        server.globals.register('dspool_func', dspool_func)    
        server.globals.register('total_requests', 0)
        server.globals.register('counter', 0)

        server.serve_forever()
    finally:
        print ("Closing Down")
        
        for i in range(2):
            print('Collecting %d ...' % i)
            n = gc.collect()
            print('Unreachable objects:', n)
            print('Remaining Garbage:', pprint.pprint(gc.garbage))
            print

        trace_memory_leaks()
        #traceback_memory_leaks()

                

                
'''
list = [1, 2, 3]
dictionary = {1: 'one', 2: 'two', 3: 'three'}
tuple = (1, 2, 3)
set = {1, 2, 3}
'''
