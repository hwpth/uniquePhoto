#!/usr/bin/python
#coding: utf-8
#обрабатываются файлы из множества sExt находящиеся в каталогах прописаных в файле path.txt
#на выходе два каталога: уникальные файлы - unique и дубли dup
#исходные файлы удаляются

import os, sys, hashlib, shutil, re, time, ctypes

testMode = False
sDir = set()
sTmp = set()
lUnique = list()
lDup = list()
lMaxFileSize = 0

#>>>>>>>>>>> настройки
sExt = {".jpeg", ".jpg"}

destPath = "C:\\Users\\Andrey\\Downloads"



def walk(dir):
    global lMaxFileSize
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            ext = "." + name.split(".")[-1]
            if ext in sExt:
                f = open(path, "rb")
                h = hashlib.new("sha256", f.read())
                f.close()
                tmp = os.path.getsize(path)
                if tmp > lMaxFileSize:
                    lMaxFileSize = tmp
                if h.hexdigest() in sTmp:
                    lDup.append((h.hexdigest(), dir, name, tmp))
                else:
                    lUnique.append((h.hexdigest(), dir, name, tmp))
                    sTmp.add(h.hexdigest())
                
        else:
            walk(path)

def getDestFileName(dir, fullName):
    n = 0
    ext = fullName.split(".")[-1]
    name = re.sub("." + ext, "", fullName)
    name = re.sub("\(\d+\)", "", name)
    name = name.strip()
    if len(name) == 0:
        name = "img"
    newName = name + "." + ext
    while True:
        if n != 0:
            newName = name + "(" + str(n) + ")." + ext
        path = os.path.join(dir, newName)
        if not os.path.exists(path):
            return path
        n += 1

time.clock()

curDir = os.path.dirname(sys.argv[0])
if curDir != "":
    os.chdir(curDir)
curDir = os.getcwd()
print("Установлена рабочая директория: " + curDir)

freeBytes = ctypes.c_ulonglong(0)
ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(destPath), None, None, ctypes.pointer(freeBytes))
print("\nСвободное место на диске (Байт): " + str(freeBytes.value))

f = open(os.path.join(curDir, "path.txt"), "rt")
for s in f.readlines():
    s = s.strip()
    if len(s) > 0:
        if os.path.exists(s) and os.path.isdir(s):
            walk(s)
        else:
            print("\nДиректория '{0}' не найдена".format(s))
f.close()

print("\nУникальных файлов {0}".format(len(lUnique)))
print("Дублей            {0}".format(len(lDup)))

print("\nМаксимальная длина файла: {0}".format(lMaxFileSize))

if freeBytes.value < 10 * lMaxFileSize:
    print("\n!Не достаточно свободного места на диске")

print("\nВремя анализа: " + str(time.clock()))

if not testMode:
    destDir = os.path.join(destPath, "unique")
    if not os.path.isdir(destDir):
        os.makedirs(destDir)
    for flData in lUnique:
        shutil.move(os.path.join(flData[1], flData[2]), getDestFileName(destDir, flData[2]))

    destDir = os.path.join(destPath, "dup")
    if not os.path.isdir(destDir):
        os.makedirs(destDir)
    for flData in lDup:
        shutil.move(os.path.join(flData[1], flData[2]), getDestFileName(destDir, flData[2]))

    print("\nРабота программы завершена\nВремя выполнения: " + str(time.clock()))

# rSr4r