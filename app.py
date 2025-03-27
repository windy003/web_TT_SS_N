from DrissionPage import ChromiumPage, ChromiumOptions
import time
import os
from flask import Flask, request, render_template
import re
import html
import time
import os
import json
import traceback


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():


    url_old = ""
    content_old = ""
    # 读取 backup.json 文件
    if os.path.exists("./backup/backup.json"):
        with open("./backup/backup.json", "r", encoding="utf-8") as f:
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
    # options.set_argument('--headless=new')  # 使用新的无头模式
    # options.set_argument('--no-sandbox')    # 在Linux系统中添加此参数
    # options.set_argument('--disable-dev-shm-usage')  # 避免内存不足问题
    options.set_argument('--user-data-dir=./chrome_data')
    
    
    # 使用配置创建页面对象
    page = ChromiumPage(options)
    print("已启动浏览器...")


    # 确保data目录存在
    if not os.path.exists('./chrome_data'):
        os.makedirs('./chrome_data')

    
    # 开始操作
    try:
        # 访问文章页面
        page.get(url)
        print("正在加载页面...")
        time.sleep(2)  # 等待页面加载
        
        # 设置页面缩放比例
        page.run_js('document.body.style.zoom = "25%"')

        
        
        
        # 尝试找到并点击"点开展开剩余.."按钮
        try:
            # 使用 contains() 函数匹配包含特定文本的按钮
            more_button = page.ele('xpath://*[contains(text(), "点击展开剩余")]')
            if more_button:
                more_button.click()
                print("已点击展开更多按钮")
                time.sleep(2)  # 等待内容加载
        except Exception as e:
            print(f"未找到展开更多按钮或点击失败: {e}")
            traceback.print_exc()

        # 向下翻页,并延迟时间
        try:

            page.scroll.down()
            time.sleep(2)

            
            page.scroll.down()
            time.sleep(2)

            
            page.scroll.down()
            time.sleep(2)

            
            page.scroll.down()
            time.sleep(2)

            
            page.scroll.down()
            time.sleep(2)

            
            page.scroll.down()
            time.sleep(2)

            
            page.scroll.down()
            time.sleep(2)

            
            page.scroll.down()
            time.sleep(2)

            
            page.scroll.down()
            time.sleep(2)

            
            page.scroll.down()
            time.sleep(2)

            
            page.scroll.down()
            time.sleep(2)

            
            page.scroll.down()
            time.sleep(2)

            
            page.scroll.down()
            time.sleep(2)
        except Exception as e:
            print(f"向下翻页失败: {e}")
            traceback.print_exc()
        
        
        
        
        content=""
        # 获取文章标题
        try:
            title = page.ele('xpath://h1').text
            print(f"文章标题: {title}")
            
            content+=  f"<b>{title}</b>"
        except Exception as e:
            print(f"获取文章标题失败: {e}")
            traceback.print_exc()


        # 获取文章的发布时间和作者
        try:
        # 获取所有 span 元素
            spans = page.eles("xpath://div[@class='article-meta']/span")

            # 获取文章发布时间（第一个 span）
            if len(spans) > 0:
                article_pub_time = spans[0].text
                if article_pub_time:
                    content += "<br>" + article_pub_time + "<br>"
        except Exception as e:
            print(f"获取文章发布时间失败: {e}")
            traceback.print_exc()

        
        # 获取文章作者（第二个 span）
        try:
            if len(spans) > 2:
                article_author = spans[2].text
                if article_author:
                    content += article_author + "<br><br>"
        except Exception as e:
            print(f"获取文章作者失败: {e}")
            traceback.print_exc()

        # 判断使用哪种模式
        try:
            if len(page.eles('xpath://article/div/div/p')) > 5:
                return mode_1(page,content,url)
            elif len(page.eles('xpath://article/p')) > 4:
                return mode_2(page,content,url)
            else:
                return wtt(page,content,url)
        except Exception as e:
            print(f"判断使用哪种模式失败: {e}")
            traceback.print_exc()





       

    except Exception as e:
        print(f"爬取过程中出现错误: {e}")
        traceback.print_exc()
    finally:
        # 关闭浏览器
        page.quit()
        print("已关闭浏览器")
        traceback.print_exc()


# 将 url 和 content 写入 backup.json 文件的函数
def save_content(content,url):
    try:
        data = {
            "url": url,
            "content": content
        }
        with open("./backup/backup.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"写入 backup.json 文件失败: {e}")
        traceback.print_exc()



# 获取文章内容函数,形式1,示例:https://www.toutiao.com/article/7484780656023667211/?app=news_article&category_new=text_inner_flow&chn_id=94349612189&is_hit_share_recommend=0&req_id_new=20250323084928A9A596CD6AC5AA1F7C3B&share_did=MS4wLjACAAAAFIeCXqC-bpKxhp-FMV0EuKV-XQVB6-mSh701zwQO9RpTxDeXwV2yFdvhJIx5cc_q&share_token=188c7e83-3177-4243-a9dd-f688ccad8998&share_uid=MS4wLjABAAAASxKaOyZkLPeOekvLPbVvpEZxOI0hIbcOi5tNlEAvhVQNRKCRhGolFv7jwed4Tf1r&tt_from=copy_link&use_new_style=1&utm_campaign=client_share&utm_medium=toutiao_android&utm_source=copy_link&source=m_redirect
def mode_1(page,content,url):
    print("开始形式1")
    try:
        eles = page.eles('xpath://article/div/div/*')
        if eles:
            for ele in eles:
                if ele.tag == 'p':
                    if ele.text:
                        content += ele.text
                    elif ele.ele('xpath:.//img'):
                        content += ele.ele('xpath:.//img').html
                elif ele.tag == 'section':
                    if ele.text:
                        content += ele.text
        print("用的是形式1")
        save_content(content,url)
        return render_template('index.html',content=content)
        
    except Exception as e:
        print(f"获取文章,形式2,内容失败: {e}")
        traceback.print_exc()





# 获取文章内容,形式2
# 示例:https://www.toutiao.com/article/7482967924794655271/?app=news_article&category_new=text_inner_flow&chn_id=94349612189&is_hit_share_recommend=0&req_id_new=20250322132314A2966E0FEC34CAD309F7&share_did=MS4wLjACAAAAaXbI3K95HwYTITAe_67APNaTonE8KefZ9UqB7B5wwMa_a0T5y1eus-kan8ClPqgH&share_token=ac1d72f6-ca61-49de-9533-a3213c2b6e68&share_uid=MS4wLjABAAAASxKaOyZkLPeOekvLPbVvpEZxOI0hIbcOi5tNlEAvhVQNRKCRhGolFv7jwed4Tf1r&tt_from=copy_link&use_new_style=1&utm_campaign=client_share&utm_medium=toutiao_android&utm_source=copy_link&source=m_redirect
def mode_2(page,content,url):
    print("开始形式2")
    try:
        eles = page.eles('xpath://article/*')
        if eles:
            try:
                for ele in eles:
                    if ele.tag == 'p':
                        # 提取所有文本内容（包括嵌套标签中的文本）
                        content += ele.text
                    elif ele.tag == 'blockquote':
                        content += ele.text
                    elif ele.tag == 'div':
                        content += ele.html
                    elif ele.tag == 'img':
                        content += ele.html
                    elif ele.tag == 'h1':
                        content += ele.text
            except Exception as e:
                print(f"获取文章内容失败: {e}")
                traceback.print_exc()
        print("用的是形式2")
        save_content(content,url)
        return render_template('index.html',content=content)
    except Exception as e:
        print(f"获取文章内容失败: {e}")
        traceback.print_exc()





# 获取微头条的发布时间和作者
# https://www.toutiao.com/w/1827674248868036/?app=&category_new=text_inner_flow&chn_id=94349612189&req_id_new=2025032711472041716F68C8264F18C47B&share_did=MS4wLjACAAAAFIeCXqC-bpKxhp-FMV0EuKV-XQVB6-mSh701zwQO9RpTxDeXwV2yFdvhJIx5cc_q&share_token=4e8f8dc5-f706-4d5b-8639-241efe55b4e9&share_uid=MS4wLjABAAAASxKaOyZkLPeOekvLPbVvpEZxOI0hIbcOi5tNlEAvhVQNRKCRhGolFv7jwed4Tf1r&timestamp=1743047241&tt_from=copy_link&use_new_style=1&utm_campaign=client_share&utm_medium=toutiao_android&utm_source=copy_link&source=m_redirect
def wtt(page,content,url):
    try:
        wtt_author=page.ele("xpath://div[@class='desc']/a").text  
        if wtt_author:
            content+= wtt_author + "<br>"
    except Exception as e:
        print(f"获取微头条作者失败: {e}")
        traceback.print_exc()
    try:
        wtt_pub_time=page.ele("xpath://div[@class='desc']/p/span").text
        if wtt_pub_time:
            content+= wtt_pub_time + "<br><br>"
    except Exception as e:
        print(f"获取微头条发布时间失败: {e}")
        traceback.print_exc()

    # 微头条文本
    try:
        wtt = page.ele("xpath://div[@class='weitoutiao-html']")
        if wtt:
            content += wtt.text
        imgs = page.eles("xpath://article//img")
        if imgs:
            for img in imgs:
                content += img.html
    except Exception as e:
        print(f"获取微头条文本失败: {e}")
        traceback.print_exc()   

    print("用的是微头条")
    save_content(content,url)
    return render_template('index.html',content=content)






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True) 