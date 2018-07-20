from stellar_base.keypair import Keypair
from stellar_base.asset import Asset
from stellar_base.transaction import Transaction
from stellar_base.transaction_envelope import TransactionEnvelope
from stellar_base.operation import Payment, ChangeTrust
from stellar_base.address import Address
from stellar_base.horizon import horizon_testnet
from stellar_base.memo import TextMemo
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

    ISSUER_ADDRESS  = 'GB6ECAPN2AWTJ3OI5RQD3OWOOS3UBNL5CGK4EKQRKKLIH5V2MJKZAT44'
    HOLDER_ADDRESS  = 'GBJ3GXL2LRW5JTVEJFER2M2VHGFUY4WJGCEXBQIDVVVE4QC2PLJYV72U'
    ISSUER_SEED     = 'SBUVNJJ4EMIJHEPPVQVYSNDS3M3KAYUFYUVSRKRN3YN7WRTMJDMIWTK7'
    HOLDER_SEED     = 'SCZCRMN42FTE3X3OHB65C3Y5U4DASGY43V75GRV6ICMPI3M5R6MD4NEC'

    #We use this to fund our wallet with some Lumens on the testnet
    # cash = fund_account(HOLDER_ADDRESS)
    # print(cash)

    horizon = horizon_testnet()

    issuer  =   Keypair.from_seed(ISSUER_SEED)
    holder  =   Keypair.from_seed(HOLDER_SEED)

    #Now let's get the account information


    iss     =   Address(address=issuer.address().decode())
    hodl    =   Address(address=holder.address().decode())

    # print(issuer.address().decode())

    iss.get()
    hodl.get()

    # print("=" * 50)
    # print("=" *50)
    # print("ISSUER DETAILS")
    # print("=" * 50)
    # print("=" *50)    
    
    # print("Balances: {}".format(iss.balances))
    # print("Sequence Number: {}".format(iss.sequence))
    # print("Flags: {}".format(iss.flags))
    # print("Signers: {}".format(iss.signers))
    # print("Data: {}".format(iss.data))

    # print("\n")
    # print("\n")

    # print("=" * 50)
    # print("=" *50)
    # print("HOLDER DETAILS")
    # print("=" * 50)
    # print("=" *50)  

    # print("Balances: {}".format(hodl.balances))
    # print("Sequence Number: {}".format(hodl.sequence))
    # print("Flags: {}".format(hodl.flags))
    # print("Signers: {}".format(hodl.signers))
    # print("Data: {}".format(hodl.data))

  
    asset = Asset('FT', ISSUER_ADDRESS)
    # create op
    op = Payment(
        source=issuer.address().decode(),
        destination=HOLDER_ADDRESS,
        asset=asset,
        amount='100'
    )
    # create a memo
    msg = TextMemo('Buy Finche Token!')


    sequence = horizon.account(holder.address().decode('utf-8')).get('sequence')
    #Lets trust our own Token
    # trust       =   ChangeTrust({'asset': asset, 'limit': '1000'})

    tx = Transaction(
        source=holder.address().decode(),
        sequence=sequence,
        memo = msg,
        fee=100,
        operations=[
            op,
        ],
    )
    # Build Envelope
    envelope    =   TransactionEnvelope(tx=tx, network_id = 'TESTNET')
    #sign
    envelope.sign(issuer)
    #Submit
    env_xdr = envelope.xdr
    print(env_xdr)
    # response =  horizon.submit(base64.b64encode(env_xdr.encode('utf-8')))
    response =  horizon.submit(env_xdr)

    if 'result_xdr' in response:
        print("Successfully Transfered")
    else:
        print("WTH happened?")
