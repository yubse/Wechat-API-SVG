import os
import tkinter as tk
from tkinter import filedialog
import moviepy.editor as mp
import pyperclip
from PIL import Image, ImageTk
from moviepy.video.fx.crop import crop
import imageio
from moviepy.video.io.VideoFileClip import VideoFileClip


# 视频转GIF
class VideoToGifConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("Video to GIF Converter")

        # 创建面板
        self.panel = tk.Frame(self.master)
        self.panel.pack()

        # 创建输入框和标签
        self.start_label = tk.Label(self.panel, text="开始秒数: ")
        self.start_label.grid(row=0, column=0, padx=10, pady=10)
        self.start_entry = tk.Entry(self.panel)
        self.start_entry.grid(row=0, column=1, padx=10, pady=10)

        self.end_label = tk.Label(self.panel, text="结束秒数: ")
        self.end_label.grid(row=1, column=0, padx=10, pady=10)
        self.end_entry = tk.Entry(self.panel)
        self.end_entry.grid(row=1, column=1, padx=10, pady=10)

        self.loop_label = tk.Label(self.panel, text="循环次数(0为无限循环): ")
        self.loop_label.grid(row=4, column=0, padx=10, pady=10)
        self.loop_var = tk.StringVar(value="0")
        self.loop_menu = tk.OptionMenu(self.panel, self.loop_var, "1", "2", "0")
        self.loop_menu.grid(row=4, column=1, padx=10, pady=10)

        # 创建帧数控件
        self.fps_label = tk.Label(self.panel, text="帧数: ")
        self.fps_label.grid(row=2, column=0, padx=10, pady=10)
        self.fps_entry = tk.StringVar(value="15.0")
        self.fps_entry_ = tk.Entry(self.panel, textvariable=self.fps_entry)
        self.fps_entry_.grid(row=2, column=1, padx=10, pady=10)

        # 创建GIF大小
        self.ratio_label = tk.Label(self.panel, text="新宽度: ")
        self.ratio_label.grid(row=3, column=0, padx=10, pady=10)
        self.ratio_entry = tk.StringVar(value="800")
        self.ratio_entry_ = tk.Entry(self.panel, textvariable=self.ratio_entry)
        self.ratio_entry_.grid(row=3, column=1, padx=10, pady=10)

        # 创建选择文件按钮
        self.file_button = tk.Button(self.panel, text="选择视频", command=self.choose_file)
        self.file_button.grid(row=5, column=0, padx=10, pady=10)

        # 创建转换按钮
        self.convert_button = tk.Button(self.panel, text="转为GIF", command=self.convert)
        self.convert_button.grid(row=5, column=1, padx=10, pady=10)

    def choose_file(self):
        # 弹出文件选择对话框
        file_path = filedialog.askopenfilename()
        video=VideoFileClip(file_path)
        duration=video.duration
        self.width,self.height=video.size

        if self.start_entry.get() == '':
            self.start_entry.insert(0, str(0))  # 设置新文本
        if self.end_entry.get() == '':
            self.end_entry.insert(0, str(duration))  # 设置新文本
        self.file_button.config(text=file_path)

    def convert(self):
        # 获取文件路径和转换参数
        file_path = self.file_button.cget("text")
        start_time = float(self.start_entry.get())
        end_time = float(self.end_entry.get())
        fps = float(self.fps_entry.get())
        ratio = float(self.ratio_entry.get())
        loop = int(self.loop_var.get())

        # 使用 MoviePy 库将视频剪辑为 GIF
        clip = mp.VideoFileClip(file_path).subclip(start_time, end_time)
        if loop == 0:
            # 设置为无限循环
            loop = -1

        folder_path = filedialog.askdirectory()
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        gif_path = os.path.join(folder_path, file_name + ".gif")

        ratio_=ratio/self.width
        clip = clip.resize(ratio_)
        clip.write_gif(gif_path, fps=fps, loop=loop,colors=256)

        # 获取导出的 GIF 文件的大小
        gif_size = os.path.getsize(gif_path)

        gif_size_kb = gif_size / (1024 * 1024)
        print("GIF file size:", gif_size_kb, "MB")


# 按钮函数调用区
def VideoToGif():
    new_window = tk.Toplevel(root)
    new_panel = VideoToGifConverter(new_window)


# 导出gif最后一帧函数
def extract_last_frame():
    # 弹出文件选择对话框，允许选择多个文件
    file_paths = filedialog.askopenfilenames(filetypes=[("GIF files", "*.gif")])
    if file_paths:
        # 弹出文件夹选择对话框，确定导出文件夹
        folder_path = filedialog.askdirectory()
        if folder_path:
            for file_path in file_paths:
                # 打开 GIF 文件并提取最后一帧
                with Image.open(file_path) as im:
                    last_frame = im.seek(im.n_frames - 1)
                    last_frame = im.convert("RGBA")

                # 获取文件名（不包括扩展名）
                file_name = os.path.splitext(os.path.basename(file_path))[0]

                # 将最后一帧保存为 PNG 文件
                output_path = os.path.join(folder_path, file_name + "最后一帧.png")
                last_frame.save(output_path)
                print(file_name, "最后一帧导出成功")
# 导出gif第一帧函数
def first_frame():
    # 弹出文件选择对话框，允许选择多个文件
    file_paths = filedialog.askopenfilenames(filetypes=[("GIF files", "*.gif")])
    if file_paths:
        # 弹出文件夹选择对话框，确定导出文件夹
        folder_path = filedialog.askdirectory()
        if folder_path:
            for file_path in file_paths:
                # 打开 GIF 文件并提取最后一帧
                with Image.open(file_path) as im:
                    last_frame = im.seek(0)
                    last_frame = im.convert("RGBA")

                # 获取文件名（不包括扩展名）
                file_name = os.path.splitext(os.path.basename(file_path))[0]

                # 将最后一帧保存为 PNG 文件
                output_path = os.path.join(folder_path, file_name + "第一帧.png")
                last_frame.save(output_path)
                print(file_name, "第一帧导出成功")

# from PIL import Image
#
# # 打开GIF文件
# with Image.open('example.gif') as im:
#     # 将第一帧转换为图像对象并保存为PNG
#     im.save('first_frame.png', format='PNG', save_all=True, append_images=im.seek(0))

# 计算中心点函数
def calculate_transform_origin():
    top = tk.Toplevel(root)
    # 弹出文件选择对话框，选择照片
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    # 获取文件名（不包括扩展名）
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    if file_path:
        # 打开照片并创建 PhotoImage 对象
        with Image.open(file_path) as im:
            im = im.resize((im.width // 3, im.height // 3))

            # 创建新面板
            panel_ = tk.Frame(top)
            panel_.pack()

            photo = ImageTk.PhotoImage(im)

            # 在面板上显示照片
            label = tk.Label(panel_, image=photo)
            label.image = photo
            label.grid(row=0, column=0)

        # 为标签绑定鼠标单击事件
        def on_click(event):
            # 计算 transform-orgin 点的坐标
            x, y = event.x, event.y
            width, height = label.winfo_width(), label.winfo_height()
            origin_x = x / width * 100
            origin_y = y / height * 100
            code_transformOrgin = '''<g id="{id}" transform-origin="{x:.2f}% {y:.2f}%" style="visibility: visible;">
    <animateTransform attributeName="transform" type="scale" values="1;1.3;1" repeatCount="indefinite" dur="2s"
        restart="never" fill="freeze" additive="sum" begin="0"></animateTransform>
        </g>
            '''
            code_transformOrgin = code_transformOrgin.format(x=origin_x, y=origin_y, id=file_name)
            print(code_transformOrgin)
            pyperclip.copy(code_transformOrgin)
            print("已粘贴代码至剪切")

        label.bind("<Button-1>", on_click)



def func4():
    print("Button 4 was clicked!")


# 创建主窗口
root = tk.Tk()

# 创建面板
panel = tk.Frame(root)
panel.pack()

# 创建按钮，并使用 grid() 方法将其放置在面板中
button1 = tk.Button(panel, text="视频转gif", command=VideoToGif)
button1.grid(row=0, column=0, padx=10, pady=10)

button2 = tk.Button(panel, text="导出GIF最后一帧", command=extract_last_frame)
button2.grid(row=1, column=0, padx=10, pady=10)
button5 = tk.Button(panel, text="导出GIF第一帧", command=first_frame)
button5.grid(row=2, column=0, padx=10, pady=10)

button3 = tk.Button(panel, text="中心点计算", command=calculate_transform_origin)
button3.grid(row=0, column=1, padx=10, pady=10)

button4 = tk.Button(panel, text="button", command=func4)
button4.grid(row=0, column=2, padx=10, pady=10)

# 运行主循环
root.mainloop()
