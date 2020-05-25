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

def rpc_delay(rpc, interval):
    rpc.sleep(interval)
    rpc.mine(interval)

# -----------------
# test burn()
# -----------------
@pytest.mark.parametrize('amount', [100e18, 0.001e18, 202.5e18, 0.001e18])
def test_burn_self(goldx, paxg, amount, accounts):
    """
    burn()
    """
    print(f'---------------- start to burn by self ----------------\n')
    burn_selector = 0x9dc29fac
    uint = goldx.unit()
    burn_fee = Decimal(goldx.fee(burn_selector))
    fee_recipient = goldx.feeRecipient()

    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 1000e18, {'from': accounts[1]})
    after_mint_user_balance = goldx.balanceOf(accounts[1])
    print(f'the balance of goldx of account[1] is: {after_mint_user_balance}')
    before_burn_total_supply = goldx.totalSupply()
    print(f'before burning, total supply is: {before_burn_total_supply}')
    before_burn_receipt_balance = goldx.balanceOf(fee_recipient)
    print(f'before burning, receipt has goldx: {before_burn_receipt_balance}\n')

    burn_amount = int(amount)
    print(f'account[1] is going to burn {burn_amount} goldx\n')
    goldx.burn(accounts[1], burn_amount, {'from': accounts[1]})

    after_burn_user_balance=goldx.balanceOf(accounts[1])
    print(f'after  burning, the balance of goldx of account[1] is: {after_burn_user_balance}')

    after_burn_total_supply = goldx.totalSupply()
    changing_total_supply = before_burn_total_supply - after_burn_total_supply
    print(f'after  burning, total supply is: {after_burn_total_supply}')

    after_burn_receipt_balance = goldx.balanceOf(fee_recipient)
    changing_receipt_balance = after_burn_receipt_balance - before_burn_receipt_balance
    print(f'after  burning, receipt has goldx: {after_burn_receipt_balance}\n')

    expected_burn_fee = Decimal(burn_amount) * burn_fee / BASE
    print(f'expected burning fee is: {expected_burn_fee}')

    assert burn_amount == after_mint_user_balance - after_burn_user_balance
    assert changing_total_supply == burn_amount - changing_receipt_balance
    assert expected_burn_fee == changing_receipt_balance
    print(f'---------------- end to burn by self ----------------\n')

def test_burn_all(goldx, paxg, accounts):
    print(f'---------------- start to burn all balance of user ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    paxg.approve(goldx.address, max_allowance, {'from': accounts[2]})
    paxg.approve(goldx.address, max_allowance, {'from': accounts[3]})

    goldx.mint(accounts[1], 20e18, {'from': accounts[1]})
    goldx.mint(accounts[2], 33.45e18, {'from': accounts[2]})
    goldx.mint(accounts[3], 65.36e18, {'from': accounts[3]})

    for i in range(1, 4):
        before_balance = goldx.balanceOf(accounts[i])
        print(f'before burn, the balance of goldx of account[{i}] has: {before_balance}')
        goldx.burn(accounts[i], before_balance, {'from': accounts[i]})
        after_balance = goldx.balanceOf(accounts[i])
        print(f'after burn, the balance of goldx of account[{i}] has: {after_balance}')
    print(f'---------------- end to burn all balance of user ----------------\n')


def test_burn_another(goldx, paxg, accounts):
    """
    burn()
    """
    print(f'---------------- start to burn another ----------------\n')
    burn_selector = 0x9dc29fac
    uint = goldx.unit()
    burn_fee = Decimal(goldx.fee(burn_selector))
    fee_recipient = goldx.feeRecipient()

    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 100e18, {'from': accounts[1]})
    after_mint_user_balance = goldx.balanceOf(accounts[1])
    print(f'the balance of goldx of account[1] is: {after_mint_user_balance}')
    goldx.approve(accounts[2], max_allowance, {'from': accounts[1]})
    print(f'the allowance of user1 approved to user2 is: {goldx.allowance(accounts[1], accounts[2])}')

    before_burn_user2_balance = goldx.balanceOf(accounts[2])
    print(f'the balance of goldx of account[2] is: {before_burn_user2_balance}')
    before_burn_total_supply = goldx.totalSupply()
    print(f'before burning, total supply is: {before_burn_total_supply}')
    before_burn_receipt_balance = goldx.balanceOf(fee_recipient)
    print(f'before burning, receipt has goldx: {before_burn_receipt_balance}\n')

    print(f'account[2] is going to burn 50 goldx of acount[1]\n')
    burn_amount = 50e18
    goldx.burn(accounts[1], burn_amount, {'from': accounts[2]})

    after_burn_user_balance=goldx.balanceOf(accounts[1])
    print(f'after  burning, the balance of goldx of account[1] is: {after_burn_user_balance}')
    after_burn_user2_balance=goldx.balanceOf(accounts[2])
    print(f'after  burning, the balance of goldx of account[2] is: {after_burn_user2_balance}')

    after_burn_total_supply = goldx.totalSupply()
    changing_total_supply = before_burn_total_supply - after_burn_total_supply
    print(f'after  burning, total supply is: {after_burn_total_supply}')

    after_burn_receipt_balance = goldx.balanceOf(fee_recipient)
    changing_receipt_balance = after_burn_receipt_balance - before_burn_receipt_balance
    print(f'after  burning, receipt has goldx: {after_burn_receipt_balance}\n')

    expected_burn_fee = Decimal(burn_amount) * burn_fee / BASE
    print(f'expected burning fee is: {expected_burn_fee}')

    assert burn_amount == after_mint_user_balance - after_burn_user_balance
    assert changing_total_supply == burn_amount - changing_receipt_balance
    assert expected_burn_fee == changing_receipt_balance
    print(f'---------------- end to burn another ----------------\n')

def test_burn_by_balcklist(goldx, paxg, accounts):
    print(f'---------------- start to burn by blacklist ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 100e18, {'from': accounts[1]})
    print(f'current account[1] has goldx: {goldx.balanceOf(accounts[1])}\n')

    print(f'account[1] is in blacklist: {goldx.blacklists(accounts[1])}')
    print(f'account[1] is going to burn 50 goldx')
    goldx.burn(accounts[1], 50e18, {'from': accounts[1]})

    print(f'after burning, account[1] has goldx: {goldx.balanceOf(accounts[1])}\n')

    print(f'owner is going to add account[1] to the blacklist')
    goldx.addBlacklist(accounts[1])
    print(f'account[1] is in blacklist: {goldx.blacklists(accounts[1])}')

    with brownie.reverts("checkPrecondition: Address is frozen!"):
        goldx.burn(accounts[1], 1e18, {'from': accounts[1]})

    print(f'---------------- end to burn by blacklist ----------------\n')

def test_burn_insufficient_balance(goldx, paxg, accounts):
    print(f'---------------- start to burn with insufficient balance ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 1e18, {'from': accounts[1]})
    print(f'current account[1] has goldx: {goldx.balanceOf(accounts[1])}\n')

    print(f'account[1] is going to burn 50 goldx')
    with brownie.reverts("checkPrecondition: Insufficient balance!"):
        goldx.burn(accounts[1], 50e18, {'from': accounts[1]})

    print(f'---------------- end to burn with insufficient balance ----------------\n')

def test_burn_insufficient_allowance(goldx, paxg, accounts):
    print(f'---------------- start to burn with insufficient allowance ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    paxg.approve(goldx.address, max_allowance, {'from': accounts[2]})
    goldx.mint(accounts[1], 100e18, {'from': accounts[1]})
    goldx.mint(accounts[2], 100e18, {'from': accounts[2]})
    print(f'current account[1] has goldx: {goldx.balanceOf(accounts[1])}')
    print(f'current account[2] has goldx: {goldx.balanceOf(accounts[2])}\n')

    goldx.approve(accounts[2], 1e18, {'from': accounts[1]})
    print(f'the allowance of user1 approved to user2 is: {goldx.allowance(accounts[1], accounts[2])}')

    print(f'account[2] is going to burn 50 goldx of account[1]')
    with brownie.reverts("checkPrecondition: Insufficient allowance!"):
        goldx.burn(accounts[1], 50e18, {'from': accounts[2]})

    print(f'after burn, account[1] has goldx: {goldx.balanceOf(accounts[1])}')
    print(f'after burn, account[2] has goldx: {goldx.balanceOf(accounts[2])}\n')

    print(f'---------------- end to burn with insufficient allowance ----------------\n')

def test_burn_zero(goldx, paxg, accounts):
    print(f'---------------- start to burn zero ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    goldx.mint(accounts[1], 100e18, {'from': accounts[1]})
    print(f'current account[1] has goldx: {goldx.balanceOf(accounts[1])}\n')

    print(f'account[1] is going to burn 0 goldx')
    with brownie.reverts("burn: Do not satisfy min burning amount!"):
        goldx.burn(accounts[1], 0, {'from': accounts[1]})

    print(f'---------------- end to burn zero ----------------\n')
