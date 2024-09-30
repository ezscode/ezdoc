import os
import sys  
import getpass 
import requests 
import random
import time 
from lxml import etree
from data_util import * 



# login_user = getpass.getuser()
# save_dir = f'/Users/{login_user}/Documents/wxpsg' 


def rqst_detail(url):
    url = url.strip() 
    if not url.startswith('https://mp.weixin.qq.com'):return 

    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38'
    headers = { 'User-Agent': agent}

    try:
        ret = requests.get(url, headers=headers)    
        print(f'-- rqst_detail {ret.status_code}')
        if ret.status_code != 200:return ''
        
        html = ret.text.strip()
        html_doc = etree.HTML(html)  
        
        title = ''.join(html_doc.xpath('//h1//text()')).strip() 
        content_path = '//div[@id="js_content"]'  
        print(title)

        content_nodes = html_doc.xpath(content_path)

        if len(content_nodes) == 0:
            print(f'xx rqst_detail blk {title} {url}')  
            return ''

        #  style="visibility: hidden; opacity: 0; 
        inner_html = etree.tostring(content_nodes[0], encoding="unicode")
        inner_html = inner_html.replace('data-src="https://', 'src="https://').replace('style="visibility: hidden; opacity: 0;', ' ')  
 
        # md_path = os.path.join(save_dir, f'{title}.md') 
        md_path = f'{title}.md' 
        md= html2md(inner_html)
        md = clean_zh_md(clean_en_md(md))
        md = '<' + url + '>' + '\n***\n# ' + title + '\n' + md 
        with open(md_path, 'w') as f:f.write(md) 
        print('-- 保存成功 ： ', md_path) 

        return inner_html

    except Exception as err:
        print(f'xx rqst_detail err {title}', err)  
        return ''


if __name__ == '__main__':
    
    urls = sys.argv[1:]  
    print('-- ', urls) 
    for url in urls:    
        rqst_detail(url) 
