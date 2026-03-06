import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import os
import threading


def sanitize_filename(name):
    # 替换非法字符
    return re.sub(r'[\\/:*?"<>|]', '_', name)


class WeChatImageDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("微信公众号图片下载器")
        self.root.geometry("800x600")
        self.create_widgets()
        self.images = []

    def create_widgets(self):
        # 输入框和确认按钮
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, fill=tk.X)
        self.url_entry = ttk.Entry(input_frame, width=70)
        self.url_entry.pack(side=tk.LEFT, padx=5)
        self.confirm_btn = ttk.Button(input_frame, text="确认", command=self.fetch_images)
        self.confirm_btn.pack(side=tk.LEFT)

        # 操作按钮
        operation_frame = ttk.Frame(self.root)
        operation_frame.pack(pady=5, fill=tk.X)
        self.select_all_btn = ttk.Button(operation_frame, text="全选", command=self.select_all)
        self.select_all_btn.pack(side=tk.LEFT)
        self.download_btn = ttk.Button(operation_frame, text="下载", command=self.download_images)
        self.download_btn.pack(side=tk.RIGHT)

        # 图片展示区域
        self.canvas = tk.Canvas(self.root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def fetch_images(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("警告", "请输入公众号文章链接")
            return

        self.images = []
        self.frame.destroy()
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")

        self.download_thread = threading.Thread(target=self.download_image_urls, args=(url,))
        self.download_thread.start()

    def download_image_urls(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all(['img', 'svg'])

            for tag in img_tags:
                # 处理 img 标签
                if tag.name == 'img':
                    img_url = tag.get('data-src') or tag.get('src') or tag.get('data-lazy-src')

                # 处理 svg 标签
                elif tag.name == 'svg':
                    style = tag.get('style', '')
                    # 从 style 属性中提取 url
                    start = style.find('url(') + 5
                    end = style.find(')', start)
                    if start != -1 and end != -1:
                        img_url = style[start:end].strip('"; ')

                    # 从 data-lazy-bgimg 属性中提取 url
                    if not img_url:
                        img_url = tag.get('data-lazy-bgimg')

                # 验证并添加到图片列表
                if img_url and img_url.startswith('http'):
                    self.images.append(img_url)

            self.root.after(0, self.show_images)
        except Exception as e:
            messagebox.showerror("错误", f"获取图片链接失败: {e}")

    def show_images(self):
        for img_url in self.images:
            try:
                response = requests.get(img_url, timeout=10)
                if response.status_code == 200:
                    img_data = response.content
                    img = tk.PhotoImage(data=img_data)
                    label = ttk.Label(self.frame, image=img)
                    label.image = img
                    label.pack(side="top", fill="none", expand=True)
            except Exception as e:
                print(f"Error loading image {img_url}: {e}")
        self.root.update_idletasks()

    def select_all(self):
        for widget in self.frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.select()

    def download_images(self):
        selected_indices = [i for i, widget in enumerate(self.frame.winfo_children()) if isinstance(widget, ttk.Label) and widget.cget('selected')]
        if not selected_indices:
            messagebox.showwarning("警告", "请至少选择一张图片")
            return

        folder = filedialog.askdirectory(title="选择保存图片的文件夹")
        if not folder:
            return

        for idx, index in enumerate(selected_indices, 1):
            img_url = self.images[index]
            try:
                response = requests.get(img_url, timeout=10)
                if response.status_code == 200:
                    img_name = f"image_{idx:03d}.jpg"
                    img_name = sanitize_filename(img_name)
                    with open(os.path.join(folder, img_name), "wb") as f:
                        f.write(response.content)
            except Exception as e:
                print(f"Error downloading image {img_url}: {e}")
        messagebox.showinfo("完成", "图片下载完成")


if __name__ == "__main__":
    root = tk.Tk()
    app = WeChatImageDownloader(root)
    root.mainloop()


