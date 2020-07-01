# Created: 7/03/2020
# Made by Rhys Nicholas
# Statistical Sentence Translator
# from Mathematical Approaches to Machine Translation
#
# Requires text files: en.txt, 1Gram.txt, 2Gram.txt,
#                      P-1Gram.txt, P-2Gram.txt, Tmatrix.txt

#Useful for combinations and Permutations
import itertools
        
#Model 2 Statistical translator
#Main function
def STrans(Sen):
    Words = Sen.split() #Convert input to Vector
    Trans = [] # Vector for translation
    Matrix = [] #Full matrix of all translation words
    Tmatrix = [] #Matrix for Sentence Generation

    #Open Translation Matrix and read to placeholder variable 
    with open("Tmatrix.txt","r") as f: 
        T = f.read().split("\n")
        
    #Convert Translation Matrix from Place holder to Matrix (List of Lists)
    for i in range(len(T)): 
        Matrix.append(T[i])
       # print(Matrix)

    #Import all Source Language (SL) words: 1000 Basic English
    with open("en.txt","r") as en:
        enD = en.read().split("\n") 

    #Create New matrix in terms of the input SL
    #Each nth row represents the possible translations of the nth word 
    for i in range(len(Words)):
        Tmatrix.append(Matrix[enD.index(Words[i])].split())

    #Create permutations of possible translations of words
    #Uses SenGen function
    SMatrix = SenGen(Tmatrix)
    print("Generating:", len(SMatrix), "Possible Sentences")#Print number of generations
    
    #Steepest Acsent Algorithm
    P = 0  #Start with probability 0 (minimum)
    for i in range(len(SMatrix)):   #For each Sentence 
        if Prob(SMatrix[i])>P:      #Determine Probability
            P = Prob(SMatrix[i])    #Retain probability if higher than previous
            Trans = SMatrix[i]
            
    return " ".join(Trans)  #Return resultant string 

#Model 2: Sub Function    
#Generates combinations of sentences
def SenGen(Matrix): #Takes input List of Lists (Matrix)
    #Create permutations and store to placeholder variable
    Gen = list(itertools.product(*Matrix)) 
    SMatrix = [] #Permutation Matrix variable

    #Called function for permutations uses tuples
    #Loop through elements, convert to list, store in Permutation Matrix variable
    for i in range(len(Gen)):
        SMatrix.append(list(Gen[i]))
        
    return SMatrix #Return Permutation Matrix
    #Note does not produce arrangments therefore not true permutation


    
#Model 2: Sub Function
#Calculate Probability of a vector sentence
def Prob(Vec): #Takes input list of words, representing a sentence string

    #Data is finite therefore if no data is available
    #Assume probability is less than data obtained and use Fail Data
    TFail = 0.0001 #Fail Probability of 1-gram (words)
    OFail = 0.00000009 #Fail Probability of 2-gram (pairs of words)

    ##Following Data is organised such that nth elements will be corresponding per ngram
    ##E.g: The nth element of the 2gram probability list is the probability of the nth 2gram element word
    #Open 2 Gram Data store to variable
    with open("2Gram.txt","r") as f:
        TwoGram = f.read().split("\n")
    #Open 2 Gram probability Data store to variable
    with open("P-2Gram.txt","r") as f:
        PTwo = f.read().split()
    #Open 1 Gram Data store to variable   
    with open("1Gram.txt","r") as f:
        OneGram = f.read().split()
    #Open 1 Gram probability Data store to variable 
    with open("P-1Gram.txt","r") as f:
        POne = f.read().split()
    
    ##Decomposes input sentence into 2-gram words:
    ##E.g: go to shop => (go to, to shop)
    TVec=[] #Vector/List for Storing 2 Grams from sentence input
    #Create 2 grams of string input
    for i in range(len(Vec)-1):
        #There are N-1 possible 2-grams for N words

        #Join the elements together with " " space, to match the Data
        TVec.append(" ".join([Vec[i],Vec[i+1]]))

    
    ##Calculate 2Gram Probability
    PT = [] #Store probability of each 2gram
    for i in range(len(TVec)):  #For each 2gram
        if TVec[i] in TwoGram:  #If probability exists store it
            PT.append(float(PTwo[TwoGram.index(TVec[i])]))
            #Expanlation:   Append the probability value of current word from probability data to Storage
            #               using the index of the current 2-gram word from position in the 2-gram data
            
        else:                   
            PT.append(TFail)    #Else use Failure Probability

    ##Calculate 2Gram Probability
    PO = [] #Store probability of each 1gram
    for i in range(len(Vec)):   #For each 1gram
        if Vec[i] in OneGram:   #If probability exists store it
            PO.append(float(POne[OneGram.index(Vec[i])]))
            ##Explanation: Refer to 2gram

       #Else use Failure Probability
        else: 
            PO.append(OFail)

    P = 1 #Let Probability = 1
    for i in range(len(PO)): #Multiply by all 1gram probability
        P = P*PO[i]
    for j in range(len(PT)): #Multiply by all 2gram probability 
        P = P*PT[j]
            
    return P #Return Resulting Probability 
        
        
