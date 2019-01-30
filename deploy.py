import subprocess
import sys
import os
import time
import json
# @author Ben Cardoen
# @date 20190130
# @license GPLv3


def readconfig(path, file):
    rdata = {}
    with open(os.path.join(path, file)) as f:
        return json.load(f)

def writeconfig(path, file, data):
    with open(os.path.join(path, file), 'w') as outfile:
        json.dump(data, outfile)




def launch(cmd):
    try:
        return subprocess.Popen(cmd, close_fds=True, bufsize=-1, stdin=open(os.devnull,'rb'), shell=True)
    except Exception as e:
        print('----- Launching \n {}  resulted in \{}'.format(cmd, e))
        return None


def run(cmds):
    ps = []
    for i,cmd in enumerate(cmds):
        ps.append(launch(cmd))
        print('----- Launched job nr {}'.format(i))
    return ps


def runbatch(cmds, batchsize):
    statuscodes = {}
    running = 0
    ps = []
    assert(batchsize > 0)
    N = min(len(cmds), batchsize)
    # Launch the batch, then walk over the process, remove waited=0, and replace them
    print("----- Launching {} jobs".format(N))
    for i in range(N):
        cmd = cmds.pop()
        _p = launch(cmd)
        ps.append((cmd, _p))
    print("----- Launched {} jobs".format(N))
    print("----- Checking queue...".format(N))
    alldone=False
    while not alldone:
        alldone = True
        for i,(cmd,p) in enumerate(ps):
            if p:
                alldone=False
                status = p.poll()
                if status != None:
                    # print("\nCommand Completed\n".format(N))
                    statuscodes[cmd] = status
                    if len(cmds):
                        nc = cmds.pop()
                        ps[i] = (nc, launch(nc))
                        print('----- Launching new job')
                    else:
                        ps[i] = (None, None)
            time.sleep(1)
    print("\n----- All processes done\n")
    return statuscodes

if __name__ == '__main__':

    start = time.time()
    config = readconfig('.', 'config.json')
    script = config['script']
    scriptpath = config['script_path']
    range_1 = config['param_1']
    range_2 = config['param_2']
    batchsize = config['batchsize']
    cmd = []
    for r in range_1:
        for s in range_2:
            cmd.append(' {} {} {}'.format(os.path.join(scriptpath, script), r, s))
    print('\n\n----- Have total of {} commands to be scheduled in parallel...\n\n'.format(len(cmd)))
    s2 = time.time()
    statuscodes = runbatch(cmd, batchsize)
    last = time.time()
    print('----- Total time jobs = \n\t{} seconds'.format(int(last-start)))
    for c,s in statuscodes.items():
        print('Command {} had exit code {}'.format(c, s))
