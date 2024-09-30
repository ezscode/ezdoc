from quickdoc import QuickDoc 


# 测试下载文档
def test_doc():

    qd = QuickDoc()
    qd.domain_name = 'llamaindex' 
    qd.doc_urls = ['https://docs.llamaindex.ai/en/stable/']
    qd.doc_xpath_list = '//nav[@data-md-level="1"]/ul/li[@class="md-nav__item"]'
    qd.doc_xpath_content = '//article[@class="md-content__inner md-typeset"]' 

    qd.setup() 
 
    qd.get_doc_urls()  
    qd.open_doc_urls_list() # 打开 url 列表文件，查看；建议查看筛选后，再爬取所有详情  

    # qd.get_doc_all_pages() 


# 测试下载 pillow github readme 
def test_gh():

    qd = QuickDoc()  
    qd.repo_name = 'python-pillow/Pillow'  
    qd.setup()  
    qd.get_github_readme()   



    