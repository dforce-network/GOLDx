#!/usr/bin/python3
from brownie import rpc

import pytest

mint_selector = 0x40c10f19
burn_selector = 0x9dc29fac
transfer_selector = 0xa9059cbb
transferFrom_selector = 0x23b872dd
function_fee = 0.001e18


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    pass


@pytest.fixture(scope="module")
def paxg(PAXGImplementation, accounts):
    print(f'\n-------- deploy pax gold contract --------')
    paxg_contract = accounts[0].deploy(PAXGImplementation, 18)
    print(f'pax gold contract state is: {paxg_contract.paused()}')
    paxg_contract.unpause()
    print(f'pax gold contract state is: {paxg_contract.paused()}\n')

    print(f'before fee rate is {paxg_contract.feeRate()}')
    paxg_contract.setFeeRate(20)
    print(f'after  fee rate is {paxg_contract.feeRate()}\n')

    paxg_contract.allocateTo(accounts[0], 5000e18)
    paxg_contract.allocateTo(accounts[1], 4000e18)
    paxg_contract.allocateTo(accounts[2], 3000e18)
    paxg_contract.allocateTo(accounts[3], 2000e18)

    return paxg_contract

@pytest.fixture(scope="module")
def new_paxg(PAXGImplementation, accounts):
    print(f'\n-------- deploy new pax gold contract --------')
    paxg_contract = accounts[0].deploy(PAXGImplementation, 6)
    print(f'new pax gold contract state is: {paxg_contract.paused()}')
    paxg_contract.unpause()
    print(f'new pax gold contract state is: {paxg_contract.paused()}\n')

    print(f'before fee rate is {paxg_contract.feeRate()}')
    paxg_contract.setFeeRate(20)
    print(f'after  fee rate is {paxg_contract.feeRate()}\n')

    paxg_contract.allocateTo(accounts[0], 5000e18)
    paxg_contract.allocateTo(accounts[1], 4000e18)
    paxg_contract.allocateTo(accounts[2], 3000e18)
    paxg_contract.allocateTo(accounts[3], 2000e18)

    return paxg_contract

@pytest.fixture(scope="module")
def goldx(GOLDx, paxg, accounts):
    print(f'\n-------- deploy goldx contract --------')
    glodx_contract = accounts[0].deploy(GOLDx, "wrapped pax gold", "goldx", paxg.address)

    print(f'before, min minting amount is: {glodx_contract.minMintAmount()}')
    glodx_contract.setMinMintAmount(0.001e18)
    print(f'after,  min minting amount is: {glodx_contract.minMintAmount()}\n')

    print(f'before, min burning amount is: {glodx_contract.minBurnAmount()}')
    glodx_contract.setMinBurnAmount(0.001e18)
    print(f'after,  min burning amount is: {glodx_contract.minBurnAmount()}\n')

    print(f'before, fee of mint is {glodx_contract.fee(mint_selector)}')
    glodx_contract.setFee(mint_selector, function_fee)
    print(f'after,  fee of mint is {glodx_contract.fee(mint_selector)}\n')

    print(f'before, fee of burn is {glodx_contract.fee(burn_selector)}')
    glodx_contract.setFee(burn_selector, function_fee)
    print(f'after,  fee of burn is {glodx_contract.fee(burn_selector)}\n')

    print(f'before, fee of transfer is {glodx_contract.fee(transfer_selector)}')
    glodx_contract.setFee(transfer_selector, function_fee)
    print(f'after,  fee of transfer is {glodx_contract.fee(transfer_selector)}\n')

    print(f'before, fee of transferFrom is {glodx_contract.fee(transferFrom_selector)}')
    glodx_contract.setFee(transferFrom_selector, function_fee)
    print(f'after,  fee of transferFrom is {glodx_contract.fee(transferFrom_selector)}\n')

    return glodx_contract
