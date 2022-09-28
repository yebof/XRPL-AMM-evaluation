# author: yebof
#
# For testing
 
import amm as amms

def testcase_1_basic():
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

if __name__ == "__main__":
    print("Testing...")
    testcase_1_basic()
    