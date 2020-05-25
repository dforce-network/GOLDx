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
# test Blacklist()
# ----------------------
def test_add_then_remove_blacklist(goldx, paxg, rpc, accounts):
    print(f'---------------- start to add then remove blacklist ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    print(f'before minting, account[1] has goldx: {goldx.balanceOf(accounts[1])}')
    print(f'account[1] is going to mint 1 goldx')
    goldx.mint(accounts[1], 1e18, {'from': accounts[1]})
    print(f'after  minting, account[1] has goldx: {goldx.balanceOf(accounts[1])}\n')

    print(f'account[1] is in the blacklist: {goldx.blacklists(accounts[1])}')
    print(f'owner is going to add account[1] to the blacklist')
    goldx.addBlacklist(accounts[1])
    print(f'account[1] is in the blacklist: {goldx.blacklists(accounts[1])}\n')
    print(f'account[1] is going to mint 1 goldx when he is in the blacklist')
    with brownie.reverts("mint: Address is frozen!"):
        goldx.mint(accounts[1], 1e18, {'from': accounts[1]})
    print(f'owner is going to remove account[1] from the blacklist')
    goldx.removeBlacklist(accounts[1])
    print(f'account[1] is in the blacklist: {goldx.blacklists(accounts[1])}\n')

    print(f'account[1] is going to mint another 1 goldx')
    goldx.mint(accounts[1], 1e18, {'from': accounts[1]})
    print(f'after  minting, account[1] has goldx: {goldx.balanceOf(accounts[1])}\n')

    print(f'---------------- end to add then remove blacklist ----------------\n')

def test_wipe_balance_of_blacklist(goldx, paxg, rpc, accounts):
    print(f'---------------- start to wipe the balance when account in the blacklist ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    print(f'before minting, account[1] has goldx: {goldx.balanceOf(accounts[1])}')
    print(f'account[1] is going to mint 1 goldx')
    goldx.mint(accounts[1], 10e18, {'from': accounts[1]})
    print(f'after  minting, account[1] has goldx: {goldx.balanceOf(accounts[1])}\n')

    print(f'account[1] is in the blacklist: {goldx.blacklists(accounts[1])}')
    print(f'owner is going to add account[1] to the blacklist')
    goldx.addBlacklist(accounts[1])
    print(f'account[1] is in the blacklist: {goldx.blacklists(accounts[1])}\n')

    print(f'owner is going to wipe balance of account[1] when he is in the balcklist')
    goldx.wipeBlackAddress(accounts[1])
    print(f'after wiping balance, the balacne of goldx of account[1] is: {goldx.balanceOf(accounts[1])}')

    print(f'---------------- end to wipe the balance when account in the blacklist ----------------\n')

def test_retrieve_blacklist(goldx, paxg, rpc, accounts):
    print(f'---------------- start to retrieve the balance when account in the blacklist ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    print(f'before minting, account[1] has goldx: {goldx.balanceOf(accounts[1])}')
    print(f'account[1] is going to mint 1 goldx')
    goldx.mint(accounts[1], 10e18, {'from': accounts[1]})
    before_user1_goldx_balance = goldx.balanceOf(accounts[1])
    print(f'after  minting, account[1] has goldx: {before_user1_goldx_balance}\n')

    print(f'account[1] is in the blacklist: {goldx.blacklists(accounts[1])}')
    print(f'owner is going to add account[1] to the blacklist')
    goldx.addBlacklist(accounts[1])
    print(f'account[1] is in the blacklist: {goldx.blacklists(accounts[1])}\n')

    before_retrive_owner_goldx_balance = goldx.balanceOf(accounts[0])
    print(f'before retriving, the balance of goldx of owner is: {before_retrive_owner_goldx_balance}')

    print(f'owner is going to retrieve balance of account[1] when he is in the balcklist')
    goldx.retrieveBlackAddress(accounts[1])
    after_user1_goldx_balance = goldx.balanceOf(accounts[1])
    print(f'after retriving balance, the balacne of goldx of account[1] is: {after_user1_goldx_balance}')
    assert after_user1_goldx_balance == 0

    after_retrive_owner_goldx_balance = goldx.balanceOf(accounts[0])
    print(f'before retriving, the balance of goldx of owner is: {after_retrive_owner_goldx_balance}')
    owner_goldx_changing_balance = after_retrive_owner_goldx_balance - before_retrive_owner_goldx_balance

    assert owner_goldx_changing_balance == before_user1_goldx_balance

    print(f'---------------- end to retrieve the balance when account in the blacklist ----------------\n')
