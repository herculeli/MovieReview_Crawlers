#coding=utf-8
import requests
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook 
#first_url = 'https://movie.douban.com/subject/26794994/comments?start=240&limit=20&sort=new_score&status=P&percent_type='
first_url = 'https://www.rottentomatoes.com/m/peter_rabbit_2018/reviews/?page=1&sort='
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
    global n
    res = requests.get(url=url,allow_redirects=False)
    #print(res.status_code)
    #print(res.url)
    #print(res.text)
    #print(res.content)
    soup = BeautifulSoup(res.content,'html5lib')
    n += 1
    div_review = soup.find_all('div',class_='row review_table_row')
    for rev in div_review:
        username = rev.find('a',class_='unstyled bold articleLink').get_text()
        print(username)
        review_date = rev.find('div',class_='review_date subtle small').get_text()
        print(review_date)
        if len(rev.find('div',class_='small subtle').get_text().split(':')) == 2:
            score = rev.find('div',class_='small subtle').get_text().split(':')[1:][0].strip()#.split('\n')[0]
        else:
            score = 'None'
        print(score)
        review = rev.find('div',class_='the_review').get_text()
        print(review)
    '''div_review = soup.find_all('div',class_='review pad_top1')
    for rev in div_review:
        username = rev.find('span',class_='author').get_text()
        print(username)
        review_date = rev.find('span',class_='date').get_text()
        print(review_date)
        score = rev.find('div',class_='left fl').get_text().strip()
        print(score)
        if rev.find('span',class_='blurb blurb_collapsed') == None:
            review = rev.find('div',class_='review_body').get_text().strip()
        else:
            review = rev.find('span',class_='blurb blurb_expanded').get_text()
        print(review)'''
        reviews.append([username,review_date,score,review])

        time.sleep(3)
    # 检查是否有下一页
    #next_url = soup.find('a',class_='btn btn-xs btn-primary-rt')
    #if next_url:
        #temp = next_url['href']#.strip().split('&amp;') # 获取下一个url
        #next_url = ''.join(temp)
        #next_url = temp
        #print(next_url)
    # print(next_url)
    if n <= 5:
       visit_URL('https://www.rottentomatoes.com/m/peter_rabbit_2018/reviews/?page='+str(n)+'&sort=')


if __name__ == '__main__':
    n = 1
    reviews = []
    wb = Workbook()
    ws = []  
    ws = wb.create_sheet()  
    ws.append(['username','review_date','score','review'])
    visit_URL(first_url)
    #visit_URL('https://www.rottentomatoes.com/m/insidious_the_last_key/reviews/?page=2&sort=')
    #visit_URL('https://www.rottentomatoes.com/m/insidious_the_last_key/reviews/?page=3&sort=')
    #visit_URL('https://www.rottentomatoes.com/m/insidious_the_last_key/reviews/?page=4&sort=')
    #visit_URL('https://www.rottentomatoes.com/m/insidious_the_last_key/reviews/?page=5&sort=')
    for mr in reviews:
        ws.append([mr[0],mr[1],mr[2],mr[3]])
    wb.save('review5.xlsx')
