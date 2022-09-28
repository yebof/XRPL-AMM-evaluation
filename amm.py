# author: yebof
#
# AMM simulator

import math
import numpy as np

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

            # S = (L1-L0)/L0 * T
            total_liquidity_after = self.total_liquidity()
            number_of_new_tokens = (total_liquidity_after - total_liquidity_before)/total_liquidity_before * self.total_LP_token
            self.total_LP_token += number_of_new_tokens
            return amount_of_added_B_asset, number_of_new_tokens

        elif type_of_added_asset == 'B':
            amount_of_added_A_asset = self.asset_A_amount * amount_of_added_asset / self.asset_B_amount
            self.asset_B_amount += amount_of_added_asset
            self.asset_A_amount += amount_of_added_A_asset

            # S = (L1-L0)/L0 * T
            total_liquidity_after = self.total_liquidity()
            number_of_new_tokens = (total_liquidity_after - total_liquidity_before)/total_liquidity_before * self.total_LP_token
            self.total_LP_token += number_of_new_tokens
            return amount_of_added_A_asset, number_of_new_tokens

        else:
            raise Exception("Wrong input! Enter eithor A or B for asset type!")
    
    def withdraw(self, LP_tokens_to_burn):
        # input the number of LP tokens (float) to burn 
        # return the number of token A (float) and B (float) to withdraw

        # dx = X * S/T
        # dy = Y * S/T
        A_to_withdraw = self.asset_A_amount * LP_tokens_to_burn / self.total_LP_token
        B_to_withdraw = self.asset_B_amount * LP_tokens_to_burn / self.total_LP_token

        # update the AMM
        self.asset_A_amount -= A_to_withdraw
        self.asset_B_amount -= B_to_withdraw
        self.total_LP_token -= LP_tokens_to_burn

        return A_to_withdraw, B_to_withdraw
    
    def check_SP_price(self, asset_type):
        # input the asset type (str: 'A' or 'B')
        # return the reference price (float) for this type of asset

        # TODO!!!!!!!!!!!!!

        if asset_type == 'A':
            return self.asset_B_amount/self.asset_A_amount
        elif asset_type == 'B':
            return self.asset_A_amount/self.asset_B_amount
        else:
            raise Exception("Wrong input! Enter eithor A or B!")




class XRPL_amm:

    def __init__(self, fee_rate, asset_A_amount, asset_B_amount, LP_token_number):
        # initialize the AMM 

        self.fee_rate = fee_rate
        self.asset_A_amount = asset_A_amount
        self.asset_B_amount = asset_B_amount
        self.constant = self.asset_A_amount * self.asset_B_amount
        self.total_LP_token = LP_token_number