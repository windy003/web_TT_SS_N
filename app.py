from DrissionPage import ChromiumPage, ChromiumOptions
import time
import os
from flask import Flask, request, render_template
import re
import html
import time
import os
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():


    url_old = ""
    content_old = ""
    # 读取 backup.json 文件
    if os.path.exists("./backup.json"):
        with open("./backup.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            url_old = data.get("url", "").strip()
            content_old = data.get("content", "")

    if request.method == 'POST':
        if 'url' in request.form:
            url = request.form['url'].strip()
            if url_old:
                if url == url_old:
                    return render_template('index.html',content=content_old)
                else:
                    return load_from_url(url)
            else:
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
        

        
        # 尝试找到并点击"点开展开剩余.."按钮
        try:
            # 使用 contains() 函数匹配包含特定文本的按钮
            more_button = page.ele('xpath://*[contains(text(), "点击展开剩余")]')
            more_button.click()
            print("已点击展开更多按钮")
            time.sleep(2)  # 等待内容加载
        except Exception as e:
            print(f"未找到展开更多按钮或点击失败: {e}")


        # 向下翻页,并延迟时间
        try:
            time.sleep(2)

            # 滚动页面以触发懒加载
            page.scroll.down()
            time.sleep(2)  # 等待图片加载

            # 滚动页面以触发懒加载
            page.scroll.down()
            time.sleep(2)  # 等待图片加载
            page.scroll.down()
            time.sleep(2)  # 等待图片加载

            # 滚动页面以触发懒加载
            page.scroll.down()
            time.sleep(2)  # 等待图片加载
            page.scroll.down()
            time.sleep(2)  # 等待图片加载

            # 滚动页面以触发懒加载
            page.scroll.down()
            time.sleep(2)  # 等待图片加载

            page.scroll.down()
            time.sleep(2)  # 等待图片加载
            page.scroll.down()
            time.sleep(2)  # 等待图片加载

            # 滚动页面以触发懒加载
            page.scroll.down()
            time.sleep(2)  # 等待图片加载
        except Exception as e:
            print(f"向下翻页失败: {e}")

        content=""


        # 获取文章标题
        title = page.ele('xpath://h1').text
        print(f"文章标题: {title}")
        
        content+=  f"<h1>{title}</h1>"

        # 获取文章的发布时间和作者
        # 获取所有 span 元素
        spans = page.eles("xpath://div[@class='article-meta']/span")

        # 获取文章发布时间（第一个 span）
        if len(spans) > 0:
            article_pub_time = spans[0].text
            if article_pub_time:
                content += article_pub_time + "<br>"

        # 获取文章作者（第二个 span）
        if len(spans) > 2:
            article_author = spans[2].text
            if article_author:
                content += article_author + "<br><br>"

        # 获取微头条的发布时间和作者
        wtt_author=page.ele("xpath://div[@class='desc']/a").text  
        if wtt_author:
            content+= wtt_author + "<br>"

        wtt_pub_time=page.ele("xpath://div[@class='desc']/p/span").text
        if wtt_pub_time:
            content+= wtt_pub_time + "<br><br>"


        # 微头条文本
        wtt = page.ele("xpath://div[@class='weitoutiao-html']")
        if wtt:
            content += wtt.text



        if page.eles('xpath://article//p/span'):
            for ele in page.eles('xpath://article//p/span'):
                content += ele.text
        else:
            for ele in page.eles('xpath://article//p'):
                content += ele.text

    

        print(f"文章内容: {content}")


        imgs_lists = page.eles('xpath://article/img')
        imgs_tags = ""
        for img in imgs_lists:
            imgs_tags += img.html

        content += imgs_tags


        imgs_A_Ds_lists = page.eles('xpath://div[@class="pgc-img"]')

        imgs_A_Ds_tags = "" # 用于存储完整的 img 标签
        for imgs_A_Ds in imgs_A_Ds_lists:
            imgs_A_Ds_html = imgs_A_Ds.html  # 获取 img 标签的完整 HTML 代码
            imgs_A_Ds_tags+=imgs_A_Ds_html
        
        # print(f"imgs_A_Ds_tags:{imgs_A_Ds_tags}")  # 打印所有 img 标签
        
        wtt_imgs_tags_lists = page.eles('xpath://img[@class="weitoutiao-img"]')

        wtt_imgs_tags = "" # 用于存储完整的 img 标签
        for wtt_imgs in wtt_imgs_tags_lists:
            wtt_imgs_html = wtt_imgs.html  # 获取 img 标签的完整 HTML 代码
            wtt_imgs_tags+=wtt_imgs_html

        content += imgs_A_Ds_tags
        content += wtt_imgs_tags


        # 将 url 和 content 写入 backup.json 文件
        data = {
            "url": url,
            "content": content
        }
        with open("./backup.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return render_template('index.html',content=content)

    except Exception as e:
        print(f"爬取过程中出现错误: {e}")
    finally:
        # 关闭浏览器
        page.quit()
        print("已关闭浏览器")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True) 