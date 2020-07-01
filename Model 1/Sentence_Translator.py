# Created: 10/12/2019
# Made by Rhys Nicholas
# Sentence Translator
# from Mathematical Approaches to Machine Translation
#
# Requires text files: cy.txt, en.txt

def DTrans(Sentence): #Define function: Dtrans [Dictionary Translation], 
    Words = Sentence.split()  #Convert Sentence to a list of words
    Trans = [] #Define List for translations to be added to

    #For each word collect corresponding words
    for i in range(len(Words)):  
        with open("en.txt","r") as en:  #Open txt English
            enD = en.read().split("\n") #Create list of words based on each line of English txt
            with open("cy.txt","r", encoding='utf-8-sig') as cy:      #Open Welsh
                    cyD = cy.read().split("\n") #Create list of words based on each line of 
            if Words[i].casefold() in enD: #If current Word in Loop is in English txt, [ignoring case]
                Trans.append(cyD[enD.index(Words[i].casefold())]) #Append corresponding Welsh word 
            else: #If Current word not found
                Trans.append(Words[i])
        
    return(' '.join(Trans)) #Print Translation with blank space for each word 
    
                
    
 
