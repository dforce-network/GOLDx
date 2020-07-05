#!/usr/bin/python3
from brownie import rpc, Wei

import pytest
import brownie
from brownie import Wei
from decimal import *
import math

# fix decimal
getcontext().prec = 72

mint_selector = 0x40c10f19
burn_selector = 0x9dc29fac
transfer_selector = 0xa9059cbb
transferFrom_selector = 0x23b872dd

# 2**256-1
max_allowance = 115792089237316195423570985008687907853269984665640564039457584007913129639935
BASE = Decimal(10 ** 18)
zero_address = '0x0000000000000000000000000000000000000000'
exchange_rate = 31103476800000000000
sub_paxg_fee = 0.99998e18  # 1-20/10**6
sub_goldx_fee = 0.999e18 # 1-0.001e18

def rpc_delay(rpc, interval):
    rpc.sleep(interval)
    rpc.mine(interval)

def div(x, y):
    return math.floor(Decimal(x) / Decimal(y))

def mul(x, y):
    return math.floor(Decimal(x) * Decimal(y))

def rdiv(x, y):
    return math.floor(Decimal(x) * BASE / Decimal(y))

def rmul(x, y):
    return math.floor(Decimal(x) * Decimal(y) / BASE)

def convert_by_decimals(src_decimal, dst_decimal, amount):
    if (src_decimal > dst_decimal):
        return div(amount, 10 ** (src_decimal - dst_decimal))
    elif (src_decimal == dst_decimal):
        return rmul(amount, 10 ** 18)
    else:
        return mul(amount, 10**(dst_decimal - src_decimal))

def check_diff(goldx, underlying_token, function_name, amount, fee_receiver, user, exchange_rate=31103476800000000000, another_user=zero_address, without_paxg_fee=0.99998e18):
    # user balance details
    before_user_goldx_balance = goldx.balanceOf(user)
    before_user_underlying_token_balance = underlying_token.balanceOf(user)

    before_another_user_goldx_balance = goldx.balanceOf(another_user) # only for goldx transfer and transferFrom

    # cause owner will receive goldx fee
    before_owner_goldx_balance = goldx.balanceOf(fee_receiver)
    # cause owner will receive paxg fee
    before_owenr_underlying_balance = underlying_token.balanceOf(fee_receiver)

    # goldx contract details
    before_goldx_total_balance = goldx.totalSupply()
    before_goldx_underlying_balance = underlying_token.balanceOf(goldx.address)

    if (function_name == 'mint'):
        goldx.mint(user, amount, {'from': user})
    elif (function_name == 'burn'):
        goldx.burn(user, amount, {'from': user})
    elif (function_name == 'transfer'):
        goldx.transfer(another_user, amount, {'from': user})
    elif (function_name == 'transferFrom'):
        goldx.transferFrom(user, another_user, amount, {'from': another_user})

    after_user_goldx_balance = goldx.balanceOf(user)
    after_user_underlying_token_balance = underlying_token.balanceOf(user)

    after_another_user_goldx_balance = goldx.balanceOf(another_user)

    after_owner_goldx_balance = goldx.balanceOf(fee_receiver)
    after_owenr_underlying_balance = underlying_token.balanceOf(fee_receiver)

    after_goldx_total_balance = goldx.totalSupply()
    after_goldx_underlying_balance = underlying_token.balanceOf(goldx.address)

    if (function_name == 'mint'):
        mint_fee = goldx.fee(mint_selector)
        changed_user_balance = after_user_goldx_balance - before_user_goldx_balance
        changed_user_underlying_balance = before_user_underlying_token_balance - after_user_underlying_token_balance

        changed_goldx_total_balance = after_goldx_total_balance - before_goldx_total_balance
        changed_underlying_in_goldx = after_goldx_underlying_balance - before_goldx_underlying_balance

        changed_owner_balance = after_owner_goldx_balance - before_owner_goldx_balance
        changed_owner_underlying_balance = after_owenr_underlying_balance - before_owenr_underlying_balance

        sub_paxg_fee = convert_by_decimals(underlying_token.decimals(), goldx.decimals(), rmul(amount, without_paxg_fee))

        assert changed_goldx_total_balance == rmul(sub_paxg_fee, exchange_rate)
        assert changed_owner_balance == rmul(changed_goldx_total_balance, mint_fee)
        assert changed_owner_balance + changed_user_balance == changed_goldx_total_balance
        assert changed_user_underlying_balance == amount
        assert amount == changed_underlying_in_goldx + changed_owner_underlying_balance
    elif (function_name == 'burn'):
        burn_fee = goldx.fee(burn_selector)
        changed_user_balance = before_user_goldx_balance - after_user_goldx_balance
        changed_user_underlying_balance = after_user_underlying_token_balance - before_user_underlying_token_balance

        changed_goldx_total_balance = before_goldx_total_balance - after_goldx_total_balance
        changed_underlying_in_goldx = before_goldx_underlying_balance - after_goldx_underlying_balance

        changed_owner_balance = after_owner_goldx_balance - before_owner_goldx_balance
        changed_owner_underlying_balance = after_owenr_underlying_balance - before_owenr_underlying_balance

        assert changed_owner_balance == rmul(amount, burn_fee)
        assert changed_user_balance == amount
        assert changed_user_balance == changed_goldx_total_balance + changed_owner_balance
        paxg_with_fee = convert_by_decimals(goldx.decimals(), underlying_token.decimals(), rdiv(changed_goldx_total_balance, exchange_rate))
        assert paxg_with_fee == changed_owner_underlying_balance + changed_user_underlying_balance
        # assert changed_user_underlying_balance == rmul(paxg_with_fee, without_paxg_fee)
        assert changed_owner_underlying_balance == rmul(paxg_with_fee, 0.00002e18)

        # TODO:
        if (goldx.decimals() > underlying_token.decimals()):
            assert changed_user_underlying_balance == rmul(paxg_with_fee, without_paxg_fee)
        else:
            assert changed_user_underlying_balance == rmul(paxg_with_fee, without_paxg_fee) + 1
    elif (function_name == 'transfer'):
        transfer_fee = goldx.fee(transfer_selector)
        transfer_without_fee = math.floor(1e18) - math.floor(transfer_fee)
        changed_user_balance = before_user_goldx_balance - after_user_goldx_balance
        changed_another_user_balance = after_another_user_goldx_balance - before_another_user_goldx_balance
        changed_owner_balance = after_owner_goldx_balance - before_owner_goldx_balance
        assert changed_owner_balance == rmul(amount, transfer_fee)
        assert changed_another_user_balance == math.floor(math.floor(amount) - math.floor(changed_owner_balance))
        changed_goldx_total_balance = before_goldx_total_balance - after_goldx_total_balance
        changed_underlying_in_glodx = after_goldx_underlying_balance - before_goldx_underlying_balance

        assert changed_user_balance == amount
        assert changed_user_balance == changed_another_user_balance + changed_owner_balance
        assert changed_goldx_total_balance == 0
        assert changed_owner_balance == rmul(amount, transfer_fee)
        assert changed_underlying_in_glodx == 0


# ----------------------
# test Blacklist()
# ----------------------
def test_add_then_remove_blacklist(goldx, paxg, rpc, accounts):
    print(f'---------------- start to add then remove blacklist ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    transferFrom_fee = goldx.fee(transferFrom_selector)

    mint_amount = 20e18
    check_diff(goldx, paxg, 'mint', mint_amount, accounts[0], accounts[1])

    print(f'account[1] is going to burn goldx')
    burn_amount = 10.0098e18
    check_diff(goldx, paxg, 'burn', burn_amount, accounts[0], accounts[1])

    print(f'account[1] is going to transfer 2 goldx to account[2]')

    transfer_amount = 10.459e18
    check_diff(goldx, paxg, 'transfer', transfer_amount, accounts[0], accounts[1], another_user=accounts[2])

    after_transfering_owner_balance = goldx.balanceOf(accounts[0])
    after_transfering_balance = goldx.balanceOf(accounts[1])
    after_transfering_user2_balance = goldx.balanceOf(accounts[2])

    print(f'account[1] is going to approve 2 goldx to account[2]')
    approved_amount = 2e18
    goldx.approve(accounts[2], 4e18, {'from': accounts[1]})
    goldx.transferFrom(accounts[1], accounts[2], approved_amount, {'from': accounts[2]})

    # print('transferFrom_fee is: ', transferFrom_fee)
    after_transferFrom_owner_balance = goldx.balanceOf(accounts[0])
    actual_transferFrom_fee = after_transferFrom_owner_balance - after_transfering_owner_balance
    # print(f'actual_transferFrom_fee is: ', actual_transferFrom_fee)

    after_transferFrom_balance = goldx.balanceOf(accounts[1])
    actual_user1_changed_amount = after_transfering_balance - after_transferFrom_balance
    # print(f'actual_user1_changed_amount is: ', actual_user1_changed_amount)

    after_transferFrom_user2_balance = goldx.balanceOf(accounts[2])
    actual_user2_changed_balance = after_transferFrom_user2_balance - after_transfering_user2_balance
    # print(f'actual_user2_changed_balance is: ', actual_user2_changed_balance)

    assert actual_transferFrom_fee + actual_user2_changed_balance == actual_user1_changed_amount
    assert actual_transferFrom_fee == rmul(approved_amount, transferFrom_fee)

    print(f'owner is going to add account[1] to the blacklist')
    goldx.addBlacklist(accounts[1])
    assert goldx.blacklists(accounts[1]) == True

    with brownie.reverts("mint: Address is frozen!"):
        goldx.mint(accounts[1], 1e18, {'from': accounts[1]})
    with brownie.reverts("checkPrecondition: Address is frozen!"):
        goldx.burn(accounts[1], 1e18, {'from': accounts[1]})
    with brownie.reverts("checkPrecondition: Address is frozen!"):
        goldx.transfer(accounts[2], 1e18, {'from': accounts[1]})
    with brownie.reverts("checkPrecondition: Address is frozen!"):
        goldx.transferFrom(accounts[1], accounts[2], 1e18, {'from': accounts[2]})
    print(f'owner is going to remove account[1] from the blacklist')
    goldx.removeBlacklist(accounts[1])
    assert goldx.blacklists(accounts[1]) == False

    print(f'account[1] is going to mint another 1 goldx')
    goldx.mint(accounts[1], 1e18, {'from': accounts[1]})
    goldx.burn(accounts[1], 1e18, {'from': accounts[1]})
    goldx.transfer(accounts[2], 1e18, {'from': accounts[1]})
    goldx.transferFrom(accounts[1], accounts[2], 1e18, {'from': accounts[2]})
    print(f'after  minting, account[1] has goldx: {goldx.balanceOf(accounts[1])}\n')

    print(f'---------------- end to add then remove blacklist ----------------\n')

def test_wipe_balance_of_blacklist(goldx, paxg, rpc, accounts):
    print(f'---------------- start to wipe the balance when account in the blacklist ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 10e18, {'from': accounts[1]})

    print(f'account[1] is in the blacklist: {goldx.blacklists(accounts[1])}')
    goldx.addBlacklist(accounts[1])
    assert goldx.blacklists(accounts[1]) == True

    print(f'owner is going to wipe balance of account[1] when he is in the balcklist')
    goldx.wipeBlackAddress(accounts[1])
    print(f'after wiping balance, the balacne of goldx of account[1] is: {goldx.balanceOf(accounts[1])}')
    assert goldx.balanceOf(accounts[1]) == 0

    print(f'---------------- end to wipe the balance when account in the blacklist ----------------\n')

def test_retrieve_blacklist(goldx, paxg, rpc, accounts):
    print(f'---------------- start to retrieve the balance when account in the blacklist ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    print(f'account[1] is going to mint 1 goldx')
    goldx.mint(accounts[1], 10e18, {'from': accounts[1]})
    before_user1_goldx_balance = goldx.balanceOf(accounts[1])

    print(f'account[1] is in the blacklist: {goldx.blacklists(accounts[1])}')
    goldx.addBlacklist(accounts[1])
    assert goldx.blacklists(accounts[1]) == True

    before_retrive_owner_goldx_balance = goldx.balanceOf(accounts[0])

    print(f'owner is going to retrieve balance of account[1] when he is in the balcklist')
    goldx.retrieveBlackAddress(accounts[1])
    after_user1_goldx_balance = goldx.balanceOf(accounts[1])
    print(f'after retriving balance, the balacne of goldx of account[1] is: {after_user1_goldx_balance}')
    assert after_user1_goldx_balance == 0

    after_retrive_owner_goldx_balance = goldx.balanceOf(accounts[0])
    print(f'before retriving, the balance of goldx of owner is: {after_retrive_owner_goldx_balance}')
    # cause owner will get the fee, so ignore the fee at here!
    owner_goldx_changing_balance = after_retrive_owner_goldx_balance - before_retrive_owner_goldx_balance

    assert owner_goldx_changing_balance == before_user1_goldx_balance

    print(f'---------------- end to retrieve the balance when account in the blacklist ----------------\n')
