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
# without_paxg_fee = 0.99998e18

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
# test upgradeProtocol()
# ----------------------
def test_upgrade_protocol(goldx, new_paxg, paxg, rpc, accounts):
    print(f'---------------- start to upgrade protocol ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})

    check_diff(goldx, paxg, 'mint', 100.078e18, accounts[0], accounts[1])
    check_diff(goldx, paxg, 'burn', 50.56909e18, accounts[0], accounts[1])
    check_diff(goldx, new_paxg, 'transfer', 32.098e18, accounts[0], accounts[1], 0, accounts[2])

    interval = 60
    upgradeTime = rpc.time() + interval
    upgradeToken = new_paxg.address
    upgradeUint = 1.05e18
    upgradeMinMintAmount = 0.001e18
    upgradeMinBurnAmount = 0.001e18

    print(f'owner is going to set upgrading config for contract')
    goldx.upgradeProtocol(upgradeTime, upgradeToken, upgradeUint, upgradeMinMintAmount, upgradeMinBurnAmount)

    rpc_delay(rpc, interval + 1)

    before_remove_goldx_amount = goldx.totalSupply()

    before_remove_owner_balance = paxg.balanceOf(accounts[0])

    before_remove_contract_reserve = paxg.balanceOf(goldx.address)

    transfer_paxg_fee = paxg.getFeeFor(before_remove_contract_reserve)

    print(f'owner is going to remove reserve of the contract\n')
    goldx.removeReserve()
    after_remove_owner_balance = paxg.balanceOf(accounts[0])

    after_remove_contract_reserve = paxg.balanceOf(goldx.address)

    assert after_remove_contract_reserve == 0
    # actually paxg and goldx should be the different owner, that is the owner should not get paxg transfering fee,
    # so it should be:
    assert after_remove_owner_balance == before_remove_owner_balance + before_remove_contract_reserve

    should_add_new_reserve_amount = goldx.getOutstanding(new_paxg.address, upgradeUint)

    decimal_diff = goldx.decimals() - new_paxg.decimals()

    expected_add_new_reserve_amount = div(rdiv(before_remove_goldx_amount, upgradeUint), 10**decimal_diff)

    print(f'expected contract adds new reserve amount is: {expected_add_new_reserve_amount}\n')
    assert expected_add_new_reserve_amount == should_add_new_reserve_amount

    print(f'owner is going to add new reserve')
    new_paxg.transfer(goldx.address, (should_add_new_reserve_amount + 10**new_paxg.decimals()))

    print(f'owner is going to confirm upgrade')
    goldx.confirmUpgrade()

    new_paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})

    mint_amount = 100.123e18
    check_diff(goldx, new_paxg, 'mint', mint_amount, accounts[0], accounts[1], upgradeUint)

    burn_amount = 10.0098e18
    check_diff(goldx, new_paxg, 'burn', burn_amount, accounts[0], accounts[1], upgradeUint)

    transfer_amount = 10.459e18
    check_diff(goldx, new_paxg, 'transfer', transfer_amount, accounts[0], accounts[1], upgradeUint, accounts[2])

    goldx.approve(accounts[2], 100e18, {'from': accounts[1]})
    goldx.transferFrom(accounts[1], accounts[2], 10e18, {'from': accounts[2]})

    print(f'---------------- end to upgrade protocol ----------------\n')

def test_upgrade_protocol_with_upgrade_time_is_zero(goldx, new_paxg, paxg, rpc, accounts):
    print(f'---------------- start to upgrade protocol with time is zero ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 100e18, {'from': accounts[1]})
    goldx.burn(accounts[1], 50e18, {'from': accounts[1]})

    interval = 60
    upgradeTime = 0
    upgradeToken = new_paxg.address
    upgradeUint = 1.05e18
    upgradeMinMintAmount = 0.001e18
    upgradeMinBurnAmount = 0.001e18

    print(f'owner is going to upgrade with time is zero')
    with brownie.reverts('upgradeProtocol: Upgrading time should be greater than 0!'):
        goldx.upgradeProtocol(upgradeTime, upgradeToken, upgradeUint, upgradeMinMintAmount, upgradeMinBurnAmount)
    print(f'---------------- end to upgrade protocol with time is zero ----------------\n')

def test_upgrade_protocol_with_upgrade_token_is_zero_address(goldx, new_paxg, paxg, rpc, accounts):
    print(f'---------------- start to upgrade protocol with tokne is zero address ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 100e18, {'from': accounts[1]})
    goldx.burn(accounts[1], 50e18, {'from': accounts[1]})

    interval = 60
    upgradeTime = rpc.time() + interval
    upgradeToken = zero_address
    upgradeUint = 1.05e18
    upgradeMinMintAmount = 0.001e18
    upgradeMinBurnAmount = 0.001e18

    print(f'owner is going to upgrade with tokne is zero address')
    with brownie.reverts('upgradeProtocol: New anchored asset should not be zero address!'):
        goldx.upgradeProtocol(upgradeTime, upgradeToken, upgradeUint, upgradeMinMintAmount, upgradeMinBurnAmount)
    print(f'---------------- end to upgrade protocol with tokne is zero address ----------------\n')

def test_remove_reserve_when_do_not_reach_time(goldx, new_paxg, paxg, rpc, accounts):
    print(f'---------------- start to remove reserve but does not reach time ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 100e18, {'from': accounts[1]})
    goldx.burn(accounts[1], 50e18, {'from': accounts[1]})

    with brownie.reverts('removeReserve: Too early to remove reserve!'):
        goldx.removeReserve()

    interval = 60
    upgradeTime = rpc.time() + interval
    upgradeToken = new_paxg.address
    upgradeUint = 1.05e18
    upgradeMinMintAmount = 0.001e18
    upgradeMinBurnAmount = 0.001e18

    goldx.upgradeProtocol(upgradeTime, upgradeToken, upgradeUint, upgradeMinMintAmount, upgradeMinBurnAmount)
    with brownie.reverts('removeReserve: Too early to remove reserve!'):
        goldx.removeReserve()
    print(f'owner is going to remove reserve but does not reach time')
    print(f'---------------- end to remove reserve but does not reach time ----------------\n')

def test_confirm_upgrade_when_do_not_reach_time(goldx, new_paxg, paxg, rpc, accounts):
    print(f'---------------- start to confirm upgrade but does not reach time ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 100e18, {'from': accounts[1]})
    goldx.burn(accounts[1], 50e18, {'from': accounts[1]})

    with brownie.reverts('confirmUpgrade:  Too early to confirm upgrading!'):
        goldx.confirmUpgrade()

    interval = 60
    upgradeTime = rpc.time() + interval
    upgradeToken = new_paxg.address
    upgradeUint = 1.05e18
    upgradeMinMintAmount = 0.001e18
    upgradeMinBurnAmount = 0.001e18

    goldx.upgradeProtocol(upgradeTime, upgradeToken, upgradeUint, upgradeMinMintAmount, upgradeMinBurnAmount)
    with brownie.reverts('confirmUpgrade:  Too early to confirm upgrading!'):
        goldx.confirmUpgrade()
    print(f'owner is going to confirm upgrade but does not reach time')
    print(f'---------------- end to confirm upgrade but does not reach time ----------------\n')

def test_cancel_upgrade(goldx, new_paxg, paxg, rpc, accounts):
    print(f'---------------- start to cancel upgrade ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 100e18, {'from': accounts[1]})
    goldx.burn(accounts[1], 50e18, {'from': accounts[1]})

    goldx.cancelUpgrade()
    print(f'---------------- end to cancel upgrade ----------------\n')

def test_cancel_upgrade_when_upgrade_protocol(goldx, new_paxg, paxg, rpc, accounts):
    print(f'---------------- start to cancel upgrade when upgradeprotocol ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 100e18, {'from': accounts[1]})
    goldx.burn(accounts[1], 50e18, {'from': accounts[1]})

    interval = 60
    upgradeTime = rpc.time() + interval
    upgradeToken = new_paxg.address
    upgradeUint = 1.05e18
    upgradeMinMintAmount = 0.001e18
    upgradeMinBurnAmount = 0.001e18

    goldx.upgradeProtocol(upgradeTime, upgradeToken, upgradeUint, upgradeMinMintAmount, upgradeMinBurnAmount)

    goldx.cancelUpgrade()

    print(f'---------------- end to cancel upgrade when upgradeprotocol ----------------\n')

def test_cancel_upgrade_without_enough_new_reserve(goldx, new_paxg, paxg, rpc, accounts):
    print(f'---------------- start to cancel upgrade without enough new reserve ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 100e18, {'from': accounts[1]})
    goldx.burn(accounts[1], 50e18, {'from': accounts[1]})

    interval = 60
    upgradeTime = rpc.time() + interval
    upgradeToken = new_paxg.address
    upgradeUint = 1.05e18
    upgradeMinMintAmount = 0.001e18
    upgradeMinBurnAmount = 0.001e18

    goldx.upgradeProtocol(upgradeTime, upgradeToken, upgradeUint, upgradeMinMintAmount, upgradeMinBurnAmount)

    rpc_delay(rpc, interval + 1)

    goldx.removeReserve()

    with brownie.reverts('cancelUpgrade: Add more current anchored asset!'):
        goldx.cancelUpgrade()

    print(f'---------------- end to cancel upgrade without enough new reserve ----------------\n')

def test_cancel_upgrade_without_enough_original_reserve(goldx, new_paxg, paxg, rpc, accounts):
    print(f'---------------- start to cancel upgrade without enough origianl reserve----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 100.001e18, {'from': accounts[1]})

    print(f'previous unit is: {goldx.unit()}')

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

    new_paxg.transfer(goldx.address, (should_add_new_reserve_amount + 10 ** new_paxg.decimals()))

    with brownie.reverts('cancelUpgrade: Add more current anchored asset!'):
        goldx.cancelUpgrade()


def test_upgrade_protocol_without_lower_decimal_reserve(goldx, new_paxg_6, paxg, rpc, accounts):
    print(f'---------------- start to upgrade protocol with lower decimal reserve ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 100.001e18, {'from': accounts[1]})

    interval = 60
    upgradeTime = rpc.time() + interval
    upgradeToken = new_paxg_6.address
    upgradeUint = 1.05e18
    upgradeMinMintAmount = 0.001e6
    upgradeMinBurnAmount = 0.001e6

    goldx.upgradeProtocol(upgradeTime, upgradeToken, upgradeUint, upgradeMinMintAmount, upgradeMinBurnAmount)
    rpc_delay(rpc, interval + 1)
    goldx.removeReserve()
    should_add_new_reserve_amount = goldx.getOutstanding(new_paxg_6.address, upgradeUint)
    new_paxg_6.transfer(goldx.address, (should_add_new_reserve_amount + 10**new_paxg_6.decimals()))
    goldx.confirmUpgrade()

    new_paxg_6.approve(goldx.address, max_allowance, {'from': accounts[1]})

    mint_amount = 100.123e6
    check_diff(goldx, new_paxg_6, 'mint', mint_amount, accounts[0], accounts[1], upgradeUint, without_paxg_fee=1e18)

    burn_amount = 10.0098e6
    check_diff(goldx, new_paxg_6, 'burn', burn_amount, accounts[0], accounts[1], upgradeUint, without_paxg_fee=1e18)

    transfer_amount = 10.459e6
    check_diff(goldx, new_paxg_6, 'transfer', transfer_amount, accounts[0], accounts[1], upgradeUint, accounts[2], without_paxg_fee=1e18)

    goldx.approve(accounts[2], 100e6, {'from': accounts[1]})
    goldx.transferFrom(accounts[1], accounts[2], 10.59493e6, {'from': accounts[2]})

