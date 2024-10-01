import os
import sys 
from openai import OpenAI

base_url="http://localhost:4000/"
llm_key = 'sk-1234'
model_name = 'zhipu--GLM-4-Flash' 


client = OpenAI(
  base_url=base_url,
  api_key=llm_key
)

def tran_md(content):

    completion = client.chat.completions.create(
        model=model_name,

        # 3、代码内容不翻译，包括行内的代码(`包裹) 和 跨行代码（```包裹）
        messages=[
            {"role": "system", "content": "你是一个程序开发类翻译小助手"},
            {"role": "user", "content": f"请将下面 markdown 文档内容从英文翻译为中文，只返回翻译结果就好。要求：1、保留原本的 markdown 格式； 2、斜体字(两个* 包围的内容)不翻译。 markdown 内容如下：\n {content} "}  
        ],
        user="user-hf"
    )

    print('\n--------\n')
    print(completion) 
    print('\n--------\n') 

    translation = completion.choices[0].message.content
    return translation



from md_parse import SectionType, parse_md

def translate_sections(sections):
    for section in sections:
        content = ''.join(section.lines) 
        if section.type != SectionType.text:
            section.trans = content
            continue
        
        section.trans = tran_md(content) 
        
    trans_ret = ''
    for section in sections:
        if len(section.trans) == 0:continue
        trans_ret += section.trans + '\n'

    return trans_ret

def translate_md(md_path, save_path):

    sections = parse_md(md_path)
    trans_ret = translate_sections(sections) 

    with open(save_path, 'w') as f:f.write(trans_ret) 


def prcs(file_path):
    print('-- ', file_path) 
    save_path = file_path.replace('.md', '_t.md') 
    translate_md(file_path, save_path)
    

def handle_paths(paths):
    for path in paths: 
        if os.path.isfile(path):
            print('-- ', path) 
            prcs(path)

        if os.path.isdir(path):
            
            for file_name in os.listdir(path):
                file_path = os.path.join(path, file_name)
                handle_paths(file_path)

def test(): 
    content = '## hello  \n this is *italic* text \n ## goodbye \n see you!'
    translation = tran_md(content)
    print(translation) 

    
if __name__ == '__main__':
    
    paths = sys.argv[1:]
    print('-- ', paths) 
    handle_paths(paths) 

