from tkinter import *
from tkinter.messagebox import *
import serial
import struct
import threading
from time import sleep


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('SerialTool')
        self.resizable(width=False, height=False)

        # 变量初始化
        self.port = StringVar()
        self.port.set('port')
        self.COM_LIST = []

        self.br = IntVar()
        self.br.set(9600)
        self.BR_LIST = [
            9600,
            11200,
            19200,
        ]

        self.connect = StringVar()
        self.connect.set('connect')
        self.send = StringVar()
        self.send.set('send')

        # 串口扫描
        for i in (range(10)):
            try:
                self.ser = serial.Serial('COM' + str(i))
                self.COM_LIST.append('COM' + str(i))
                self.ser.close()
            except:
                pass

        # 加载界面
        self.UI()

    def UI(self):
        self.t_read = Text(self, width=45, height=12, fg='red', bg='black')
        self.t_read.grid(row=0, column=0, rowspan=3)
        OptionMenu(self, self.port, *self.COM_LIST).grid(row=0, column=1, padx=12)
        OptionMenu(self, self.br, *self.BR_LIST).grid(row=1, column=1, padx=12)
        Button(self, textvariable=self.connect, width=9, height=1, command=self.f_connect).grid(row=2, column=1, padx=12)

        self.t_write = Text(self, width=45, height=4)
        self.t_write.grid(row=3, column=0)
        Button(self, textvariable=self.send, width=9, height=1, command=self.f_send).grid(row=3, column=1, padx=12)

    # 串口连接
    def f_connect(self):
        if(self.port.get() == 'port'):
            showwarning(title='connect failed', message='port was unselected')
        else:
            if self.connect.get() == 'connect':
                try:
                    self.ser = serial.Serial(self.port.get(),self.br.get(), timeout=0.5)
                    self.connect.set('close')
                    self.thread_it(self.reading)
                except:
                    pass
            else:
                self.connect.set('connect')
                self.ser.close()

    # 发送数据
    def f_send(self):
        if(self.ser.isOpen() != True):
            showwarning(title='send failed', message='port was unselected')
        else:
            write_data = self.t_write.get(1.0, END).strip().split(' ') # 取得输入数据 list['1','2','3']
            self.ser.write(bytes([int(i, 16) for i in write_data])) # 16进制发送

    # 监听串口 读取数据
    def reading(self):
        while True:
            res = self.ser.readline()
            if res != b'':
                res = struct.unpack(str(len(res)) + 'B', res) # b'' 解压成 list
                self.t_read.insert(END, [hex(i) for i in res]) # 16进制显示
                self.t_read.insert(END, '\n')

    # 多线程
    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    app = App()
    app.mainloop()