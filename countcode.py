#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: w4nde3
# @Date:   2020-10-20 10:47:22
# 提取一个py文件中的所有类名和函数、全局函数、类函数

import os
import re
from functools import reduce


class CodeHandle:
    def __init__(self, target):
        self.target = target
        self.current_class = ""
        self.classify = {'global_func': []}
        self.files = []

    def main(self):
        def core(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                line = f.readline()
                while line:
                    res, data = self.handle(
                        line) if self.handle(line) else (0, 0)
                    if res == 'class':
                        self.current_class = data
                        # self.classify.update({"'{}':{}".format(self.current_class,list())})
                        self.classify[self.current_class] = list()
                    elif res == 'function':
                        self.classify.get(self.current_class).append(
                            data) if self.current_class else self.classify.get('global_func').append(data)
                    elif res == 'global_func':
                        self.classify.get('global_func').append(data)
                    else:
                        pass
                    line = f.readline()

        if os.path.isfile(self.target) and self.target.endswith('.py'):
            self.files.append(self.target)
            core(self.target)
            self.save_to_file(py_name=self.target)
        elif os.path.isdir(self.target):
            files = [self.target +
                     x for x in os.listdir(self.target) if x.endswith('.py')]
            for f in files:
                self.files.append(f)
                core(f)
                self.save_to_file(py_name=f)
                self.current_class = ""
                self.classify = {'global_func': []}
        else:
            print("参数不正确，需传入文件或目录")
            exit(1)

    def handle(self, content):
        if content.startswith('def '):
            return "global_func", content.replace(':', '').replace('def ', '').replace('\n', '')

        for match in [{'re': re.compile(r'class \w+:'), 'flag': 'class'}, {'re': re.compile(r'def \w+(.*):'), 'flag': 'function'}]:
            if match.get('re').search(content):
                return match.get('flag'), match.get('re').search(content).group().replace(':', '').replace('class ', '').replace('def ', '')
        else:
            pass

    def show(self):
        for key, value in self.classify.items():
            print("[*] class", key)
            for i in value:
                print("\t[+] {}".format(i))

    def save_to_file(self, py_name):
        with open('log.txt', 'a+', encoding='utf-8') as f:
            f.write("\n文件名："+py_name+"\n")
            for key, value in self.classify.items():
                f.write("[*] class {}\n".format(str(key)))
                for i in value:
                    f.write("\t[+] {}\n".format(i))


demo = CodeHandle("/Users/wander/Desktop/temp/supervisor/")
demo.main()
