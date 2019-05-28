import dns_struct as d_s

black_dict = {'majsoul.union-game.com':'0.0.0.0',
			  'granbluefantasy.jp':'0.0.0.0'
			  }

local_dict = {'www.baidu.com':{'cname':'','name':'www.nicaiwoshiguanwnagma.com','ip':['111.13.100.92','111.13.100.91'],'arrs':'0000000000000011'},
                'www.shidaify.com':{'cname':'www.yzc.com','name':'www.mine.com','ip':['130.01.10.84','176.115.85.53'],'arrs':'0000000000000100'}
			  }

url1=[]

def b16_to_str2(b):
	b2 = b.hex()#bytes to str
	leng = len(b2)
	b3 = int(b2,16)#str_16 to str_10
	b4 = format(b3,'b').rjust(leng*4,'0')#str_10 to str_2
	return b4

def str2_to_b16(s):
	leng = len(s)
	#print(s)
	s2 = int(s,2)#str_2 to str_10
	s3 = bytes().fromhex(format(s2,'x').rjust(leng//4,'0'))#str_10 to bytes_16
	return s3

def circle(s,url1):
	if s[:8] == '00000000':
		return url1
	b = int(s[:8],2)
	url1.append(s[8:8+b*8])
	url1 = circle(s[8+b*8:],url1)
	return url1

def url_word(d):
	url1 = circle(d,[])
	s=''
	for i in url1:
		for t in range(len(i)//8):
			s+=chr(int(i[8*t:8*t+8],2))
		s+='.'
	return s[:-1]


def init_q(data):
	"""输入传输来的报文"""
	# data_16 = data.hex()
	# leng = len(data_16)
	# data_10 = int(data_16,16)
	# data_2 = format(data_10,'b').rjust(leng*4,'0')
	data_2 = b16_to_str2(data)
	#print(data_2)
	header_q = d_s.header(data_2[:16],#ID
					  data_2[16:17],#qr
					  data_2[17:21],#opcode
					  data_2[21:22],#aa
					  data_2[22:23],#tc
					  data_2[23:24],#rd
					  data_2[24:25],#ra
					  data_2[25:28],#z
					  data_2[28:32],#rcode
					  data_2[32:48],#qdcount
					  data_2[48:64],#ancount
					  data_2[64:80],#nscount
					  data_2[80:96]#arcount	
					  )
	question_q = d_s.question(data_2[96:-32],data_2[-32:-16],data_2[-16:])
	#print(header_q.ID,type(header_q.ID))
	#print(str2_to_b16(header_q.out_header()))
	#print(str2_to_b16(question_q.out_question()))
	u = url_word(question_q.qname)
	#print(u)
	return u,header_q,question_q

#da_q=b'\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x011\x010\x010\x03127\x07in-addr\x04arpa\x00\x00\x0c\x00\x01'
#init_q(da_q)
def url_ascall(url):
	url = url.split('.')
	u = ''
	for i in url:
		u += format(len(i),'b').rjust(8,'0')
		for l in i:
			u += format(ord(l),'b').rjust(8,'0')
	u += '00000000'
	return u

def ip_16(ip):
	ip = ip.split('.')
	new_ip = ''
	for p in ip:
		new_ip += format(int(p),'b').rjust(8,'0')
	return new_ip




def get_answer(url,header_q,question_q):

	black = 0
	if url in black_dict or question_q.qtype == "0000000000011100":#由于进入此处的是确认在本地的地址，所以只有黑名单与以知地址两种
		rcode = '0101'
		ancount = '0000000000000000'
		black = 1
	else:
		rcode = '0000'
		ancount = local_dict[url]['arrs']

	header_a = d_s.header(header_q.ID,
						  '1',
						  header_q.opcode,
						  '0',
						  '0',
						  header_q.rd,
						  '1',
						  '000',
						  rcode,#黑名单时为5，其他普遍为0
						  header_q.qdcount,
						  ancount,#根据有无正则名称以及IP数量决定
						  '0000000000000000',#由于本地不为权威服务器，所以置为0
						  '0000000000000000'#置零
							)
	question_a = question_q#问题一样



	if black == 1:
		return str2_to_b16(header_a.out_header()+question_a.out_question())
	l1 = 24+question_a.leng()
	#print(l,type(l))
	second_url = '11'+format(l1,'b').rjust(14,'0')
	second = 0
	all_answer=''
	u_now = d_s.first_url
	l_a1 = 0
	if local_dict[url]['cname'] != '':
		second = 1
		web_url = local_dict[url]['cname']
		#print(local_dict[url]['cname'])
		rdl = format((len(web_url)+2),'b').rjust(16,'0')
		answer = d_s.a_data(u_now,d_s.CNAME,d_s.IN,'00000000000000000000000100101100',rdl,url_ascall(web_url))
		l_a1 = answer.leng()
		#print("l_aq",l_a1)
		all_answer += answer.out_a_data()
	if local_dict[url]['name'] != '' and local_dict[url]['name'] !=url:#如相同则应直接解析ip
		web_url = local_dict[url]['name']
		#print(web_url)
		rdl = format((len(web_url)+2),'b').rjust(16,'0')
		#print('rdl',rdl)
		if second != 0:
			u_now = second_url	
		answer = d_s.a_data(u_now,d_s.CNAME,d_s.IN,'00000000000000000000000100101100',rdl,url_ascall(web_url))
		#print(answer.d_ttl,'\n',answer.out_a_data())
	
		all_answer += answer.out_a_data()
		u_now = '11'+format((24+question_a.leng()+l_a1),'b').rjust(14,'0')
		#print(u_now)
	for p in local_dict[url]['ip']:
		#print('ads',p)
		#print(u_now)
		answer = d_s.a_data(u_now,d_s.A,d_s.IN,'00000000000000000000000100101100','0000000000000100',ip_16(p))
		#print(answer.out_a_data())
		all_answer += answer.out_a_data()
                #print(all_answer)
	all_answer = header_a.out_header() + question_a.out_question() +all_answer
	all_answer = str2_to_b16(all_answer)
	#print(all_answer)
	return all_answer


#d=b'\x00\x02\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x05baidu\x03com\x00\x00\x01\x00\x01'
#u,h,q = init_q(d)
#print(u)
#get_answer(u,h,q)
