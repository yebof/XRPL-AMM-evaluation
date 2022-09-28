# yebof
#
# AMM simulator

import math

class Uniswap_amm:

    def __init__(self, fee_rate, asset_A_amount, asset_B_amount, LP_token_number):
        # initialize the AMM 

        self.fee_rate = fee_rate
        self.asset_A_amount = asset_A_amount
        self.asset_B_amount = asset_B_amount
        self.constant = self.asset_A_amount * self.asset_B_amount
        self.total_LP_token = LP_token_number
    
    def total_liquidity(self):
        # Here, use sqrt(XY) to calculate the total liquidity
        # Output: float 
        return math.sqrt(self.asset_A_amount * self.asset_B_amount)
    
    def add_liquidity(self, type_of_added_asset, amount_of_added_asset):
        
        total_liquidity_before = self.total_liquidity()

        # db = Bda/A
        # da = Adb/B
        if type_of_added_asset == 'A':
            self.asset_A_amount += amount_of_added_asset
            amount_of_added_B_asset = self.asset_B_amount * amount_of_added_asset / self.asset_A_amount
            self.asset_B_amount += amount_of_added_B_asset
        elif type_of_added_asset == 'B':
            self.asset_B_amount += amount_of_added_asset
            amount_of_added_A_asset = self.asset_A_amount * amount_of_added_asset / self.asset_B_amount
            self.asset_A_amount += amount_of_added_A_asset
        else:
            raise Exception("Wrong input! Enter eithor A or B for asset type!")
    
    def check_SP_price(self, asset_type):
        # input the asset type (str: 'A' or 'B')
        # return the reference price (float) for this type of asset

        if asset_type == 'A':
            return self.asset_B_amount/self.asset_A_amount
        elif asset_type == 'B':
            return self.asset_A_amount/self.asset_B_amount
        else:
            raise Exception("Wrong input! Enter eithor A or B!")