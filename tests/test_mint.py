#!/usr/bin/python3
from brownie import rpc, Wei
from brownie.test import given, strategy

import pytest
import brownie
from brownie import Wei
from decimal import *

# fix decimal
getcontext().prec = 18

mint_selector = 0x40c10f19
burn_selector = 0x9dc29fac
transfer_selector = 0xa9059cbb
transferFrom_selector = 0x23b872dd

# 2**256-1
max_allowance = 115792089237316195423570985008687907853269984665640564039457584007913129639935
BASE = Decimal(10 ** 18)

def rpc_delay(rpc, interval):
    rpc.sleep(interval)
    rpc.mine(interval)

def test_paxg(paxg, accounts):
    assert paxg.balanceOf(accounts[0]) == 5000e18
    assert paxg.balanceOf(accounts[1]) == 4000e18
    assert paxg.balanceOf(accounts[2]) == 3000e18
    assert paxg.balanceOf(accounts[3]) == 2000e18

def test_glodx(goldx, accounts):
    print('goldx  symbol is: ', goldx.symbol())

# -----------------
# test mint()
# -----------------
@pytest.mark.parametrize('amount', [1000e18, 0.001e18, 202.5e18, 0.001e18])
def test_mint_for_self(goldx, paxg, accounts, amount):
    """
    mint()
    """
    print(f'---------------- start to mint for self ----------------\n')
    mint_selector = 0x40c10f19
    uint = goldx.unit()
    valid_exchange_rate = Decimal(10 ** 18) - Decimal(paxg.getFeeFor(10 ** 18))
    without_mint_fee = Decimal(10 ** 18) - Decimal(goldx.fee(transfer_selector))
    fee_recipient = goldx.feeRecipient()

    print(f'before accounts[1] approve, the allowance is: {paxg.allowance(accounts[1], goldx.address)}')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    print(f'after  accounts[1] approve, the allowance is: {paxg.allowance(accounts[1], goldx.address)}\n')

    before_mint_user_goldx_balance = goldx.balanceOf(accounts[1])
    print(f'before minting, account[1] has goldx: {before_mint_user_goldx_balance}')
    before_mint_user_paxg_balance = paxg.balanceOf(accounts[1])
    print(f'before minting, account[1] has paxg: {before_mint_user_paxg_balance}')
    before_mint_total_supply = goldx.totalSupply()
    print(f'before minting, total supply is: {before_mint_total_supply}')
    before_mint_receipt_balance = goldx.balanceOf(fee_recipient)
    print(f'before minting, receipt has goldx: {before_mint_receipt_balance} \n')

    mint_amount = amount
    print(f'account[1] is going to mint {mint_amount} goldx')
    goldx.mint(accounts[1], mint_amount, {'from': accounts[1]})
    after_mint_user_goldx_balance = goldx.balanceOf(accounts[1])
    goldx_changing_balance = after_mint_user_goldx_balance - before_mint_user_goldx_balance
    print(f'after  minting, account[1] has goldx: {after_mint_user_goldx_balance}')
    after_mint_user_paxg_balance = paxg.balanceOf(accounts[1])
    paxg_changing_balance = after_mint_user_paxg_balance - before_mint_user_goldx_balance
    print(f'after  minting, account[1] has paxg: {paxg_changing_balance}')

    after_mint_total_supply = goldx.totalSupply()
    changing_total_supply = after_mint_total_supply - before_mint_total_supply
    print(f'after  minting, total supply is: {after_mint_total_supply}')

    after_mint_receipt_balance = goldx.balanceOf(fee_recipient)
    changing_receipt_balance = after_mint_receipt_balance - before_mint_receipt_balance
    print(f'after  minting, receipt has goldx: {after_mint_receipt_balance}\n')

    expected_goldx = Decimal(mint_amount) / BASE * Decimal(uint) / BASE * valid_exchange_rate * without_mint_fee / BASE
    assert expected_goldx == goldx_changing_balance
    assert goldx_changing_balance + changing_receipt_balance == changing_total_supply
    assert mint_amount == before_mint_user_paxg_balance - after_mint_user_paxg_balance

    print(f'---------------- end to mint for self ----------------\n')

def test_mint_for_another(goldx, paxg, accounts):
    print(f'---------------- start to mint for another account ----------------\n')
    mint_selector = 0x40c10f19
    uint = goldx.unit()
    valid_exchange_rate = Decimal(10 ** 18) - Decimal(paxg.getFeeFor(10 ** 18))
    without_mint_fee = Decimal(10 ** 18) - Decimal(goldx.fee(transfer_selector))
    fee_recipient = goldx.feeRecipient()

    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    before_mint_user1_goldx_balance = goldx.balanceOf(accounts[1])
    print(f'before minting, account[1] has goldx: {before_mint_user1_goldx_balance}')
    before_mint_user2_goldx_balance = goldx.balanceOf(accounts[2])
    print(f'before minting, account[2] has goldx: {before_mint_user2_goldx_balance}')
    before_mint_user1_paxg_balance = paxg.balanceOf(accounts[1])
    print(f'before minting, account[1] has paxg: {before_mint_user1_paxg_balance}')
    before_mint_user2_paxg_balance = paxg.balanceOf(accounts[2])
    print(f'before minting, account[2] has paxg: {before_mint_user2_paxg_balance}')

    before_mint_total_supply = goldx.totalSupply()
    print(f'before minting, total supply is: {before_mint_total_supply}')
    before_mint_receipt_balance = goldx.balanceOf(fee_recipient)
    print(f'before minting, receipt has goldx: {before_mint_receipt_balance} \n')

    mint_amount = 10e18
    print(f'account[1] is going to mint 10 goldx for account[2]')
    goldx.mint(accounts[2], mint_amount, {'from': accounts[1]})

    after_mint_user1_goldx_balance = goldx.balanceOf(accounts[1])
    print(f'after  minting, account[1] has goldx: {after_mint_user1_goldx_balance}')
    after_mint_user2_goldx_balance = goldx.balanceOf(accounts[2])
    print(f'after  minting, account[2] has goldx: {after_mint_user2_goldx_balance}\n')
    after_mint_user1_paxg_balance = paxg.balanceOf(accounts[1])
    print(f'after minting, account[1] has paxg: {after_mint_user1_paxg_balance}')
    after_mint_user2_paxg_balance = paxg.balanceOf(accounts[2])
    print(f'after minting, account[2] has paxg: {after_mint_user2_paxg_balance}\n')

    user2_goldx_changing_balance = after_mint_user2_goldx_balance - before_mint_user2_goldx_balance
    print(f'after minting, account[2] gets goldx: {user2_goldx_changing_balance}')
    user1_paxg_changing_balance = before_mint_user1_paxg_balance - after_mint_user1_paxg_balance
    print(f'after minting, account[1] costs paxg: {user1_paxg_changing_balance}')
    user2_paxg_changing_balance = after_mint_user2_paxg_balance - before_mint_user2_paxg_balance
    print(f'after minting, account[2] costs paxg: {user2_paxg_changing_balance}\n')

    after_mint_total_supply = goldx.totalSupply()
    changing_total_supply = after_mint_total_supply - before_mint_total_supply
    print(f'after  minting, total supply is: {after_mint_total_supply}\n')

    after_mint_receipt_balance = goldx.balanceOf(fee_recipient)
    changing_receipt_balance = after_mint_receipt_balance - before_mint_receipt_balance
    print(f'after  minting, receipt has goldx: {after_mint_receipt_balance}')

    expected_goldx = Decimal(mint_amount) / BASE * Decimal(uint) / BASE * valid_exchange_rate * without_mint_fee / BASE
    assert expected_goldx == user2_goldx_changing_balance
    assert user2_goldx_changing_balance + changing_receipt_balance == changing_total_supply
    assert user1_paxg_changing_balance == mint_amount
    assert user2_paxg_changing_balance == 0
    print(f'---------------- end to mint for another account ----------------\n')

def test_mint_by_blacklist(goldx, paxg, accounts):
    print(f'---------------- start to mint by blacklist ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    print(f'before minting, account[1] has goldx: {goldx.balanceOf(accounts[1])}')
    print(f'account[1] is going to mint 1 goldx')
    goldx.mint(accounts[1], 1e18, {'from': accounts[1]})
    print(f'after  minting, account[1] has goldx: {goldx.balanceOf(accounts[1])}\n')

    goldx.addBlacklist(accounts[1])
    with brownie.reverts("mint: Address is frozen!"):
        goldx.mint(accounts[1], 1e18, {'from': accounts[1]})
    print(f'---------------- end to mint by blacklist ----------------\n')

def test_mint_without_approve(goldx, paxg, accounts):
    print(f'---------------- start to mint without approve ----------------\n')
    print(f'the allowance of accounts[1] approved to contract is: {paxg.allowance(accounts[1], goldx.address)}')
    with brownie.reverts("insufficient allowance"):
        goldx.mint(accounts[1], 1e18, {'from': accounts[1]})
    print(f'---------------- end to mint without approve ----------------\n')

def test_mint_with_zero(goldx, paxg, accounts):
    print(f'---------------- start to mint with zero ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})

    with brownie.reverts('mint: Do not satisfy min minting amount!'):
        goldx.mint(accounts[1], 0, {'from': accounts[1]})
    print(f'---------------- end to mint with zero ----------------\n')

def test_mint_when_paused(goldx, paxg, accounts):
    print(f'---------------- start to mint when paused ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    print(f'contract current has paused: {goldx.paused()}')

    print(f'before minting, account[1] has goldx: {goldx.balanceOf(accounts[1])}')
    print(f'account[1] is going to mint 1 goldx')
    goldx.mint(accounts[1], 10e18, {'from': accounts[1]})
    print(f'after minting, account[1] has goldx: {goldx.balanceOf(accounts[1])}\n')

    print(f'owner is going to pause the contract')
    goldx.pause()
    print(f'contract current has paused: {goldx.paused()}\n')

    print(f'account[1] is going to mint another 1 goldx')
    with brownie.reverts('whenNotPaused: paused'):
        goldx.mint(accounts[1], 1e18, {'from': accounts[1]})

    print(f'---------------- end to mint when paused ----------------\n')

# @given(amount=strategy('uint', max_value=100e18, min_value=0.0005e18))
# def test_mint_for_self(goldx, paxg, accounts, amount):
#     """
#     mint()
#     """
#     print(f'---------------- start to mint for self ----------------\n')
#     mint_selector = 0x40c10f19
#     uint = goldx.unit()
#     valid_exchange_rate = Decimal(10 ** 18) - Decimal(paxg.getFeeFor(10 ** 18))
#     without_mint_fee = Decimal(10 ** 18) - Decimal(goldx.fee(transfer_selector))
#     fee_recipient = goldx.feeRecipient()

#     print(f'before accounts[1] approve, the allowance is: {paxg.allowance(accounts[1], goldx.address)}')
#     paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
#     print(f'after  accounts[1] approve, the allowance is: {paxg.allowance(accounts[1], goldx.address)}\n')

#     before_mint_user_goldx_balance = goldx.balanceOf(accounts[1])
#     print(f'before minting, account[1] has goldx: {before_mint_user_goldx_balance}')
#     before_mint_user_paxg_balance = paxg.balanceOf(accounts[1])
#     print(f'before minting, account[1] has paxg: {before_mint_user_paxg_balance}')
#     before_mint_total_supply = goldx.totalSupply()
#     print(f'before minting, total supply is: {before_mint_total_supply}')
#     before_mint_receipt_balance = goldx.balanceOf(fee_recipient)
#     print(f'before minting, receipt has goldx: {before_mint_receipt_balance} \n')

#     mint_amount = amount # 500000000000010
#     print(f'account[1] is going to mint {mint_amount} goldx')
#     goldx.mint(accounts[1], mint_amount, {'from': accounts[1]})
#     after_mint_user_goldx_balance = goldx.balanceOf(accounts[1])
#     goldx_changing_balance = after_mint_user_goldx_balance - before_mint_user_goldx_balance
#     print(f'after  minting, account[1] has goldx: {after_mint_user_goldx_balance}')
#     after_mint_user_paxg_balance = paxg.balanceOf(accounts[1])
#     paxg_changing_balance = after_mint_user_paxg_balance - before_mint_user_goldx_balance
#     print(f'after  minting, account[1] has paxg: {paxg_changing_balance}')

#     after_mint_total_supply = goldx.totalSupply()
#     changing_total_supply = after_mint_total_supply - before_mint_total_supply
#     print(f'after  minting, total supply is: {after_mint_total_supply}')

#     after_mint_receipt_balance = goldx.balanceOf(fee_recipient)
#     changing_receipt_balance = after_mint_receipt_balance - before_mint_receipt_balance
#     print(f'after  minting, receipt has goldx: {after_mint_receipt_balance}\n')

#     expected_goldx = Decimal(mint_amount) / BASE * Decimal(uint) / BASE * valid_exchange_rate/ BASE * without_mint_fee
#     assert int(expected_goldx) == goldx_changing_balance
#     assert goldx_changing_balance + changing_receipt_balance == changing_total_supply
#     assert mint_amount == before_mint_user_paxg_balance - after_mint_user_paxg_balance

#     print(f'---------------- end to mint for self ----------------\n')
