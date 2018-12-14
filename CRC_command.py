# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         test
# Description:  
# Author:       Leon
# e-mail:       qinhui@aisono.com
# Date:         2018/12/10 13:48
# -------------------------------------------------------------------------------
import crcmod.predefined
import json


class StrFormat(object):
    def __init__(self, data):
        if type(data) is not bytes:
            data = bytes(data, encoding='utf-8')
        self.byte = b'S' + data
        self.crc8 = CRCGenerator()

    @property
    def crc_value(self):
        return self.crc8.crc_calculate(self.byte)

    @property
    def get_length(self):
        return bytes([len(self.byte+self.crc_value)+1])

    @property
    def get_command(self):
        return self.byte+self.crc_value+self.get_length+b'!'


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
        result = chr(crc8.crcValue)
        return result


class CommandFormat(object):

    def __init__(self, cmd=None, **kwargs):
        '''
        初始化 指令
        :param cmd: 设备指令（非运动指令）
        :param kwargs:
        '''
        self.crc8 = CRCGenerator()
        self.data = {'Type': 'a'}
        if kwargs.items():
            self.data['Type'] = 'A'

        if cmd is not None:
            self.data['Cmd'] = cmd

        for key, value in kwargs.items():
            self.data[key] = value
        self.data = json.dumps(self.data, separators=(',', ':'))
        self.data = json.loads(self.data)

    @property
    def get_crc_value(self):
        '''
        获取 CRC 循环校验码的 返回值
        :return:
        '''
        print(str(self.data))
        return self.crc8.crc_calculate(str(self.data))

    @property
    def get_length(self):
        '''
        获取 data 的长度
        :return:
        '''
        return len(str(self.data))

    @property
    def get_command(self):
        cmd = {}
        cmd['DATA'] = self.data
        cmd['CRC'] = self.get_crc_value
        cmd['LEN'] = self.get_length
        return bytes(str(cmd).replace(' ', '').replace('\'', '"'), encoding='utf-8')


if __name__ == "__main__":

    # crc = CRCGenerator()
    # print(crc.create(tmp_str))
    # a = b'0'
    # # print(bytes(tmp_str, encoding='utf-8')+crc.create(tmp_str))
    # tmp_str = 'aB'
    # print(StrFormat('a000b12345c123d1234e1234f1234g1234h1234i1234').crc_value)

    cmd = {}

    cmd['a'] = 50
    cmd['b'] = 60
    cmd['c'] = 70

    print(CommandFormat(**cmd).get_command)

