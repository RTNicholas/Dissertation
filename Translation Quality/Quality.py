#Example Sentence
X = "the dog and the cat"
Y = "the dog and the black cat"
Z = "The dog and the cat"

#Import Matrix Function
from Matrix import *

#Define Tested here
#from Sentence_Translator import TESTED as translate


#Reference and input sentences 
with open("Acy.txt","r") as f:
    CExample = f.read().split("\n")
with open("Aen.txt","r") as f:
    Example = f.read().split("\n")


#==========BLEU==========#
#Bleu Method of Quality Testing
#Vec = Translation string
def Bleu(Vec,Ref,NGram=1):

    #Split strings into lists
    Vec = Vec.split()
    Ref = Ref.split()

    #If NGram more than 1 convert References and input to n-grams
    if NGram > 1:
        Vec = Gram(Vec,NGram)
        Ref = Gram(Ref,NGram)
        #Define Set of unique words for n > 1
        SRef =  [list(i) for i in set(tuple(i) for i in Ref)]
    else:
        #Define set of unique words for n = 1
        SRef = set(Ref)

    #Length of translation
    N = len(Vec)

    #Foe element in Reference count occurance in:
    CVec = list(Vec.count(elem) for elem in SRef) #Translation
    CRef = list(Ref.count(elem) for elem in SRef) #Reference

    Bleu = 0
    #Sum of words
    for i in range(len(SRef)): 
        Bleu = Bleu + min(CVec[i],CRef[i])

    #Divide by Length
    Bleu = Bleu/N

    #Return Score
    return Bleu

#==========WORDERROR==========#
#Word error rate 
def Wer(Vec,Ref,NGram=1):

    #Convert to lists
    Vec = Vec.split()
    Ref = Ref.split()

    #If NGram more than 
    if NGram > 1:
        Vec = Gram(Vec,NGram)
        Ref = Gram(Ref,NGram)

    #Define Lengths
    m = len(Vec)
    M = len(Ref)
    
    #Matrix of size i,j
    Matrix = mBuild(m+1,M+1)

    #For elements in matrix
    for i in range(len(Matrix)):
        for j in range(len(Matrix[0])):
            if i == 0: #Let first column be 0 to M 
                Matrix[i][j] = j
            if j ==0: #Let first row be 0 to N 
                Matrix[i][j] = i
    
            Sub = 1 #If col and row word are the same
            if Vec[i-1] == Ref[j-1]:
                Sub = 0 #Sub is free

            if i >0 and j>0: #for all other elements minimie function
                Matrix[i][j] = min(Matrix[i-1][j]+1,Matrix[i][j-1]+1,Matrix[i-1][j-1]+Sub)
                
    #Final element over size of reference
    return Matrix[m][M]/M 

#==========NGRAM==========#
#Sub function converts vector sentence to n gram
def Gram(Vec,n):
    V = []
    
    #string can be split into Len(string)-n+1 possible n grams
    for i in range(len(Vec)-n + 1):
        V.append([])
        for j in range(n):
            V[i].append(Vec[i+j])
            
    return V #Return converted n gram list

#==========Quality Script==========#


#Variables for data export        
BleuExportData = []
WerExportData = []
BleuExportSen = []
WerExportSen = []

#Function for testing loop
def Quality(Vec,Ref):
    #Conert to lower case
    Vec = Vec.lower()
    Ref = Ref.lower()

    #Hold WER information
    Hold = []
    #Hold Translation
    Trans = translate(Vec)

    #For n grams 1 to 4 Collect Bleu Results
    for i in range(4):
        try: #Try get data
            
            #Bleu Score
            B  = Bleu(Trans,Ref,i+1)

            #Print information
            print("SL:", Vec) 
            print("TL:", Trans)
            print("Ref:", Ref)        
            print("Bleu n =",i+1,":", B)

            #Store Results
            BleuExportData.append(B) 
            BleuExportSen.append([Vec,Trans,Ref])
            
        except: #Skip if error
            pass    
        
        try: #Try get WER data
            if i<2:
                
                #WER Score
                W = Wer(Trans,Ref,i+1)

                #Hold Info
                Hold.append(W)

                #Store Results
                WerExportData.append(W)
                WerExportSen.append([Vec,Trans,Ref])

        except: #Skip Error
            pass

    #Print WER information
    #Assures WER is given after BLEU
    for i in range(len(Hold)):
        print("SL:", Vec)
        print("TL:", Trans)
        print("Ref:", Ref)        
        print("WER n =",i+1,":", Hold[i])

#Declare Loop in Script
for i in range(len(Example)):
	Quality(Example[i],CExample[i])

#Allows writing to files with utf8
import io

#Export Bleu Data
with open("ResultsBData.txt","w") as f:
    for i in BleuExportData:
        f.write("%s\n" % i)

with io.open("ResultsB.txt","w", encoding = 'utf8') as f:
    for i in BleuExportSen:
        for j in i:
            f.write("%s\t" % j)
        f.write("\n")
	
#Export Wer Data
with open("ResultsWData.txt","w") as f:
    for i in WerExportData:
        f.write("%s\n" % i)

with io.open("ResultsW.txt","w", encoding = 'utf8') as f:
    for i in WerExportSen:
        for j in i:
            f.write("%s\t" % j)
        f.write("\n")
