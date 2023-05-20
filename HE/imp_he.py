from phe import paillier
import time
import libnum
import gmpy2 as gy
import math
import numpy as np


s = 1
r = 11
k = 3
padding =3
total_len = padding + s + r + k


def Encode(public_key,m):
    cipher_text = public_key.encrypt(m)
    return cipher_text

def Decode(private_key,cipher):
    decrypt_text = private_key.decrypt(cipher)
    return decrypt_text

def bitreverse(bin_x):
    res = ''
    for i in range(len(bin_x)):
        if bin_x[i] == '0':
            res += '1'
        else:
            res += '0'
    return res

def Q_1(x):

    if x[padding] == '1':  
        x = int(x,2)
        res = x % (1 << (r + k))
        res = res - (1 << (r+k))
    else:
        x = int(x,2)
        res = x % (1 << (r + k))
    return res  / (1 << r)

def reset(plain):
    res = []
    num_elem = len(plain) // (padding + s + k + r)
    
    for i in range(num_elem):
        tmp = plain[i*total_len:(i+1)*total_len]
        res.append(round(Q_1(tmp),3))
    return res

def quantification(x,x_len):
    bin_x = bin(int((1 << r) * x))
    
    return bin_x[2:].zfill(x_len) if x  >= 0 else bin_x[3:].zfill(x_len)

def complement(x):
    bin_x = quantification(x,r+k)
    if x >= 0:
        return '0'* (padding + s) + bin_x
    
    else:
        com_x = '0' * padding + '1' * s + bin(int(bitreverse(bin_x),2) + 1)[2:]
        return com_x

def complement_add(com_a,com_b):
    res = (int(com_a,2) + int(com_b,2)) % (1 << (r + k))
    bin_res = bin(res)[2:].zfill(s+r+k)
    if bin_res[2] == '0':
        return res
    else:
        return res - (1 << (r+k))

def Encode(public_key,m):
    cipher_text = public_key.encrypt(m)
    return cipher_text

def Decode(private_key,cipher):
    decrypt_text = private_key.decrypt(cipher)
    return decrypt_text

def worker_process(list_x):
    HE_input = ''
    for x in list_x:
        HE_input += complement(x)
    HE_output = Encode(public_key,int(HE_input,2))
    return HE_output

def BatchCrypt(text,num_elem):
    
    global k
    global total_len
    global r
    pre_total = padding + s + k + r
    k = 0
    r = pre_total - padding - s - k
    
    total_len = padding + s + r 
    HE_out = 0
    for i in range(num_worker):
        HE_out+=worker_process(text[i])
    
    plain = Decode(private_key,HE_out)
    plain = bin(plain)[2:].zfill(num_elem * (padding + s + k + r))
    res = reset(plain)
    return res

def MY_HE(text,elem):
    HE_out = 0
    for i in range(num_worker):
        HE_out+=worker_process(text[i])

    plain = Decode(private_key,HE_out)
    plain = bin(plain)[2:].zfill(elem * (padding + s + k + r))
    HE_res = reset(plain)
    return HE_res

if __name__ == '__main__':

    public_key, private_key = paillier.generate_paillier_keypair()
    num_worker = 10
    text = -1 + 2*np.random.random((50 ,160))
    num_elem = len(text[0])
    print('*'*100)
    print("Num_workers:",num_worker)
    print("Element num:",num_elem)
    print("Padding bit:",padding)
    print("Sign bit:",s)
    print("Reserved bit:",k)
    print("Quantification bit:",r)



    #***************************************    Real SUM           ***************************************************************************************/
    np.set_printoptions(precision=3)
    real_res = np.sum(text,axis = 0)
    print("Real_Value:\n",real_res)
 
    #***************************************    MY HE SUM        ***************************************************************************************/
    HE_res = MY_HE(text,num_elem)
    print("My_HE:\n",HE_res)

    #***************************************    BatchCrypt SUM        ***************************************************************************************/
    Batch_HE = BatchCrypt(text,num_elem)
    print("BatchCrypt:\n",Batch_HE)

    #***************************************     Diff MY HE       ***************************************************************************************/
    diff1 = [round((real_res[i]-HE_res[i])/num_worker,3) for i in range(num_elem)]
    print("Diff(Real-My_HE):\n",diff1)


    #***************************************     Diff BatchCrypt       ***************************************************************************************/
    diff2 = [round(real_res[i]-Batch_HE[i]/num_worker,3) for i in range(num_elem)]  
    print("Diff(Real-Batch_HE):\n",diff2)






