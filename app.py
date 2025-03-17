from DrissionPage import ChromiumPage, ChromiumOptions
import time
import os
from flask import Flask, request, render_template
import re
import html
import time
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'url' in request.form:
            url = request.form['url']
            url = url.split(' ',1)[0]
            return load_from_url(url)
    
    return render_template('index.html')



def load_from_url(url):
    """
    爬取今日头条文章内容
    :param url: 文章URL
    :return: 文章标题、内容和图片URL列表
    """
    # 创建配置对象
    options = ChromiumOptions()
    options.set_argument('--headless=new')  # 使用新的无头模式
    options.set_argument('--no-sandbox')    # 在Linux系统中添加此参数
    options.set_argument('--disable-dev-shm-usage')  # 避免内存不足问题
    
    # 使用配置创建页面对象
    page = ChromiumPage(options)
    print("已启动无头浏览器...")
    
    try:
        # 访问文章页面
        page.get(url)
        print("正在加载页面...")
        time.sleep(2)  # 等待页面加载
        
        # 获取文章标题
        title = page.ele('xpath://h1').text
        print(f"文章标题: {title}")
        
        # 获取文章内容，排除 pgc-img 标签及其子节点
        content = ''.join([
            ele.text 
            for ele in page.eles('xpath://article//node()[not(ancestor-or-self::div[@class="pgc-img"])]')
        ])
        

        # 尝试找到并点击"点开展开剩余.."按钮
        try:
            # 使用 contains() 函数匹配包含特定文本的按钮
            more_button = page.ele('xpath://*[contains(text(), "点击展开剩余")]')
            more_button.click()
            print("已点击展开更多按钮")
            time.sleep(2)  # 等待内容加载
        except Exception as e:
            print(f"未找到展开更多按钮或点击失败: {e}")

        
        time.sleep(2)

        # 滚动页面以触发懒加载
        page.scroll.down()
        time.sleep(2)  # 等待图片加载

        # 滚动页面以触发懒加载
        page.scroll.down()
        time.sleep(2)  # 等待图片加载


        imgs_A_Ds_lists = page.eles('xpath://div[@class="pgc-img"]')

        imgs_A_Ds_tags = "" # 用于存储完整的 img 标签
        for imgs_A_Ds in imgs_A_Ds_lists:
            imgs_A_Ds_html = imgs_A_Ds.html  # 获取 img 标签的完整 HTML 代码
            imgs_A_Ds_tags+=imgs_A_Ds_html
        
        # print(f"imgs_A_Ds_tags:{imgs_A_Ds_tags}")  # 打印所有 img 标签
        
        content += imgs_A_Ds_tags

        
        return render_template('index.html', title=title, content=content)
    
    except Exception as e:
        print(f"爬取过程中出现错误: {e}")
    finally:
        # 关闭浏览器
        page.quit()
        print("已关闭浏览器")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True) 