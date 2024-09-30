#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   data_util.py
@Time    :   2024-09-30 11:15:14
@Author  :   shushu
@Version :   1.0
@Desc    :   None
''' 

import re  

from markdownify import markdownify as md, ATX 


rp_dict1 = {
    '\n\n##': '\n***\n##',
    '\n\n```\n$': '\n\n```shell\n$',
    '\n\n```\n%': '\n\n```shell\n%',
    '\n\n```\npip': '\n\n```shell\npip',
    '\n\n```\nnpm': '\n\n```shell\nnpm',
    '\n\n```\nbash': '\n\n```shell\nbash',
    '\n\n```\ngit': '\n\n```shell\ngit',
    '\n\n```\nsudo': '\n\n```shell\nsudo', 
    '\n\n```\ncd': '\n\n```shell\ncd',
    '\n\n```\n.': '\n\n```shell\n.',
    '\n\n```\nnpm': '\n\n```shell\nnpm',
    '\n\n```\nmake': '\n\n```shell\nmake',
    '\n\n```\npython': '\n\n```shell\npython',
    '\n\n```\n{': '\n\n```json\n{',
    '\n\n```\nimport': '\n\n```python\nimport',
    '\n\n```\nfrom': '\n\n```python\nfrom', 
    '\n\n```\n>>>': '\n\n```python\n>>>', 
    '\n\n```\n-': '\n\n```yaml\n-', 
    '\n\n```\n//': '\n\n```c\n//', 
    # '\n\n```\n': '\n\n```python\n', 
    '\n```\n\n': '\n```\n***\n', 
    '\n```\nCREATE': '\n```sql\nCREATE', 
    '\n```\nINSERT': '\n```sql\nINSERT', 
    '\n```\nSELECT': '\n```sql\nSELECT', 
    '.png)\n':'.png)\n***\n',
    '.webp)\n':'.webp)\n***\n',
    '.jpg)\n':'.jpg)\n***\n',
    '.gif)\n':'.gif)\n***\n', 
    # ' ': 'Kubernetes ',
    '\n\n  ```\n': '\n\n  ```python\n',
    '=jpeg)\n': '=jpeg)\n***\n',
    '=jpg)\n': '=jpg)\n***\n',
    '=webp)\n': '=webp)\n***\n', 
    '=png)\n': '=png)\n***\n', 
    # '':'', 
}

rp_dict2 = {
    '\n\n-':'\n-',

    '码头工人': 'Docker',
    '法学硕士': 'LLM ',
    '拥抱脸': 'Hugging Face ',
    '变形金刚': 'Transformers ',
    '蟒蛇': 'Python',
    '开放人工智能': 'OpenAI',
    '超文本标记语言': ' HTML ',
    '蟒蛇': 'Python',
    '多模式': '多模态',
    'from=appmsg)\n':'from=appmsg)\n***\n'
}





# 主要处理 代码片，不处理太多格式
def clean_en_md(text):

    for k,v in rp_dict1.items():
        text = text.replace(k, v) 

    return text


pat_link = '<a.*>Â¶</a>' 
# <a class="headerlink" href="#basic-data-types" title="Permalink to this headline">&#182;</a>
pat_link2 = '<a class="headerlink".*>&#182;</a>'
 

# 处理格式 及 翻译错误 
def clean_zh_md(text):

    text = re.subn(pat_link, ' ', text)[0]  
    text = re.subn(pat_link2, ' ', text)[0]  

    for k,v in rp_dict2.items():
        text = text.replace(k, v) 

    text = re.sub('\n*\*\*\*\n*\*\*\*\n', "\n***\n", text) 
    # text = re.sub('\s+\|', " |", text)
    text = re.sub('\n{3,20}', "\n\n", text) 
    text = re.sub('\*\*\*\n+', "***\n", text) 
    text = re.sub('\[#\]\(.+\)', ' ', text) # 去掉 # 标题后面的链接 

    # 去掉表格中的多余空格
    text = re.sub('(?:[^\S\n])+\|', " |", text) 
    text = re.sub('\|(?:[^\S\n])+', "| ", text)

    return text



def prcs(file_path):
    if not file_path.endswith('.md'):return
    try:
        print('-- ', file_path)
        text = open(file_path).read() 

        text = clean_en_md(text) 
        text = clean_zh_md(text)  

        with open(file_path, 'w') as f:f.write(text.strip())  
        
        return text 
    except Exception as err:
        print('xx ', file_path, err) 



def html2md(content_html): 
    md_str = md(content_html, heading_style=ATX)  
    return md_str 

