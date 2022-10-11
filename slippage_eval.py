# author: yebof
#
# For evaluating the slippage

import amm as amms
import trans_generator as tg
import os

def save_list_to_file_linebyline(list, filename):
    # read the file name 
    dirname = os.path.dirname(__file__)
    absolute_filename = os.path.join(dirname, filename)

    with open(absolute_filename, 'w') as list_file:
        for i in list:
            list_file.write(str(i)+'\n')

if __name__ == "__main__":
    print("evaluaing")

    # create the amm instances 
    xrpl_amm = amms.XRPL_amm(0.003, 600000, 180000, 0.5, 0.5)
    uniswap_amm = amms.Uniswap_amm(0.003, 600000, 180000, 100)

    # read the transactions 
    trans_list = tg.read_list_from_file_linebyline("transaction_list.txt")
    trans_list.append([12,"A",1])
    print(trans_list)

    # measure the slippage 
    xrpl_slippage = []
    uniswap_slippage = []

    xrpl_block = []
    uniswap_block = []
    for i in trans_list:
        time_index = i[0]
        if time_index == 0:
            xrpl_block.append(i)
            uniswap_block.append(i)
        else:
            if time_index % 4 == 0:
                xrpl_spot_price_A = xrpl_amm.check_SP_price('A')
                xrpl_spot_price_B = xrpl_amm.check_SP_price('B')
                for j in xrpl_block:
                    final_amount, slippage = xrpl_amm.swap(j[1], j[2], xrpl_spot_price_A if j[1]=='A' else xrpl_spot_price_B)
                    xrpl_slippage.append(slippage)
                xrpl_block = []
            if time_index % 12 == 0:
                uniswap_spot_price_A = uniswap_amm.check_SP_price("A")
                uniswap_spot_price_B = uniswap_amm.check_SP_price("B")
                for k in uniswap_block:
                    final_amount, slippage = uniswap_amm.swap(j[1], j[2], uniswap_spot_price_A if j[1]=='A' else uniswap_spot_price_B)
                    uniswap_slippage.append(slippage)
                uniswap_block = []
            xrpl_block.append(i)
            uniswap_block.append(i)
    
    print(xrpl_slippage)
    print(uniswap_slippage)
    save_list_to_file_linebyline(xrpl_slippage, "xrpl_slippage.txt")
    save_list_to_file_linebyline(uniswap_slippage, "uniswap_slippage.txt")
