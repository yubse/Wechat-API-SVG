import requests
import re
from bs4 import BeautifulSoup

# # 恣伏
# client_id = "wx00c3b7d9db7553a0"
# client_secret = "cc793a572170ea90746d68d6944f2e89"
# grant_type = "client_credential"

# 宋荣子
client_id = "wx772b83593792d05d"
client_secret = "ebd08472eb399be190686975b02485ba"
grant_type = "client_credential"

# 获得access_token
def get_access_token():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type={grant_type}&appid={client_id}&secret={client_secret}"
    response = requests.get(token_url)
    access_token = response.json().get("access_token")
    errcode = response.json().get("errcode")
    errmsg = response.json().get("errmsg")

    print("Access token: {}".format(access_token))
    print("errcode: {}".format(errcode))
    print("errmsg: {}".format(errmsg))
    return access_token

# 上传到微信后台，获得网络链接
def upload_images(image_path):
    access_token=get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}"

    files = {'media': open(image_path.strip('\'"'), 'rb')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        data = response.json()
        image_url = data.get('url')
        print("image_url",image_url)
        return image_url

# 在html中查找本地图片链接，并替换
def replace_image_urls(html_file,output_file):
    with open(html_file, 'r',encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    # 查找所有的 < svg > 标签
    svg_tags = soup.find_all('svg')

    for svg_tag in svg_tags:
        # 获取原始的本地图片链接
        style_attr = svg_tag.get('style')
        if style_attr:
            # 提取背景图像链接（本地链接）
            match = re.search(r'background-image: url\("([^"]+)"\)', style_attr)
            if match:
                local_url = match.group(1)
                # 使用 upload_images 函数将本地链接上传并获取网络链接
                new_url = upload_images(local_url)  # 替换为实际的上传函数以及返回的网络链接变量名
                print("new_url: " + new_url)

                # 替换本地链接为网络链接
                new_style_attr = style_attr.replace(local_url, new_url)
                svg_tag['style'] = new_style_attr
                print(local_url,"成功替换为",new_url)

    # 将修改后的 SVG 内容写入输出文件
            with open(output_file, 'w') as file:
                file.write(str(soup))


# 示例用法
# 源代码文件
html_file= "test1.html"
# 输出代码文件
output_file = 'modified.html'
replace_image_urls(html_file,output_file)
