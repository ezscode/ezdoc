import os
import requests 
import time  
import json
from lxml import etree 
from lxml.html import tostring
from urllib.parse import urljoin
from markdownify import markdownify as md, ATX 
from crawl_doc import * 
from config import * 


class QuickDoc(object):
    def __init__(self):
        self.domain_name = ''
        self.repo_name = ''
        
        self.github_url = ''
        self.git_readme = ''  # readme 文件名，有些后缀为 rst
        # self.git_readme = ''
        self.git_branch = '' # 目前主要为main，过去为 master，有些为 dev
        self.git_ownerAvatar = ''

        self.domain_dir = ''

        self.doc_urls = ''
        self.doc_xpath_list = ''
        self.doc_xpath_content = ''
        self.doc_list_path = ''
        self.doc_dir = ''
        self.doc_trans_dir = ''

    def setup(self, skip_gh=0): 

        if len(self.github_url) == 0 and len(self.repo_name) == 0 and len(self.domain_name) == 0:return


        if len(self.repo_name) > 0:  # 以 repo 名为主 
            self.domain_name = self.repo_name.replace('/', '--') 
        
        if len(self.repo_name) == 0 and len(self.github_url) == 0:
            skip_gh = 1
        else: 
            if len(self.github_url) == 0 and len(self.repo_name) > 0:
                self.github_url = 'https://github.com/' + self.repo_name 

            if len(self.repo_name) == 0 and len(self.github_url) > 0:
                self.repo_name = self.github_url.split('?')[0].replace('https://github.com/', '').strip()  

            if skip_gh == 0:
                self.get_gitrepo_detail()


        # 创建文件夹
        self.domain_dir = os.path.join(quickdoc_root_dir, self.domain_name)  
        self.doc_dir = os.path.join(self.domain_dir, 'doc') 
        self.doc_trans_dir = os.path.join(self.domain_dir, 'doc_tran')

        if not os.path.isdir(self.domain_dir):os.makedirs(self.domain_dir)   

        self.doc_list_path = os.path.join(self.domain_dir, f'lis_{self.domain_name}.txt') 

    
    def get_doc_urls(self):
        
        if len(self.doc_urls) == 0 or len(self.doc_list_path) == 0:
            print('xx 文档或保存地址不存在') 
            return 
        
        # get_navi_urls(self.doc_urls, self.doc_xpath_list, self.doc_list_path )
        get_navi_urls_section(self.doc_urls, self.doc_xpath_list, self.doc_list_path)

    def open_doc_urls_list(self):

        os.system(f'code {self.doc_list_path} ')    


    def open_domain_dir(self):

        os.system(f'code {self.doc_dir} ')   


    def get_doc_all_pages(self):

        if not os.path.isdir(self.doc_dir):os.makedirs(self.doc_dir)  
        # if not os.path.isdir(self.doc_trans_dir):os.makedirs(self.doc_trans_dir) 
        get_all_content(self.doc_list_path, self.doc_dir, self.doc_xpath_content)  

    
    def get_gitrepo_detail(self):

        if len(self.github_url) == 0 and len(self.repo_name) == 0:return

        ret = requests.get(self.github_url)
        print('-- ', ret) 
        if ret.status_code != 200:return 
        # with open('github_page.html', 'w') as f:f.write(ret.text)   
        html_doc = etree.HTML(ret.text)   
        scripts = html_doc.xpath('//script//text()') 

        for script in scripts:

            try:
                if script.find('defaultBranch') == -1 or script.find('overviewFiles') == -1:
                    continue

                script_dict = json.loads(script) 
                self.git_branch = script_dict['props']['initialPayload']['repo']['defaultBranch']
                self.git_ownerAvatar = script_dict['props']['initialPayload']['repo']['ownerAvatar']

                overviewFiles = script_dict['props']['initialPayload']['overview']['overviewFiles'] 
                for file in overviewFiles:
                    if file.get('preferredFileType', '') != 'readme':continue
                    readme_path = file.get('path', '')
                    if len(readme_path) > 0:self.git_readme = readme_path

                print(self.git_branch, self.git_readme)
            except Exception as err:
                print('xx ', err) 

    def get_github_readme(self):
        # 获取 readme 文件，如非 md 则转换为 md

        if len(self.github_url) == 0 and len(self.repo_name) == 0:return

        g_readme_url = f'https://raw.githubusercontent.com/{self.repo_name}/refs/heads/{self.git_branch}/{self.git_readme}'  
        print('-- g_readme_url : ', g_readme_url) 

        ret = requests.get(g_readme_url)
        print(ret)

        if ret.status_code != 200:return

        if self.git_readme.endswith('.md'):
            save_name = self.domain_name + '.md'   
            save_path= os.path.join(self.domain_dir, save_name)
        
        with open(save_path, "wb") as code:
            code.write(ret.content)

        # rst
        if self.git_readme.endswith('.rst'):
            # rst --> markdown 
            pass 

    def translate(self):
        pass 

    # 拼接所有已翻译的文档
    def concact_translation_files(self):

        files = os.listdir(self.doc_trans_dir) 
        files.sort()
        file_paths = [os.path.join(self.doc_trans_dir, file_name) for file_name in files]  
        save_path = os.path.join(self.domain_dir, f'doc_translations.md') 
        concact_files(file_paths, save_path) 
    

             
if __name__ == '__main__':
    
    pass 



