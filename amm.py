# author: yebof
#
# AMM simulator

import math
import numpy as np

class Amm:
    def __init__(self, fee_rate, asset_A_amount, asset_B_amount):
        # initialize the AMM 

        self.fee_rate = fee_rate
        self.asset_A_amount = asset_A_amount
        self.asset_B_amount = asset_B_amount
        self.total_LP_token = 0
    
    def print_detailed_info(self):
        # print detailed info of the Amm 

        print("Total number of outstanding tokens: ", self.total_LP_token)
        print("A reserves: ", self.asset_A_amount)
        print("B reserves: ", self.asset_B_amount)
        print("Transaction fee:", self.fee_rate)


class Uniswap_amm(Amm):

    def __init__(self, fee_rate, asset_A_amount, asset_B_amount, initial_LP_token_number):
        # initialize the Uniswap_amm

        super(Uniswap_amm, self).__init__(fee_rate, asset_A_amount, asset_B_amount)
        self.total_LP_token = initial_LP_token_number
        self.constant = self.asset_A_amount * self.asset_B_amount
    
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
        # return the reference/spot price (float) for this type of asset

        trans_fee_multiplier = 1 / (1-self.fee_rate)

        if asset_type == 'A':
            return self.asset_B_amount/self.asset_A_amount * trans_fee_multiplier
        elif asset_type == 'B':
            return self.asset_A_amount/self.asset_B_amount * trans_fee_multiplier
        else:
            raise Exception("Wrong input! Enter eithor A or B!")

    def swap(self, target_asset_type, amount, SP_price):
        # input the type of asset you want to buy (str: 'A' or 'B'),
        # the amount of that asset (float)
        # and the reference/spot price (float) for that

        # return the final price and slippage 

        # dx = Xdy/(Y-dy)

        if target_asset_type == 'A':
            # you need to pay B in this case 
            amount_without_fee = self.asset_B_amount * amount / (self.asset_A_amount - amount)
            # update the pool
            self.asset_A_amount -= amount
            self.asset_B_amount += amount_without_fee
            # swap fee 
            fee = amount_without_fee * self.fee_rate
            final_amount = amount_without_fee + fee
            # deposit the swap fee to the pool 
            self.asset_B_amount += fee
            self.constant = self.asset_A_amount * self.asset_B_amount

        elif target_asset_type == 'B':
            # you need to pay A in this case 
            amount_without_fee = self.asset_A_amount * amount / (self.asset_B_amount - amount)
            # update the pool
            self.asset_A_amount += amount_without_fee
            self.asset_B_amount -= amount
            # swap fee
            fee = amount_without_fee * self.fee_rate
            final_amount = amount_without_fee + fee
            # deposit the swap fee to the pool 
            self.asset_A_amount += fee
            self.constant = self.asset_A_amount * self.asset_B_amount

        else:
            raise Exception("Wrong input! Enter eithor A or B!")
        
        effective_price = final_amount/amount
        slippage = (effective_price - SP_price) / SP_price
        
        return final_amount, slippage


class XRPL_amm(Amm):

    def __init__(self, fee_rate, asset_A_amount, asset_B_amount, weight_A, weight_B):
        # initialize the XRPL amm

        super(XRPL_amm, self).__init__(fee_rate, asset_A_amount, asset_B_amount)

        self.weight_A = weight_A
        self.weight_B = weight_B
        # according to equation I: 
        self.constant = (self.asset_A_amount ** 0.5) * (self.asset_B_amount ** 0.5)
        self.total_LP_token = (self.asset_A_amount ** 0.5) * (self.asset_B_amount ** 0.5)
    
    def deposite_all(self, type_of_added_asset, amount_of_added_asset):
        # input the type of asset to deposit (str: 'A' or 'B') and the amount of the asset (float)
        # return the amount of another type of asset (float) to deposit and the number of returned LP tokens (float)

        # db = Bda/A
        # da = Adb/B
        if type_of_added_asset == 'A':
            amount_of_added_B_asset = self.asset_B_amount * amount_of_added_asset / self.asset_A_amount
            
            number_of_new_tokens = amount_of_added_asset / self.asset_A_amount * self.total_LP_token
            
            self.asset_A_amount += amount_of_added_asset
            self.asset_B_amount += amount_of_added_B_asset
            self.total_LP_token += number_of_new_tokens

            return amount_of_added_B_asset, number_of_new_tokens

        elif type_of_added_asset == 'B':
            amount_of_added_A_asset = self.asset_A_amount * amount_of_added_asset / self.asset_B_amount

            number_of_new_tokens = amount_of_added_asset / self.asset_B_amount * self.total_LP_token
            

            self.asset_B_amount += amount_of_added_asset
            self.asset_A_amount += amount_of_added_A_asset
            self.total_LP_token += number_of_new_tokens

            return amount_of_added_A_asset, number_of_new_tokens

        else:
            raise Exception("Wrong input! Enter eithor A or B for asset type!")
    
    def deposite_single(self, type_of_added_asset, amount_of_added_asset):
        # input the type of asset to deposit (str: 'A' or 'B') and the amount of the asset (float)
        # return the amount of returned LP tokens (float)

        if type_of_added_asset == 'A':
            number_of_new_tokens = self.total_LP_token * ( (1+(amount_of_added_asset - self.fee_rate * (1-self.weight_A)*amount_of_added_asset)/self.asset_A_amount)**self.weight_A - 1 )
            self.asset_A_amount += amount_of_added_asset
            self.total_LP_token += number_of_new_tokens

            return number_of_new_tokens

        elif type_of_added_asset == 'B':
            number_of_new_tokens = self.total_LP_token * ( (1+(amount_of_added_asset - self.fee_rate * (1-self.weight_B)*amount_of_added_asset)/self.asset_B_amount)**self.weight_B - 1 )
            self.asset_B_amount += amount_of_added_asset
            self.total_LP_token += number_of_new_tokens

            return number_of_new_tokens

        else:
            raise Exception("Wrong input! Enter eithor A or B for asset type!")
    
    def withdraw_all(self, amount_of_tokens):
        # input the amount of LP tokens you want ot withdraw (float)
        # return the amount of asset A (float) and asset B (float) you can get

        asset_A_return = amount_of_tokens / self.total_LP_token * self.asset_A_amount
        asset_B_return = amount_of_tokens / self.total_LP_token * self.asset_B_amount

        self.asset_A_amount -= asset_A_return
        self.asset_B_amount -= asset_B_return
        self.total_LP_token -= amount_of_tokens

        return asset_A_return, asset_B_return
    
    def withdraw_single(self, type_of_added_asset, amount_of_tokens):
        # input type of asset (str: 'A' or 'B') and the amount of LP tokens you want ot withdraw (float)
        # return the amount of asset (float) you can get

        if type_of_added_asset == 'A':
            asset_return = self.asset_A_amount * (1-(1-amount_of_tokens/self.total_LP_token)**(1/self.weight_A)) * (1-(1-self.weight_A)*self.fee_rate)

            self.asset_A_amount -= asset_return
            self.total_LP_token -= amount_of_tokens

            return asset_return

        elif type_of_added_asset == 'B':
            asset_return = self.asset_B_amount * (1-(1-amount_of_tokens/self.total_LP_token)**(1/self.weight_B)) * (1-(1-self.weight_B)*self.fee_rate)

            self.asset_B_amount -= asset_return
            self.total_LP_token -= amount_of_tokens

            return asset_return

        else:
            raise Exception("Wrong input! Enter eithor A or B for asset type!")

    def check_SP_price(self, asset_type):
        # input the asset type (str: 'A' or 'B')
        # return the reference/spot price (float) for this type of asset

        trans_fee_multiplier = 1 / (1-self.fee_rate)

        if asset_type == 'A':
            return (self.asset_B_amount/self.weight_B) / (self.asset_A_amount/self.weight_A) * trans_fee_multiplier
        elif asset_type == 'B':
            return (self.asset_A_amount/self.weight_A) / (self.asset_B_amount/self.weight_B) * trans_fee_multiplier
        else:
            raise Exception("Wrong input! Enter eithor A or B!")
    
    def swap(self, target_asset_type, amount, SP_price):
        # input the type of asset you want to buy (str: 'A' or 'B'),
        # the amount of that asset (float)
        # and the reference/spot price (float) for that

        # return the final price and slippage 
        if target_asset_type == 'A':
            final_amount = self.asset_B_amount * ((self.asset_A_amount/(self.asset_A_amount-amount))**(self.weight_A/self.weight_B)-1)*(1/(1-self.fee_rate))

            self.asset_A_amount -= amount
            self.asset_B_amount += final_amount

        elif target_asset_type == 'B':
            final_amount = self.asset_A_amount * ((self.asset_B_amount/(self.asset_B_amount-amount))**(self.weight_B/self.weight_A)-1)*(1/(1-self.fee_rate))

            self.asset_B_amount -= amount
            self.asset_A_amount += final_amount

        else:
            raise Exception("Wrong input! Enter eithor A or B!")
        
        effective_price = final_amount/amount
        slippage = (effective_price - SP_price) / SP_price

        return final_amount, slippage


class Balancer_amm(Amm):

    def __init__(self, fee_rate, asset_A_amount, asset_B_amount, LP_token_number):
        # initialize the Balancer_amm

        super(Balancer_amm, self).__init__(fee_rate, asset_A_amount, asset_B_amount, LP_token_number)
