# -*- coding: utf-8 -*                                           #语料为中文，采用UTF-8编解码
import re
import math


#该类用于实现Unigram
class unigram:
    def __init__(self):                                          #初始化
        self.token=self.linecounter()
        self.v=self.getV()
        self.dict=self.getDict()


    def __del__(self):
        pass


    def linecounter(self):                                      #获取token总数
        file=open("uniDict.txt",'r')                            #打开词典文件
        lines=len(file.readlines())
        file.close()                                            #关闭词典文件
        return lines


    def getV(self):                                             #获取词表大小
        file=open("uniDict.txt",'r')                            #打开词典文件
        v=0
        for line in file.readlines():
            word=re.split(r'\s+',line)
            word.remove("")
            v+=int(word[1])
        file.close()                                            #关闭词典文件
        return v


    def getDict(self):                                          #获取词表
        file=open("uniDict.txt",'r')                            #打开词典文件
        dictionary={}
        for line in file.readlines():
            word=re.split(r'\s+',line)
            word.remove("")
            dictionary[word[0]]=word[1]
        dictionary["<unknown>"]=0                               #预留项
        file.close()                                            #关闭词典文件
        return dictionary


    def getPerplexity(self,p,v):                                #计算困惑度
        return math.pow(2,-p/v)


    def add_one(self):                                          #Add-one平滑方法
        smoothDict=self.dict.copy()
        for key in smoothDict.keys():                           #对词典进行加一处理
            smoothDict[key]=math.log((float(smoothDict[key])+1.0)/(self.token+self.v),2)
        p=0.0
        testV=0
        file=open("test.txt",'r')                               #打开测试文件
        for line in file.readlines():
            words=re.split(r'\s+',line)
            words.remove("")
            testV+=len(words)                                   #获取测试文件词表大小
            for i in range(0,len(words)):                       #计算测试语料出现概率
                if words[i] in smoothDict:
                    p+=smoothDict[words[i]]
                else:
                    p+=smoothDict["<unknown>"]
        perplexity=self.getPerplexity(p,testV)                  #计算困惑度
        print(">>                      The perplexity of Add-one smoothing is %.2f.                      <<"%perplexity)
        file.close()                                            #关闭测试文件


    def good_turing(self):                                      #Good-turing平滑方法
        smoothDict=self.dict.copy()
        Nc={}
        for key in smoothDict.keys():                           #对词典进行分频率统计
            if smoothDict[key] in Nc:
                Nc[smoothDict[key]]+=1.0
            else:
                Nc[smoothDict[key]]=1.0
        tmp=sorted(Nc.items(),key=lambda item:int(item[0]),reverse=False)
        for i in range(0,len(tmp)-1):                           #计算折扣
            tmp[i]=(tmp[i][0],int(tmp[i+1][0])*tmp[i+1][1]/tmp[i][1])
        V=0.0
        for i in range(0,len(tmp)):
            V+=tmp[i][1]
        for i in range(0,len(tmp)):                             #计算单词出现概率
            tmp[i]=(tmp[i][0],tmp[i][1]/V)
            Nc[tmp[i][0]]=tmp[i][1]
        for key in smoothDict.keys():
            smoothDict[key]=math.log(Nc[smoothDict[key]],2)
        p=0.0
        testV=0
        file=open("test.txt",'r')                               #打开测试文件
        for line in file.readlines():
            words=re.split(r'\s+',line)
            words.remove("")
            testV+=len(words)                                   #获取测试文件词表大小
            for i in range(0,len(words)):                       #计算测试语料出现概率
                if words[i] in smoothDict:
                    p+=smoothDict[words[i]]
                else:
                    p+=smoothDict["<unknown>"]
        perplexity=self.getPerplexity(p,testV)                  #计算困惑度
        print(">>                     The perplexity of Good-turing smoothing is %.2f.                   <<"%perplexity)
        file.close()



print(">>                                          unigram                                          <<")
gram=unigram()                                                  #创建对象
print("***********************************************************************************************")
gram.add_one()                                                  #Add-one平滑
print("***********************************************************************************************")
gram.good_turing()                                              #Good-turing平滑
print("***********************************************************************************************")