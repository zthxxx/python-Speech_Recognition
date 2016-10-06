# -*- coding:utf-8 -*-

import sys,os,time
try:
    import ConfigParser
except:
    import configparser as ConfigParser


class InitializationConfigParser:

    def __init__(self, path):
        self.path = path
        self.config = ConfigParser.ConfigParser()

    def GetAllNodeItems(self,field):
        result = dict()
        try:
            self.config.read(self.path)
            keys = self.config.options(field)
        except ConfigParser.NoSectionError:
            return result
        for key in keys:
            result[key] = self.GetOneKeyValue(field,key)
        return result

    def GetOneKeyValue(self, field, key,type=None):
        result = None
        try:
            self.config.read(self.path)
            if type is int:
                result = self.config.getint(field, key)
            else:
                result = self.config.get(field, key)
        except ConfigParser.NoSectionError:
            print("There is no the Section!")
        except ValueError:
            print("There is no value like int!")
        except:
            pass
        return result

    def SetOneKeyValue(self, filed, key, value):
        '''
        :param filed: 字段
        :param key: 键名 (注： 这里键名最好全用小写，因为大写的键名最后保存时也是以小写保存的)
        :param value: 值
        :return:
        '''
        try:
            self.config.read(self.path)
            self.config.options(filed)
        except ConfigParser.NoSectionError:
            self.config.add_section(filed)
        except:
            return False
        try:
            self.config.set(filed, key, value)
        except TypeError:
            self.config.set(filed, key, str(value))
        except:
            return False
        self.config.write(open(self.path,'w'))
        return True


if  __name__ == '__main__':
    initializationConfigParser = InitializationConfigParser("UnitTest.ini")
    initializationConfigParser.SetOneKeyValue("ServerSocket","ipAddress","127.0.0.1")
    initializationConfigParser.SetOneKeyValue("ServerSocket","port",5000)
    initializationConfigParser.SetOneKeyValue("ServerSocket","key","12abdfgrc3")

    print(initializationConfigParser.GetOneKeyValue("ServerSocket","ipAddress"))
    print(initializationConfigParser.GetOneKeyValue("ServerSocket","port",type=int))
    print(initializationConfigParser.GetOneKeyValue("ServerSocket","key"))
