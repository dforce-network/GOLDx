#!/usr/bin/python3
from brownie import rpc, Wei

import pytest
import brownie
from brownie import Wei
from decimal import *

# fix decimal
getcontext().prec = 15

mint_selector = 0x40c10f19
burn_selector = 0x9dc29fac
transfer_selector = 0xa9059cbb
transferFrom_selector = 0x23b872dd

# 2**256-1
max_allowance = 115792089237316195423570985008687907853269984665640564039457584007913129639935
BASE = Decimal(10 ** 18)
zero_address = '0x0000000000000000000000000000000000000000'

def rpc_delay(rpc, interval):
    rpc.sleep(interval)
    rpc.mine(interval)


# ----------------------
# test upgradeProtocol()
# ----------------------
def test_upgrade_protocol(goldx, new_paxg, paxg, rpc, accounts):
    print(f'---------------- start to upgrade protocol ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 100e18, {'from': accounts[1]})
    goldx.burn(accounts[1], 50e18, {'from': accounts[1]})
    print(f'previous unit is: {goldx.unit()}')

    interval = 60
    upgradeTime = rpc.time() + interval
    upgradeToken = new_paxg.address
    upgradeUint = 1.05e18
    upgradeMinMintAmount = 0.001e18
    upgradeMinBurnAmount = 0.001e18

    print(f'before upgrade, contract details are: ')
    print(f'upgradeTime is {goldx.upgradeTime()}')
    print(f'pendingToken is {goldx.pendingToken()}')
    print(f'pendingUnit is {goldx.pendingUnit()}')
    print(f'pendingMinMintAmount is {goldx.pendingMinMintAmount()}')
    print(f'pendingMinBurnAmount is {goldx.pendingMinBurnAmount()}\n')
    print(f'owner is going to set upgrading config for contract')
    goldx.upgradeProtocol(upgradeTime, upgradeToken, upgradeUint, upgradeMinMintAmount, upgradeMinBurnAmount)
    print(f'after  upgrade, contract details are: ')
    print(f'upgradeTime is {goldx.upgradeTime()}')
    print(f'pendingToken is {goldx.pendingToken()}')
    print(f'pendingUnit is {goldx.pendingUnit()}')
    print(f'pendingMinMintAmount is {goldx.pendingMinMintAmount()}')
    print(f'pendingMinBurnAmount is {goldx.pendingMinBurnAmount()}\n')

    rpc_delay(rpc, interval + 1)
    print(f'current time is: {rpc.time()}')
    before_remove_goldx_amount = Decimal(goldx.totalSupply())
    print(f'before removing, contract has goldx is: {before_remove_goldx_amount}')
    before_remove_owner_balance = paxg.balanceOf(accounts[0])
    print(f'the balance of paxg of owner is: {before_remove_owner_balance}')
    before_remove_contract_reserve = paxg.balanceOf(goldx.address)
    print(f'before removing reserve, contract has reserve: {before_remove_contract_reserve}\n')
    print(f'owner is going to remove reserve of the contract\n')
    goldx.removeReserve()
    after_remove_owner_balance = paxg.balanceOf(accounts[0])
    print(f'the balance of paxg of owner is: {after_remove_owner_balance}')
    after_remove_contract_reserve = paxg.balanceOf(goldx.address)
    print(f'after removing reserve, contract has reserve: {after_remove_contract_reserve}\n')
    assert after_remove_contract_reserve == 0
    assert after_remove_owner_balance == before_remove_owner_balance + before_remove_contract_reserve

    should_add_new_reserve_amount = goldx.getOutstanding(new_paxg.address, upgradeUint)
    print(f'should add new reserve amount is: {should_add_new_reserve_amount}\n')
    expected_add_new_reserve_amount = int(before_remove_goldx_amount / Decimal(upgradeUint) * Decimal(10**new_paxg.decimals()))
    print(f'expected contract adds new reserve amount is: {expected_add_new_reserve_amount}\n')
    assert expected_add_new_reserve_amount == should_add_new_reserve_amount

    print(f'before add new reserve, contract has new reserve: {new_paxg.balanceOf(goldx.address)}')
    print(f'owner is going to add new reserve')
    new_paxg.transfer(goldx.address, (should_add_new_reserve_amount + 10**new_paxg.decimals()))
    print(f'after add new reserve, contract has new reserve: {new_paxg.balanceOf(goldx.address)}\n')

    print(f'owner is going to confirm upgrade')
    goldx.confirmUpgrade()
    print(f'after confirm, contract details are: ')
    print(f'upgradeTime is {goldx.upgradeTime()}')
    print(f'pendingToken is {goldx.pendingToken()}')
    print(f'pendingUnit is {goldx.pendingUnit()}')
    print(f'pendingMinMintAmount is {goldx.pendingMinMintAmount()}')
    print(f'pendingMinBurnAmount is {goldx.pendingMinBurnAmount()}\n')

    print(f'---------------- end to upgrade protocol ----------------\n')

def test_upgrade_protocol_then_burn(goldx, new_paxg, paxg, rpc, accounts):
    print(f'---------------- start to upgrade protocol ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    paxg.approve(goldx.address, max_allowance, {'from': accounts[2]})
    paxg.approve(goldx.address, max_allowance, {'from': accounts[3]})
    goldx.mint(accounts[1], 100.001e18, {'from': accounts[1]})
    goldx.mint(accounts[2], 2.36985e18, {'from': accounts[2]})
    goldx.mint(accounts[3], 26.569852e18, {'from': accounts[3]})

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

    new_paxg.transfer(goldx.address, (should_add_new_reserve_amount + 10**new_paxg.decimals()))

    goldx.confirmUpgrade()

    for i in range(1, 4):
        before_balance = goldx.balanceOf(accounts[i])
        print(f'before burn, the balance of goldx of account[{i}] has: {before_balance}')
        goldx.burn(accounts[i], before_balance, {'from': accounts[i]})
        after_balance = goldx.balanceOf(accounts[i])
        print(f'after burn, the balance of goldx of account[{i}] has: {after_balance}\n')


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

# def test_confirm_upgrade_when_do_not_reach_time(goldx, new_paxg, paxg, rpc, accounts):
#     print(f'---------------- start to confirm upgrade but does not reach time ----------------\n')

#     goldx.confirmUpgrade()
#     print(f'owner is going to confirm upgrade but does not reach time')
#     print(f'---------------- end to confirm upgrade but does not reach time ----------------\n')
