from sys import platform as _platform
import os

def getPlatform():
    if _platform == "linux" or _platform == "linux2":
        return 'linux'
    elif _platform == "darwin":
        return 'osx'
    elif _platform == "win32":
        return 'windows'

    return None

def clear():
    pfm = getPlatform()
    if pfm == 'linux' or pfm == 'osx':
        os.system('clear')
    elif pfm == 'windows':
        os.system('cls')
