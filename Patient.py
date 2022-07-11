class Patient :
  id = None
  name = None
  account = None
  email = None
  testname = None
  surgeryname = None
  hospitalname = None
  date = None
  cost = None
  meds = None
  meds_price = 0
  meds_paid = None
  count = 0
  count_hadmin = 0
  count_ladmin = 0
  insurance_plan = None
  insurance_availdate = None
  premium = None
  rem_amt = None
  insurance_amt_paid = None
  
  def add_record(self,id,name,account,email,testname,surgeryname,hospitalname,date,cost) : 
     self.id,self.name,self.account,self.email,self.testname,self.surgeryname,self.hospitalname,self.date,self.cost=id,name,account,email,testname,surgeryname,hospitalname,date,cost
  
  def add_med(self,meds):
    self.meds = meds
    self.price_cal()

  def price_cal(self):
        for i in self.meds[:,3]:
            self.meds_price = int(i) + self.meds_price
        self.cost = int(self.cost)+int(self.meds_price)

  def hadmin_sign(self):
      if(self.count_hadmin == 0) :
        self.count_hadmin += 1
        self.count += 1
      elif(self.count_hadmin >= 1) :
        print('Sign limit exceeded!')
      else:
        print('Sign limit exceeded!')
  
  def ladmin_sign(self):
      if(self.count_ladmin == 0) :
        self.count_ladmin += 1
        self.count += 1
      elif(self.count_ladmin >= 1) :
        print('Sign limit exceeded!')
      else:
        print('Sign limit exceeded!')