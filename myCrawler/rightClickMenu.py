# -*- coding: utf-8 -*-

import _winreg
import sys
import os
import os.path

class rightClickMenu():
    ''' 为程序添加右键菜单打开方式 '''
    def __init__(self,menu_name,process,shortcut):
        self.menu_name = menu_name
        self.process = process
        self.shortcut = shortcut #(&I )表示指定快捷键为I）


    def doReg(self):
        try:
            # 打开名称为"HEKY_CLASSES_ROOT\*\shell"的键key
            key = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, r'*\\shell',0, _winreg.KEY_ALL_ACCESS)
            # 为键key新建名称为menu_name的子键，
            # 并设置其数据为REG_SZ(字符串值)类型的menu_name（(&I)表示指定快捷键为I）
            _winreg.SetValue(key, self.menu_name, _winreg.REG_SZ, self.menu_name + self.shortcut)
            # 打开名称为menu_name的子键prog_key
            prog_key = _winreg.OpenKey(key, menu_name)
            # 为键prog_key新建名称为'command'的子键
            # 并设置其数据为REG_SZ（字符串值）类型的prog_path
            prog_path = self.getProcessPath()
            print prog_path
            _winreg.SetValue(prog_key, 'command', _winreg.REG_SZ, prog_path)
            _winreg.CloseKey(prog_key) # 关闭键prog_key
            _winreg.CloseKey(key) # 关闭键key
        except Exception as e:
            if e.args[0] == 5:
                print "Permission denied!Set python run as administrator,it's path is %s" %self.getPythonPath()
            else:
                print e

    def getPythonPath(self):
        pp = sys.executable # path of python.exe
        pwp = os.path.join(os.path.dirname(pp),'pythonw.exe') # path of pythonw.exe
        if os.path.exists(pwp):
            return pwp
        else:
            return pp
 
    def getProcessPath(self):
        pp = self.getPythonPath()
        pp = pp if pp else 'python'
        return  pp + ' '+ self.process

if "__main__" == __name__:
    menu_name = 'goout' # 程序名称（即右键菜单中显示的名称）
    pname = 'goOut.py'
    parg = ' -c go -p "%1"' # %1 is the file path focus on right click
    process = os.path.join(os.getcwd(),pname) + parg # 程序路径（即可执行文件所在路径）
    goout = rightClickMenu(menu_name,process,'(&G) ')
    goout.doReg()
    
