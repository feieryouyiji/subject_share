import time
import asyncio
import logging

import logging


logging.info('logging start')
now = lambda : time.time()

async def do_some_work(x):
   print('Waiting: ', x)
   await asyncio.sleep(x)

start = now()

coroutine = do_some_work(2)
print('coroutine', coroutine)

loop = asyncio.get_event_loop()
loop.run_until_complete(coroutine)
print('end')
print('TIME: ', now() - start)

