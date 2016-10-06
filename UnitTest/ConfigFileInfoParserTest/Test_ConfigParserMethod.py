# -*- coding: utf-8 -*-
import logging
import random
from ConfigFileInfoParser.InitializationConfigParser import InitializationConfigParser


def initialization_read_save_test():
    logging.warning("Test initialization config read and save ...")
    config_sample_path = "ConfigFileInfoParser/UnitTest.ini"
    ini_Parser = InitializationConfigParser(config_sample_path)
    check_data = str(random.random())
    ini_Parser.SetOneKeyValue("UnitReadSaveTest","save_test",check_data)
    ini_Parser = InitializationConfigParser(config_sample_path)
    node_UnitReadSaveTest = ini_Parser.GetAllNodeItems("UnitReadSaveTest")
    read_data = node_UnitReadSaveTest.get("save_test")
    assert str(read_data) == check_data
    logging.warning("Test initialization config  read and save method OK.")


if __name__ == '__main__':
    initialization_read_save_test()
