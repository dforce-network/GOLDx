#!/usr/bin/python3
from brownie import rpc, Wei

import pytest
import brownie
from brownie import Wei
from decimal import *
import math
import random

# fix decimal
getcontext().prec = 27

mint_selector = 0x40c10f19
burn_selector = 0x9dc29fac
transfer_selector = 0xa9059cbb
transferFrom_selector = 0x23b872dd
function_fee = 0.001e18

# 2**256-1
max_allowance = 115792089237316195423570985008687907853269984665640564039457584007913129639935
BASE = Decimal(10 ** 18)
zero_address = '0x0000000000000000000000000000000000000000'
without_paxg_fee = 0.99998e18

def rpc_delay(rpc, interval):
    rpc.sleep(interval)
    rpc.mine(interval)

def rdiv(x, y):
    return math.floor(Decimal(x) * BASE / Decimal(y))

def rmul(x, y):
    return math.floor(Decimal(x) * Decimal(y) / BASE)

def reset_fee(goldx):
    goldx.setFee(mint_selector, 0)
    goldx.setFee(burn_selector, 0)
    goldx.setFee(transfer_selector, 0)
    goldx.setFee(transferFrom_selector, 0)
    assert goldx.fee(mint_selector) == 0
    assert goldx.fee(burn_selector) == 0
    assert goldx.fee(transfer_selector) == 0
    assert goldx.fee(transferFrom_selector) == 0

def randomly_mint_and_burn(paxg, goldx, accounts, loop_times):
    for i in range(1, 6):
        paxg.approve(goldx.address, max_allowance, {'from': accounts[i]})
        goldx.mint(accounts[i], 1000000e18, {'from': accounts[i]})

    current_times = 1
    while current_times <= loop_times:
        current_times += 1
        random_user = accounts[random.randint(1, 5)]
        # print(f'random_user is:', random_user)
        random_receiver = accounts[random.randint(1, 5)]

        random_amount = math.floor(random.random() * 10**18)

        function_index = random.randint(0, 2)

        if (function_index == 0):
            goldx.mint(random_user, random_amount, {'from': random_user})
        elif (function_index == 1):
            goldx.burn(random_user, random_amount, {'from': random_user})
        elif (function_index == 2):
            goldx.transfer(random_receiver, random_amount, {'from': random_user})

    after_loop_goldx_total_amount = goldx.totalSupply()
    assert after_loop_goldx_total_amount > 0

    for i in range(1, 6):
        account_balance = goldx.balanceOf(accounts[i])
        goldx.burn(accounts[i], account_balance, {'from': accounts[i]})
        assert goldx.balanceOf(accounts[i]) == 0

def replace_underlying(goldx, new_paxg, paxg, rpc, accounts):
    interval = 60
    upgradeTime = rpc.time() + interval
    upgradeToken = new_paxg.address
    upgradeUint = 1.05e18
    upgradeMinMintAmount = 0.001e18
    upgradeMinBurnAmount = 0.001e18

    goldx.upgradeProtocol(upgradeTime, upgradeToken, upgradeUint, upgradeMinMintAmount, upgradeMinBurnAmount)

    rpc_delay(rpc, interval + 1)

    goldx.removeReserve()

    should_add_new_reserve_amount = goldx.getOutstanding(new_paxg.address, upgradeUint)

    new_paxg.transfer(goldx.address, (should_add_new_reserve_amount + 10**new_paxg.decimals()))

    goldx.confirmUpgrade()

def test_mint_then_burn_all_without_fee_with_same_decimal(goldx, paxg, rpc, accounts):
    print(f'---------------- start to mint then burn all ----------------\n')
    reset_fee(goldx)
    loop_times = 10
    randomly_mint_and_burn(paxg, goldx, accounts, loop_times)

    final_goldx_total_amount = goldx.totalSupply()
    assert final_goldx_total_amount == 0
    print(f'---------------- end to mint then burn all ----------------\n')

def test_mint_then_burn_all_with_fee_with_same_decimal(goldx, paxg, rpc, accounts):
    print(f'---------------- start to mint then burn all ----------------\n')
    loop_times = 10
    randomly_mint_and_burn(paxg, goldx, accounts, loop_times)

    final_goldx_total_amount = goldx.totalSupply()

    assert final_goldx_total_amount > 0

    # burn all fee receiver balance
    account_balance = goldx.balanceOf(accounts[0])
    goldx.burn(accounts[0], account_balance, {'from': accounts[0]})
    assert goldx.balanceOf(accounts[0]) > 0

    print(f'---------------- end to mint then burn all ----------------\n')

def test_mint_then_burn_all_without_fee_with_different_decimal(goldx, paxg, new_paxg_6, rpc, accounts):
    print(f'---------------- start to mint then burn all with different decimal ----------------\n')
    replace_underlying(goldx, new_paxg_6, paxg, rpc, accounts)
    reset_fee(goldx)
    loop_times = 10
    randomly_mint_and_burn(new_paxg_6, goldx, accounts, loop_times)

    final_goldx_total_amount = goldx.totalSupply()
    assert final_goldx_total_amount == 0
    print(f'---------------- end to mint then burn all with different decimal ----------------\n')

def test_mint_then_burn_all_with_fee_with_different_decimal(goldx, paxg, rpc, accounts):
    print(f'---------------- start to mint then burn all with different decimal ----------------\n')

    loop_times = 10
    randomly_mint_and_burn(paxg, goldx, accounts, loop_times)

    final_goldx_total_amount = goldx.totalSupply()

    assert final_goldx_total_amount > 0

    # burn all fee receiver balance
    account_balance = goldx.balanceOf(accounts[0])
    goldx.burn(accounts[0], account_balance, {'from': accounts[0]})
    assert goldx.balanceOf(accounts[0]) > 0

    print(f'---------------- end to mint then burn all with different decimal ----------------\n')
