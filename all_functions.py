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
    command_line = "oc get pods --all-namespaces"
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
                    print("The pod is not ready!")
                    print(line)
                    return res
        res = 0
    else:
        print(err)
    return res

def get_logs():
    res = 1
    command_line = "oc get pods --all-namespaces"
    #Get the list of all pods in all namespaces
    pod_list = []
    print(command_line)
    p = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    output = str(output)
    if err is None:
        for line in output.split("\\n"):
            if "NAME" not in line:
                if "Running" in line or "Completed" in line:
                    print(line)
                    pod_list.append([line.split()[1], line.split()[0], []])
                elif line!="'":
                    print("The pod is not ready!")
                    print(line)
                    return res
        res = 0
    else:
        print(err)

    #Get log for every pod
    for el in pod_list:
        command_line = "oc logs %s -n %s > log.txt"%(el[0], el[1])
        print(command_line)
        p = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        output = str(output)
        if err is None and "Error" not in output:
            statinfo = os.stat('log.txt')
            if statinfo.st_size > 0:
                continue
            else:
                print(err)
                print("Empty logfile for pod %s in namespace %s"%(el[0], el[1]))
                res = 1

        else:
             if err == 1:
                 if "a container name must be specified" in output:
                    el[2] = output.split(":")[-1].strip().strip("[").strip("]").split()
                    for c in el[2]:
                        command_line = "oc logs %s -n %s -c %s> log.txt"%(el[0], el[1], c)
                        print(command_line)
                        p = subprocess.Popen(command_line, stdout=subprocess.PIPE, shell=True)
                        (output, err) = p.communicate()
                        output = str(output)
                        if err is None:
                            statinfo = os.stat('log.txt')
                            if statinfo.st_size > 0:
                                continue
                            else:
                                print("Empty logfile for container %s in pod %s in namespace %s"%(c, el[0], el[1]))
                                res = 1
                                return res
                 else:
                    print("Fail to find logfile for pod %s in namespace %s"%(el[0], el[1]))
                    res = 1
                    return res


    return res