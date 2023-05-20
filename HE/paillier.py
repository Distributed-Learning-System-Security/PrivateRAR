from phe import paillier
import time
import libnum
import gmpy2 as gy
import math
import numpy as np


def get_sequence(Q,nums):
    seq = []
    rs = gy.random_state(int(time.time()))
    for i in range(nums):
        seq_sum = gy.mpz(0)
        if i >= 1:
            for j in range(i):
                seq_sum += seq[j] * Q
        
        k = gy.mpz_urandomb(rs,32+i*15)
        
        while not (gy.is_prime(k) and seq_sum < k):
            k += 1
        #print("prime ",i,":",k)

        seq.append(k)
    print("素数生成完成")
    return seq


def Encode(public_key,m):
    cipher_text = public_key.encrypt(m)
    return cipher_text

def Decode(private_key,cipher):
    decrypt_text = private_key.decrypt(cipher)
    return decrypt_text


#gy.get_context().precision=100

def reset(x,primes):
    res = [0 for i in range(feature_nums)]
    X = [gy.mpz(0) for i in range(feature_nums)]
    X[feature_nums - 1] = x
    for m in range(feature_nums-1,0,-1):
        X[m-1] = X[m] % primes[m]
        #x_tmp = gy.powmod(x,1,primes[m])
        res[m] = gy.mpz(gy.div(X[m] - X[m-1],primes[m]))
    res[0] = gy.div(X[0],primes[0])
    return res

def get_sum(list_x):
    Q =  np.sum(list_x)

    print("here",Q)
    Q = math.ceil(Q)+ 1
    return Q

def get_sg(primes,list_x):
    sg = gy.mpz(0)

    for i in range(feature_nums):
        sg = sg+ primes[i] * gy.mpz(float(list_x[i]))
    return sg

import random
def generate_large_number(length):
    # 生成数字范围为0到9的随机数列表
    digits = [random.randint(0, 9) for _ in range(length)]
    # 将数字列表转换为字符串并连接起来
    number_str = ''.join(map(str, digits))
    # 将字符串转换为整数
    return int(number_str)

if __name__ == '__main__':
    public_key, private_key = paillier.generate_paillier_keypair(n_length=2048)
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # 数据
    data = [764.47,60.74]

    # 选择颜色方案
    #colors = sns.color_palette("pastel")
    colors = sns.color_palette("Set2")

    # 创建柱状图
    fig, ax = plt.subplots()
    ax.bar(['BatchCrypt', 'LayerSampling'], data, color=colors,width=0.5)

    for i, v in enumerate(data):
        ax.text(i-0.09, v*1.04 , str(v), color='black', fontsize='13')
    # 设置图表标题和坐标轴标签
    ax.set_title('Fashion MNIST Dec Time')
    ax.set_ylim(0,900)
    #ax.set_xlabel('Data')
    ax.set_ylabel('Time (h)')

    # 显示图表
    plt.show()
    


    '''
    t = 0.0654
    cipher_nums = [17136000,9794543,151798416,12061007,5609548000,3812153888]
    enc_t = 0.05036
    dec_t = 0.01813
    enc_time = []
    dec_time = []
    for i in cipher_nums:
        enc_time.append(i*enc_t/3600)
        dec_time.append(i*dec_t/3600)
    print("加密",enc_time)
    print("解密",dec_time)
    '''
    import matplotlib.pyplot as plt

    # 数据
    data1 = [0.05036, 0.01813]
    data2 = [0.00864, 0.00246]
    data3 = [0.00123, 0.00037]

    MAX_LEN = (len(str(public_key.n//3)) - 1)
    tmp = []
    nums = 1
    for i in range(nums):
        tmp.append(generate_large_number(MAX_LEN))

    c = []

    begin = time.time()
    for i in range(nums):
        c.append( Encode(public_key,tmp[i]))
    end  = time.time()

    print("一次加密用时:",(end-begin)/nums)

    begin = time.time()
    for i in range(nums):
        Decode(private_key,c[i])
    end  = time.time()       
    print("一次解密密用时:",(end-begin)/nums)
   # print("length",c1.ciphertext().bit_length())
