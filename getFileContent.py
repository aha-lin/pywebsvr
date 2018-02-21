import sys
import os

def getHtmlFile(data):
    msgSendtoClient=""
    requestType=data[0:data.find("/")].rstrip()
    if requestType=="GET":
        msgSendtoClient=responseGetRequest(data,msgSendtoClient)
    if requestType=="POST":
        msgSendtoClient=responsePostRequest(data,msgSendtoClient)
    return msgSendtoClient

def getFile(msgSendtoClient,file):
        for line in file:
          msgSendtoClient+=line
        return msgSendtoClient

def getMidStr(data,startStr,endStr):
    startIndex = data.index(startStr)
    if startIndex>=0:
        startIndex += len(startStr)
        endIndex = data.index(endStr)
        return data[startIndex:endIndex]

def getFileSize(fileobject):
    fileobject.seek(0,2)
    size = fileobject.tell()
    return size

def setParaAndContext(msgSendtoClient,type,file,openFileType):
    msgSendtoClient+="Content-Type: "+type+";charset=utf-8"
    msgSendtoClient+="Content-Length: "+str(getFileSize(open(file,"r")))+"\n"+"\n"
    htmlFile=open(file,openFileType)
    msgSendtoClient=getFile(msgSendtoClient,htmlFile)
    return msgSendtoClient

def setParaAndContext(msgSendtoClient,msgStr):
    msgSendtoClient+="Content-Type: "+"text/html"+";charset=utf-8"
    msgSendtoClient+="Content-Length: "+str(len(msgStr))+"\n"+"\n"
    msgSendtoClient+=msgStr
    return msgSendtoClient

def responseGetRequest(data,msgSendtoClient):
    return responseRequest(getMidStr(data,'GET /','HTTP/1.1'),msgSendtoClient)

def responsePostRequest(data,msgSendtoClient):
    return responseRequest(getMidStr(data,'POST /','HTTP/1.1'),msgSendtoClient)

def responseRequest(getRequestPath,msgSendtoClient):
    headFile=open("head.txt","r")
    msgSendtoClient=getFile(msgSendtoClient,headFile)
    if getRequestPath==" ":
        print "Nothing to do"
    else:
        rootPath=getRequestPath
        print >>sys.stderr, "come here:%s,%d" % (rootPath, len(rootPath))
        if rootPath == 'restartvpn ':
            os.system('echo 111 >> /tmp/restartvpn')
            msgSendtoClient=setParaAndContext(msgSendtoClient,rootPath)
            print >>sys.stderr, "come here"
        else:
            print >>sys.stderr, "fail path "
            msgSendtoClient=setParaAndContext(msgSendtoClient," ")

    print >>sys.stderr, rootPath
    return msgSendtoClient
