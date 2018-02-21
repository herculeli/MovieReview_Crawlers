#coding=utf-8
import requests
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook 
#first_url = 'https://movie.douban.com/subject/26794994/comments?start=240&limit=20&sort=new_score&status=P&percent_type='
first_url = 'https://movie.douban.com/subject/26794994/comments?status=F'
#first_url = 'https://movie.douban.com/subject/26649604/comments?status=F'
# 请求头部
headers = {
    'Host':'movie.douban.com',
    'Referer':'https://movie.douban.com/subject/26794994/?tag=%E7%83%AD%E9%97%A8&from=gaia_video',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
}

#allow_redirects=False
def visit_URL(url):
    res = requests.get(url=url,headers=headers,allow_redirects=False)
    print(res.status_code)
    print(res.url)
    print(res.text)
    print(res.content)
    soup = BeautifulSoup(res.content,'html5lib')
    print(soup)
    div_comment = soup.find_all('div',class_='comment-item') # 找到所有的评论模块
    print(div_comment)
    for com in div_comment:
        username = com.find('div',class_='avatar').a['title']
        print(username)
        comment_time = com.find('span',class_='comment-time')['title']
        print(comment_time)
        votes = com.find('span',class_='votes').get_text()
        print(votes)
        '''s1 = com.find('span',class_='allstar10 rating')
        s2 = com.find('span',class_='allstar20 rating')
        s3 = com.find('span',class_='allstar30 rating')
        s4 = com.find('span',class_='allstar40 rating')
        s5 = com.find('span',class_='allstar50 rating')
        comment_level = None
        if s1!=None:
            comment_level = s1['title']
            print(s1['title'])
        if s2!=None:
            comment_level = s2['title']
            print(s2['title'])
        if s3!=None:
            comment_level = s3['title']
            print(s3['title'])
        if s4!=None:
            comment_level = s4['title']
            print(s4['title'])
        if s5!=None:
            comment_level = s5['title']
            print(s5['title'])'''
        comment = com.p.get_text()
        print(comment)
        reviews.append([username,comment_time,votes,comment])
        #with open('text.txt','a',encoding='utf8') as file:
            #file.write('评论人：'+username+'\n')
            #file.write('评论时间：'+comment_time+'\n')
            #file.write('支持人数：'+votes+'\n')
            #if comment_level != None:
            #    file.write('评论打分：'+comment_level+'\n')
            #file.write('评论内容：'+comment+'\n')

        time.sleep(3)
    # 检查是否有下一页
    next_url = soup.find('a',class_='next')
    if next_url:
        temp = next_url['href'].strip().split('&amp;') # 获取下一个url
        next_url = ''.join(temp)
        print(next_url)
    # print(next_url)
    if next_url:
        visit_URL('https://movie.douban.com/subject/26794994/comments'+next_url)


if __name__ == '__main__':
    reviews = []
    wb = Workbook()
    ws = []  
    ws = wb.create_sheet()  
    ws.append(['评论人','评论时间','支持人数','评论内容']) 
    visit_URL(first_url)
    for mr in reviews:
        ws.append([mr[0],mr[1],mr[2],mr[3]])
    wb.save('reviews3.xlsx') 
