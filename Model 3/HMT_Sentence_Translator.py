# Created: 16/03/2020
# Made by Rhys Nicholas
# Statistical Sentence Translator
# from Mathematical Approaches to Machine Translation
#
# Requires text files: en.txt, 1Gram.txt, 2Gram.txt, 3Gram.txt
#                      P-1Gram.txt, P-2Gram.txt,P-3Gram.txt TMatrix.txt


#Useful for combinations and Permutations
import itertools

#============Statistical Translation Functions============#
#Model 3 Hybrid translator
#Main function
def HTrans(Sen):
    
    Trans = [] # Vector for translation
    Matrix = [] #Full matrix of all translation words
    Tmatrix = [] #Matrix for Sentence Generation

    #Allows capital first letter to carry through
    Caps = 0 #Capital First letter 
    if ord(Sen[0]) < 91 and ord(Sen[0]) >64:
        Caps = 1
    Sen = Sen.lower() #Strip any uppercase
    Words = Sen.split() #Convert input to Vector

    #Open Translation Matrix and read to placeholder variable 
    with open("TMatrix.txt","r") as f: 
        T = f.read().split("\n")
        
    #Convert Translation Matrix from Place holder to Matrix (List of Lists)
    for i in range(len(T)): 
        Matrix.append(T[i])
       
    #Import all Source Language (SL) words: 1800 Basic English
    with open("en.txt","r") as en:
        enD = en.read().split("\n")

    #Create New matrix in terms of the input SL
    #Each nth row represents the possible translations of the nth word 
    for i in range(len(Words)):
        if Words[i] in enD and Matrix[enD.index(Words[i])] != '':
           Tmatrix.append(Matrix[enD.index(Words[i])].split())
    #Carry through unknown words
        else:
            Tmatrix.append([Words[i]])
            
    #Create permutations of possible translations of words
    #Uses SenGen function
    SMatrix = SenGen(Tmatrix)
    
   
    #Steepest Acsent Algorithm
    P = 0  #Start with probability 0 (minimum)
    for i in range(len(SMatrix)):   #For each Sentence 
        if Prob(SMatrix[i])>P:      #Determine Probability
            P = Prob(SMatrix[i])    #Retain probability if higher than previous
            Trans = SMatrix[i]
    Trans = RBMT(Trans, Caps)
    
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

    #Print number of generations     
    print("Generating:", len(SMatrix), "Possible Sentences")

    #Optimise
    SMatrix = Optimse(SMatrix)
    
    return SMatrix #Return Permutation Matrix
    #Note does not produce arrangments therefore not true permutation


    
#Model 2: Sub Function
#Calculate Probability of a vector sentence
def Prob(Vec): #Takes input list of words, representing a sentence string
    #Data is finite therefore if no data is available
    #Assume probability is less than data obtained and use Fail Data

    
    for i in range(len(Vec)):
        if "_" in Vec[i]:
            Vec[i]=Vec[i].replace("_"," ")
    Vec =" ".join(Vec)
    Vec = Vec.split()
    
    ThFail = 0.00009 #Fail Probability of 3-gram (triplets of words)
    TFail = 0.00009 #Fail Probability of 2-gram  (pairs of words) 
    OFail = 0.00000009 #Fail Probability of 1-gram (words)

    ##Following Data is organised such that nth elements will be corresponding per ngram
    ##E.g: The nth element of the 2gram probability list is the probability of the nth 2gram element word

    #Open 3 Gram Data store to variable
    with open("3Gram.txt","r") as f:
        TriGram = f.read().split("\n")
    #Open 3 Gram probability Data store to variable
    with open("P-3Gram.txt","r") as f:
        PTri = f.read().split()
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


    ##Decomposes input sentence into 3-gram words:
    ##E.g: go to the shop => (go to the, to the shop)
    ThVec=[] #Vector/List for Storing 3 Grams from sentence input
    #Create 3 grams of string input
    for i in range(len(Vec)- 2):
        #There are N-2 possible 3-grams for N words
        #Join the elements together with " " space, to match the Data
        ThVec.append(" ".join([Vec[i],Vec[i+1],Vec[i+2]]))
    
    ##Calculate 3Gram Probability
    PTh = [] #Store probability of each 3gram
    for i in range(len(ThVec)):  #For each 3gram
        if ThVec[i] in TriGram:  #If probability exists store it
            PTh.append(float(PTri[TriGram.index(ThVec[i])]))
            #Expanlation:   Append the probability value of current word from probability data to Storage
            #               using the index of the current 3-gram word from position in the 2-gram data
            
        else:                   
            PTh.append(ThFail)    #Else use Failure Probability


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

            
        else: 
            PO.append(OFail)    #Else use Failure Probability

    P = 1 #Let Probability = 1
    for i in range(len(PO)): #Multiply by all 1gram probability
        P = P*PO[i]
    for j in range(len(PT)): #Multiply by all 2gram probability 
        P = P*PT[j]
    for j in range(len(PTh)): #Multiply by all 3gram probability 
        P = P*PTh[j]
            
    return P #Return Resulting Probability

#============Hybrid Rule Based Functions============#

#Check Matrix of sentence Vectors for bad Sentences
def Optimse(Matrix):
    #Optimise: Contractions
    #Assumes contractions can't be the first word
    for i in range(len(Matrix)):
        if "'" in Matrix[i][0]:
            Matrix[i] = "DELETEME"

    #Optimise: Definite Gramatical case
    #Converts all forms a case to single one that is corrected after
    #Does not effect probability as it is done to all
    The = ["'r","yr"]
    IN = ["yn","ym","yng"]

    #Check every word
    for i in range(len(Matrix)):    
       for j in range(len(Matrix[i])):
    #Subrule: Definite Article
          if Matrix[i][j] in The:
              Matrix[i][j] = "y"
    #Subrule: IN cases
          if Matrix [i][j] in IN:
              Matrix[i][j] = "yn"

    #Remove dead elements
    while "DELETEME" in Matrix:
        Matrix.remove("DELETEME")
    
    #Removes all duplicate elements in matrix 
    Matrix.sort()
    Matrix = list(Matrix for Matrix,_ in itertools.groupby(Matrix)) #Remove Repeats
    #Declare number optimised to
    print("Optimised to:", len(Matrix), "Sentence(s)")
    #Return Optimised Matrix
    return Matrix

#Rule Based Proofer
def RBMT(Vec,Caps): 
              
    #Gramatical Rules that need to check each word
    for i in range(len(Vec)):
          
    #Rule: Mutations
    #If mutation call relevant Mutation Function
        if Mutate(Vec[i]) == 2 and i< len(Vec[i])-1:
            Vec[i+1] = Trwynol(Vec[i+1])
        elif Mutate(Vec[i]) == 1 and i< len(Vec[i])-1:
            Vec[i+1] = Meddal(Vec[i+1])
        elif Mutate(Vec[i]) == 3 and i< len(Vec[i])-1:
            Vec[i+1] = Meddal(Vec[i+1])

    #Rules: Gramatatical  Cases
    #Assure Grammar for Gramatical Cases
        The = "y"
        IN = "yn"
    #Subrules: Definite Article
    #Convert all forms of Welsh "The" to 1 form
        if Vec[i] == The:
            if i == 0 or Olaf(Vec[i-1]) == 0:
                if i == len(Vec)-1 or Cyntaf(Vec[i+1]) == 0:
                    Vec[i] = "y"
                else:
                    Vec[i] = "yr"
            else:
                Vec[i] = "'r"
    #Subrules: In Cases
    #Convert all forms of Welsh "in" to 1 form
        if Vec[i] == IN:
            if i != len(Vec)-1:
                if Vec[i+1][0] == "m":
                    Vec[i] = "ym"
                elif Vec[i+1][0] == "n" and Vec[i+1][0] == "g":
                    Vec[i] = "yng"

    
    #Rule: Contractions 
    #Assume ' means contraction therefore combine words    
    for i in range(len(Vec)):
        if Vec[i][0] =="'":
            Vec[i-1] = "".join([Vec[i-1],Vec[i]])
            Vec[i] = "DELETEME"

    #Rule: Capitalisation
    #Capitalise first letter if input is
    if Caps == 1: 
        Vec[0] = Vec[0].capitalize()

    #Remove dead words
    if "DELETEME" in Vec:
        Vec.remove("DELETEME")

    #Return Proofed Sentence Vector
    return Vec

    
        
#Return 1 or 0 for Vowel or Consonant for first letter of word
#Cyntaf == First in welsh
#Used for gramatical rules: Mutations, The
def Cyntaf(Word):

    #Welsh Vowels and h
    Vowels = ["a","e","i","o","u","Y","w","h"]

    #Check if sucessive word ends in vowel or h
    if Word[0] in Vowels:
        return 1
    else:
        return 0

#Return 1 or 0 for Vowel or Consonant for Last letter of word
#Olaf == Last in welsh
#Used for gramatical rules: The
def Olaf(Word):
    
    #Welsh Vowels
    Vowels = ["a","e","i","o","u","w","y"]
    
    #Check if preceeidng word ends in a vowel 
    if Word[len(Word)-1] in Vowels:
        return 1
    else:
        return 0


#Simple Mutation detection System
#Checks small sets of possible mutation causing words
def Mutate(Word):
    #Mutation word sets
    Nasal = ["yn","fy"] 
    Soft = ["am","ar","at","gan","heb","i","o","dan","dros","trwy","wrth","hyd"]
    Aspirate = ["a","â", "chwe","ei","gyda","na","oni","tri","tua"]

    #Check if mutating word and return relevant
    if Word in Soft:
          return 1
    if Word in Nasal:
          return 2
    if Word in Aspirate:
        return 3
    else:
        return 0

#Soft mutation, Does not consider letters: ll or rh
#Meddal = Soft (welsh)
def Meddal(Word):
    #Mutating Consontants
    Con = ['b','c','d','g','p','t','m']
    #Mutated Consonant pair
    Mut = ['f','g','dd','','b','d','f']

    #Convert word to list to modify
    Word = list(Word)

    #If intial letter is Mutatable Consonant
    if Word[0] in Con:
    #Then mutate letter
        Word[0] = Mut[Con.index(Word[0])]

    #Convert back to word
    Word = "".join(Word)
    
    #Return mutated word
    return Word


#Nasal mutation
#Trwynol = Nasal (welsh)
def Trwynol(Word):
    #Mutating Consontants
    Con = ['b','c','d','g','p','t']
    #Mutated Consonant pair
    Mut = ['m','ngh','n','ng','mh','nh']

    #Mutated Consonant pair
    Word = list(Word)
    
    #If intial letter is Mutatable Consonant
    if Word[0] in Con:
    #Then mutate letter
        Word[0] = Mut[Con.index(Word[0])]

    #Convert back to word
    Word = "".join(Word)

    #Return mutated word
    return Word

#Aspirate
#Llaes = Aspirate (Welsh)
def Llaes(Word):
    #Mutating Consontants   
    Con = ['t','p','c']
    #Mutated Consonant pair
    Mut = ['th','ph','ch']

    #Mutated Consonant pair
    Word = list(Word)

    #If intial letter is Mutatable Consonant
    if Word[0] in Con:
    #Then mutate letter
        Word[0] = Mut[Con.index(Word[0])]

    #Convert back to word
    Word = "".join(Word)

    #Return mutated word
    return Word






    
