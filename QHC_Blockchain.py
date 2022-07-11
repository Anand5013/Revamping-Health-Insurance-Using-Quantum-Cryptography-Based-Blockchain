from blockchain_qhc import Message,SimpleChain,Block

class Test :
    chain  = SimpleChain()
    block = Block()

    def add_block(self,data):
      self.block.add_message(Message(data))
      if(len(self.block.messages) > 0):
        self.chain.add_block(self.block)
        self.block = Block()
      else:
        print("Block is empty, try adding some messages")

    def show_block(self,index):
         if(len(self.chain.chain)>0) :
          previous_hash = self.chain.chain[index].prev_hash
          hash = self.chain.chain[index].hash
          data = str(self.chain.chain[index].messages)
          ind1 = data.find('[')+1
          ind2 = data.find(']')
          message = data[ind1:ind2]
          timestamp = self.chain.chain[index].timestamp
          print('previous hash : ',previous_hash,'\n','current hash : ',hash,'\n','data : ',message,'\n','timestamp : ',timestamp)
         else :
          print('issue occurred!!')

    def show_wholechain(self):
        for b in self.chain.chain :
           print('previous hash : ',b.prev_hash)
           print('current hash : ',b.hash)
           data = str(b.messages)
           ind1 = data.find('[')+1
           ind2 = data.find(']')
           message = data[ind1:ind2]
           print('data : ',message)
           print('timestamp : ',b.timestamp)
           print("----------------")
    
    def check_integrity(self):
        if self.chain.validate(): 
          print("Integrity validated.")     
        else : 
          print("Integrity not validated.")


"""

def add_b():
    a = input('>')
    test.add_block(a)

def show():
    i = int(input('$'))
    test.show_block(i)

def show_chain():
    test.show_wholechain()

def check():
    test.check_integrity()

test = Test()
add_b()
show()
show_chain()
check()
"""