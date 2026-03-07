import tkinter as tk
from tkinter import filedialog

import pyperclip
from PIL import ImageTk, Image
import os

global whole_code


def partial_code(i, rect_now, rect_list, image):
    print("rect_list", rect_list)
    print("image", image)
    width = 0
    sum_height = 0
    image_svg_whole = ""
    for file_path in image:
        image = Image.open(file_path)
        width, height = image.size
        sum_height = height + sum_height
        image_svg = '''                        <svg data-copyright="微信公众号:恣伏"
                                     style="-webkit-user-select:none;-webkit-user-select:none;background-image: url(&quot;{}&quot;);background-size: 100%;background-repeat: no-repeat;display: inline;line-height: 0;"
                                     viewBox="0 0 {} {}"></svg>
        '''.format(file_path, width, height)
        image_svg_whole += image_svg
        print("宽度:", width)
        print("总高度", sum_height)
    part5 = '''        
    <section
                style="overflow: visible; display: block; line-height: 0 !important; visibility: visible;">
            <section
                    style="line-height: 0;visibility: visible;">
''' + image_svg_whole + '''            </section>
        </section>
'''
    part1 = '''
                <g opacity="0" pointer-events="visible">
                    <animateTransform attributeName="transform" attributeType="XML" begin="touchstart" dur="1000s"
                                      fill="freeze" keyTimes="0;0.0003;0.00031;1" restart="always" type="translate"
                                      values="1080 0;1080 0;0 0;0 0"></animateTransform>
    ''' + rect_now + '''
                        <g transform="translate(1080 0)">
                        <animateTransform attributeName="transform" begin="touchstart" dur="0.31s" fill="remove"
                                          restart="always" type="translate" values="100000;100000"></animateTransform>
'''
    code_list_sum = ""
    for rect in rect_list:
        print("rect", rect)
        code_list_sum += rect

    part3 = '''
        <section id={} style="height: 0;">
        <section>
            <svg preserveAspectRatio="xMidYMin slice" style="width: 100%;overflow: visible;min-height: 1px !important;"
                 viewBox="0 0 {} {}">
'''.format(++i,width, sum_height)
    part4 = '''
                        </g>
                    <animateTransform attributeName="transform" attributeType="XML" begin="click+0.31s" dur="1000s"
                                      fill="freeze" restart="always" type="translate"
                                      values="-1080 0"></animateTransform>
                    <animateTransform attributeName="transform" attributeType="XML" begin="touchstart" dur="1000s"
                                      fill="freeze" keyTimes="0;0.0003;0.00031;1" restart="always" type="translate"
                                      values="-1080 0;-1080 0;0 0;0 0"></animateTransform>
                    <animateTransform attributeName="transform" attributeType="XML" begin="touchmove" dur="1000s"
                                      fill="freeze" restart="always" type="translate"
                                      values="-1080 0"></animateTransform>
                </g>
                <animate additive="replace" attributeName="height" attributeType="css" begin="click" dur="0.001"
                         fill="freeze" restart="always" values="1"></animate>
                <animate additive="replace" attributeName="height" attributeType="css" begin="touchstart" dur="1000s"
                         fill="freeze" keyTimes="0;0.0003;0.00031;1" restart="always" values="1;1;100%;100%"></animate>
                <animate additive="replace" attributeName="height" attributeType="css" begin="touchmove" dur="0.001"
                         fill="freeze" restart="always" values="1"></animate>
                <animate attributeName="opacity" attributeType="css" begin="click+0.31s" dur="0.001" fill="freeze"
                         restart="always" values="0"></animate>
                <animate attributeName="opacity" attributeType="css" begin="touchstart" dur="1000s" fill="freeze"
                         keyTimes="0;0.0003;0.00031;1" restart="always" values="0;0;1;1"></animate>
                <animate attributeName="opacity" attributeType="css" begin="touchmove" dur="0.001" fill="freeze"
                         restart="always" values="0"></animate>
            </svg>
        </section>

    '''
    part6 = part3 + part1 + code_list_sum + part4 + part5 + "</section>"

    return part6, width, sum_height


def select_image(index):
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        selected_images[index] = list(file_paths)
        image_names = [os.path.basename(file_path) for file_path in file_paths]
        select_buttons[index].configure(text=", ".join(image_names))
        image_labels[index].configure(text=", ".join(image_names))
        print("选择的图片名称:", ", ".join(image_names))
        for file_path in file_paths:
            image = Image.open(file_path)
            width, height = image.size
            # print("图片路径:", file_path)
            # print("宽度:", width)
            # print("高度:", height)
        # total_height = sum(
        #     [Image.open(file_path).height for image_paths in selected_images for file_path in image_paths])


def generate_code():
    part_sum = ""
    width = 0
    sum_height = 0
    for i in range(len(entries)):
        rect_list = []
        print("当前输入框内容：", entries[i].get())
        # print("当前选择图片名称：", ", ".join([os.path.basename(file_path) for file_path in selected_images[i]]))
        image_names = [os.path.basename(file_path) for file_path in selected_images[i]]
        for j in range(len(entries)):
            if i != j:
                rect_list.append(entries[j].get())
                # print(entries[j].get())

        part_code, width, sum_height = partial_code(i, entries[i].get(), rect_list, image_names)
        part_sum += part_code
        # print(partial_code(i, entries[i].get(), rect_list, selected_images[i]))

    part1 = '''
    <section style="overflow: hidden;pointer-events: none;line-height: 0;font-size: 0px;visibility: visible;">
        <section style="height: 0px;visibility: visible;">
        <section style="visibility: visible;">
            <svg preserveAspectRatio="xMidYMin slice"
                 style="width: 100%;overflow: visible;min-height: 1px !important;visibility: visible;"
                 viewBox="0 0 {} {}">
                <g opacity="0" pointer-events="visible">
                    <g transform="translate(1080 0)">
                        <animateTransform attributeName="transform" begin="touchstart" dur="0.31s" fill="remove"
                                          restart="always" type="translate" values="100000;100000"></animateTransform>
'''.format(width, sum_height)

    part2 = ""
    for i in range(len(entries)):
        part2 += entries[i].get()

    part3 = '''
                        </g>
                    <animateTransform attributeName="transform" attributeType="XML" begin="0.1s" dur="1000s"
                                      fill="freeze" restart="always" type="translate"
                                      values="-1080 0"></animateTransform>
                    <animateTransform attributeName="transform" attributeType="XML" begin="click+0.31s" dur="1000s"
                                      fill="freeze" restart="always" type="translate"
                                      values="-1080 0"></animateTransform>
                    <animateTransform attributeName="transform" attributeType="XML" begin="touchstart" dur="1000s"
                                      fill="freeze" keyTimes="0;0.0003;0.00031;1" restart="always" type="translate"
                                      values="-1080 0;-1080 0;0 0;0 0"></animateTransform>
                    <animateTransform attributeName="transform" attributeType="XML" begin="touchmove" dur="1000s"
                                      fill="freeze" restart="always" type="translate"
                                      values="-1080 0"></animateTransform>
                </g>
                <animate additive="replace" attributeName="height" attributeType="css" begin="click" dur="0.001"
                         fill="freeze" restart="always" values="1"></animate>
                <animate additive="replace" attributeName="height" attributeType="css" begin="0.1s" dur="0.001"
                         fill="freeze" restart="always" values="1"></animate>
                <animate additive="replace" attributeName="height" attributeType="css" begin="touchstart" dur="1000s"
                         fill="freeze" keyTimes="0;0.0003;0.00031;1" restart="always" values="1;1;100%;100%"></animate>
                <animate additive="replace" attributeName="height" attributeType="css" begin="touchmove" dur="0.001"
                         fill="freeze" restart="always" values="1"></animate>
                <animate attributeName="opacity" attributeType="css" begin="click+0.31s" dur="0.001" fill="freeze"
                         restart="always" values="0"></animate>
                <animate attributeName="opacity" attributeType="css" begin="0.1s" dur="0.001" fill="freeze"
                         restart="always" values="0"></animate>
                <animate attributeName="opacity" attributeType="css" begin="touchstart" dur="1000s" fill="freeze"
                         keyTimes="0;0.0003;0.00031;1" restart="always" values="0;0;1;1"></animate>
                <animate attributeName="opacity" attributeType="css" begin="touchmove" dur="0.001" fill="freeze"
                         restart="always" values="0"></animate>
            </svg>
        </section>
'''
    image_name = ", ".join([os.path.basename(file_path) for file_path in selected_images[0]])
    part4 = '''
    <svg data-copyright="微信公众号:恣伏" style="-webkit-user-select:none;-webkit-user-select:none;background-image: url(&quot;{}&quot;);background-size: 100%;background-repeat: no-repeat;display: inline;line-height: 0;"
                                     viewBox="0 0 {} {}"></svg>'''.format(image_name, width, sum_height) + "</section>"
    part6=''' <svg viewBox="0 0 {} {}"></svg>'''.format(width, sum_height) + "</section>"

    part_whole=part1+part2+part3+part4+part_sum+part6
    print(part_whole)
    pyperclip.copy(part_whole)
    print("成功复制到剪切板")


def add_entry():
    entry_frame = tk.Frame(root)
    entry_frame.pack()

    entry = tk.Entry(entry_frame)
    entry.pack(side=tk.LEFT)
    entries.append(entry)

    image_label = tk.Label(entry_frame)
    image_label.pack(side=tk.LEFT)
    image_labels.append(image_label)

    select_button = tk.Button(entry_frame, text="选择图片")
    select_button.configure(command=lambda index=len(select_buttons): select_image(index))
    select_button.pack(side=tk.LEFT)
    select_buttons.append(select_button)
    selected_images.append([])  # 添加一个空列表，表示尚未选择图片


root = tk.Tk()
root.geometry("300x300")  # 设置窗口大小

entries = []
image_labels = []
select_buttons = []
selected_images = []

# 创建四个输入框和选择图片按钮
for _ in range(3):
    entry_frame = tk.Frame(root)
    entry_frame.pack()

    entry = tk.Entry(entry_frame)
    entry.pack(side=tk.LEFT)
    entries.append(entry)

    image_label = tk.Label(entry_frame)
    image_label.pack(side=tk.LEFT)
    image_labels.append(image_label)

    select_button = tk.Button(entry_frame, text="选择图片")
    select_button.configure(command=lambda index=len(select_buttons): select_image(index))
    select_button.pack(side=tk.LEFT)
    select_buttons.append(select_button)
    selected_images.append([])  # 添加一个空列表，表示尚未选择图片

# 创建添加输入框和选择图片按钮的按钮
add_button = tk.Button(root, text="+", command=add_entry)
add_button.pack(side=tk.BOTTOM, pady=10)

# 创建生成代码的按钮
generate_button = tk.Button(root, text="生成代码", command=generate_code)
generate_button.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
