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
    mint_amount = 1000e18
    check_diff(goldx, paxg, 'mint', mint_amount, accounts[0], accounts[1])

    burn_amount = Decimal(amount)
    check_diff(goldx, paxg, 'burn', burn_amount, accounts[0], accounts[1])
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

def test_burn_under_min_burning_amount(goldx, paxg, accounts):
    print(f'---------------- start to mint under min burning amount ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    print(f'account[1] is going to mint 1 goldx')
    goldx.mint(accounts[1], 1e18, {'from': accounts[1]})

    min_burn_amount = goldx.minBurnAmount()
    with brownie.reverts("burn: Do not satisfy min burning amount!"):
        goldx.burn(accounts[1], min_burn_amount-1, {'from': accounts[1]})
    print(f'---------------- end to mint under min burning amount ----------------\n')

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
