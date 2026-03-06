import datetime
import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.filedialog import askdirectory

import clipboard
import pyperclip
from PIL import Image

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 全局变量存储图片信息
image_info = []
# 恣伏
client_id = "wx00c3b7d9db7553a0"
client_secret = "782415b7aa6a62098cf21e2fbafb4614"
grant_type = "client_credential"

# # 宋荣子
# client_id = "wx772b83593792d05d"
# client_secret = "ebd08472eb399be190686975b02485ba"
# grant_type = "client_credential"

import requests
from bs4 import BeautifulSoup
import re
import hashlib
import chardet

# 第一标签页功能

import sys
import os
import tkinter.filedialog as filedialog
from PIL import Image

import configparser

import configparser
import os
import tkinter.filedialog as filedialog
from PIL import Image

image_info = []


def Get_Image():
    config = configparser.ConfigParser()
    config.read('config.ini')
    base_dir = config.get('Paths', 'base_directory')
    if not os.path.isabs(base_dir):
        script_path = os.path.abspath(__file__)
        base_dir = os.path.join(os.path.dirname(script_path), base_dir)
    base_dir = os.path.abspath(base_dir)

    # 打开文件选择对话框，选择图片文件
    filepaths = filedialog.askopenfilenames(filetypes=[("All Files", "*.*")])

    # 清空image_info列表
    image_info.clear()

    for filepath in filepaths:
        file_drive = os.path.splitdrive(filepath)[0]  # 获取文件所在磁盘分区
        base_drive = os.path.splitdrive(base_dir)[0]  # 获取基础目录所在磁盘分区
        if file_drive != base_drive:
            # 如果跨磁盘分区，构建一种包含磁盘分区信息的相对路径表示
            relative_path = file_drive + os.sep + os.path.relpath(filepath, file_drive).replace("\\", "/")
        else:
            relative_path = os.path.relpath(filepath, base_dir).replace("\\", "/")

        # 读取图片文件并获取宽度和高度
        image = Image.open(filepath)
        width, height = image.size

        # 获取图片文件名称
        image_name = os.path.splitext(os.path.basename(filepath))[0]

        # 将图片信息添加到image_info列表中
        image_info.append({
            'name': image_name,
            'width': width,
            'height': height,
            'path': relative_path
        })

    return image_info


def No_Edge_Image():
    Get_Image()
    code = ""
    # 在button2_click函数中处理图片信息
    for info in image_info:
        code += f'<svg id="{info["name"]}" style="background-image: url(&quot;{info["path"]}&quot;);background-size: 100%;background-repeat: no-repeat;margin-top:-0.33vw;line-height: 0;" viewbox="0 0 {info["width"]} {info["height"]}"></svg>\n'
        # 复制到粘贴板

    clipboard.copy(code)
    return code


def Fo_Image():
    Get_Image()
    code = ""
    for info in image_info:
        code += f'''<g id="{info["name"]}">
  <foreignObject x="0" y="0" width="100%" height="100%">
    <svg style="background-image: url(&quot;{info["path"]}&quot;);background-size: 100%;background-repeat: no-repeat;margin-top:-0vw;line-height: 0;" viewbox="0 0 {info["width"]} {info["height"]}">
    </svg>
  </foreignObject>
</g>\n'''

    clipboard.copy(code)
    return code


# 序列帧
def Se_Frames():
    x = 2000
    Get_Image()
    if not image_info:
        Log_Write("请选择图片！")
        return None

    code = '<g id="序列帧">\n'
    code += '<animateTransform attributeName="transform" type="translate" values="'
    for i in range(len(image_info)):
        if i != 0:
            code += ';'
        code += f'-{x * (i + 1)} 0'
    code += f'" begin="0" dur="3s" repeatCount="indefinite" restart="always" calcMode="discrete" fill="freeze"></animateTransform>\n'

    code += '<g id="序列">\n'

    F_Element = image_info[0]
    code += '''<g transform="translate(0 0)">
    <foreignObject x="0" y="0" width="{}" height="{}">
    <svg style="-webkit-user-select:none;-webkit-user-select:none;background-image: url(&quot;{}&quot;);background-size: 100%;background-repeat: no-repeat;display: inline;line-height: 0;" viewBox="0 0 {} {}">
    </svg>
    </foreignObject>
    </g>
    '''.format(F_Element['width'], F_Element['height'], F_Element['path'], F_Element['width'], F_Element['height'])

    for i, info in enumerate(image_info):
        code += f'\n<g transform="translate({x * (i + 1)} 0)">\n'
        code += f'<foreignObject x="0" y="0" width="{info["width"]}" height="{info["height"]}">\n'
        code += f'<svg style="-webkit-user-select:none;-webkit-user-select:none;background-image: url(&quot;{info["path"]}&quot;);background-size: 100%;background-repeat: no-repeat;display: inline;line-height: 0;"'
        code += f' viewBox="0 0 {info["width"]} {info["height"]}">\n'
        code += '</svg>\n'
        code += '</foreignObject>\n'

        code += '</g>\n'

    code += '</g>\n'
    code += '</g>\n'
    clipboard.copy(code)
    return code


# 自适应左划
def Auto_HuaDong():
    Get_Image()
    code = ""
    ShouldHeight = image_info[0]['height']
    ShouldWidth = image_info[0]['width']
    TitleName = "自适应滑动容器"
    for info in image_info:
        min_width = (ShouldHeight / info["height"] * 100) * info["width"] / ShouldWidth
        # 先执行SVG构建函数，构建基础SVG图
        code += f'<section id={info["name"]} style="min-width:{min_width}%;scroll-snap-align:center;flex: none;flex-direction: column;">\n<svg id="{info["name"]}" style="background-image: url(&quot;{info["path"]}&quot;);background-size: 100%;background-repeat: no-repeat;margin-top:-0vw;line-height: 0;" viewbox="0 0 {info["width"]} {info["height"]}"></svg>\n</section>\n'

    output = f'<section id="{TitleName}"style="margin-top:-0.33vw;display: flex;overflow-x: auto;overflow-y: hidden;pointer-events:visible;">' + code + '\n</section>'
    pyperclip.copy(str(output))
    return output


# 多张渐显
def Mul_Opcaity():
    Get_Image()
    code = ""
    Begin_time = 0.5
    for info in image_info:
        code += f'''<g id="{info["name"]}" opacity="0">
        <animate attributeName="opacity" begin="{Begin_time}" restart="never" dur="0.5s" values="0;1;1" fill="freeze"></animate>
      <foreignObject x="0" y="0" width="100%" height="100%">
        <svg style="background-image: url(&quot;{info["path"]}&quot;);background-size: 100%;background-repeat: no-repeat;margin-top:-0vw;line-height: 0;" viewbox="0 0 {info["width"]} {info["height"]}">
        </svg>
      </foreignObject>
    </g>\n'''
        Begin_time += 0.8

    clipboard.copy(code)
    print('多张渐显代码已复制！')
    Log_Write('多张渐显代码已复制！')


# 二维码
def QR_Code():
    Get_Image()
    code = ""
    for info in image_info:
        code += f'''<section id="二维码"
         style="-webkit-touch-callout:none;-webkit-user-select:none;-khtml-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;overflow: hidden;text-align: center;line-height: 0;margin-top:-0.33vw;">
    <section style="height:0;opacity:0;pointer-events:visible;">
        <img src="{info["path"]}" style="width: 100% !important; height: auto !important; visibility: visible !important;">
    </section>
    <section style="pointer-events:none;transform: scale(1);">
        <svg data-copyright="Open实验室"
             style='background-image: url(&quot;{info["path"]}&quot;);background-size: 100%;background-repeat: no-repeat;margin-top:-1px;line-height: 0;'
             viewbox="0 0 {info["width"]} {info["height"]}">
        </svg>
    </section>
</section>
\n'''

    clipboard.copy(code)
    return code


# 抽签海报
def Lottery():
    Get_Image()
    Base_Width = 88
    code = '''<section style="text-align: center;flex: 1;">
                                <section
                                        style="display: flex;flex-direction: column;overflow: hidden;line-height: 0;flex-direction: column;">
                                    <br></section>
                            </section>
                            <section style="text-align: center;flex: 1;">
                                <section
                                        style="display: flex;flex-direction: column;overflow: hidden;line-height: 0;flex-direction: column;">
                                    <br></section>
                            </section>
'''
    print(image_info)
    for info in image_info:
        code += f'''<section style="text-align: center;flex: 1;">
                                <section
                                        style="display: flex;flex-direction: column;overflow: hidden;line-height: 0;flex-direction: column;">
                                    <section
                                            style="-webkit-touch-callout:none;-webkit-user-select:none;-khtml-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;overflow: hidden;text-align: center;line-height: 0;margin-top:-0vw;z-index:0;">
                                        <section style="height:0;opacity:1;pointer-events:visible;">
                                            <img data-h="{info["height"]}" data-w="{info["width"]}" powered-by="Open实验室"
                                                 src="{info["path"]}"
                                                 style="width:100%;pointer-events:painted;-webkit-user-drag:none;">
                                        </section>
                                        <section style="pointer-events:none;transform: scale(1);">
                                            <svg id="8-1-1"
                                                 style="background-image: url(&quot;{info["path"]}&quot;);background-size: 100%;background-repeat: no-repeat;margin-top:0vw;line-height: 0;"
                                                 viewBox="0 0 {info["width"]} {info["height"]}"></svg>
                                        </section>
                                    </section>
                                </section>
                            </section>\n'''

    length = len(image_info)
    first_width = image_info[0]['width']
    first_height = image_info[0]['height']
    code1 = F''' 
                        <svg opacity="1"
                         style="display:inline-block;overflow:visible;max-width:none!important;vertical-align:top;opacity: 1;"
                         viewBox="0 0 {first_width} {first_height}" width="100%"></svg>
                    <section style="margin-left: {-(length + 3) * Base_Width}vw;display: inline-block;width: 100%;vertical-align: top;">
                        <section
                                style="display: flex;max-width: none !important;width: {(length + 2) * 100}%;transform: rotate(0deg);line-height: 0;">

    '''
    Value_Code = "100.1%"

    for i in range(length - 1):
        Value_Code += f";{(i + 1) * 100}%"

    code2 = f'''
                        <svg opacity="1"
                         style="display: inline-block; overflow: visible; vertical-align: top; opacity: 1; z-index: 300; min-width: 100%; transform: scale(1); isolation: isolate; max-width: none !important; visibility: visible;"
                         viewBox="0 0 {first_width} {first_height}" width="100%">
                        <animate attributeName="width" begin="0.2" calcMode="discrete" dur="2" end="click" fill="freeze"
                                 repeatCount="indefinite"
                                 values="{Value_Code}"></animate>
                        <g opacity="0" style="pointer-events:visible;">
                            <set attributeName="visibility" begin="click" dur="0.01s" fill="freeze" from="visible"
                                 restart="always" to="hidden"></set>
                            <animateTransform attributeName="transform" begin="click" calcMode="discrete" dur="1000s"
                                              fill="freeze" keyTimes="0;0.000001;1" restart="never" type="translate"
                                              values="0 0;-10000000 0;-10000000 0"></animateTransform>
                            <rect fill="#000000" height="100000000" opacity="1" style="pointer-events:visible;"
                                  width="1000000" x="-200000" y="-100000">
                                <animate attributeName="height" begin="click" calcMode="discrete" dur="0.0001s"
                                         fill="freeze" restart="never" to="0"></animate>
                            </rect>
                        </g>
                    </svg>

'''
    code3 = ''' <section data-mpa-powered-by="Open实验室" id="抽签"
         style="line-height: 0;margin: -1px auto;pointer-events: none;overflow: hidden;font-size: 0px;width: 88vw;user-select: none;visibility: visible;">
    <section style="display: flex; overflow: hidden; line-height: 0; flex-direction: column; visibility: visible;">
        <section style="height: 0px; visibility: visible;">
            <section draggable="true"
                     style="white-space: nowrap; width: 100%; margin: auto; overflow: hidden; pointer-events: none; font-size: 0px; visibility: visible;">
                <section style="display: flex; line-height: 0; visibility: visible;">
'''

    code4 = f''' </section>
            </section>
        </section>
</section></section>

        <svg viewBox="0 0 {first_width} {first_height}"></svg>
    </section>
</section> '''

    final_code = code3 + code2 + code1 + code + code4
    clipboard.copy(final_code)
    print('海报抽签代码已复制！')
    Log_Write('海报抽签代码已复制！')
    return final_code


# 第三标签页功能
def Get_FileEncode(html_file):
    # 读取文件内容
    with open(html_file, 'rb') as file:
        raw_data = file.read()

    # 检测文件编码方式

    encoding_result = chardet.detect(raw_data)
    file_encoding = encoding_result['encoding']
    return file_encoding


def Log_Write(contest):
    with open('log.txt', 'a') as file:
        file.write(current_time + ":" + contest + '\n')  # 写入日志文件
        print(current_time + ":" + contest)


img_heights = {}


# 更新图片高度，高度动画，并且将image替换为fo
def Update_Viewbox():
    file_encoding = Get_FileEncode("test.html")

    with open("test.html", 'r', encoding=file_encoding) as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    svg_tags = soup.select('svg[style*=background-image]')
    img_heights.clear()
    for svg in svg_tags:
        style = svg['style']
        # 使用正则表达式匹配图片URL，假设背景图片URL是在background-image: url("...")这种格式中
        match = re.search(r'background-image: url\("([^"]+)"\)', style)
        if match:
            img_url = match.group(1)  # 获取匹配到的图片URL
            before = svg['viewbox']
            if os.path.exists(img_url):
                image = Image.open(img_url)
                width = image.width
                height = image.height
                img_heights[img_url] = height
                # 这样读取到的每一个图片的高度都会被保存
                viewbox = svg['viewbox']
                if viewbox:
                    viewbox_values = viewbox.split(' ')
                    if len(viewbox_values) == 4:
                        viewbox_values[2] = str(width)
                        viewbox_values[3] = str(height)
                        svg['viewbox'] = ' '.join(viewbox_values)
                        after = svg['viewbox']
                        if before != after:
                            Log_Write(f"{img_url} 的viewBox由 {before} 更新为 {after}")
        else:
            # 如果没有匹配到，进行相应处理，比如记录日志提示无法获取图片URL等
            Log_Write(f"svg {svg} 的'style'属性中未找到有效的图片URL")

    with open("test.html", 'w', encoding='utf-8') as file:
        file.write(str(soup))
    # Update_Height()
    return img_heights


def Update_Height():
    file_encoding = Get_FileEncode("test.html")

    with open("test.html", 'r', encoding=file_encoding) as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    animate_elements = soup.find_all('animate', {'attributename': 'width'})

    if not os.path.exists('height_list.json'):
        return img_heights

    with open('height_list.json', 'r') as f:
        height_dict = json.load(f)

    for animate in animate_elements:
        # 获取id属性值中的数字
        id_list, id_num = animate['id'].split('-')
        # print(id_list, id_num)

        height_list = height_dict[id_list]
        # print(height_list, len(height_list))
        sum_height = 0
        first_height = 0
        # print('animate', animate)
        for i, img in enumerate(height_list):
            for items in img:
                sum_height += img_heights[items]

            if i == 0:
                first_height = sum_height
                # print('first height:', first_height)

            if i == int(id_num):
                new_proportion_start = sum_height / first_height * 100
                new_proportion_start = round(new_proportion_start, 2)
                values_list = animate['values'].split(';')
                before = float(values_list[0][:-1])
                values_list[0] = new_proportion_start
                new_values = ";".join(
                    [str(round(float(v.replace('%', '')) if isinstance(v, str) else v, 2)) + "%" for v in
                     values_list])
                animate['values'] = new_values
                if before != new_proportion_start:
                    print('animate width:', animate['id'], '的第一个值由', before, '更改为', new_proportion_start)
                    Log_Write('animate width:', animate['id'], '的第一个值由', before, '更改为', new_proportion_start)

            if i == int(id_num) + 1:
                new_proportion_end = sum_height / first_height * 100
                new_proportion_end = round(new_proportion_end, 2)
                values_list = animate['values'].split(';')
                before = float(values_list[1][:-1])
                values_list[1] = values_list[2] = new_proportion_end
                new_values = ";".join(
                    [str(round(float(v.replace('%', '')) if isinstance(v, str) else v, 2)) + "%" for v in
                     values_list])
                animate['values'] = new_values

                if before != new_proportion_end:
                    print('animate width:', animate['id'], '的第二、三个值由', before, '更改为', new_proportion_end)
                    Log_Write('animate width:', animate['id'], '的第二、三个值由', before, '更改为', new_proportion_end)
                continue

    with open("test.html", 'w', encoding='utf-8') as file:
        file.write(str(soup))

        # 写入日志文件
    Log_Write("全文高度更新完成")
    return img_heights


# 一个处理计算高度的函数
def height_proportion(image_lists, image_height, num):
    # 1、先计算每个列表的高度
    height_list = []

    for image_list in image_lists:
        sum_height = 0
        # 计算每个panel中图片的高度
        for image_name in image_list:
            if image_name in image_height:
                height = image_height[image_name]
                sum_height += height
                # print(f"{image_name}: {sum_height}")
            else:
                print(f"没有找到{image_name}，请重新查看！")
                Log_Write(f"没有找到{image_name}，请重新查看！")
        height_list.append(sum_height)

    # 2、计算每个动画的values 用字典对应起来
    height_values = {}
    sum_height = 0
    flag_num = 0
    for height_e in height_list:
        sum_height += height_e  # 累计高度
        # 3、计算比例
        height_proport = sum_height / height_list[0] * 100
        height_values[flag_num] = height_proport
        flag_num += 1
        # 计算出来的结果应当是{0：100，1：200，2：300...}

    # 生成代码 通过ID
    # 如果是多个伸长，需要有id来区分
    code_width = f'<svg id={num} style="max-width:none!important;" viewBox="0 0 345 {height_list[0]}">\n'
    click = 0
    for i in range(len(height_values) - 1):
        anim_str = f'<animate id="{num}-{i}" attributeName="width" fill="freeze" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1" restart="always" ' \
                   f'values="{height_values[i]}%;{height_values[i + 1]}%;{height_values[i + 1]}%" dur="1.5s" begin="{click}"></animate>\n'
        code_width += anim_str
        click += 2
    code_width += f'<rect x="0" y="0" width="100%" height="100%" style="pointer-events: visiblePainted;opacity:0;"><animate attributeName="height" fill="freeze" restart="never" calcMode="spline" keySplines="0.42 0 0.58 1.0; 0.42 0 0.58 1.0" keyTimes="0;0.0001;1" values="100%;0%;0%" dur="1000s" begin="click"></animate></rect></svg>'

    # return height_list
    pyperclip.copy(code_width)
    print('高度动画代码已复制')
    Log_Write('高度动画代码已复制')


class ImagePanel(tk.Frame):
    def __init__(self, master):
        self.panels = []
        self.count = 1
        self.panel_canvas = tk.Canvas(master)

        self.panel_frame = tk.Frame(self.panel_canvas)
        self.panel_scrollbar = tk.Scrollbar(master, orient=tk.VERTICAL, command=self.panel_canvas.yview)
        self.panel_canvas.configure(yscrollcommand=self.panel_scrollbar.set)
        self.panel_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.panel_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.panel_canvas.create_window((0, 0), window=self.panel_frame, anchor=tk.NW)
        self.panel_frame.bind("<Configure>", lambda event, canvas=self.panel_canvas: self.on_frame_configure(canvas))

        self.add_button = tk.Button(master, text="+", command=self.add_panel)
        self.add_button.pack(side=tk.TOP, padx=5, pady=5)

        self.num_entry = tk.Entry(master)
        self.num_entry.pack(side=tk.TOP, padx=5, pady=5)

        self.create_button = tk.Button(master, text="Create Function", command=self.create_function)
        self.create_button.pack(side="right", padx=5, pady=5)

    def add_panel(self, button=None):
        name = f"imgList{self.count}"
        panel = tk.Frame(self.panel_frame, name=name, bd=1, relief="raised")
        panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        label = tk.Label(panel, text=name)
        label.pack(side=tk.TOP, padx=5, pady=5)

        inner_panel = tk.Frame(panel)
        inner_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        browse_button = tk.Button(inner_panel, text="Browse", command=lambda: self.browse_images(inner_panel))
        browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        remove_button = tk.Button(inner_panel, text="Remove", command=lambda: self.remove_images(inner_panel))
        remove_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.panels.append(panel)
        self.count += 1

        # 如果传递了 button 参数，则将新的 "+" 按钮添加到这个 button 旁边
        # if button is not None:
        #     add_button.pack(in_=button.master, side=tk.RIGHT, padx=5, pady=5)

    def remove_panel(self, panel):
        self.panels.remove(panel)
        panel.destroy()

    def browse_images(self, panel):
        filetypes = (("Image Files", "*.jpg;*.png;*.gif;*jpeg"),)
        images = filedialog.askopenfilenames(filetypes=filetypes)
        for image in images:
            image_name = image.split("/")[-1]
            label = tk.Label(panel, text=image_name)
            label.pack(side=tk.TOP, padx=5, pady=5)

    def remove_images(self, panel):
        children = panel.winfo_children()
        for child in children:
            if isinstance(child, tk.Label):
                if child in children:
                    child.destroy()

    def create_function(self):
        # 存储所有面板的图片列表
        image_lists = []
        height_list = {}
        for panel in self.panels:
            panel_name = panel.winfo_name()
            # print(f"Panel: {panel_name}")
            panel_children = panel.winfo_children()
            image_list = []  # 存储当前面板的图片列表
            for child in panel_children:
                if isinstance(child, tk.Frame):
                    frame_children = child.winfo_children()
                    for frame_child in frame_children:
                        if isinstance(frame_child, tk.Label):
                            image_name = frame_child.cget("text")
                            image_list.append(image_name)
                            # print(f"    {image_name}")
            image_lists.append(image_list)

        # 输出所有面板的图片列表
        img_heights = Update_Viewbox()
        value = int(self.num_entry.get())
        height_list[value] = image_lists
        # print("img_heights",img_heights)
        # print('image_lists',image_lists)
        # print('height_list',height_list)
        height_proportion(image_lists, img_heights, value)
        # 保存到json

        # 检查文件是否存在
        if os.path.exists('height_list.json'):
            # 如果文件存在并且不为空，读取内容
            if os.path.getsize('height_list.json') > 0:
                with open('height_list.json', 'r') as f:
                    old_list = json.load(f)
            # 如果文件存在但为空，将空的字典写入文件
            else:
                with open('height_list.json', 'w') as f:
                    json.dump(height_list, f)
                    old_list = {}
        else:
            # 如果文件不存在，创建文件并将空的字典写入文件
            with open('height_list.json', 'w') as f:
                json.dump(height_list, f)
                print("创建json文件成功")
                old_list = {}

        old_list.update(height_list)

        with open('height_list.json', 'w') as f:
            json.dump(old_list, f)
            print("更新json文件成功")

    def on_frame_configure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))


# 字典用于保存图片的本地路径、哈希值和对应的网络链接
image_data = {}


def create_new_panel():
    new_window = tk.Toplevel(root)
    new_panel = ImagePanel(new_window)


# 读取本地的 image_data.json 文件并加载数据到 image_data 字典中
def load_image_data_from_file():
    image_data.clear()

    try:
        with open("image_data.json", 'r') as file:
            data = json.load(file)
            image_data.update(data)
    except (FileNotFoundError, json.JSONDecodeError):
        # 处理文件不存在或解析错误的情况
        pass


def save_image_data_to_file():
    with open("image_data.json", 'w') as file:
        json.dump(image_data, file, indent=4)


def calculate_hash(file_path):
    # 计算文件的哈希值
    with open(file_path, 'rb') as f:
        data = f.read()
        return hashlib.md5(data).hexdigest()


def upload_image(image_path):
    # 上传单张图片
    # 实现图片上传的代码逻辑
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type={grant_type}&appid={client_id}&secret={client_secret}"
    response = requests.get(token_url)
    access_token = response.json().get("access_token")
    errcode = response.json().get("errcode")
    errmsg = response.json().get("errmsg")

    # print("Access token: {}".format(access_token))
    # print("图片errcode: {}".format(errcode))
    # print("图片errmsg: {}".format(errmsg))

    if errcode or errmsg:
        Log_Write("上传图片errcode:" + str(errcode))
        Log_Write("上传图片errmsg:" + str(errmsg))
        Log_Write("请将您的ip地址写入微信开发接口白名单中！")
        return False

    image_url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}"

    files = {'media': open(image_path.strip('\'"'), 'rb')}
    response = requests.post(image_url, files=files)
    if response.status_code == 200:
        data = response.json()
        image_url = data.get('url')
        # print("image_url",image_url)

    return image_url


# 保存每个图片的链接到image_data.json中
def Get_List():
    with open("test.html", 'r', encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    svg_tags = soup.find_all('svg')
    load_image_data_from_file()
    for svg_tag in svg_tags:
        style_attr = svg_tag.get('style')
        if style_attr:
            match = re.search(r'background-image: url\("([^"]+)"\)', style_attr)
            if match:
                local_url = match.group(1)

                try:
                    local_hash = calculate_hash(local_url)
                    if local_url in image_data:
                        # 检查图片是否已上传且未更改过
                        if local_hash == image_data[local_url]['hash']:
                            pass
                        else:
                            image_url = upload_image(local_url)
                            # 保存图片数据到字典
                            image_data[local_url] = {'url': image_url, 'hash': local_hash}
                            save_image_data_to_file()
                            Log_Write(local_url + "已替换")
                    else:
                        image_url = upload_image(local_url)
                        if image_url:
                            # 保存图片数据到字典
                            image_data[local_url] = {'url': image_url, 'hash': local_hash}
                            save_image_data_to_file()
                            Log_Write(local_url + "已上传")
                        else:
                            Log_Write("图片链接为空，请检查ip地址是否正确以及图片大小是否小于10M！")
                except Exception as e:
                    Log_Write(local_url + "图片未找到")


# 将图片链接替换为网络链接，并保存到output.html中
def Output_List():
    load_image_data_from_file()
    file_encoding = Get_FileEncode("test.html")

    with open("test.html", 'r', encoding=file_encoding) as file:
        html_content = file.read()

    # 先替换img标签里src的相对路径
    for image_name, data in image_data.items():
        # print(image_name,data)
        if data["url"]:
            old_src_string = 'src="' + image_name
            new_src_string = 'src="' + data["url"]
            html_content = html_content.replace(old_src_string, new_src_string)
        else:
            print("请注意在image_data.json文件中",image_name,"路径是否不为null")
            Log_Write("请注意在image_data.json文件中",image_name,"路径是否不为null")

    # 再替换svg标签里background-image里的相对路径
    for image_name, data in image_data.items():
        if data["url"]:
            old_bg_string = 'background-image: url(&quot;' + image_name + '&quot;)'
            new_bg_string = 'background-image: url(&quot;' + data["url"] + '&quot;)'
            html_content = html_content.replace(old_bg_string, new_bg_string)
        else:
            print("请注意在image_data.json文件中",image_name,"路径是否不为null")
            Log_Write("请注意在image_data.json文件中",image_name,"路径是否不为null")

    soup = BeautifulSoup(html_content, 'html.parser')  # 解析HTML内容为Beautiful Soup对象

    # 将修改后的 SVG 内容写入输出文件
    with open("output.html", 'w', encoding=file_encoding) as file:
        file.write(html_content)
    Log_Write("成功更新网络链接保存在output.html文件中！")


# 在标签页中显示预览的信息，标题，摘要，作者

def Display_Draft():
    preview_path = "预览信息.json"
    title = ""
    author = ""
    digest = ""
    content = ""
    content_source_url = ""
    # 解析预览信息并提取相应数据
    if os.path.exists(preview_path):
        filencode = Get_FileEncode(preview_path)
        with open(preview_path, 'r', encoding=filencode) as file:
            articles_info = json.load(file)
            articles = articles_info.get("articles", [])
            if articles:
                # 提取表格数据、摘要和作者
                preview_info = articles[0]
                title = preview_info.get("title", "")
                author = preview_info.get("author", "")
                digest = preview_info.get("digest", "")
                content = preview_info.get("content", "")
                content_source_url = preview_info.get("content_source_url", "")

        # 在 tab4 中展示相应的数据
    title_label = ttk.Label(tab4, text="标题:")
    title_label.grid(row=0, column=0, sticky="e")
    title_text = ttk.Entry(tab4)
    title_text.grid(row=0, column=1)
    title_text.insert(0, title)

    author_label = ttk.Label(tab4, text="作者:")
    author_label.grid(row=1, column=0, sticky="e")
    author_text = ttk.Entry(tab4)
    author_text.grid(row=1, column=1)
    author_text.insert(0, author)

    digest_label = ttk.Label(tab4, text="摘要:")
    digest_label.grid(row=2, column=0, sticky="e")
    digest_text = ttk.Entry(tab4)
    digest_text.grid(row=2, column=1)
    digest_text.insert(0, digest)

    digest_label = ttk.Label(tab4, text="内容:")
    digest_label.grid(row=3, column=0, sticky="e")
    digest_text = ttk.Entry(tab4)
    digest_text.grid(row=3, column=1)
    digest_text.insert(0, content)

    digest_label = ttk.Label(tab4, text="阅读原文:")
    digest_label.grid(row=4, column=0, sticky="e")
    digest_text = ttk.Entry(tab4)
    digest_text.grid(row=4, column=1)
    digest_text.insert(0, content_source_url)


# 永久素材链接
def Upload_FM(file_path):
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type={grant_type}&appid={client_id}&secret={client_secret}"
    response = requests.get(token_url)
    access_token = response.json().get("access_token")
    errcode = response.json().get("errcode")
    errmsg = response.json().get("errmsg")
    if errcode or errmsg:
        Log_Write("上传图片errcode:" + str(errcode))
        Log_Write("上传图片errmsg:" + str(errmsg))
        Log_Write("请将您的ip地址写入微信开发接口白名单中！")
        return None

    # print("Access token: {}".format(access_token))
    # print("永久素材errcode: {}".format(errcode))
    # print("永久素材errmsg: {}".format(errmsg))

    upload_url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
    files = {'media': open(file_path, 'rb')}
    response = requests.post(upload_url, files=files)
    result = response.json()
    media_id = result.get("media_id")

    return media_id


# 获得封面id
def Get_FM_Id():
    # 弹出文件选择框，选择图片文件
    file_path = filedialog.askopenfilename(title="选择封面图片", filetypes=[("All Files", "*.*")])
    # 上传图片文件并获取永久素材的 media_id
    media_id = Upload_FM(file_path)
    FileEncode = Get_FileEncode('预览信息.json')
    if media_id:
        # 打开 JSON 文件并读取数据
        with open('预览信息.json', 'r', encoding=FileEncode) as file:
            data = json.load(file)

        data["articles"][0]["thumb_media_id"] = media_id
        with open('预览信息.json', 'w', encoding=FileEncode) as file:
            json.dump(data, file, indent=4)
        Log_Write("预览信息.json中的封面链接已修改！")
        # print(media_id)
        # Log_Write("图片media_id为", media_id)
        return media_id
    else:
        Log_Write("图片链接为空，请检查ip地址是否正确！")
        return None


def Create_Update_Draft():
    draft_info_path = "预览信息.json"
    draft_media_id = "草稿media_id.txt"
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type={grant_type}&appid={client_id}&secret={client_secret}"
    response = requests.get(token_url)
    access_token = response.json().get("access_token")
    errcode = response.json().get("errcode")
    errmsg = response.json().get("errmsg")

    # print("Access token: {}".format(access_token))
    print("草稿errcode: {}".format(errcode))
    print("草稿errmsg: {}".format(errmsg))

    if errcode or errmsg:
        Log_Write("草稿errcode:" + str(errcode))
        Log_Write("草稿errmsg:" + str(errmsg))
        Log_Write("请将您的ip地址写入微信开发接口白名单中！")
        return None

    url_create = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    url_update = f"https://api.weixin.qq.com/cgi-bin/draft/update?access_token={access_token}"

    if os.path.exists(draft_info_path):
        filecode = Get_FileEncode(draft_info_path)
        with open(draft_info_path, 'r', encoding=filecode) as file:
            data = json.load(file)
        # 获取文章对象列表
        articles = data.get('articles', [])

        # 检查是否存在文章对象并处理第一个对象
        if articles:
            # 获取第一个文章对象
            first_article = articles[0]
            # 从第一个文章对象中获取HTML文件路径
            content_path = first_article.get('content', '')

            # 读取HTML文件内容
            if content_path:
                with open(content_path, 'r', encoding='utf-8') as html_file:
                    html_content = html_file.read()
                html_content = html_content.replace('\n', '')
                # 更新第一个文章对象的content字段
                first_article['content'] = html_content
                # 修改草稿
                if os.path.exists(draft_media_id):
                    with open(draft_media_id, 'r', encoding='utf-8') as file:
                        media_id = file.read()

                    data = {
                        "media_id": media_id,
                        "index": 0,
                        "articles":
                            {
                                "title": first_article['title'],
                                "author": first_article['author'],
                                "digest": first_article['digest'],
                                "content": html_content,
                                "content_source_url": "",
                                "thumb_media_id": "QDbclvHclKPNR1QUhJ9a5KLuirimVpBG_hMjO1RYIczMECJUzd1WMaSWhleADUQ1",
                                "need_open_comment": 0,
                                "only_fans_can_comment": 0,
                                "pic_crop_235_1": "0_0_1_0.2987",
                                "pic_crop_1_1": "0_0.2987_1_1"
                            }
                    }
                    # print(html_content)

                    response = requests.post(url_update, json=data)
                    # 设置字符编码为utf-8
                    response.encoding = 'utf-8'
                    # print("response", response)
                    response_data = response.json()
                    # print("response_data", response_data)
                    if response.status_code == 200 and response_data["errcode"] == 0:
                        Log_Write("草稿更新成功！")
                    else:
                        Log_Write("草稿更新失败！")
                else:
                    # 创建文章对象
                    data = {
                        "articles": [
                            {
                                "title": first_article['title'],
                                "author": first_article['author'],
                                "digest": first_article['digest'],
                                "content": html_content,
                                "content_source_url": "",
                                "thumb_media_id": "QDbclvHclKPNR1QUhJ9a5KLuirimVpBG_hMjO1RYIczMECJUzd1WMaSWhleADUQ1",
                                "need_open_comment": 0,
                                "only_fans_can_comment": 0,
                                "pic_crop_235_1": "0_0_1_0.2987",
                                "pic_crop_1_1": "0_0.2987_1_1"
                            }
                        ]
                    }

                    response = requests.post(url_create, json=data)
                    # 设置字符编码为utf-8
                    response.encoding = 'utf-8'
                    # print("response", response)
                    response_data = response.json()
                    # print("response_data", response_data)

                    # 处理响应
                    if response.status_code == 200 and "errcode" not in response_data:
                        Log_Write("草稿上传成功")
                        media_id = response_data["media_id"]
                        # 保存 media_id 到本地
                        with open("草稿media_id.txt", "w") as file:
                            file.write(media_id)
                        Log_Write("草稿的media_id 已保存到本地。")
                    else:
                        Log_Write("草稿上传失败")

        else:
            Log_Write("未查到预览信息，请查看:预览信息.json！")

    else:
        Log_Write("请创建:预览信息.json！")


def Rotate_Images():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="选择照片", filetypes=(("All Files", "*.*"),))
    file_paths = root.tk.splitlist(file_paths)
    if file_paths:
        for image_path in file_paths:
            image = Image.open(image_path)
            rotated_image = image.rotate(-90, expand=True)
            rotated_image.save(image_path)
            print(f"{image_path}已旋转")

    else:
        print("没有选择任何照片。")


def Press_JPG():
    file_paths = filedialog.askopenfilenames(filetypes=[("All Files", "*.*")])

    for file_path in file_paths:
        image = Image.open(file_path)
        output_path = file_path[:-4] + ".JPG"

        if image.format == "PNG":
            jpg_image = image.convert("RGB")
            jpg_image.save(output_path, optimize=True, quality=85)
        elif image.format == "JPEG":
            image.save(output_path, optimize=True, quality=85)

        print(output_path, "压缩成功")


current_time = str((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M"))


def Update_Content():
    # 清空文本域内容
    text.delete("1.0", tk.END)

    # 读取日志文件内容
    with open('log.txt', 'r') as file:
        lines = file.readlines()
        # 将内容插入文本域中
        text.insert(tk.END, lines)

        # 滚动到最新内容的位置
    text.see(tk.END)

    text.configure(state="disabled")  # 设置文本域为只读状态


def execute_function():
    # 在这里调用你要执行的函数
    Update_Viewbox()
    time.sleep(1)
    Get_List()
    time.sleep(1)
    Output_List()
    time.sleep(1)
    Create_Update_Draft()
    Update_Content()


interval_ids = []  # 用于存储定时器的标识符


def start_execution():
    messagebox.showinfo("提示", "已开始自动更新，时间间隔为3小时一次。")
    execute_function_periodically()


def execute_function_periodically():
    execute_function()
    interval = 60 * 60 * 3  # 30分钟（单位：秒）
    interval_id = root.after(interval * 1000, execute_function_periodically)
    interval_ids.append(interval_id)


def stop_execution():
    for interval_id in interval_ids:
        root.after_cancel(interval_id)
    interval_ids.clear()
    messagebox.showinfo("提示", "已停止自动更新")


# 视频号
def Generate_VidoeCode(text, image_path):
    # 这里可以实现根据文本和图片路径生成代码的逻辑
    # 目前只是一个示例，实际应用中需根据具体需求进行实现
    code1 = '''
    < section
    id = "视频号" >
    < section
    style = "height:0;opacity:0" >
    < !--    下面这个svg的viewbox可在视频号偏上，位置不对应时调整。可将10往上调大 -->
    < svg
    viewBox = "0 0 1080 10" > < / svg >
    < section

    class ="channels_iframe_wrp custom_select_card_wrp" >

    < !--        这是视频号链接 -->


'''

    code2 = '''
    < / section >
    < / section >
    < !--        这是视频号封面，可修改为一个空的svg + 2
    个fo图 -->
    '''
    code3 = '''
    < / section > '''

    code = code1 + text.get(1.0, 'end-1c') + code2 + image_path + code3

    clipboard.copy(code)
    return code


# 尾缀
def Last_Line():
    code1 = '''
< section
powered - by = "wakeupandblock"
style = "line-height: 0;pointer-events: auto;" >
< section
style = "line-height: 0;height: 0;opacity: 0;pointer-events: none;" >
< svg
style = "pointer-events: none;"
viewBox = "0 0 345 359" > < / svg >
< section


class ="mp_profile_iframe_wrp" style="line-height: 0;pointer-events: auto;" >

< mp - common - profile


class ="js_uneditable custom_select_card mp_profile_iframe js_wx_tap_highlight mp_common_widget" data-alias="torraswx" data-biz_account_status="0" data-from ="0" data-headimg="http://mmbiz.qpic.cn/mmbiz_png/kDELV1BPfszMiaCxjhReIdwunjcAXSuD949bwFICNcFf6yqJAvGwaicXjJbZWjBWNBEiaQibYIwAKcrnVfFQGQgAGA/300?wx_fmt=png&amp;wxfrom=19" data-id="Mzg3MDg3MzY1OA==" data-index="0" data-is_biz_ban="0" data-isban="0" data-nickname="图拉斯" data-origin_num="54" data-pluginname="mpprofile" data-signature="Never Stop" > < / mp-common-profile >

< / section >
< / section >
< svg


class ="" data-fail="0" style="background-size: 100%; background-repeat: no-repeat; margin-top: -0.5vw; line-height: 0;" viewBox="0 0 345 589.375" > '''

    code2 = '''

< a
data - linktype = "2"
href = "https://www.xiaohongshu.com/user/profile/5faa3e1c000000000100a330"
name = "1 小红书"
style = "transform: scale(1);pointer-events: painted;height: 100%;width: 100%;display: block;"
target = "_blank" >
& nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp;
& nbsp;
< rect
height = "64.38"
style = "pointer-events:visible;opacity: 0;"
width = "140.61"
x = "26.35"
y = "88.84" > < / rect >
< / a > < a


class ="weapp_text_link js_weapp_entry wx_tap_link js_wx_tap_highlight" data-miniprogram-appid="wxe9385e53966beeeb" data-miniprogram-applink="#小程序://图拉斯/whrJSvhQBL6VISu" data-miniprogram-nickname="图拉斯官方商城" data-miniprogram-path="pages/home/dashboard/index" data-miniprogram-servicetype="" data-miniprogram-type="text" href="" style="font-size:17px;" >

< rect
height = "64.38"
style = "pointer-events:visible;opacity: 0;"
width = "140.61"
x = "174.97"
y = "89.84" > < / rect >
< / a > & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; < a
data - linktype = "2"
href = "http://qr61.cn/oq4qXI/qEuUPsr"
name = "3 视频号"
style = "transform: scale(1);pointer-events: painted;height: 100%;width: 100%;display: block;"
target = "_blank" >
& nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp;
< rect
height = "64.38"
style = "pointer-events:visible;opacity: 0;"
width = "140.61"
x = "24.11"
y = "172.82" > < / rect >
< / a > < a
data - linktype = "2"
href = "https://weibo.com/u/3925653034"
name = "4 微博"
style = "transform: scale(1);pointer-events: painted;height: 100%;width: 100%;display: block;"
target = "_blank" >
& nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp;
< rect
height = "64.38"
style = "pointer-events:visible;opacity: 0;"
width = "140.61"
x = "176.36"
y = "172.82" > < / rect >
< / a > < a
data - linktype = "2"
href = "https://www.torras.cn/"
name = "5 官网"
style = "transform: scale(1);pointer-events: painted;height: 100%;width: 100%;display: block;"
target = "_blank" >
& nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp; & nbsp;
< rect
height = "64.38"
style = "pointer-events:visible;opacity: 0;"
width = "284.15"
x = "29.43"
y = "256.75" > < / rect >
< / a > < / svg >
< / section > '''

    code = code1 + Fo_Image() + code2
    clipboard.copy(code)
    return code


# 创建主窗口
root = tk.Tk()
root.title("控制台")

# 创建标签页控件
notebook = ttk.Notebook(root)

# 第一个标签页
tab1 = ttk.Frame(notebook)

# 创建Canvas和Scrollbar
canvas = tk.Canvas(tab1)
scrollbar = ttk.Scrollbar(tab1, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 在scrollable_frame中创建按钮
button1 = ttk.Button(scrollable_frame, text="无缝图", command=No_Edge_Image)
button1.grid(row=0, column=0, padx=20, pady=20)
button2 = ttk.Button(scrollable_frame, text="fo图", command=Fo_Image)
button2.grid(row=1, column=0, padx=20, pady=20)
button3 = ttk.Button(scrollable_frame, text="序列帧", command=Se_Frames)
button3.grid(row=2, column=0, padx=20, pady=20)

button4 = ttk.Button(scrollable_frame, text="旋转图片", command=Rotate_Images)
button4.grid(row=0, column=1, padx=20, pady=20)
button5 = ttk.Button(scrollable_frame, text="压缩为jpg", command=Press_JPG)
button5.grid(row=1, column=1, padx=20, pady=20)

button2 = ttk.Button(scrollable_frame, text="图拉斯尾部版图", command=Last_Line)
button2.grid(row=0, column=2, padx=20, pady=20)


# button6 = ttk.Button(scrollable_frame, text="压缩透明背景", command=Press_PNG)
# button6.grid(row=2, column=1, padx=20, pady=20)
# button5 = ttk.Button(scrollable_frame, text="GIF第一帧", command=First_Frame)
# button5.grid(row=3, column=1, padx=20, pady=20)
# button6 = ttk.Button(scrollable_frame, text="GIF最后帧", command=Last_Frame)
# button6.grid(row=4, column=1, padx=20, pady=20)


# 鼠标滚轮事件处理程序
def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# 绑定鼠标滚轮事件到Canvas
canvas.bind_all("<MouseWheel>", on_mousewheel)

# 将标签页添加到notebook中
notebook.add(tab1, text="基础功能")
# 第二个标签页
tab6 = ttk.Frame(notebook)
# 创建文本输入框
text_entry = tk.Text(tab6, height=5, width=50)
text_entry.insert(tk.END, "输入视频号<mp-common-videosnap>")
text_entry.grid(row=0, column=0, padx=20, pady=20)

# 创建生成代码按钮
generate_button = ttk.Button(tab6, text="生成视频号代码",
                             command=lambda: Generate_VidoeCode(text_entry, No_Edge_Image()))
generate_button.grid(row=2, column=0, padx=20, pady=20)
notebook.add(tab6, text="视频号生成")

# 第二个标签页
tab2 = ttk.Frame(notebook)
button3 = ttk.Button(tab2, text="滑动容器", command=Auto_HuaDong)
button3.grid(row=0, column=0, padx=20, pady=20)
button3 = ttk.Button(tab2, text="多张渐变", command=Mul_Opcaity)
button3.grid(row=0, column=1, padx=20, pady=20)
button3 = ttk.Button(tab2, text="宽度动画", command=create_new_panel)
button3.grid(row=1, column=0, padx=20, pady=20)
button3 = ttk.Button(tab2, text="抽签海报", command=Lottery)
button3.grid(row=1, column=1, padx=20, pady=20)
notebook.add(tab2, text="效果生成")

# 第4个标签页
tab4 = ttk.Frame(notebook)
Display_Draft()

button3 = ttk.Button(tab4, text="更新高度", command=Update_Viewbox)
button3.grid(row=7, column=0, padx=20, pady=20)
button3 = ttk.Button(tab4, text="上传链接", command=Get_List)
button3.grid(row=8, column=0, padx=20, pady=20)
button3 = ttk.Button(tab4, text="输出output.html", command=Output_List)
button3.grid(row=9, column=0, padx=20, pady=20)
button3 = ttk.Button(tab4, text="新建/更新草稿", command=Create_Update_Draft)
button3.grid(row=10, column=0, padx=20, pady=20)
button3 = ttk.Button(tab4, text="修改封面", command=Get_FM_Id)
button3.grid(row=7, column=1, padx=20, pady=20)

notebook.add(tab4, text="网络功能")

# 第5个标签页
tab5 = ttk.Frame(notebook)

style = ttk.Style()
style.configure("Custom.TButton", foreground="black", font=("Helvetica", 12))
container = ttk.Frame(tab5)
container.pack(fill="both", expand=True)

buttons_frame = ttk.Frame(container)
buttons_frame.pack(side="left", fill="y")

content_frame = ttk.Frame(container)
content_frame.pack(side="right", fill="both", expand=True)
# 创建按钮
start_button = tk.Button(container, text="开始执行", command=start_execution)
start_button.pack()

stop_button = tk.Button(container, text="停止执行", command=stop_execution)
stop_button.pack()

# button = ttk.Button(container, text="更新日志", command=Update_Content)
# button.pack()

text = tk.Text(content_frame)
text.pack(padx=20, pady=20, fill="both", expand=True)
notebook.add(tab5, text="自动化")

# 将标签页控件放置在主窗口中
notebook.pack(expand=True, fill="both")

# 运行主循环
root.mainloop()
