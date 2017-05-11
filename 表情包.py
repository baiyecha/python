# -*- coding: utf-8 -*-
import requests
import re
import os

baseUrl = 'http://www.doutula.com';
code = requests.get(baseUrl);
if not os.path.isdir('image_biaoqingbao'):
     os.mkdir('image_biaoqingbao');

#print code.text;
maxPage = re.search("</li><li class=\"disabled\"><span>...</span></li><li><a href=\"/article/list/\?page=.+\">(.+?)</a></li> <li><a href=\"/article/list/\?page=2\" rel=\"next\">&raquo;", code.text).group(1);
print maxPage;
for i in range(20, int(maxPage)):
    url = baseUrl + '/article/list/?page=' + '%d' %i;
    #print url;
    try:
        urlHtml = requests.get(url).text;
    except requests.RequestException as e:
        continue;
    #print urlHtml;
    imageUrlList = re.finditer('<a class="list-group-item" href="(.+?)">', urlHtml);
    for urlItem in imageUrlList:
        print urlItem.group(1);
        try:
            urlItemHtml = requests.get(urlItem.group(1)).text;
        except requests.RequestException as e:
            continue;
        #print urlItemHtml;
        imageDirName = re.search(' <meta property="og:description" content="(.+?)"/>', urlItemHtml).group(1);
        print imageDirName;
        if not os.path.isdir('image_biaoqingbao'+ '/' + imageDirName):
            os.mkdir('image_biaoqingbao'+ '/' + imageDirName);
        imageList = re.finditer('img src="(.+?)" alt=', urlItemHtml);
        j = 0;
        for imageUrl in imageList:
            print imageUrl.group(1);
            try:
                imageData = requests.get(imageUrl.group(1), timeout=10);
            except requests.RequestException as e:
                continue;
            except requests.exceptions.ConnectTimeout:
                continue;
            except requests.exceptions.Timeout:
                continue;
            else:
                try:
                    open('image_biaoqingbao'+ '/' + imageDirName + '/' + '%d'%j + '.jpg','wb').write(imageData.content);
                except IOError:
                    pass;
                else:
                    j+=1;
