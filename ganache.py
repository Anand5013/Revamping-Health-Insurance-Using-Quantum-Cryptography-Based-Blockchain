from web3 import Web3



ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
hadmin_addr = "0xc052e0B74742bA02715777e2471f1F8981d29d9F"
ladmin_addr = "0xA48FD82b1aF7C1418016a48900aA0F7915a9Adf4"
insurance_addr = "0x5FB96a52d95D7fFD80752630014D34DbAcA39218"
pharmacy_addr = "0xb7653A2C2295F8f9d4DcD1D6Ae38852F3887942f"

"""
def contract_creation(account_1,private_key) :
 if(account_1 == hadmin_addr) :
  account_2 = "0x5795f1BE8a8a97C323a0E7FC22606996a98263eC"
  nonce = web3.eth.getTransactionCount(account_1)

  tx = {
     'nonce': nonce,
     'to' : account_2,
     'value' : web3.toWei(0, 'ether'),
     'gas' : 100000,
     'gasPrice' : web3.toWei(10 , 'gwei')
   }

  signed_tx = web3.eth.account.signTransaction(tx, private_key)
  tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
  #print(web3.toHex(tx_hash))
  tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
  #print(tx_receipt)
  if tx_hash != None :
      return True
  else :
      return False
 else :
     return False

"""  

def get_insr_addr():
  return insurance_addr
  
def add_record_transaction(account_1,private_key) :
 if(account_1 == hadmin_addr) :
  account_2 = "0xe60Ba07b748d4BB03972cd915d8d68559a0B6F9B"
  nonce = web3.eth.getTransactionCount(account_1)

  tx = {
     'nonce': nonce,
     'to' : account_2,
     'value' : web3.toWei(0, 'ether'),
     'gas' : 200000,
     'gasPrice' : web3.toWei(10 , 'gwei')
   }

  signed_tx = web3.eth.account.signTransaction(tx, private_key)
  tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
  tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
  if tx_hash != None :
      return True
  else :
      return False
 else :
     return False

def add_med_transaction(account_1,private_key) :
 if(account_1 == pharmacy_addr) :
  account_2 = "0x47502cf36b1400F9881F2aE542088a6Faf15aD6e"
  nonce = web3.eth.getTransactionCount(account_1)

  tx = {
     'nonce': nonce,
     'to' : account_2,
     'value' : web3.toWei(0, 'ether'),
     'gas' : 200000,
     'gasPrice' : web3.toWei(10 , 'gwei')
   }

  signed_tx = web3.eth.account.signTransaction(tx, private_key)
  tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
  tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
  if tx_hash != None :
      return True
  else :
      return False
 else :
     return False


def payment_portal(from_account,to_account,private_key,value,gas,gasprice):
    nonce = web3.eth.getTransactionCount(from_account)
    tx = {
           'nonce': nonce,
           'to' :to_account,
           'value' : web3.toWei(value, 'ether'),
           'gas' : gas,
           'gasPrice' : web3.toWei(gasprice , 'gwei')
         }

    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    if tx_hash != None :
       return True
    else :
       return False
  
def insr_basicpay_transaction(account,plan) :
  if(plan == 'A'):
      to = insurance_addr
      value = 5
      gas = 200000
      gasprice = 10
      bal = web3.eth.getBalance(account)
      balance = web3.fromWei(bal,'ether')
      #payment_portal(account,to,private_key,value,gas,gasprice)
      pay_info = [to, value, gas, gasprice, balance]
      return pay_info

  elif(plan == 'B'):
       to = insurance_addr
       value = 7
       gas = 200000
       gasprice = 10
       bal = web3.eth.getBalance(account)
       balance = web3.fromWei(bal,'ether')
       pay_info = [to, value, gas, gasprice, balance]
       return pay_info
  else:
    return False

#def insurance_claim()

def sign_record_transaction(account_1,private_key) :
 if(account_1 == hadmin_addr) :
  account_2 = "0x4968ac910149f5059F7e9982a4C699D5f5B2d97f"
  nonce = web3.eth.getTransactionCount(account_1)

  tx = {
     'nonce': nonce,
     'to' : account_2,
     'value' : web3.toWei(0, 'ether'),
     'gas' : 200000,
     'gasPrice' : web3.toWei(10 , 'gwei')
   }

  signed_tx = web3.eth.account.signTransaction(tx, private_key)
  tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
  tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
  if tx_hash != None :
      return True
  else :
      return False
 elif(account_1 == ladmin_addr) :
     account_2 = "0xf7955600BB3c6Cb12496AaCb93347e298ef41830"
     nonce = web3.eth.getTransactionCount(account_1)

     tx = {
       'nonce': nonce,
       'to' : account_2,
       'value' : web3.toWei(0, 'ether'),
       'gas' : 200000,
       'gasPrice' : web3.toWei(10 , 'gwei')
      }

     signed_tx = web3.eth.account.signTransaction(tx, private_key)
     tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
     tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
     if tx_hash != None :
       return True
     else :
      return False
 else:
     return False

def med_bills_transaction(account,price) :
      to = pharmacy_addr
      value = price
      gas = 200000
      gasprice = 10
      bal = web3.eth.getBalance(account)
      balance = web3.fromWei(bal,'ether')
      pay_info = [to, value, gas, gasprice, balance]
      return pay_info

def insurance_patient_transaction(account,premium) :
      to = insurance_addr
      value = premium
      gas = 200000
      gasprice = 10
      bal = web3.eth.getBalance(account)
      balance = web3.fromWei(bal,'ether')
      pay_info = [to, value, gas, gasprice, balance]
      return pay_info

      
def insurance_insr_transaction(account,rem_amt) :
  to = hadmin_addr
  value = rem_amt
  gas = 200000
  gasprice = 20
  bal = web3.eth.getBalance(account)
  balance = web3.fromWei(bal,'ether')
  pay_info = [to, value, gas, gasprice, balance]
  return pay_info