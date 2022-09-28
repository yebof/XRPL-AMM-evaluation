# yebof
#
# AMM simulator

class uniswap_amm:

    def __init__(self, fee_rate, asset_A_reserve, asset_B_reserve):
        # initialize the AMM 

        self.fee_rate = fee_rate
        self.asset_A_reserve = asset_A_reserve
        self.asset_B_reserve = asset_B_reserve
    
    def check_price(self, asset_type):
        # input the asset type (str: 'A' or 'B')
        # return the reference price (float) for this type of asset

        if asset_type == 'A':
            return self.asset_B_reserve/self.asset_A_reserve
        elif asset_type == 'B':
            return self.asset_A_reserve/self.asset_B_reserve
        else:
            raise Exception("Wrong input! Enter eithor A or B!")