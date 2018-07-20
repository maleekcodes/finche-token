from stellar_base.keypair import Keypair
from stellar_base.asset import Asset
from stellar_base.builder import Builder
from stellar_base.horizon import horizon_testnet
from stellar_base.address import Address

import requests
import base64

def gen_address():
    kp = Keypair.random() #Generate a random Keypair value
    public_key = kp.address().decode() #Wallet Address
    seed = kp.seed().decode() #Password
    return public_key, seed

def fund_account(address):
    r = requests.get('https://horizon-testnet.stellar.org/friendbot?addr=' + address)
    return r.text

if __name__ == '__main__':
    #This would generate the address and the seed
    # address, password = gen_address()
    # print(address, password)

    ISSUERS_ADDRESS =   "GCA3IT4NDEAZN5QPPWB72D2X5HFT3GPNONJKCAYHCBHN7MGBSYF4VEFU"
    ISSUERS_SEED    =   "SBFYTBQQPSIP3CSWU43FDFRPMETW56O7J2RUKVOKLDFL6XC4OTVUAUIT"

    RECEIVING_ADDRESS   =   "GBYXARVIA3SF5PQZOOKX2RRPZNUDWCERQZ7HEY5GQ4AZ32LD7M3J6RV2"
    RECEIVING_SEED      =   "SAJDKZPCNBYCGVRH7C3M5CJ2YAXVFCKLFJKID7S2VONJIVYDNUPCRHIU"

    horizon     =   horizon_testnet()

    ISSUER        =   Address(address=ISSUERS_ADDRESS)
    RECEIVER        =   Address(address=RECEIVING_ADDRESS)
    ISSUER.get()
    RECEIVER.get()
    
    #We get the balance of ISSUER and RECEIVER

    ISSUER_BALANCE      =   ISSUER.balances
    RECEIVER_BALANCE    =   RECEIVER.balances

    #We use testnet to fund the account for now
    # req = fund_account(RECEIVING_ADDRESS) 
    # print(req)

    asset = Asset("FT", ISSUERS_ADDRESS)

    builder = Builder(
        RECEIVING_SEED, network="TESTNET"
    ).append_trust_op(
        destination=asset.issuer, code = asset.code
    )

    builder.sign()
    resp = builder.submit()
    print(resp)

    Now we send payment
    builder = Builder(
        ISSUERS_SEED, network="TESTNET"
    ).append_payment_op(
        destination = RECEIVING_ADDRESS,
        amount = 1000,
        asset_code=asset.code,
        asset_issuer=asset.issuer

    )

    builder.sign()
    resp = builder.submit()
    print(resp)
