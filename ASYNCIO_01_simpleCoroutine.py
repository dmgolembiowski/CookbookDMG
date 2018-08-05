import asyncio

async def say(what, when):
    await asyncio.sleep(when)
    print(what)

loop = asyncio.get_event_loop()
loop.run_until_complete(say('Hello World!', 6))
loop.close()

"""
This example uses the asyncio.BaseEventLoop.run_until_complete()
method to schedule a simple function that will wait one second, print "hello world"
then finish.

Note: Because it's launched with run_until_complete(), the 
'event loop' itself will terminate once the 
'coroutine' is completed.
"""
