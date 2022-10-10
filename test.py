# author: yebof
#
# For testing
 
import amm as amms

def testcase_uniswap_1():
    new_amm = amms.Uniswap_amm(0.003, 90, 9, 36)
    print("Should be 90:")
    print(new_amm.asset_A_amount)
    print("Should be 9:")
    print(new_amm.asset_B_amount)
    print("Should be 36:")
    print(new_amm.total_LP_token)
    print("Should be 10:")
    print(new_amm.check_SP_price("B"))
    print("Should be 28.46:")
    print(new_amm.total_liquidity())
    print("Should be (1.0, 4):")
    print(new_amm.deposite('A',10))
    print("Should be (10.0, 1.0):")
    print(new_amm.withdraw(4))
    print("Should be 90:")
    print(new_amm.asset_A_amount)
    print("Should be 9:")
    print(new_amm.asset_B_amount)
    print("Should be 36:")
    print(new_amm.total_LP_token)
    new_amm.print_detailed_info()

def testcase_uniswap_2():
    new_amm = amms.Uniswap_amm(0.003, 10000, 100000, 10)
    print(new_amm.check_SP_price('B'))
    print(new_amm.swap('B',90,new_amm.check_SP_price('B')))

def testcase_xrpl_amm():
    new_amm = amms.XRPL_amm(0.003, 10000, 100000, 0.5, 0.5)
    print(new_amm.check_SP_price('B'))
    print(new_amm.swap('B',90,new_amm.check_SP_price('B')))

if __name__ == "__main__":
    print("Testing...")
    # testcase_uniswap_1()
    testcase_uniswap_2()
    testcase_xrpl_amm()