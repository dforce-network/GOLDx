#!/usr/bin/python3
from brownie import rpc, Wei
from brownie.test import given, strategy

from brownie import Wei
from decimal import *
import pytest
import brownie
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


def test_paxg(paxg, accounts):
    assert paxg.balanceOf(accounts[0]) == 50000000e18
    assert paxg.balanceOf(accounts[1]) == 50000000e18
    assert paxg.balanceOf(accounts[2]) == 50000000e18
    assert paxg.balanceOf(accounts[3]) == 50000000e18

def test_glodx(goldx, accounts):
    print('goldx  symbol is: ', goldx.symbol())

# -----------------
# test mint()
# -----------------
@pytest.mark.parametrize('amount', [1000e18, 0.001e18, 202.5e18, 0.0001e18])
# @pytest.mark.parametrize('amount', [20e18])
def test_mint_for_self(goldx, paxg, accounts, amount):
    """
    mint()
    """
    print(f'---------------- start to mint for self ----------------\n')
    uint = goldx.unit()
    without_paxg_fee = 0.99998*10**18
    without_mint_fee = 0.999*10**18
    fee_recipient = goldx.feeRecipient()

    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    check_diff(goldx, paxg, 'mint', amount, accounts[0], accounts[1])

    print(f'---------------- end to mint for self ----------------\n')

def test_mint_for_another(goldx, paxg, accounts):
    print(f'---------------- start to mint for another account ----------------\n')
    mint_selector = 0x40c10f19
    uint = goldx.unit()
    without_paxg_fee = Decimal(10 ** 18) - Decimal(paxg.getFeeFor(10 ** 18))
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

    expected_goldx = Decimal(mint_amount) / BASE * Decimal(uint) / BASE * without_paxg_fee * without_mint_fee / BASE
    print(f'=======expected_goldx', expected_goldx)
    assert expected_goldx == user2_goldx_changing_balance
    assert user2_goldx_changing_balance + changing_receipt_balance == changing_total_supply
    assert user1_paxg_changing_balance == mint_amount
    assert user2_paxg_changing_balance == 0
    print(f'---------------- end to mint for another account ----------------\n')

def test_mint_under_min_minting_amount(goldx, paxg, accounts):
    print(f'---------------- start to mint under min minting amount ----------------\n')
    uint = goldx.unit()
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})

    mint_amount = 156.9568e18
    check_diff(goldx, paxg, 'mint', mint_amount, accounts[0], accounts[1])

    min_mint_amount = goldx.minMintAmount()
    actual_min_mint_amount = rdiv(min_mint_amount, uint)

    with brownie.reverts("mint: Do not satisfy min minting amount!"):
        goldx.mint(accounts[1], actual_min_mint_amount-1, {'from': accounts[1]})
    print(f'---------------- end to mint under min minting amount ----------------\n')

def test_mint_by_blacklist(goldx, paxg, accounts):
    print(f'---------------- start to mint by blacklist ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})

    mint_amount = 1e18
    check_diff(goldx, paxg, 'mint', mint_amount, accounts[0], accounts[1])

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

def test_mint_too_much(goldx, paxg, accounts):
    print(f'---------------- start to mint too much ----------------\n')
    allocate_amount = 100e18
    paxg.allocateTo(accounts[8], allocate_amount)
    paxg.approve(goldx.address, max_allowance, {'from': accounts[8]})
    with brownie.reverts("insufficient funds"):
        goldx.mint(accounts[8], allocate_amount*1000, {'from': accounts[8]})
    print(f'---------------- end to mint too much ----------------\n')

def test_mint_when_paused(goldx, paxg, accounts):
    print(f'---------------- start to mint when paused ----------------\n')
    paxg.approve(goldx.address, max_allowance, {'from': accounts[1]})
    check_diff(goldx, paxg, 'mint', 56.336e18, accounts[0], accounts[1])

    goldx.pause()

    print(f'account[1] is going to mint another 1 goldx')
    with brownie.reverts('whenNotPaused: paused'):
        goldx.mint(accounts[1], 1e18, {'from': accounts[1]})

    print(f'---------------- end to mint when paused ----------------\n')
