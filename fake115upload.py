__author__ = 'T3rry'

import os,sys
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder 
import json
import hashlib
#############################################################  Need your cookie
COOKIES={}
COOKIESTEXT="115_lang=zh; OOFL=51051904; UID=51051904_A1_1556868230; CID=73c21c9efe13fa29b5eba87c56c39418; SEID=e04613b1514f615772f4f690a29885bbe6677f2bea2827eb0e129d797703b45c09445367f81e65be9ba475cae9a5518cb3b6e62dc5ae4541166d7684; last_video_volume=100"
#############################################################  Need your cookie
user_id=""
userkey=""
target="U_1_0"
end_string="000000"
app_ver='11.2.0'
pickcode=""
header = { "User-Agent" : 'Mozilla/5.0  115disk/11.2.0'}
linksfile="115links.txt"
#######################################################################
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
		hash=hashlib.sha1(user_id+fileid+quickid+pickcode+target+'0').hexdigest()
		a=userkey+hash+end_string
		sig=hashlib.sha1(a).hexdigest().upper()
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
	hash=hashlib.sha1((user_id+fileid+quickid+pickcode+target+'0')).hexdigest()
	a=userkey+hash+end_string
	print a
	sig=hashlib.sha1(a).hexdigest().upper()
	print sig
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
	#r = requests.post(URL, data=postData,headers=header)
	#print(r.text)

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
		
