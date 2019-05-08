
__author__ = 'T3rry'

import ctypes,os,sys
import urllib2, urllib, cookielib
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder 
import json
############################################################################### Need your cookie
COOKIES={}
COOKIESTEXT="115_lang=zh; OOFL=1234; UID=12304_A1_1556868230; CID=123c9efe13fa29b5eba87c56c39418; SEID=e1233b1514f615772f4f690a29885bbe6677f2bea2827eb0e129d797703b45c09445367f81e65be9ba475cae9a5518cb3b6e62dc5ae4541166d7684; last_video_volume=100"
############################################################################### Need your cookie
user_id=""
userkey=""
target="U_1_0"
end_string="000000"
app_ver='11.2.0'
pickcode=""
header = { "User-Agent" : 'Mozilla/5.0  115disk/11.2.0'}
linksfile="115links.txt"
################################################################################
def int_overflow(val):
    maxint = 2147483647
    if not -maxint-1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val

def unsigned_right_shitf(n,i):
    if n<0:
        n = ctypes.c_uint32(n).value
    if i<0:
        return -int_overflow(n << abs(i))
    return int_overflow(n>>i)

def  build_hash(a):
	v0 = "0123456789abcdef"
	v1 = ""
	v2=0
	for i in range(0,len(a)*4):
		v3 = v2 >> 2
		v5 = (3 - v2 % 4) * 8;
		v4 = v0[(a[v3] >> v5 + 4 & 15)]
		v3_1 = v0[(a[v3]>> v5 & 15)]
		v1 = v1 + v4 + v3_1
		v2+=1
	return v1
   
def dha(a):

	v0 =[0]*len(a)*8
	for i in range(0,len(v0),8):
		v1=i>>5
		v0[v1]|=(ord(a[i/8])&255)<<24-i%32
	i_v3=0
	for i in v0:
		if i!=0:
			i_v3+=1
	v3=[0]*i_v3
	for j in range(0,len(v3)):
		v3[j]=v0[j]
	return v3

def dhaa(a,b):
	v1=b>>5
	v2=dhbb(a,v1)
	v2[v1]|=128<<24-b%32
	v1=(b+64>>9<<4)+15
	v2=dhbb(v2,v1)
	v2[v1]=b
	v0=80
	v1_1=[0]*80
	v5=0
	v6=0x67452301
	v7=-0x10325477
	v8=-0x67452302
	v9=0x10325476
	v10=-0x3c2d1e10
	while(True):
		v12=1
		v13=5
		if (v5 >=len(v2)):
			break
		v14=v6
		v15=v7
		v3=v8
		v4=v9
		v16=v10
		v11=0
		while (v11<v0):
			v1_1[v11]=v2[v5+v11] if v11<16 else dhc(v1_1[v11-3]^v1_1[v11-8]^v1_1[v11-14]^v1_1[v11-16],v12)
			v0=dhb(dhb(dhc(v14,v13),dhd(v11,v15,v3,v4)),dhb(dhb(v16,v1_1[v11]),dhe(v11)))
			v12=dhc(v15,30)
			v11+=1
			v16=v4
			v15=v14
			v13=5
			v14=v0
			v4=v3
			v3=v12
			v0=80
			v12=1
		v6=dhb(v14,v6)
		v7=dhb(v15,v7)
		v8=dhb(v3,v8)
		v9=dhb(v4,v9)
		v10=dhb(v16,v10)
		v5+=16
		v0=80
	ret=[v6,v7,v8,v9,v10]
	return ret

def dhb(ia,ib):
	v1=int_overflow(ia&65535)+(ib&65535)
	return int_overflow(int_overflow(int_overflow(ia>>16)+int_overflow(ib>>16)+int_overflow(v1>>16)<<16)|v1&65535)

def dhbb(a,b):
	v0 = len(a)
	v1 = b + 1;
	if(v0 >= v1):
		return a    
	v1_1 = [0]*v1
	v2 = 0   
	while(v2 < v0) :
		v1_1[v2] = a[v2];
		v2+=1
	return v1_1

def dhc(a,b):
	return int_overflow(int_overflow(unsigned_right_shitf(a,32-b)) | int_overflow(a << b))

def dhd(a,b,c,d):
	if a<20:
		return b&c|(b^-1)&d
	if a<40:
		return b^c^d
	if a<60:
		return b&c|b&d|c&d
	return b^c^d

def dhe(a):
	if a<20:
		a=0x5a827999
	elif a<40:
		a=0x6ed9eba1
	elif a<60:
		a=-0x70e44324
	else:
		a=-0x359d3e2a
	return a

def get_signature (s):
	return build_hash(dhaa(dha(s), len(s) * 8))

############################################################################################################
def Upload_files_by_sha1_from_links(filename):  #link sample : 1.mp4|26984894148|21AEB458C98643D5E5E4374C9D2ABFAAA4C6DA6
	GetUserKey()
	for l in open(filename,'r'):
		link=l.split('|')
		filename=link[0]
		filesize=link[1]
		fileid=link[2]
		if(len(fileid)!=40):
			print 'Error links'
		quickid=fileid
		hash=get_signature(user_id+fileid+quickid+pickcode+target+'0')
		a=userkey+hash+end_string
		sig=get_signature(a).upper()
		URL="http://uplb.115.com/3.0/initupload.php?isp=0&appid=0&appversion=11.2.0&format=json&sig="+sig
		header = { "User-Agent" : 'Mozilla/5.0  115disk/11.2.0'}
		postData={
				'preid':'',
				'filename':filename,
				'quickid':fileid,
				'user_id':user_id,
				'app_ver':app_ver,
				'filesize':filesize,
				'userid':user_id,
				'exif':'',
				'target':target,
				'fileid':fileid
			  }
		r = requests.post(URL, data=postData,headers=header)
		print(r.text)


def GetFileSize(file):
	return os.path.getsize(file)

def GetUserKey():
	global user_id,userkey
	AddCookie(COOKIESTEXT)
	r = requests.get("http://proapi.115.com/app/uploadinfo",headers=header,cookies=COOKIES)
	resp=json.loads(r.content) 
	user_id=str(resp['user_id'])
	userkey=str(resp['userkey']).upper()

def AddCookie(cook):
	for line in COOKIESTEXT.split(';'):   
		name,value=line.strip().split('=',1)  
		COOKIES[name]=value 

def Upload_file_by_sha1(fileid,filesize,filename):  #quick
	GetUserKey()
	fileid=fileid.upper()
	quickid=fileid
	hash=get_signature(user_id+fileid+quickid+pickcode+target+'0')
	a=userkey+hash+end_string
	sig=get_signature(a).upper()
	URL="http://uplb.115.com/3.0/initupload.php?isp=0&appid=0&appversion=11.2.0&format=json&sig="+sig
	postData={
				'preid':'',
				'filename':filename,
				'quickid':fileid,
				'user_id':user_id,
				'app_ver':app_ver,
				'filesize':filesize,
				'userid':user_id,
				'exif':'',
				'target':target,
				'fileid':fileid
			  }
	r = requests.post(URL, data=postData,headers=header)
	print(r.text)

def Upload_file_from_local(filename):  #slow
	uri='http://uplb.115.com/3.0/sampleinitupload.php'
	AddCookie(COOKIESTEXT)
	postdata={"userid":user_id,"filename":filename,"filesize":GetFileSize(filename),"target":target}
	r = requests.post(uri,headers=header,cookies=COOKIES,data=postdata)
	resp=json.loads(r.content) 
	print resp
	req_headers = {'Content-Type': "multipart/form-data; boundary=----WebKitFormBoundarya2JSh7swYU46OdJ0"}
	m = MultipartEncoder(fields=[('name', filename), 
                             ('key', resp['object']),
                             ('policy',resp['policy']),
                             ('OSSAccessKeyId', resp['accessid']),
                             ('success_action_status', '200'),
                             ( 'callback',resp['callback']),
                             ('signature',resp['signature']),
                             ('file',(filename,open(filename, 'rb'), 'video/mp4'))],
                     		boundary='----WebKitFormBoundarya2JSh7swYU46OdJ0'
                    )
	r = requests.post(resp['host'],headers=req_headers,data=m)
	print r.content

#Upload_files_by_sha1_from_links('links.txt')
#Upload_file_by_sha1('321AEB458C98643D5E5E4374C9D2ABFAAA4C6DA6','26984894148','1.mp4')
#Upload_file_from_local("1.mp4")
if __name__ == '__main__':
	if len(sys.argv)>1:
		filename=sys.argv[1]
		Upload_file_from_local(filename)
	else:
		Upload_files_by_sha1_from_links(linksfile)
		
