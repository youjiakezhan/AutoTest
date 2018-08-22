# coding=utf-8
import os


def get_ip():
    a = os.popen('ipconfig').readlines()
    for i in a:
        if 'IPv4' in i:
            print(i.split()[-1])
            return i.split()[-1]


if __name__ == '__main__':
    get_ip()