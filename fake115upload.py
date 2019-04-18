import ctypes
import numpy
import urllib2, urllib, cookielib
import requests

#############################################################
user_id="342296031"
userkey="61CC6FA7318AAD4A0BAC73DC9D7DF7446AC9E3E8".upper()
target="U_1_0"
end_string="000000"
app_ver='11.2.0'
pickcode=""
fileid="DB3D9A85D248312FE16C3B2AC12BD0D1E416ED79".upper()
quickid=fileid
filesize='2347218627'
filename="1Flames.of.Desire.EP09.720p.HDTV.x264-NGB.mkv"
#115code={}
##############################################################
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

hash=get_signature(user_id+fileid+quickid+pickcode+target+'0')
a=userkey+hash+end_string
sig=get_signature(a).upper()
#print "Signature:",sig

############################################################################################################
def read_115link_from_txt():
	f=open('115link.txt','r')
	f.close()

def get_file_by_sha1(fileid,filesize,filename):
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

get_file_by_sha1(fileid,filesize,filename)

