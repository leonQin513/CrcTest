# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         Crc_commmand
# Description:   CRC 循环冗余校验码 编码
# Author:       Leon
# e-mail:       qinhui@aisono.com
# Date:         2018/12/10 13:48
# -------------------------------------------------------------------------------
import crcmod.predefined
import json
import serial


class CRCGenerator(object):
    def __init__(self, module='crc-8'):
        # crcmod is a module for crc algrithms inpython
        #  It concludes the modules likecrc-8,crc-16...
        #  you can refer to the website below:
        # http://crcmod.sourceforge.net/crcmod.predefined.html
        self.module = module

    def crc_calculate(self, data):
        '''
        CRC 循环冗余校验码   计算
        :param data: 字符串数据
        :return: 字符码
        '''
        if type(data) is not bytes:
            data = bytes(data, encoding='utf-8')
        crc8 = crcmod.predefined.Crc(self.module)
        crc8.update(data)
        result = int(crc8.crcValue)
        return result


class CommandFormat(object):

    def __init__(self, **kwargs):
        '''
        初始化 指令
         设备指令
        :param kwargs:
        '''
        self.data = {}
        self.crc8 = CRCGenerator()

        for key, value in kwargs.items():
            self.data[key] = value

        self.datajson = self.data
        self.datastr = str(self.data).replace(' ', '').replace('\'', '"')

    @property
    def get_crc_value(self):
        '''
        获取 CRC 循环校验码的 返回值
        :return:
        '''
        return self.crc8.crc_calculate(self.datastr)

    @property
    def get_length(self):
        '''
        获取 data 的长度
        :return:
        '''
        return len(self.datastr)

    @property
    def get_command(self):
        cmd = {}
        cmd['DATA'] = self.datajson
        cmd['CRC'] = self.get_crc_value
        cmd['LEN'] = self.get_length
        return bytes(str(cmd).replace(' ', '').replace('\'', '"'), encoding='utf-8')


class Motor_command(object):
    def __init__(self, cmd, args):
        self.data = {}
        self.cmd = cmd
        self.tmp_list = args
        self.data['Cmd'] = self.cmd
        self.data['Group'] = self.tmp_list[0]
        self.data['Time'] = self.tmp_list[1]

        self.data['V1'] = self.tmp_list[2]
        self.data['a1'] = self.tmp_list[3]
        self.data['a2'] = self.tmp_list[4]

        self.data['Vmax'] = self.tmp_list[5]
        self.data['a1max'] = self.tmp_list[6]
        self.data['a2max'] = self.tmp_list[7]
        self.data['Distance'] = self.tmp_list[8]
    @property
    def get_cmd(self):
        return CommandFormat(**self.data).get_command


class Basic_command(object):
    def __init__(self, cmd=None, args=None):
        # if cmd is None or args is None:
        #     raise
        self.data = {}
        self.data['Cmd'] = cmd
        self.data['Type'] = args

    @property
    def get_cmd(self):
        return CommandFormat(**self.data).get_command

class Basic_command2(object):
    def __init__(self, args):
        self.data = {}
        tmp_list = []
        for item in args:
            tmp_list.append(item)
        self.data['Cmd'] = tmp_list[0]
        self.data['Type'] = tmp_list[1]

    @property
    def get_cmd(self):
        return CommandFormat(**self.data).get_command





def serial_open(device, baud_rate=9600 , errCount = 0):
    """
       串口打开函数   (使用递归调用5次）
    :param device: USB串口号
    :return: 打开USB串口
    """
    try:
        ser = serial.Serial(device, baud_rate)  # 打开串口
        if ser.isOpen == False:
            ser.open()
        return ser
    except Exception as e:
        if errCount > 5:
            return None
        ser = serial_open(device, baud_rate, errCount + 1)  # 递归调用
    return ser

if __name__ == "__main__":

    # ser = serial_open('/dev/ttyAMA0', 115200)  # 打开与下位机通信串口
    # print(CommandFormat('a', 'B').get_command)
    # ser.write(CommandFormat('a','B').get_command)
    # print(ser.readline(10))
    # print(ser.readline(10))
    # ser.close()

    # print(Motor_command('A',[0,1,0.7,0.15,0.15,10,0.05,0.05,10]).get_cmd)
    #
    # print(Basic_command2('aB').get_cmd)

    a = {"DATA": {"Cmd":"A","Group":0,"Time":1,"V1":0.7,"a1":0.15,"a1max":0.05,"a2":0.15,"a2max":0.05,"Vmax":10,"Distance":10},"CRC":195,"LEN":109}



