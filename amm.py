# author: yebof
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
    
    def deposite(self, type_of_added_asset, amount_of_added_asset):
        # input the type of asset to deposit (str: 'A' or 'B') and the amount of the asset (float)
        # return the amount of another type of asset (float) to deposit and the number of returned LP tokens (float)
        
        total_liquidity_before = self.total_liquidity()

        # db = Bda/A
        # da = Adb/B
        if type_of_added_asset == 'A':
            amount_of_added_B_asset = self.asset_B_amount * amount_of_added_asset / self.asset_A_amount
            self.asset_A_amount += amount_of_added_asset
            self.asset_B_amount += amount_of_added_B_asset

            total_liquidity_after = self.total_liquidity()
            number_of_new_tokens = (total_liquidity_after - total_liquidity_before)/total_liquidity_before * self.total_LP_token
            self.total_LP_token += number_of_new_tokens
            return amount_of_added_B_asset, number_of_new_tokens

        elif type_of_added_asset == 'B':
            amount_of_added_A_asset = self.asset_A_amount * amount_of_added_asset / self.asset_B_amount
            self.asset_B_amount += amount_of_added_asset
            self.asset_A_amount += amount_of_added_A_asset

            total_liquidity_after = self.total_liquidity()
            number_of_new_tokens = (total_liquidity_after - total_liquidity_before)/total_liquidity_before * self.total_LP_token
            self.total_LP_token += number_of_new_tokens
            return amount_of_added_A_asset, number_of_new_tokens

        else:
            raise Exception("Wrong input! Enter eithor A or B for asset type!")
    
    def withdraw(self, LP_tokens_to_burn):
        # TODO 
        return 0
    
    def check_SP_price(self, asset_type):
        # input the asset type (str: 'A' or 'B')
        # return the reference price (float) for this type of asset

        if asset_type == 'A':
            return self.asset_B_amount/self.asset_A_amount
        elif asset_type == 'B':
            return self.asset_A_amount/self.asset_B_amount
        else:
            raise Exception("Wrong input! Enter eithor A or B!")