import socket
import multiprocessing
import os
import random
import time
import test_header as t_h

address1 = ('127.0.0.1',53)
address2 = ('10.3.9.4',53)

def sock(no):

    print(no)
    loc_me = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    me_buptdns = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    loc_me.bind(address1)
    #count=0
    while(True):
        time.sleep(2)
        data_q,addr_q = loc_me.recvfrom(2048)#固定从53收
    	
        u,h,q = t_h.init_q(data_q)
        #print('\n\nu',u,'\n')

        if(u in t_h.black_dict or u in t_h.local_dict):
            data_a = t_h.get_answer(u,h,q)
            #count+=1
        else: 
            me_buptdns.sendto(data_q,address2)
            data_a,addr_a = me_buptdns.recvfrom(2048)#一次性从address2收

        address3 = ('127.0.0.1',addr_q[1])
        #print("data_q:",data_q)
        print("data_a:",data_a.hex())
        loc_me.sendto(data_a,address3)#返回回答
        print(address3)

    #print('count\n\n',count)


 
# 3表示进程池中最多有三个进程一起执行
if __name__=="__main__":
    multiprocessing.freeze_support() 
    pool=multiprocessing.Pool(3)
    for i in range(3):
        print('---%d---'%i)
        pool.apply_async(sock,(i,))
        
 
    pool.close() # 关闭进程池
    pool.join()  # 主进程在这里等待，只有子进程全部结束之后，在会开启主线程



