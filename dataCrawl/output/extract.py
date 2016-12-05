# -*- coding: utf-8 -*-
#!/usr/bin/python

# from lxml import etree
# import itertools
# import sys
# import time
from os import listdir,walk
from os.path import isfile, join, dirname, realpath
import json
from pprint import pprint
from lxml import etree

# return a list of folder's real directory
def folder_dir():
    folders_dir = []
    dir_path = dirname(realpath(__file__))
    sub_dir = walk(dir_path)
    for x in sub_dir:
        folders_dir.append(x[0])
    return folders_dir


# check if a string contains number (used to find file name with number, e.g. `1.txt`)
def hasNumbers(str):
    return any(char.isdigit() for char in str)


def main():
    folders = folder_dir()
    for folder in folders[1:]: # ignore index [0] which denote parent directory
        wcid = folder.split('\\')[-1]
        print("current wechatid: {}".format(wcid))
        all_article = open(join(folder, 'all_article.txt'), 'w+')
        files = [f for f in listdir(folder) if isfile(join(folder,f)) and hasNumbers(f)]
        # print ("current folder: {}, current files: {}".format(folder, files))
        if (not files): continue
        for file in files:
            f = open(join(folder, file))
            # extract value of `content_html`
            content = json.load(f)
            page = etree.HTML(content["content_html"])
            try:
                pure_txt = '\n'.join(list(filter(None, page.xpath('//body//*/text()')))).encode('utf-8').strip()
                # put all text of same article in one line.
                pure_txt = pure_txt.replace('\n',' ')
            except AttributeError:
                pass
            else:
                all_article.write('%s,%s\t%s\n' % (wcid,file.split('.')[0], pure_txt))
        all_article.close()

if __name__ == '__main__':
    main()
