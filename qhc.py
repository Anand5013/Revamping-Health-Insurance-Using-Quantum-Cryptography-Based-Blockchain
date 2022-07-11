import os
import time
from datetime import timedelta
#from matplotlib import pyplot as plt
import numpy as np
import json




# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
### Functions for presentation and outputs ###

RATE = 4.2535969274764765e-05 # seconds per character.

def createHashcodeString(digest):
    """
    Returns a hexadecimal hash string of alphanumeric characters, 
    given a digest list of integers ranging from 0 to 15.
    """
    map_num2hex = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    hashcodelist = [None] * len(digest)
    
    for i1 in range(0, len(digest)):
        digest_i = digest[i1]                       # Extracts the number from the digest.
        hashcodelist[i1] = map_num2hex[digest_i]    # Turns the number to a hex value and assigns it to the hashcodelist.
    
    hashcodestring = ""
    
    for i1 in range(0, len(hashcodelist)):
        hashcodestring = hashcodestring + hashcodelist[i1] # Appends the characters to form a string.
    
    return hashcodestring


def hashcodeGrid4x4x4(hashcodestring):
    """
    Prints a 4 x 4 x 4 grid of alphanumeric hexadecimal characters, 
    representing a 64 character hash string.
    """
    hashcodegrid = [" "," "," "," "]
    
    i1 = 0
    while i1 < 64: # every character.
        linenum = int(i1/16) # every 16th character.
        if i1 % 4 == 3: # every 4th character.
            hashcodegrid[linenum] = hashcodegrid[linenum] + hashcodestring[i1] + " "
        else: # every other character.
            hashcodegrid[linenum] = hashcodegrid[linenum] + hashcodestring[i1]
        i1=i1+1
    '''
    #print("- - - - - - - - - - -")
    print("+---- ---- ---- ----+")
    for line in hashcodegrid:
        print(line)
    print("+---- ---- ---- ----+")
    #print("- - - - - - - - - - -")
    '''

def approximateTime(meal):
    """
    Returns an estimated time to compute a hash of a given meal string.
    The relationship is known to be linear.
    """
    RATE = 4.2535969274764765e-05 # seconds per character.
    time = len(meal)**1 * RATE
    return time
    

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
### Functions for preparing the data ###



def prepareMealFromString(string=""):
    """
    Prepares a meal as a string, from a string input.
    """
    binstring = ""
    for char in string:
        binstring += bin(ord(char))
        
    binstring = binstring.replace("b","10")
    
    stringSuffix = "10"*128 # filler string of length 256.
    # Adds enough filler string to be multiple of 256:
    binstring += stringSuffix[:((len(stringSuffix)-len(binstring))%len(stringSuffix))]
    
    return binstring


def splitUpMeal(bigmeal, max_multiple=16):
    """
    Returns a list of equally long partitions of a very large meal string.
    Helps with frequent feedback between hashing partitions, such as 
    print statements of estimated time left.
    """
    batch_size = 256 * max_multiple # 4096
        
    stringSuffix = "10" * int(batch_size/2) # filler string of length 256.
    # Adds enough filler string to be multiple of 256:
    bigmeal += stringSuffix[:((len(stringSuffix)-len(bigmeal))%len(stringSuffix))]
        
    batch_list = [bigmeal[i:i+batch_size] for i in range(0, len(bigmeal), batch_size)]
    return batch_list
    




# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
### Functions for creating a hash ###

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

def createIts(meal):
    its = [prime%(len(meal)) for prime in primes]
    return its

#its = [prime%(len(meal)) for prime in primes]


def nom(meal, i1):
    """
    Returns a pseudorandom character derived from an input string.
    """
    # Iterators
    numOfIts = len(meal)
    its = [i1 for i1 in range(0,numOfIts)]
    its = [0,2,1,6, len(meal)]
    its = createIts(meal)
    numOfIts = len(its)
    
    newnom = 0
    for i2 in range(0,numOfIts):
        newnom += int(meal[its[i2]+i1]) + primes[i2]
        #print(primes[i2])
        #print("newnom =", newnom)
    
    newnom = str(newnom % 10)
    return newnom
    

def nibble(meal):
    """
    Returns a string made of characters returned from the nom() function,
    derived from the input meal string.
    """
    broth = ""
    for i1 in range(-len(meal), 0):
        broth += nom(meal, i1)
    return broth


def munch(broth, numOfMunches):
    """
    Repeats the nibble() function along a string, 
    to return a pseudorandom string from an input meal string.
    """
    for i1 in range(numOfMunches):
        broth = nibble(broth)
    return broth


def chew(broth):
    """
    Returns a list of pseudorandom integers ranging from 0 to 15, 
    of a quarter of the size of the (normally 256-long) 
    intermediate meal string (the broth).
    """
    broth = munch(broth, 4)
    
    #thing = broth
    #print(type(thing), len(thing), len(thing)%256)
    
    broth_list_int = []
    for char in broth:
        broth_list_int.append(int(char))
        
    #thing = broth_list_int
    #print(type(thing), len(thing), len(thing)%256)
    
        
    digest_list_four = []
    tempInt = 0
    i1 = 0
    for inte in broth_list_int:
        if i1 % 4 != 0:
            tempInt += inte
            tempInt = tempInt % 16
        else:
            digest_list_four.append(tempInt)
            tempInt = 0
        i1 += 1
        
    thing = digest_list_four
    #print(type(thing), len(thing), len(thing)%64)
    
    return digest_list_four
    

def gulp(meal):
    """
    Return a list of pseudorandom integers ranging from 0 to 15, 
    compiled from multiple runs of the chew() function, after 
    dividing a long meal string into equal parts (normally 256).
    """
    #print("Proccessing...")
    broth = meal
    chunks = [broth[i:i+256] for i in range(0, len(broth), 256)]
    #print("Number of chunks:", len(chunks))
    #print(" - Chunkified...")
    digest = [0]*64
    i1 = 1
    global Ti
    Ti = 0
    for chunk in chunks:
        t1 = time.time()
        
        if i1 == 1:
            chewed = chew(chunk)
            digest = chewed
        else:
            chewed = chew(chunk)
            digest = [(int(x) + int(y))%16 for x, y in zip(digest, chewed)]
        
        t2 = time.time()
        #print("time taken:", t2-t1)
        Ti += t2-t1
        #print("time TOTAL:", Ti)
        #print(" - Chewed!")
        
        i1 += 1
    #print("Hash finished.")
    return digest



def main(message):


    # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
    ### Preparation of the data ###

    #print("Preparing data to hash...")
    TIME_1 = time.time()
    T1 = time.time()


    meal = prepareMealFromString(message)
    #print("Output of prepare meal from string\n"+meal+"\n")


    MEAL_LENGTH = len(meal)

    batch_list = splitUpMeal(meal)
    #print("Output of split up meal\n")
    #print(batch_list)
    #print("\n")

    T2 = time.time()
    TIMETAKEN = T2-T1
    #print("time taken:", TIMETAKEN)

    #print("--- --- --- \n meal preview:\n" + str(meal[:254]) + "\n...\n")
    #print("length of meal:", len(meal))
    #print("\n")
    #print("quotient of 256:",len(meal)/256)
    #print("remainder of 256:",len(meal)%256)

    #print("##################################")
    #print("--- --- --- \n batch_list preview:\n", batch_list[0], "\n...\n")
    #print("Total batches:",len(batch_list))
    #print("##################################")
    #print("hey there")
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
### Creating a hash ###

    #print("Meal :" +meal+"\n")
    #print("##########################################################################")
    #print("\n")
    #print("Hashing...")
    T1 = time.time()

    broth = gulp(meal)

    #print("Output of Gulp :\n")
    #print(broth)
    #print("\n")
    i2 = 0
    broth_batch_list = []

    for meal in batch_list:
        broth_batch_list += [gulp(meal)]
        #print("broth_batch_list:\n", broth_batch_list)
        i2 += 1
        batch_size = len(batch_list[0])
   
    
    #print("broth_batch_list length:", len(broth_batch_list))

    broth = [((sum(x) + max(x)) % 16) for x in zip(*broth_batch_list)]

    T2 = time.time()
    TIME_2 = time.time()
    #print("##########################################################################")
    #print("DIGEST:\n", broth)
    TIMETAKEN = T2 - T1
    TIMETAKEN = TIME_2 - TIME_1
    #print("time taken:", TIMETAKEN)


# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
### Finalising a hash ###

    broth_list_int = []
    for char in broth:
        broth_list_int.append(int(char))

    tempInt = 0
    for inte in broth_list_int:
        tempInt = (tempInt + inte) % 16
    broth_list_int[0] = tempInt

   

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
### Printing the hash ###

    #print("\nOutput hash:")
    HashcodeString = createHashcodeString(broth_list_int)
    print('Hash:',HashcodeString)
    #print("\n4x4x4 hash grid.:")
    hashcodeGrid4x4x4(HashcodeString)
    return HashcodeString
''''
if __name__=="__main__":
    main(message)
'''