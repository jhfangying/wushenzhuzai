#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import urllib.request
import re
import os
categlogueHtml=''
def getHtml(url):
    response =urllib.request.urlopen(url)
    text=response.read().decode('utf-8')
    return text

def getCataloguePage(url):
    html=categlogueHtml
    if(categlogueHtml==''):
        html=getHtml(url)
    return html

def getNovelTitle(url):
    html=getCataloguePage(url)
    title=re.search(r'<div class="article".*?h1>(.*?)</h1>',html).group(1)
    return title

def getCatalogue(url):
    html=getCataloguePage(url)
    listhtml=re.search(r'<div class="list">.*?<dl>.*?</dl>.*?(<dl>.*?</dl>).*?</div>',html).group(1)
    list=re.findall(r'<dd><a href="(.*?)">(.*?)</a></dd>',listhtml)
    return list

def openNovel(url):
    response =urllib.request.urlopen(url)
    text=response.read().decode('utf-8')
    title=re.search(r'<div class="article_title"><h1>(.*?)</h1>',text).group(1)
    content=re.search(r'<div class="content_left"><div class="con_show_l"><script>show\(pc_rd\);</script></div>([\s\S]*?)<div class="con_show_r">',text).group(1);
    content=re.sub(r'<p.*?>\s*','  ',content)
    content=re.sub(r'</p.*?>','\r',content)
    content=re.sub(r'<script>.*?</script>','',content)
    contentresult=re.sub(r'<strong>[\s\S]*?</strong>','',content)
    return [title,contentresult]

def readDownloadLog(dir):
    filename=dir+'/log.txt'
    lastarticleurl=''
    with open(filename,'r') as fo:
        lastarticleurl=fo.readline()
        fo.close()
    return lastarticleurl

def writeDownloadLog(dir,url):
    filename=dir+'/log.txt'
    with open(filename,'w') as fo:
        fo.write(url)
        fo.close()

def downloadArticle(dir,url):
    filename=dir+'/wusheng.txt'
    data=openNovel(url);
    title=data[0]
    content=data[1]
    with open(filename,'a') as fo:
        print('正在抓取---《'+title+'》')
        fo.write(title)
        fo.write('\r\n')
        fo.write(content)
        fo.write('\r\n------------------------------------\r\n\r\n');
        fo.close()

currentPath=os.path.abspath('.')
baseurl='https://www.shukeba.com/'
wushengurl=baseurl+'/110312'
title=getNovelTitle(wushengurl)
novelPath=currentPath+'/'+title
lastarticleurl='';
if(os.path.isdir(novelPath)==False):
    os.mkdir(novelPath)
    #创建临时文件记录上次的下载位置
lastarticleurl=readDownloadLog(novelPath)
list=getCatalogue(wushengurl)

needdownload=False
print('开始抓取《武神主宰》')
for ca in list:
    if(needdownload==True):
        downloadArticle(novelPath,baseurl+ca[0])
        writeDownloadLog(novelPath,ca[0])
    if(ca[0]==lastarticleurl):
        needdownload=True
        continue
    continue
print('《武神主宰》下载完成')
