# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 20:21:14 2020

@author: Sharksunxf
"""
import socket
import struct
import json
import os
import sys
import shutil
import time
import threading
from threading              import Thread
from PyQt5                  import QtWidgets
from PyQt5.QtWidgets        import *
from MainServer_mainUI      import Ui_Dialog_MainServer
'''
class sendcmdthread(threading.Thread):
    def __init__(self, target_Address, cmd):
        threading.Thread.__init__(self)
        self.target_Address = target_Address
        self.status = False
        self.cmd = cmd


    def run(self):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("SendCMD")
            sk.connect(self.target_Address)
        except Exception as e:
            print('SendCMD error:{}'.format(e))
            self.status = False
        else:
            with open('netInfo.json', 'r') as f:  # 打开文件用于读
                data = json.load(f)
                f.close()
            data["CMD"] = self.cmd
            header_json = json.dumps(data)
            header_bytes = header_json.encode('utf-8')
            sk.send(struct.pack('i', len(header_bytes)))
            sk.send(header_bytes)
            #self.sk.shutdown(socket.SHUT_RDWR)
            sk.close()
            self.status = True
    def getstatus(self):
        return self.status
'''

g_ip = 0
g_port = 0



class MainForm(QMainWindow,Ui_Dialog_MainServer):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.pushButton_Start.clicked.connect(self.start_server)

        # 初始化服务器地址设置
        with open('netInfo.json', 'r') as f:
            data = json.load(f)
            f.close()
        # 显示服务器IP和Port
        serverIP = data['MainServerTrueAdd'][0]
        self.lineEdit_MainIP.setText(serverIP)
        serverport = str(data['MainServerTrueAdd'][1])
        self.lineEdit_MainPort.setText(serverport)



    def server_Process(self, ip, port):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            # 绑定套接字到服务器的网络地址
            sock.bind((ip,port))
            time.sleep(0.1)
        except Exception as e:
            self.printMessage("The server program failed to start for the reason:{}。".format(e))
            self.pushButton_Start.setEnabled(True)
            return False
        else:
            self.pushButton_Start.setEnabled(False)
            global g_ip, g_port
            g_ip, g_port = sock.getsockname()
            self.printMessage("The service program has been started，the address is:{}/{}。".format(g_ip, g_port))
            time.sleep(0.5)
            self.pushButton_hint.setEnabled(True)
            sock.listen(4)
            while True:
                sk, skname = sock.accept()
                # 1收报头长度
                obj = sk.recv(4)
                header_size = struct.unpack('i', obj)[0]
                # 2接收报头
                header_bytes = sk.recv(header_size)
                header_json = header_bytes.decode('utf-8')
                header_dic = json.loads(header_json)
                self.CMD_Process(header_dic, sk)
                sk.close()
        self.printMessage("============================================================================")
    def start_server(self):
        self.printMessage("============================================================================")
        self.printMessage("############################  A new work! ##################################")
        self.printMessage("============================================================================")
        MainServer_ip = self.lineEdit_MainIP.text()
        MainServer_port = int(self.lineEdit_MainPort.text())
        with open('netInfo.json', 'r') as f:  # 打开文件用于写
            data = json.load(f)
            data["MainServerTrueAdd"][0] = MainServer_ip
            data["MainServerTrueAdd"][1] = MainServer_port
        with open('netInfo.json', 'w') as f:
            json.dump(data, f)
        with open('netInfo.json', 'r') as f:  # 打开文件用于读
            data = json.load(f)
            f.close()
        server_Address = data["MainServerTrueAdd"]

        self.printMessage("The server is starting......")
        serverStart = Thread(target=self.server_Process, args=(server_Address[0],server_Address[1]))
        serverStart.setDaemon(True)
        serverStart.start()



    def do_inform(self,head_dic):
        dirlist = os.listdir('.\\files\\')
        for dir in dirlist:
            if dir.endswith('temp'):
                num =len(os.listdir('.\\files\\{}'.format(dir)))
                if num:
                    self.printMessage("Notifying {} to receive new files......".format(dir[0:2]))
                    try:
                        with open('.\\info\\{}.json'.format(dir[0:2]), 'r') as f:  # 打开文件用于写
                            data = json.load(f)

                    except:
                        self.printMessage("Error:There isn't the client named {}!".format(dir[0:2]))
                    else:
                        if not self.send_CF(data, "$HereIsNewFile${}$".format(str(num)), []):
                            self.printMessage("{} is down！".format(dir[0:2]))
                            self.send_CF(head_dic, "$UserIsNotAlive$", [])

    def printMessage(self, message):
        time.sleep(0.1)
        timeStamp = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        with open('info.log', 'a') as f:
            f.write("{} # {}\n".format(timeStamp, message))
        print("{} # {}".format(timeStamp,message))

    def receive_File(self, sk, header_dic):
        BUF = 1024 * 100
        total_size = header_dic['file_size']
        file_name = header_dic['file_name']

      #  print("header_dic {}".format(header_dic))
        path = os.getcwd()
        with open('.\\info\\userInfoSet.json', 'r',encoding='UTF-8') as f:  # 打开文件用于读
            data = json.load(f)
            f.close()
        if "down" in header_dic['CMD']:
            file_name_full = "{}{}{}".format(path, "\\files\\{}temp\\".format( header_dic["user_name"]), file_name)
            dstfile = "{}{}{}".format(path, "\\files\\{}\\".format( header_dic["user_name"]), file_name)
        else:
            if "JW" in header_dic['CMD']:
                for k, v in data["client"].items():
                    if v[1] in file_name:
                        file_name_full = "{}{}{}".format(path, "\\files\\{}temp\\".format(v[0]), file_name)
                        dstfile = "{}{}{}".format(path, "\\files\\{}\\".format(v[0]), file_name)
                        break
            else:
                file_name_full = "{}{}{}".format(path, "\\files\\JWtemp\\", file_name)
                dstfile = "{}{}{}".format(path, "\\files\\JW\\", file_name)




        self.printMessage("Receive the command {}".format(header_dic["CMD"]))
        self.printMessage("Receive the file {}".format(file_name_full))
        with open(file_name_full, 'wb') as f:
            recv_size = 0
            while recv_size < total_size:
                try:
                    res = sk.recv(BUF)
                except Exception as e:
                    self.printMessage("Failed to Receive the file ,{}".format(e))
                    sk.close()
                    return
                else:
                    f.write(res)
                    recv_size += len(res)
            f.close()
        shutil.copyfile(file_name_full, dstfile)
        self.printMessage("The reception is complete!")
        sk.close()




    def send_CF(self, header_dic, cmd, f):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        with open('.\\info\\{}.json'.format(header_dic["user_name"]), 'r') as ff:  # 打开文件用于读
            data = json.load(ff)
        try:
            sk.connect(tuple(header_dic["UserServer"]))
        except Exception as e:
            self.printMessage("Failed to connect user:{}".format(e))
            return False
        else:
            if f != []:
                data["file_name"] = f
                data["file_num"] = 1
                path = os.getcwd()
               # print("the user is {}".format(header_dic["user_name"]))
                if "WeNeedFileFrom" in header_dic["CMD"] :
                    file = "{}{}{}".format(path, "\\files\\{}temp\\".format(header_dic["user_name"]), f)
                    data["file_size"] = os.path.getsize(file)
            else:
                data["file_name"] = ""
                data["file_num"] = 0
            self.printMessage("Send the command {}".format(cmd))
            data["CMD"] = cmd
            header_json = json.dumps(data)
            header_bytes = header_json.encode('utf-8')
            # 2 发送报头长度
            try:
                sk.send(struct.pack('i', len(header_bytes)))  # 将报头长度转化为int类型，而int类型为4个字节，所以发送固定长度4个字节
            # 3 发报头
                sk.send(header_bytes)
            except Exception as e:
                self.printMessage("Failed to send cmd:{}".format(e))
                sk.close()
                return False
            else:
            # 4发真实数据
                if f != []:
                    self.printMessage("Send the file {}".format(f))
                    try:
                        with open(file, 'rb') as ff:
                            data = ff.read()
                        sk.sendall(data)
                    except Exception as e:
                        self.printMessage("Failed to send file:{}".format(e))
                        sk.close()
                        return False
                    else:
                        sk.close()
                        self.printMessage("Sent!")
                        return True
                else:
                    return True

    def CMD_Process(self, header_dic, sk):
        # 保存各用户的info.json文件
        with open('.\\info\\{}.json'.format(header_dic["user_name"]), 'w') as ff:
            json.dump(header_dic , ff)
            ff.close()
        mainserver_Address = header_dic['MainServerTrueAdd']
        user_Name = header_dic['user_name']
        cmd = header_dic['CMD']
        self.printMessage("============================================================================")
        self.printMessage("The client is {}.".format(header_dic["user_name"]))
        self.printMessage("The command is {}.".format(cmd))
        global g_ip, g_port# 为每个用户单独开始一个socket
        # 处理用户发出的登录指令,要在Login指令中完成与用户建立新的套接字
        if cmd == "$Login$":
            # 核对登录信息
            with open('password.json', 'r', encoding='UTF-8') as f:  # 打开用户登录名及密码文件
                d = json.load(f)
            self.printMessage("The user {} requests to log in！".format(user_Name))
            time.sleep(0.1)
            with open('.\\info\\{}.json'.format(header_dic["user_name"]), 'r') as ff:
                self.logindata = json.load(ff)
                ff.close()
            if d[user_Name][1] == header_dic['user_password']:
                self.printMessage("{}'s password is volid！".format(user_Name))
                time.sleep(0.1)
                self.printMessage("Create a new service  for {}.".format(user_Name))
                # //////密码正确后，重开一个与用户对话的线程//////////////////////
                serverStart = Thread(target=self.server_Process, args=(mainserver_Address[0], 0))
                serverStart.start()
                # 必须加如休眠时间，让线程启动完毕，此时的g_ip和g_port才是当下的值
                time.sleep(0.5)
                d = []
                d.append(g_ip)
                d.append(g_port)
                self.logindata["MainServerTempAdd"] = d
                # 在info目录中保存各用户登录信息
                newfilename = ".\\info\\" + user_Name + ".json"
                shutil.copyfile('netInfo.json', newfilename)
                self.logindata["CMD"] = "$Allowed${}${}".format(g_ip, g_port)
            else:
                self.logindata["CMD"] = "$Denied$"
                self.printMessage("User {} password error, not allowed to log in.".format(user_Name))
            header_json = json.dumps(self.logindata)
            header_bytes = header_json.encode('utf-8')
            try:
                sk.send(struct.pack('i', len(header_bytes)))
                sk.send(header_bytes)
            except Exception as e:
                self.printMessage('Error sending command:{}'.format(e))

        # 向用户发送文书
        elif "WeNeedFileFrom" in cmd:
            file_list = os.listdir(".\\files\\{}temp\\".format(user_Name))
            if len(file_list) == 0:
                self.printMessage("There is no new file.")
                self.send_CF(header_dic, "$NoNewFile$", [])
            else:
                for f in file_list:
                    self.printMessage("Start sending command {}........".format(f))
                    self.send_CF(header_dic, "$ServerIsReadyToSend$", f)
                    os.remove(".\\files\\{}temp\\{}".format(user_Name,f))
                    break

        elif "IsReadyToSendFile" in cmd:
            userAddr = tuple(header_dic['UserServer'])
            if cmd[1:3] == "JW":
                self.printMessage("Begin receiving query documents.......")
            else:
                self.printMessage("Start receiving feedback.......")
            self.receive_File(sk, header_dic)
            time.sleep(0.1)
            self.send_CF(header_dic, "$ServerIsReadyToAccept$",[])

        elif "IsEnd" in cmd :
            self.do_inform(header_dic)

        elif "Concel" in cmd:
            path = os.getcwd()
            i = cmd.split('$')
            n = i[2].split(']')
            m = n[0].strip('[')
           # print("m is {}".format(m))
            self.printMessage("The Query {} needs to be revoked.".format(i[2]))
            with open('.\\info\\userInfoSet.json', 'r', encoding='UTF-8') as f:
                userinfo = json.load(f)
                f.close()
            for k, v in userinfo["client"].items():
                if m == v[1]:
                    dir1 = "{}\\files\\{}temp\\".format(path, "{}".format(v[0]))
                    dir2 = "{}\\files\\{}\\".format(path, "{}".format(v[0]))
                    filelist = os.listdir(dir1)
                    break
            concelsw = False
            for l in filelist:
                if i[2] in l:
                  #  print("l is {}".format(l))
                    os.remove("{}{}".format(dir1, l))
                    os.remove("{}{}".format(dir2, l))
                    concelsw = True
            if concelsw:
                self.printMessage("Revoked successfully!")
                self.send_CF(header_dic, "$ConcelSuccess${}$".format(i[2]), [])
            else:
                self.printMessage("Revoked failed!")
                self.send_CF(header_dic, "$ConcelFailed${}$".format(i[2]), [])

        elif "down" in cmd:
            dblist = []
            cmdlist = cmd.split("$")
            # 保留2个最新的userdb.db3备份
            filelist = os.listdir(".\\files\\{}".format(cmdlist[1]))

            for f in filelist:
                if ".db3" in f:
                    dblist.append(f)
            # 冒泡排序法
            n = len(dblist)
            for i in range(n):
                # Last i elements are already in place
                for j in range(0, n - i - 1):
                    a = os.path.getmtime(".\\files\\{}\\{}".format(cmdlist[1],dblist[j]))
                    b = os.path.getmtime(".\\files\\{}\\{}".format(cmdlist[1],dblist[j+1]))
                    if a > b:
                        dblist[j], dblist[j + 1] = dblist[j + 1], dblist[j]
            # 删除其余旧日期文件，保留最后两个日期最新的userdb.db3文件
            while len(dblist) > 2:
                file =dblist.pop(0)
                os.remove(".\\files\\{}\\{}".format(cmdlist[1],file))


            self.printMessage("{} is about to log out!".format(cmdlist[1]))
            date = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            srcFile = ".\\files\\{}\\userdb.db3".format(cmdlist[1])
            dstFile = ".\\files\\{}\\userdb{}.db3".format(cmdlist[1], date)
            try:
                self.receive_File(sk, header_dic)
                os.rename(srcFile, dstFile)
            except Exception as e:
                self.printMessage("Database  backup failed:{}.".format(e))
            else:
                    #os.path.getmtime()#文件最近修改的时间
                os.remove(".\\files\\{}temp\\userdb.db3".format(cmdlist[1]))
                self.printMessage("Database backup successful.")

        self.printMessage("The command {} is processed!".format(cmd))
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, "提示", "是否要退出服务程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.printMessage("The server shut down normally!")
            self.printMessage("============================================================================")
            os._exit(0)
        else:
            event.ignore()

        
if __name__ == '__main__':
    # 判断是否存在文件夹如果不存在则创建为文件夹
    with open('.\\info\\userInfoSet.json', 'r', encoding='UTF-8') as f:  # 打开文件用于读
        data = json.load(f)
        f.close()
    for k, v in data["client"].items():
        path = ".\\files\\{}".format(v[0])
        isexists = os.path.exists(path)
        if not isexists:
            os.mkdir(path)
        path = ".\\files\\{}temp".format(v[0])
        isexists = os.path.exists(path)
        if not isexists:
            os.mkdir(path)


    app = QtWidgets.QApplication(sys.argv)
    win = MainForm()
    win.show()
    sys.exit(app.exec_())
    