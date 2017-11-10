# -*- coding: utf-8 -*                                                          #语料为中文，采用UTF-8编解码

import codecs
import re


#分割语料，前90%用于训练，剩余作为测试
with codecs.open("Chinese text corpus.txt",'r',encoding='UTF-8') as corpus:     #打开语料文件
    with codecs.open("train.txt",'w',encoding='UTF-8') as train:
        with codecs.open("test.txt",'w',encoding='UTF-8') as test:
            lines=0
            for line in corpus.readlines():                                     #统计语料总行数
                lines+=1
            print("There are "+str(lines)+" lines in the 'Chinese text corpus.txt'.")
            linesForTraining=int(lines*0.9)                                     #训练语料行数
            print("In these lines, the first "+str(linesForTraining)+" lines are used for training, and the rest are for testing.")
            corpus.seek(0)                                                      #指针回至文件头
            counter=0
            for line in corpus.readlines():
                if len(line)>0:                                                 #跳过空行
                    sentence=re.split(r'\s+',line[23:])                         #除去空格，提取出词/词性
                    if counter<linesForTraining:                                #处于训练语料部分
                        for i in range(0,len(sentence)):
                            word=re.split('/',sentence[i])                      #除去词性，提取出词
                            train.write(word[0])                                #写入train.txt
                            if i is not len(sentence)-1:
                                train.write(" ")
                        train.write("\r\n")
                    else:                                                       #处于测试语料部分
                        for i in range(0,len(sentence)):
                            word=re.split('/',sentence[i])
                            test.write(word[0])                                 #写入test.txt
                            if i is not len(sentence)-1:
                                test.write(" ")
                        test.write("\r\n")
                counter+=1
        test.close()                                                            #关闭语料文件
    train.close()
corpus.close()
print("\nThe corpus segmentation has been over.")



uniDict={}
biDict={}
triDict={}


with codecs.open("train.txt",'r',encoding='UTF-8') as train:
    for line in train.readlines():
        sentence=re.split(r'\s+',line)
        for i in range(0,len(sentence)):
            word=sentence[i]
            if word in uniDict:
                uniDict[word]+=1
            else:
                uniDict[word]=1
            if i<len(sentence)-1:
                word+='|'+sentence[i+1]
                if word in biDict:
                     biDict[word]+=1
                else:
                    biDict[word]=1
                if i<len(sentence)-2:
                    word+='|'+sentence[i+2]
                    if word in triDict:
                        triDict[word]+=1
                    else:
                        triDict[word]=1
                else:
                    word+="|$"
                    if word in triDict:
                        triDict[word]+=1
                    else:
                        triDict[word]=1
            else:
                word+="|$"
                if word in biDict:
                    biDict[word]+=1
                else:
                    biDict[word]=1
                