# coding=utf-8
import os

import jinja2
import yaml

# 当前脚本路径
base_path = os.path.abspath(os.path.dirname(__file__))
# yaml文件夹路径
yaml_page_path = os.path.join(base_path, "page_element")


class PageCreate(object):
    def traverse_yaml(self):
        # 功能：遍历读取yaml文件
        # 返回: yaml文件的解析对象
        # 返回类型：字典
        page_elements = {}
        for root, dirs, files in os.walk(yaml_page_path):
            for file in files:
                yaml_file_path = os.path.join(root, file)
                if yaml_file_path.endswith('.yaml'):
                    with open(yaml_file_path, 'r', encoding='utf-8') as f:
                        page = yaml.load(f)
                        page_elements.update(page)
        return page_elements

    def get_page_list(self, yaml_page):
        # 参数：解析yaml文件返回的字典对象
        # 功能：整理字典对象
        # 返回：得到各个.yaml文件内的页面和该页面上的元素
        # 返回类型：字典
        page_object = {}
        for page, names in yaml_page.items():
            loc_names = []
            locs = names['locators']
            for loc in locs:
                loc_names.append(loc['name'])
            page_object[page] = loc_names
        return page_object

    def create_page_py(self, page_list):
        # 参数：get_page_list函数返回的字典对象
        # 功能：按照给定模板自动生成一个page.py文件（各个页面和页面上的元素）
        template_loader = jinja2.FileSystemLoader(searchpath=base_path)
        template_env = jinja2.Environment(loader=template_loader)
        template_vars = {'page_list': page_list}
        template = template_env.get_template('template_page')
        with open(os.path.join(base_path, 'pages.py'), 'w', encoding='utf-8') as f:
            f.write(template.render(template_vars))


if __name__ == "__main__":
    ele = PageCreate()
    yamlpage = ele.traverse_yaml()
    pagelist = ele.get_page_list(yamlpage)
    ele.create_page_py(pagelist)
