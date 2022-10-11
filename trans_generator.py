# author: yebof
#
# For generating transactions

import random
import os

def save_list_to_file_linebyline(list, filename):
    # read the file name 
    dirname = os.path.dirname(__file__)
    absolute_filename = os.path.join(dirname, filename)

    with open(absolute_filename, 'w') as list_file:
        for i in list:
            for j in i:
                list_file.write(str(j)+', ')
            list_file.write('\n')

def generate_time_index(length, num):
    # generate the time index for transactions 

    time_index = []
    inner_length = 1/num
    for i in range(length):
        for j in range(num):
            time_index.append(i+j*inner_length)
    return time_index

def generate_trans(time_index, A_B_ratio, A_price_range, B_price_range):

    trans_list = []
    for i in time_index:
        transaction = []
        transaction.append(i)
        if random.random() <= A_B_ratio:
            transaction.append("A")
            transaction.append(random.uniform(A_price_range[0],A_price_range[1]))
        else:
            transaction.append("B")
            transaction.append(random.uniform(B_price_range[0],B_price_range[1]))

        trans_list.append(transaction)
    return trans_list

if __name__ == "__main__":
    print("Generating transactions...")
    trans_list = generate_trans(generate_time_index(96, 4), 0.7, [10, 1000], [3, 300])
    print(trans_list)
    save_list_to_file_linebyline(trans_list, "transaction_list.txt")