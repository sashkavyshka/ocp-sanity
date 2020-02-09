from all_functions import *

def OCP_26473():
    res = 1
    print("Trying to get nodes")
    res = get_nodes()
    if res !=0:
        return res

    print("Trying to get pods")
    res = get_pods()
    if res !=0:
        return res
    return res

if __name__ == "__main__":
    res = OCP_26473()
    if res == 0:
        print("OCP_26473 Finished successfully")
    else:
        print("OCP_26473 failed")
    sys.exit(res)