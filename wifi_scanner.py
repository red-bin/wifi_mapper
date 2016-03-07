#!/usr/bin/python2.7

###GOOD IDEA###
#PATH THE DIRECTION OF TICKETERS AND LOCATIONS. ALSO NETWORKX

import wifi
from collections import defaultdict
import time
import pickle
import signal
import subprocess
import psutil
import sys
import psutil
import argparse
import os

parse = argparse.ArgumentParser()
parse.add_argument("--interval", "-I", default=1)
parse.add_argument("--outfile", "-o", default="/home/matt/scans.pkl")
pargs = parse.parse_args()

INTERVAL = pargs.interval
OUTFILE = pargs.outfile

outfile = open('/home/matt/scans.pkl','w')

cells = defaultdict(list)
do_quit = False

def scan():
    scan = None
    while not scan:
        try:
            scan = wifi.scan.Cell.all('wlp2s0')
        except:
            continue

    return scan

def cleanup(outfile=outfile):
    pickle.dump(cells, outfile)
    sys.exit(0)

def signal_handler(signal, frame):
    print "Writing to ~/scans.pkl"
    do_quit = True
    cleanup()

def scan_to_cells(scan_data):
    all_cells = [ cell.__dict__ for cell in scan_data ]

    scantime = time.time()
    all_cells = {scantime: all_cells}

    return all_cells

def init_wifi():
    #{'wlp2s0': snicstats(isup=False, duplex=0, speed=0, mtu=1500), 'lo': snicstats(isup=True, duplex=0, speed=0, mtu=65536)}
    if_isup =  psutil.ne['wlp2s0'].isup
    if not if_isup:
        cmd = "/usr/bin/ip link set up wlp2s0"
        linkstat = subprocess.call(cmd.split(' '))

    return linkstat

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    linkstat = init_wifi()

    while True:
        wifi_scan = scan()
        if wifi_scan:
            scan_cells = scan_to_cells(wifi_scan)
            [ [cells[scantime].append(cell) for cell in scan_cells ] for scantime,scan_cells in scan_cells.items() ]
            time.sleep(INTERVAL)
