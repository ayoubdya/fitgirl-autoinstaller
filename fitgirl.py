import os
import pyautogui as py
import cv2
from time import sleep

py.FAILSAFE = False
DELAY=1

okImg = cv2.imread('images/ok.png')
nextImg = cv2.imread('images/next.png')
installImg = cv2.imread('images/install.png')
muteImg = cv2.imread('images/mute.png')
finishImg = cv2.imread('images/finish.png')
nextNoLineImg = cv2.imread('images/nextNoLine.png')

import sys, traceback, types
def isUserAdmin():
  if os.name == 'nt':
    import ctypes
    # WARNING: requires Windows XP SP2 or higher!
    try:
      return ctypes.windll.shell32.IsUserAnAdmin()
    except:
      traceback.print_exc()
      print("Admin check failed, assuming not an admin.")
      return False
  elif os.name == 'posix':
    # Check for root on Posix
    return os.getuid() == 0
  else:
    raise RuntimeError("Unsupported operating system for this module: %s" % (os.name,))


def runAsAdmin(cmdLine=None, wait=True):
  if os.name != 'nt':
    raise RuntimeError("This function is only implemented on Windows.")

  import win32api, win32con, win32event, win32process
  from win32com.shell.shell import ShellExecuteEx
  from win32com.shell import shellcon

  python_exe = sys.executable

  if cmdLine is None:
    cmdLine = [python_exe] + sys.argv
  elif type(cmdLine) not in (types.TupleType,types.ListType):
    raise ValueError("cmdLine is not a sequence.")
  cmd = '"%s"' % (cmdLine[0],)
  # XXX TODO: isn't there a function or something we can call to massage command line params?
  params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
  cmdDir = ''
  showCmd = win32con.SW_SHOWNORMAL
  #showCmd = win32con.SW_HIDE
  lpVerb = 'runas'  # causes UAC elevation prompt.

  # print "Running", cmd, params

  # ShellExecute() doesn't seem to allow us to fetch the PID or handle
  # of the process, so we can't get anything useful from it. Therefore
  # the more complex ShellExecuteEx() must be used.

  # procHandle = win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)

  procInfo = ShellExecuteEx(nShow=showCmd, fMask=shellcon.SEE_MASK_NOCLOSEPROCESS, lpVerb=lpVerb, lpFile=cmd, lpParameters=params)

  if wait:
    procHandle = procInfo['hProcess']
    obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
    rc = win32process.GetExitCodeProcess(procHandle)
    #print "Process handle %s returned code %s" % (procHandle, rc)
  else:
    rc = None
  return rc

def exist(path):
  status = os.path.exists(path)
  return status

def run(pathSetup):
  os.startfile(pathSetup)

def waitClick(img):
  coords = None
  while coords == None:
    coords = py.locateCenterOnScreen(img)
    sleep(DELAY)
  py.click(*coords)
  
def waitFor(img):
  coords = None
  while coords == None:
    coords = py.locateCenterOnScreen(img)
    sleep(DELAY)
  return coords
  
def resetMouse():
  py.moveTo(0,0)

def main():
  if not isUserAdmin():
    runAsAdmin()
  downloadFolder = f"C:/Users/{os.getlogin()}/Downloads/"
  setupFile = "/setup.exe"
  name = input("Enter folder name : ")
  pathSetup = downloadFolder + name + setupFile
  while True:
    sleep(1)
    if exist(pathSetup):
      print("setup exists")
      break
  run(pathSetup)
  waitClick(okImg)
  waitClick(muteImg)
  for i in range(3):
    waitClick(nextNoLineImg)
    resetMouse()
  waitClick(installImg)
  resetMouse()
  waitFor(finishImg)
  print("DONE")

if __name__ == "__main__":
  main()
