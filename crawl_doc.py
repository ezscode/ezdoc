import os
import requests
import re 
import time  

from lxml import etree 
from lxml.html import tostring
from urllib.parse import urljoin
from data_util import *

def prcs_readthedocs(url):
    if url.find('readthedocs.io/') == -1:return

def get_navi_urls(base_url, list_xpath, list_path, idx=0):

    print('-- get_navi_urls : ', base_url, list_xpath, list_path)   
    ret = requests.get(base_url)   
    ret.encoding = ret.apparent_encoding
    html_doc = etree.HTML(ret.text) 

    navi_lis = html_doc.xpath(list_xpath)
    print('-- navi_lis : ', len(navi_lis)) 

    for li in navi_lis:
        idx += 1
        href = li.xpath('.//@href')[0].strip()
        if href.find('#') != -1:
            print('xx ', href) 
            continue
        title = ' '.join(li.xpath('.//text()') ).strip() 

        if not href.startswith('http'):
            absolute_url = urljoin(base_url, href)
        else:absolute_url = href 

        with open(list_path, 'a') as fa:
            fa.write('%02d'%(idx) + ' | ' + title + ' | ' + href + ' | '  + absolute_url + '\n')
    
    return idx 
    

def get_navi_urls_section(base_urls, list_xpath, list_path):

    # 判断类型 
    # list_xpath = ''
    idx = 0
    for base_url in base_urls:
        base_url = base_url.strip() 
        if len(base_url) == 0:continue
        idx = get_navi_urls(base_url, list_xpath, list_path, idx)
        print('-- idx : ', idx)  

def get_doc_content_html(url, save_path, xpath_content): 

    ret = requests.get(url)  
    print(ret.encoding, ret.apparent_encoding) 
    ret.encoding = ret.apparent_encoding

    html_doc = etree.HTML(ret.text) 
    content = html_doc.xpath( xpath_content)[0]
    print(content)
    content_html = tostring(content)
    content_html = content_html.decode()
    # print(content_html)
    with open(save_path, 'w') as f:f.write(content_html)    
    return content_html


def get_all_content(list_path, save_dir, xpath_content): 
    
    for line in open(list_path):
        
        arr = line.split('|')
        if len(arr) < 4:
            print('xx ', line) 
            continue 
        
        idx = arr[0].strip() 
        name = arr[1].strip().replace(' ', '_').replace('/', '_') 
        url = arr[3].strip() 

        print(line) 

        # domain_dir = os.path.join(task_dir, 'svgwrite')
        html_path = os.path.join(save_dir, f'{idx}_{name}.html')
        md_path = os.path.join(save_dir, f'{idx}_{name}.md')  

        if os.path.isfile(html_path) and os.path.isfile(md_path):continue
        
        try:
            content_html = get_doc_content_html(url, html_path, xpath_content)
            md = html2md(content_html)
            with open(md_path, 'w') as f:f.write(md) 
            
            # if int(idx) > 5:return  
            time.sleep(1)
        except Exception as err:
            print('xx ', err)  


def test1():
    path = '/Users/xxxx/01_Overview.html'
    html2md(open(path).read(), path.replace('.html', '.md')) 

if __name__ == '__main__':
    
    # test1() 
    pass 