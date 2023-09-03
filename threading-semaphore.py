from threading import Semaphore
import time
import threading
import random

# accept three inputs from user
n, b, g = input().split()
n = int(n)  # input number of fitting room slot 
b = int(b)  # input number of Blue threads
g = int(g)  # input number of Green threads

blueThreadID = 0  # temporary thread ID name for debugging
greenThreadID = 0  # temporary thread ID name for debugging

b_ctr = 0  # number of blue threads waiting for a slot in the fitting room
g_ctr = 0  # number of green threads waiting for a slot in the fitting room

b_sema_ctr = Semaphore(b)  # represents the number of blue threads created
g_sema_ctr = Semaphore(g)  # represents the number of green threads created
nSema = Semaphore(n)  # represents the number of occupied slots in the fitting room

bSema = Semaphore(1)  # protect the b_ctr variable from other blue threads
gSema = Semaphore(1)  # protect the g_ctr variable from other green threads

slotOccupiedByOtherColor = Semaphore(1)  # represents if the fitting room is being used by another colored thread
master_lock = Semaphore(1)  # used to prevent the second same colored thread from proceeding to the rest of the code


# dressing or fitting when inside the fitting room
def dress():
    pass


# Blue thread
def blue(name):
    global b_ctr

    time.sleep(random.randint(0, 1))
    master_lock.acquire()  # acquire the master lock to prevent the second same colored thread from entering
    bSema.acquire()  # acquire the lock for blue thread
    if b_ctr == 0:  # if it is the first thread, claim the slotOccupiedByOtherColor lock
        slotOccupiedByOtherColor.acquire()
        print("Blue only")

    b_ctr += 1
    bSema.release()  # release the lock for blue thread
    nSema.acquire()  # get the slot in fitting room
    master_lock.release()  # release the master lock 

    time.sleep(random.randint(0, 1))

    b_sema_ctr.acquire()  # acquire to decrement the number of blue threads
    print(f"Thread ID: {threading.get_ident()} and Blue")
    dress()

    time.sleep(random.randint(0, 1))  # simulate context switching

    bSema.acquire()  # acquire the lock for blue thread
    b_ctr -= 1
    nSema.release()  # release a slot in the fitting room
    if b_ctr == 0:  # if it is the last thread, release the slotOccupiedByOtherColor lock
        slotOccupiedByOtherColor.release()
        print("Empty fitting room")
    bSema.release()  # release the lock for blue thread


# Green thread
def green(name):
    global g_ctr

    time.sleep(random.randint(0, 1))
    master_lock.acquire()  # acquire the master lock to prevent the second same colored thread from entering
    gSema.acquire()  # acquire the lock for green thread
    if g_ctr == 0:  # if it is the first thread, claim the slotOccupiedByOtherColor lock
        slotOccupiedByOtherColor.acquire()
        print("Green only")
    g_ctr += 1
    gSema.release()  # release the lock for green thread
    nSema.acquire()  # get the slot in fitting room
  
    master_lock.release()  # release the master lock 

    time.sleep(random.randint(0, 1))

    g_sema_ctr.acquire()  # acquire to decrement the number of green threads
    print(f"Thread ID: {threading.get_ident()} and Green")
    dress()

    time.sleep(random.randint(0, 1))

    gSema.acquire()  # acquire the lock for green thread
    g_ctr -= 1
    nSema.release()  # release a slot in the fitting room
    if g_ctr == 0:  # if it is the last thread, release the slotOccupiedByOtherColor lock
        slotOccupiedByOtherColor.release()
        print("Empty fitting room")
    gSema.release()  # release the lock for green thread


# create and start the blue threads
blue_threads = []
for i in range(b):
    bThread = threading.Thread(target=blue,
                               args=(f"{blueThreadID}", ),
                               daemon=True)
    blueThreadID += 1
    bThread.start()
    blue_threads.append(bThread)

# create and start the green threads
green_threads = []
for i in range(g):
    gThread = threading.Thread(target=green,
                               args=(f"{greenThreadID}", ),
                               daemon=True)
    greenThreadID += 1
    gThread.start()
    green_threads.append(gThread)

# wait for blue threads to finish
for b_t in blue_threads:
    b_t.join()

# wait for green threads to finish
for g_t in green_threads:
    g_t.join()
