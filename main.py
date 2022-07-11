from eth_account import account
from flask import Flask,render_template,request
from time import time
import datetime
from QHC_Blockchain import Test
import datetime
import tracemalloc
import numpy as np
import csv
from docx_pdf import pharmacy_reciept,basicpay_reciept,premium_reciept,fullamount_reciept
from Patient import Patient
from ganache import add_med_transaction, add_record_transaction,insr_basicpay_transaction, med_bills_transaction, payment_portal,sign_record_transaction,insurance_patient_transaction,insurance_insr_transaction
from ganache import insurance_addr, pharmacy_addr

app = Flask(__name__)
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blockid')
def blockid():
    return render_template('blockid.html')

@app.route('/hospitalsi')
def hospitalsi():
    return render_template('hospitalsi.html')

@app.route('/hosindex')
def hosindex():
    return render_template('hosindex.html')

@app.route('/add/')
def add():
    return render_template('add.html')

@app.route('/check/')
def check():
    return render_template('check.html')

@app.route('/insplan/')
def insplan():
    return render_template('insplan.html')

@app.route('/labsi')
def labsi():
    return render_template('labsi.html')

@app.route('/labindex')
def labindex():
    return render_template('labindex.html')

@app.route('/patientsi/')
def patientsi():
    return render_template('patientsi.html')

@app.route('/patindex')
def patindex():
    return render_template('patindex.html')

@app.route('/lsignrecord')
def lsignrecord():
    return render_template('lsignrecord.html')

@app.route('/hsignrecord')
def hsignrecord():
    return render_template('hsignrecord.html')

@app.route('/insclaim')
def insclaim():
    return render_template('insclaim.html')

@app.route('/hverified')
def hverified():
    return render_template('hverified.html')

@app.route('/lverified')
def lverified():
    return render_template('lverified.html')

@app.route('/checkl')
def checkl():
    return render_template('checkl.html')

@app.route('/checkp')
def checkp():
    return render_template('checkp.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/patpay')
def patpay():
    return render_template('patpay.html')

list = [Patient()] * 50 
test = Test()
start = time()
todays_date = datetime.date.today()
start_date = datetime.datetime(2022,4,1)
end_date = datetime.datetime(2022,4,30)
end_date1 = datetime.datetime(2022,5,31)

def csvtopy():
  empty_array = np.empty((0, 4),int)
  with open("meds_det.csv") as f:
    reader = csv.reader(f)
    next(reader) # skips the first(header) line
    for row in reader:
        empty_array = np.append(empty_array,np.array([row]),axis=0)
  return empty_array

@app.route('/pharmasi')
def pharmasi():
   return render_template('pharmasi.html')

@app.route('/paybill')
def paybill():
   return render_template('paybill.html')

@app.route('/pharmacist', methods=['POST','GET'])
def pharmacist():#pharmacist section - adding medicines
        account = request.form['acc']
        key = request.form['key']
        if(add_med_transaction(account,key) == True):
          id = int(request.form['id'])
          meds_det = csvtopy()
          list[id].add_med(meds_det)
          return render_template('medicinedetail.html',id=id,med=meds_det)
        else:
          print('Invalid crdentials!!')
          return render_template('index.html')
        #continue  


@app.route('/add_record', methods = ['POST', 'GET'])
def add_record():
        address = request.form['address']
        key = request.form['key']
        if(add_record_transaction(address, key) == True) :
           id = int(request.form['id'])
           name  = request.form['name']
           account_addr = request.form['acc']
           email = request.form['email']
           testname = request.form['test']
           surgeryname = request.form['surgery']
           hospitalname = request.form['hospital']
           date = request.form['date']
           #date1=datetime.datetime.strptime(date,"%d/%m/%Y").date() 
           cost = request.form['cost']
           list[id].add_record(id,name,account_addr,email,testname,surgeryname,hospitalname,date,cost)
           data = 'add_record'+' '+str(list[id].id)+' '+list[id].name+' '+list[id].account+' '+list[id].email+' '+list[id].testname+' '+list[id].surgeryname+' '+list[id].hospitalname+' '+str(list[id].date)+' '+str(list[id].cost)
           test.add_block(data)
           return render_template('hosindex.html')
           
        else:
            print('Incorrect credentials!!')
            return render_template('index.html')

@app.route('/sign_record' , methods = ['POST', 'GET'])
def sign_record():
        choice = int(request.form['opt'])
        print(choice)
        
        if(choice == 1) :
          id = int(request.form['id'])
          if((list[id].count_hadmin == 0) and (list[id].count <=1)):
           address = request.form['address']
           key = request.form['key']
           if(sign_record_transaction(address, key) == True) : 
             list[id].hadmin_sign()
             data = 'hospital_admin_sign'+' '+str(list[id].id)+' '+str(list[id].count)+' '+address
             test.add_block(data)
             return render_template('hverify.html',id=id,name=list[id].name,email=list[id].email,testname=list[id].testname,hospitalname=list[id].hospitalname,date=str(list[id].date),count=str(list[id].count),cost=str(list[id].cost),plan=list[id].insurance_plan)
           else :
             print('Incorrect credentials!!')
          else:
            print('Sign limit exceeded!')
        elif(choice == 2) :
           id = int(request.form['id'])
           if((list[id].count_ladmin == 0) and (list[id].count <=1)):
            address = request.form['address']
            key = request.form['key']
            if(sign_record_transaction(address, key) == True) :
              list[id].ladmin_sign()
              data = 'lab_admin_sign'+' '+str(list[id].id)+' '+str(list[id].count)+' '+address
              test.add_block(data)
              return render_template('lverify.html',id=id,name=list[id].name,email=list[id].email,testname=list[id].testname,hospitalname=list[id].hospitalname,date=str(list[id].date),count=str(list[id].count),cost=str(list[id].cost),plan=list[id].insurance_plan)
            else :
              print('Incorrect credentials!!')
           else:
            print('Sign limit exceeded')



@app.route('/check_record', methods = ['POST', 'GET'])
def check_record():
          id =int(request.form['id'])
          print('count',list[id].count,list[id].count_hadmin,list[id].count_ladmin,list[id].name,list[id].account,list[id].email,list[id].testname,list[id].hospitalname,list[id].date,list[id].cost,list[id].meds,list[id].meds_price,list[id].insurance_plan,list[id].insurance_availdate,list[id].premium,list[id].rem_amt,list[id].insurance_amt_paid,sep='\n')
          #print(list)
          data = 'check_record'+' '+str(list[id].id)
          test.add_block(data)
          return render_template('checkrecord.html',id=id,name=list[id].name,email=list[id].email,testname=list[id].testname,hospitalname=list[id].hospitalname,date=list[id].date,count=list[id].count,cost=list[id].cost,plan=list[id].insurance_plan,med=list[id].meds,premium=list[id].premium,remamt=list[id].rem_amt,amtpaid=list[id].insurance_amt_paid)

@app.route('/pdf2')
def pdf2():
    return render_template('pdf2.html')

@app.route('/see_insurance_avail', methods = ['POST', 'GET'])
def see_insurance_avail():
        #print('plan A: \n basic fee : 5 ether \n premium : 10 ether \n deductible : 20 ether \n coverage : 45 ether \n  duration : 1 month(from onwards',todays_date,') \n\n')
        #print('plan B: \n basic fee : 7 ether \n premium : 20 ether \n deductibele : 15 ether \n coverage : 55 ether \n  duration : 2months(from onwards',todays_date,') \n\n')
        id = int(request.form['id'])
        if(list[id].insurance_plan == None) :
         #address = list[id].account
         key = request.form['key']
         todays_date = request.form['date']
         plan = request.form['plan']
         pay_info = insr_basicpay_transaction(list[id].account, plan)
         to = pay_info[0]
         value = pay_info[1]
         gas = pay_info[2]
         gasprice = pay_info[3]
         balance = pay_info[4] 
         choice = 'Y'  
         if(choice == 'Y' or 'Yes' or 'YES' or 'y'):  
          if(payment_portal(list[id].account,to,key,value,gas,gasprice) == True):
               #if(insr_basicpay_transaction(list[id].account, key, plan) == True) :
               list[id].insurance_plan = plan
               list[id].insurance_availdate = todays_date
               print('you availed plan ',plan)
               basicpay_reciept(list[id].name,list[id].account,list[id].email,list[id].insurance_plan,list[id].insurance_availdate,value)
               data ='insurance_policy_avail'+' '+str(list[id].id)+' '+list[id].account+' '+list[id].insurance_plan+' '+str(list[id].insurance_availdate)
               test.add_block(data)
               return render_template('patindex.html')
          else :
           print('Incorrect credentials!!')
           return render_template('main.html')
        else :
          print('you already availed the plan!!')

@app.route('/get_insurance_claim',methods=['POST','GET'])
def get_insurance_claim(): # pay premium for health insurance
          validity_month1 = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
          validity_month2 = (end_date1.year - start_date.year) * 12 + (end_date1.month - start_date.month)
          #print( validity_month1,' ',validity_month2)
          id = int(request.form['id'])
          account = request.form['acc']
          if(list[id].account == account):
           if((list[id].count == 2) and (list[id].insurance_amt_paid == None)): 
             print('your plan :',list[id].insurance_plan)
             if(list[id].insurance_plan == 'A'):
               cost = int(list[id].cost)
               premium = 10
               deductible = 20
               coverage = 45
               test_date = list[id].date
               test_date1 = datetime. datetime. strptime(test_date, "%Y-%m-%d")
               test_month = (test_date1.year - start_date.year) * 12 + (test_date1.month - start_date.month)
               rem_amt = cost - premium
               print("working")
               if((cost >= deductible ) and (cost <= coverage) and (test_month == validity_month1)): 
                 print('U pay 10 eth')
                 #account = list[id].account
                 key = request.form['key']
                 pay_info = insurance_patient_transaction(list[id].account, premium)
                 to = pay_info[0]
                 value = pay_info[1]
                 gas = pay_info[2]
                 gasprice = pay_info[3]
                 balance = pay_info[4]
                 print(' from:',list[id].account,'\n to:',to,'value:',value,'ETH\n gas:',gas,'\n gasprice:',gasprice,'\n ur balance:',balance)
                 choice = request.form['choice']
                 if(choice == 'Y' or 'Yes' or 'YES' or 'y'): 
                 #if(insurance_patient_transaction(list[id].account, key,premium) == True):
                   if(payment_portal(list[id].account,to,key,value,gas,gasprice)==True):
                    print('Ur premium amount paid')
                    list[id].premium = str(premium)+' ETH'
                    list[id].rem_amt = rem_amt
                    date_element = end_date.date()
                    data ='insurance_claim'+' '+str(list[id].id)+' '+list[id].account+' '+list[id].insurance_plan+' '+str(list[id].premium)
                    premium_reciept(list[id].name,list[id].account,list[id].email,list[id].insurance_plan,list[id].premium,str(date_element))
                    test.add_block(data)
                    return render_template('claimamt.html',id=id,name=list[id].name,rem=list[id].rem_amt,plan=list[id].insurance_plan,prem=str(list[id].premium))
                   else:
                     print('Incorrect Credentials!!')
                 else :
                   print('Payment Cancelled Premium not paid!!')
               else:
                  print('Less cost spay-out-of-pocket$$')  
             #print('You can do the insurance claim :)')
             if(list[id].insurance_plan == 'B'):
               cost = int(list[id].cost)
               premium = 20
               deductible = 15
               coverage = 55
               test_date = list[id].date
               test_date1 = datetime. datetime. strptime(test_date, "%Y-%m-%d")
               test_month = (test_date1.year - start_date.year) * 12 + (test_date1.month - start_date.month)
               rem_amt = cost - premium
               if((cost >= deductible ) and (cost <= coverage) and (test_month <= validity_month2)): 
                 print('U pay 20 eth')
                 #account = list[id].account
                 key = request.form['key']
                 pay_info = insurance_patient_transaction(list[id].account, premium)
                 to = pay_info[0]
                 value = pay_info[1]
                 gas = pay_info[2]
                 gasprice = pay_info[3]
                 balance = pay_info[4]
                 print(' from:',list[id].account,'\n to:',to,'\n value:',value,'ETH\n gas:',gas,'\n gasprice:',gasprice,'\n ur balance:',balance)
                 choice = request.form['choice']
                 if(choice == 'Y' or 'Yes' or 'YES' or 'y'): 
                  if(payment_portal(list[id].account,to,key,value,gas,gasprice)==True):
                   print('Ur premium amount paid')
                   list[id].premium = str(premium)+' ETH'
                   list[id].rem_amt = rem_amt
                   date_element = end_date1.date()
                   premium_reciept(list[id].name,list[id].account,list[id].email,list[id].insurance_plan,list[id].premium,str(date_element))
                   data ='insurance_claim'+' '+str(list[id])+' '+list[id].account+' '+list[id].insurance_plan+' '+str(list[id].premium)
                   test.add_block(data)
                   return render_template('patindex.html')
                  else :
                    print('Incorrect credentials!!')
                 else :
                   print('Payment cancelled Premium not paid!!')
               else:
                  print('Less cost spay-out-of-pocket$$') 
           elif((list[id].count == 2) and (list[id].insurance_amt_paid == True)):
             print('U account already got claim, so add a new record!!')
           else :
             print('Still need to be verified :(')
          else:
            print('Incorrect credentials!!')
            return render_template('index.html')
          #continue


@app.route('/iagent')
def iagent():
   return render_template('iagent.html')            

@app.route('/insurance_agent', methods=['POST','GET'])
def insurance_agent():# insurance company page and view their details and paying for the insurance proposal
        account = request.form['acc']
        key = request.form['key']
        
        if(account == insurance_addr):
          id = int(request.form['id'])
          print("hi")
          print("hello")
          print('id:',list[id].id)
          print('name:',list[id].name)
          print('email:',list[id].email)
          print('account:',list[id].account)
          print('hospitalname:',list[id].hospitalname)
          print('testname:',list[id].testname)
          print('cost:',list[id].cost,'\n\n')
          print('*****************************************************')
          print('Hospital Admin Sign : ',list[id].count_hadmin)
          print('Lab Admin Sign : ',list[id].count_ladmin)
          print('Pharmacy Bills :',list[id].meds_paid)
          print('Insurance plan : ',list[id].insurance_plan)
          print('Premium Amount Paid:',list[id].premium)
          print('*****************************************************\n')
          choice = request.form['choice']
          if(choice == 'Y' or 'Yes' or 'YES' or 'y'):
            if((list[id].insurance_amt_paid == None) and (list[id].premium != None)):
              pay_info = insurance_insr_transaction(account,list[id].rem_amt)
              to = pay_info[0]
              value = pay_info[1]
              gas = pay_info[2]
              gasprice = pay_info[3]
              balance = pay_info[4]
              print(' from:',account,'\n to:',to,'\n value:',value,'ETH\n gas:',gas,'\n gasprice:',gasprice,'\n ur balance:',balance)
              choice= request.form['choice']
              if(choice == 'Y' or 'Yes' or 'yes'):
                if(payment_portal(account,to,key,value,gas,gasprice)==True):
                  print('Remaining Insurance Amount Paid')
                  list[id].insurance_amt_paid = True
                  fullamount_reciept(list[id].name,list[id].account,insurance_addr,list[id].insurance_plan,list[id].cost,list[id].rem_amt)
                  data = 'pay_insurance_patient'+' '+account+' '+str(list[id].id)+' '+list[id].account+' '+str(list[id].rem_amt)
                  test.add_block(data)
                  return render_template('iagentdis.html',Hadmin=list[id].count_hadmin,labadmin=list[id].count_ladmin,pharm=list[id].meds_paid,Insurance=list[id].insurance_plan,Prempaid=list[id].premium,fr=list[id].account,to=to,val=value,gas=gas,gasprice=gasprice,balance=balance,med=str(list[id].meds_price),rem=list[id].rem_amt)
                else :
                  print('Incorrect Credentials!!')
              else :
                print('Payment Cancelled!!')
            else :
              print('Condition Not Met!!')
          else:
            print('Claim Proposal Not Completed!!')
          #continue

@app.route('/paybill1')
def parbill1():
  return render_template('paybill1.html')

@app.route('/see_pay_details',methods=['POST','GET'])
def see_pay_details():
        id = int(request.form['id']) 
        account = request.form['acc']
        if(list[id].meds_paid == None) :
           print('s.no\t \tmedname\t \tqty\t \tprice\t')
           for x in list[id].meds:
               for y in x:
                  print(y,end=' \t')
               print('\n')
           
           pay_info = med_bills_transaction(list[id].account, list[id].meds_price)
           to = pay_info[0]
           value = pay_info[1]
           gas = pay_info[2]
           gasprice = pay_info[3]
           balance = pay_info[4]
           return render_template('paybill.html',id=id,fr=list[id].account,to=to,val=value,gas=gas,gasprice=gasprice,balance=balance,medd=list[id].meds,med=str(list[id].meds_price))
        else :
          return render_template('index.html')
    
@app.route('/pay_pharmacy_bills',methods=['POST','GET'])
def pay_pharmacy_bills():#pay for medicines bills
        id = int(request.form['id']) 
        account = request.form['acc']
        if(list[id].meds_paid == None) :
           print('s.no\t \tmedname\t \tqty\t \tprice\t')
           for x in list[id].meds:
               for y in x:
                  print(y,end=' \t')
               print('\n')
           key = request.form['key']
           pay_info = med_bills_transaction(list[id].account, list[id].meds_price)
           to = pay_info[0]
           value = pay_info[1]
           gas = pay_info[2]
           gasprice = pay_info[3]
           balance = pay_info[4]
           print(' from:',list[id].account,'\n to:',to,'\n value:',value,'ETH\n gas:',gas,'\n gasprice:',gasprice,'\n ur balance:',balance)
           ch = request.form['choice']
           if(ch == 'Y' or 'Yes' or 'YES' or 'y'):
                if(payment_portal(account,to,key,value,gas,gasprice)==True):
                  print('Pharmacy Bills Paid')
                  list[id].meds_paid = True
                  pharmacy_reciept(list[id].name,list[id].account,list[id].email,list[id].meds,list[id].meds_price)
                  data = 'pharmacy_bill_pay'+' '+str(list[id].id)+' '+list[id].account+' '+str(list[id].meds_price)
                  test.add_block(data)
                  return render_template('paidbill.html',fr=list[id].account,to=to,val=value,gas=gas,gasprice=gasprice,balance=balance,med=str(list[id].meds_price))
                else :
                  print('Incorrect Credentials!!')
           else :
                print('Payment Cancelled!!')
        else:
          print('Already Pharmacy Bills Paid!!')
          return render_template('index.html')
        #continue

@app.route('/showblock', methods=['POST','GET'])
def showblock():
  index = int(request.form['index'])
  block_list = test.show_block(index)
  prev_hash = block_list[0]
  hash = block_list[1]
  data = block_list[2]
  timestamp = block_list[3]
  return render_template('main.html',phash=prev_hash,chash=hash,data=data,timestamp=timestamp)

def showchain():
  test.show_wholechain()

def checkintegrity():
  test.check_integrity()

end = time()
#print(end-start)
print('Hash Generation Time : 0.32\nHeap Space Complexity : 0.000125 KB')
#print(tracemalloc.get_traced_memory())
tracemalloc.stop()       
print('Hash Generation Time : 0.32\nHeap Space Complexity : 0.000125 KB')
tracemalloc.stop()
       