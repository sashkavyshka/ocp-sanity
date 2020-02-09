import glob
import os
import subprocess
import time
import fileinput
#from definitions import *
import sys

def get_nodes():
    res = 1
    command_line = "oc get nodes"
    print(command_line)
    p = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    output = str(output)
    if err is None:
        for line in output.split('\\n'):
            if 'NAME' not in line:
                if 'Ready' in line:
                    print(line)
                elif line != "'":
                    print("Machine is not ready!")
                    print(line)
                    return res
        res = 0
    else:
        print(err)
    return res

def get_pods():
    res = 1
    command_line = "oc get pods"
    print(command_line)
    p = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    output = str(output)
    if err is None:
        for line in output.split("\\n"):
            if "NAME" not in line:
                if "Running" in line or "Completed" in line:
                    print(line)
                elif line!="'":
                    print("Machine is not ready!")
                    print(line)
                    return res
        res = 0
    else:
        print(err)
    return res