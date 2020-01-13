#! -*- coding: utf-8 -*-
"""
Author: ZhenYuSha
Create Time: 2019-1-2
Info: 通用配置信息
"""
import os
import configparser
import logging.handlers


def path_deal_all(path):
    """
    返回全路径
    :param path:
    :return:
    """
    return os.path.join(os.path.dirname(__file__), path).replace('\\', '/')


def change_ini(section, option, values=None):
    """
    更改ini文件的某个文件值
    :param section:
    :param option:
    :param values:
    :return:
    """
    with open(path_deal_all("Settings.ini"), "r", encoding="utf-8") as fl:
        context = fl.read()
        new_context = ""
        new_section = "[" + section + "]"
        new_option = option + " = "
        if new_section in context:
            cur_sec = context.split(new_section)[1]
            if "[" in cur_sec:
                cur_sec = cur_sec.split("[")[0]
            if new_option in cur_sec:
                cur_opt = cur_sec.split(new_option)[1]
                if "\n" in cur_opt:
                    cur_opt = cur_opt.split("\n")[0]
                if values == cur_opt:
                    SSetting.print("一样的值就不更新了哈:", section, option, cur_opt)
                    return
                tmp_old = new_option + cur_opt
                tmp_new = new_option + values
                cur_list = context.split(tmp_old)
                if len(cur_list) == 2:
                    pre_tmp_cur = context.split(tmp_old)[0]
                    app_tmp_cur = context.split(tmp_old)[1]
                    new_context = pre_tmp_cur + tmp_new + app_tmp_cur
    with open(path_deal_all("Settings.ini"), "w", encoding="utf-8") as fl:
        if new_context != "":
            SSetting.print("更新成功")
            fl.write(new_context)
        else:
            SSetting.print("更新异常", mode="error")


# 实例化configParser对象
qn_config = configparser.ConfigParser()
qn_config.read(path_deal_all("Settings.ini"), encoding="utf-8")

# 初始化日志文件
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s", "%m-%d %H:%M:%S")
fh = logging.handlers.RotatingFileHandler(path_deal_all("CurSystem.log"), maxBytes=50 * 1024 * 1024, backupCount=10)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)


class SSetting(object):
    @staticmethod
    def read_ini(section, option, mode="str"):
        """
        读取配置文件返回值
        :param section: section信息
        :param option: option信息
        :param mode: 字符串、整型、浮点型等
        :return: 值
        """
        if mode == "str":
            return qn_config.get(section, option)
        elif mode == "int":
            return qn_config.getint(section, option)
        elif mode == "float":
            return qn_config.getfloat(section, option)
        else:
            return qn_config.get(section, option)

    @staticmethod
    def print_info(*args, sc=55, sp="—"):
        """
        醒目打印，尽量不要直接用，在print里面有用
        :param args:不限参数个数
        :param sc:字符个数
        :param sp:默认字符
        :return:返回醒目的打印信息
        """
        str_tmp = sp
        for i in range(0, sc):
            str_tmp += sp
        print(str_tmp)
        print(*args)
        print(str_tmp)

    @staticmethod
    def print(*context, mode="normal"):
        """
        打印，debug则print，release则log
        :param context: 内容，不限个数
        :param mode: normal（默认）， warning， error， good(醒目打印), 其它
        :return:
        """
        setting_debug = SSetting.read_ini("common", "debug")
        if setting_debug == "debug":
            if mode == "normal":
                print(*context)
            elif mode == "warning":
                SSetting.print_info(*context)
            elif mode == "error" or mode == "err":
                SSetting.print_info(*context, sp="#")
            elif mode == "good":
                SSetting.print_info(*context, sp="*")
            else:
                SSetting.print_info(*context, sp="+")
        else:
            if mode == "normal":
                logger.info(context)
            elif mode == "warning":
                logger.warning(context)
            elif mode == "error" or mode == "err":
                logger.error(context)
            elif mode == "good":
                logger.info(context)
            else:
                logger.debug(context)

    @staticmethod
    def get_git_version(branch="master"):
        git_ml = "git rev-list --header " + branch + " --count"
        tmp = os.popen(git_ml).readlines()
        if len(tmp) > 0:
            version_tmp = tmp[0].strip()
            SSetting.print("Git version: ", version_tmp)
            change_ini("common", "git_version_master", version_tmp)
        else:
            SSetting.print("获取Git版本失败", mode="error")


if __name__ == '__main__':
    # 静态方法，无需实例化
    SSetting.print("开始", "参数", "随便", "搞", mode="ZhenYuSha")
    SSetting.print("通用配置信息", mode="good")
    value = SSetting.read_ini("common", "git_version_master")
    SSetting.print("Setting git_version_master:", type(value), value)
    SSetting.get_git_version()
    SSetting.print("结束", mode="ZhenYuSha")
