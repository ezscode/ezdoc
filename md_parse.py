from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path
import argparse
import os
import re
import sys

FENCES = ["```", "~~~"]
MAX_HEADING_LEVEL = 6
DIR_SUFFIX = "_split"

pat_link = "\!*\[.*?\]\(.*?\)" 
pat_table = '\n\|*.+\|.+\|*\n\|*.+\-+.+\|.+\-+.+\|*\s*.*\n\|*.+\|.+\|*' 

from enum import Enum 
class SectionType(Enum):
    text  = 'text'  
    code  = 'code'   
    image = 'image'
    link  = 'link'   
    table = 'table'

class Section(object):
    
    def __init__(self):
        self.lines = []
        self.type = SectionType.text
        self.trans = ''

        self.idx = 0
        # self.sup_section  # 上一级
        # self.head_level = 0 # 标题层级 

class Line: 
    def __init__(self, line):
        self.full_line = line 
        self.head_level = 0 # 几级标题，0-非标题
        self.within_fence = False # 在 ``` 内`
        self._detect_heading(line)

    def _detect_heading(self, line):

        self.head_level = 0
        self.heading_title = None
        result = re.search("^[ ]{0,3}(#+)(.*)", line) 

        if result != None: 
            self.head_level = len(result[1])
            self.heading_title  = result[2].strip().rstrip("#").rstrip()

    def is_fence(self):
        for fence in FENCES:
            if self.full_line.strip().startswith(fence):
                return True
        return False
    

def is_link(line):
 
    ret = re.findall(pat_link, line, re.DOTALL) 
    print(ret, len(ret))  

    if ret == None:return False 
    if len(ret) != 1:return False

    if ret[0].strip() == line.strip():
        return True


def parse_md(file_path):

    sections = []
    within_fence = False
    last_head_section = None # 上一级目录

    section = Section() 
    for line_str in open(file_path): 
 
        if len(line_str.strip()) == 0:section.lines.append(line_str)

        if is_link(line_str):
            section = Section()
            if line_str.strip().startswith('!'):
                section.type = SectionType.image
            elif line_str.strip().startswith('['):
                section.type = SectionType.link

            sections.append(section) 
            section.lines.append(line_str) 

            # 为接下来的文字，创建新的 section 
            section = Section()
            section.type = SectionType.text
            sections.append(section) 
            
            continue


        line_obj = Line(line_str)
        
        if  line_obj.is_fence(): # 代码片起始
            if within_fence == False: # 刚进入 代码片
                section = Section()
                section.type = SectionType.code
                sections.append(section) 
                section.lines.append(line_str) 
            else: # 离开代码片
                section.lines.append(line_str) 
                section = Section()
                section.type = SectionType.text
                sections.append(section) 
                
            within_fence = not within_fence
            continue
 
        if line_obj.head_level > 0:
            section = Section()
            section.type = SectionType.text
            sections.append(section) 
            # section.head_level = line.head_level 
            # last_head_section = section

     
        section.lines.append(line_str) 

    print('-- sections : ', len(sections)) 

    # for idx in range(len(sections)):
    #     section = sections[idx]
    #     print(idx, section.type, section.lines)
    #     print('\n\n')
    
    return sections


if __name__ == '__main__':
    
    paths = sys.argv[1:]
    print('-- ', paths) 
    for file_path in paths:
        parse_md(file_path)
        
        
    