#
# Created: 10/12/2019
# Made by Rhys Nicholas
# Paragraph Translator 
# from Mathematical Approaches to Machine Translation
#
# Requires access to a sentence Translator

#Import sentence translator
from SMT_Sentence_Translator import STrans as SenTran


def Translate(Paragraph): #Define Translate, 

    Trans = [] #Define List for translation
    Sentences = Paragraph.split(".") #Split input paragraph based on periods
    
    #Remove lingering Periods for all that exist 
    if "" in Sentences: 
        for i in range(Sentences.count("")): 
            Sentences.remove("")

    #For all sentences, translate, add to translation list with period
    for j in range(len(Sentences)):
        Trans.append(SenTran(Sentences[j])+ ".")
        

    #return translation as string
    return(" ".join(Trans)) 
    
        
            


