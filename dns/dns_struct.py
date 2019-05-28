#header
IN = '0000000000000001'
A = '0000000000000001'
CNAME = '0000000000000101'
first_url="1100000000001100"

class header:
    ID = ''
    qr = ''
    opcode = ''
    aa = ''
    tc = ''
    rd = ''
    ra = ''
    z = ''
    rcode = ''
    qdcount = ''
    ancount = ''
    nscount = ''
    arcount = ''

    def __init__(self,a,b,c,d,e,f,g,h,i,j,k,l,m):
        """初始化,16进制,ID:16;qr:1;opcode:4;aa:1;tc:1;rd:1;ra:1;z:3;rcode:4;qdcount:16;ancount:16;nscount:16;arcount:16"""
        self.ID = a
        self.qr = b
        self.opcode = c
        self.aa = d
        self.tc = e
        self.rd = f
        self.ra = g
        self.z = h
        self.rcode = i
        self.qdcount = j
        self.ancount = k
        self.nscount = l
        self.arcount = m

    def out_header(self):
        """获取包头"""
        s = ''
        for i,j in vars(self).items():
            s += j
        #print(s)
        return s

class question:
    qname = ''
    qtype = ''
    qclass = ''
    def __init__(self,a,b,c):
        self.qname = a
        self.qtype = b
        self.qclass = c

    def out_question(self):
        """获取问题部分"""
        s = ''
        for i,j in vars(self).items():
            s += j
        #print(s)
        return s
    def leng(self):
        l = self.out_question()
        return len(l)//8
class a_data:
    d_name = ''
    d_type = ''
    d_class = ''
    d_ttl = ''
    d_rdlength = ''
    d_rdata = ''
    def __init__(self,a,b,c,d,e,f):
        self.d_name = a
        self.d_type = b
        self.d_class = c
        self.d_ttl = d
        self.d_rdlength = e
        self.d_rdata = f

    def out_a_data(self):
        s = ''
        for i,j in vars(self).items():
            #print('i',i,'j:',j)
            s += j
           #print('s:',s)
        return s
    def leng(self):
        l = self.out_a_data()
        return len(l)//8
        
