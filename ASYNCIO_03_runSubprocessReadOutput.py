"""
An example to run (presumably BASH) commands in a subprocess using "asyncio.create_subprocess_exec"
and then sending-off that output (presumably the subprocess) using "process.communicate":
"""

import asyncio
""" 

"""

async def run_command(*args):
        # Create subprocess
        # Note: stdout must be a pipe to be accessible as process.stdout
        process = await asyncio.create_subprocess_exec(*args,"""stdout""" stdout= asyncio.subprocess.PIPE)
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        # Return stdout
        return stdout.decode().strip()


loop = asyncio.get_event_loop()
# Gather uname and date commands
commands = asyncio.gather(run_command('uname'), run_command('date'))
# Run the commands
uname, date = loop.run_until_complete(commands)
# Print the report
print('uname: {}, date: {}'.format(uname, date))
loop.close()
