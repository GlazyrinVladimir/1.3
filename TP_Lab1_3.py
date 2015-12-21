#-*- coding: utf8 -*-
import urllib
import urllib2
import re
import os

ExtList = ['gif', 'bmp', 'jpg', 'jpeg', 'png', 'js', 'css', 'html', 'ico']
WorkDir = os.getcwd()
PageNumb = 100


def SaveRecourcesUrl(MainURL, URL, Count, WorkDir):
    ExtraContent = ''
    FolderName = str(Count) #создаем имя для папки, куда будем сохранять
    NewDir = WorkDir + '\\' + FolderName
    os.mkdir(NewDir)
    os.chdir(NewDir)
    if URL.find('http') < 0:
        CorrectURL = MainURL + URL
    else:
        CorrectURL = URL
    Content = urllib2.urlopen(CorrectURL).read()
    ImgURL = re.findall('img.*?src="(.*?)"', Content)
    LinkImgURL = re.findall('href="(.*?)"', Content)
    JsURL = re.findall('script.*?src=\"(.*?.js)\"', Content)
    LinkJsURL = re.findall('link.*?href=\"(.*?.js)\"', Content)
    CssURL = re.findall('link.*?href=\"(.*?.css)\"',Content)
    URLS = ImgURL + JsURL + LinkJsURL + CssURL + LinkImgURL
    for I in range(len(URLS)):
        try:
            Adds = URLS[I]
            if Adds[Adds.rfind('.') + 1 : ] in ExtList:
                FileName = Adds[Adds.rfind('/') + 1 : ]
                Index = Content.find(Adds)
                ExtraContent = Content[ : Index] + './' + FileName + Content[Index + len(Adds):]
                Content = ExtraContent
                ExtraContent = ''
                if Adds.find('http') < 0:
                    Adds = MainURL + Adds
                if Adds.find('http') > 0:
                    Adds = Adds[Adds.find('http') : ]
                urllib.urlretrieve(Adds, FileName)
        except IOError:
            print 'Error'
    Fout = open(str(Count) + '.html', 'w')
    Fout.write(Content)
    Fout.close()



URLList = []
SavedPages = []
Count = 1
Working = True

MainURL = 'http://lenta.ru/'
Word = 'Украина'
Content = urllib2.urlopen(MainURL).read()
URLList = re.findall('a.*?href="(.*?)"', Content)
I = 0
while (I < len(URLList)) and (len(SavedPages) <= PageNumb):
    URL = URLList[I]
    if URL.find('http') < 0:
        CorrectURL = MainURL + URL
    else:
        CorrectURL = URL

    if CorrectURL[-3:] == "php":
        I += 1
    print CorrectURL
    print urllib2.Request(CorrectURL).headers
    if URL.find('@') > 0:
        URLList.pop(I)
        Working = False
    if Working:
        try:
            Content = urllib2.urlopen(CorrectURL).read()
        except:
            pass
        if (Content.find(Word) > 0) and (CorrectURL not in SavedPages) and (len(SavedPages) <= PageNumb) and (CorrectURL != (MainURL + '/rss')):
            try:
                SaveRecourcesUrl(MainURL, URL, Count, WorkDir)
                os.chdir(WorkDir)
                Count += 1
                SavedPages.append(CorrectURL)
                if len(URLList) <= 1000:
                    URLList += re.findall('a.*?href="(.*?)"', Content)
                URLList.pop(I)
            except  IOError:
                URLList.pop(I)
        elif (Content.find(Word) < 0) and (CorrectURL not in SavedPages):
            if len(URLList) <= 1000:
                URLList += re.findall('a.*?href="(.*?)"', Content)
            URLList.pop(I)
        elif ((Content.find(Word) > 0) and (CorrectURL in SavedPages)) or (CorrectURL == (MainURL + '/rss')):
            URLList.pop(I)
    Working = True
print 'End'

