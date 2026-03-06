from bs4 import BeautifulSoup

# 读取HTML文件
with open('test1.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 解析HTML内容
soup = BeautifulSoup(html_content, 'html.parser')

# 遍历所有的img标签
for img in soup.find_all('img'):
    # 获取图片的src属性
    src = img.get('src')
    # 获取图片的data-w和data-h属性
    width = img.get('data-w')
    height = img.get('data-h')

    # 创建新的svg标签
    svg = soup.new_tag('svg')
    svg['style'] = f"background-image: url(\"{src}\");background-size: 100%;background-repeat: no-repeat;margin-top:-0vw;line-height: 0;"
    svg['viewBox'] = f"0 0 {width} {height}"

    # 用svg标签替换img标签
    img.replace_with(svg)

# 将修改后的HTML内容写回文件
with open('test1.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

print("替换完成，新文件名为 1 - 副本 (2)_modified.html")