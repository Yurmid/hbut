#authour :minyuandong
#coding=gbk
import requests,time
from bs4 import BeautifulSoup

valiCode_url = 'http://run.hbut.edu.cn/Account/GetValidateCode'
login_url = 'http://run.hbut.edu.cn/Account/LogOn'
grade_url = 'http://run.hbut.edu.cn/StuGrade/Index'
base_url = 'http://run.hbut.edu.cn'
assess_url = []
link_url = []
Task_No = []
Teachers = []
Teachers_N= []
Grade = []
session = requests.session()
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Referer': 'http://run.hbut.edu.cn/Account/LogOn',
    }
captcha = session.get(valiCode_url, headers=headers)
result = captcha.content
fn = open('F:\�½��ļ���\python\��֤��\ValidateCode.jpg','wb')
fn.write(result)
fn.close()


def login():
    data = {
        'Role': 'Student',
        'UserName': input('������ѧ�ţ�'),
        'Password': input('���������루���֤���λ����'),
        'ValidateCode': input('��������֤�룺')
    }
    response = session.post(login_url, data=data, headers=headers)
    if '�һ�����' in response.text:
        retry = input('��½ʧ��,�Ƿ����ԣ���Y/N��')
        print(retry)
        if retry == 'Y' or retry == 'y':
            login()
        else:
            pass
    else:
        print('��½�ɹ�!')

def Assess_Get():
    grade_html = session.get(grade_url,headers=headers)
    bsOBJ = BeautifulSoup(grade_html.content,'html.parser')
    tds = bsOBJ('td')
    for i in tds:
        if i.a is None:
            pass
        else:
           assess_url.append(base_url+str(i.a).replace('<a href="','').replace('">ȥ����</a>',''))
    else:
        pass
    for i in assess_url:
        assess_page = session.get(i,headers=headers)
        soup = BeautifulSoup(assess_page.content,'html.parser')
        for name in soup.find_all('td'):
            Teachers.append(str(name).replace(' ','').replace('<td>\r\n','').replace('\r\n</td>',''))
        for link in soup.find_all('a'):
            link_url.append('http://run.hbut.edu.cn/'+str(link.get('href')))
            Task_No.append(link.string)
        time.sleep(1)
        print('��Ҫ��������ҵ�ʱ��...')

def Teachers_h15ander():
    for i in range(0,len(Teachers)-1):
        if i%8 == 0:
            Teachers_N.append(Teachers[i])

def Quick_assess():
    Class = input('������༶����ʽ�硰15�Ź�2������')
    for k in range(0,len(Teachers_N)):
        assessdata = {
            'Classes' : Class,
            'CUserType' : 'Student',
            'PfStr' : '10,10,10,10,10,10,10,10,10,10',
            'Opinion' : '�����ʦ��nice!',
            'SearchType':'searchAndAdd_ForGrade',
            'TaskNo':Task_No[k],
            'SumFs' : '100',
            'Teachers':Teachers_N[k],
        }

        session.post(url='http://run.hbut.edu.cn/TeachingQualityAssessment/GetRepeatEvaluateRecord',data={'Teachers':Teachers[k],'TaskNo':Task_No[k]},headers=headers)
        session.post(url='http://run.hbut.edu.cn/TeachingQualityAssessment/Update',data=assessdata,headers=headers)
        time.sleep(1)
    input('������ɣ�')
def Grade_query():
   k = []
   grade_html = session.get(grade_url, headers=headers)
   soup = BeautifulSoup(grade_html.content,'html.parser')
   for i in soup.find_all('td'):
      Grade.append(str(i.string).replace(' ','').replace('\r\n',''))
   for s in range(len(Grade)):
      if s%9 == 1 or s%9 == 5:
         k.append(Grade[s])
   for z in k :
      print(z+'\n')
login()
Assess_Get()
Teachers_h15ander()
Quick_assess()
print(Grade_query())