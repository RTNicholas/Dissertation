Author: Rhys Nicholas
Date: 24/03/2020
======================
Models Archive Guide: 
----------------------
Models 1,2,3 are organised into folders with the relevant files.
The sentence translators have the following functions:
Model 1 = DTrans("Sentence")
Model 2 = STrans("Sentence")
Model 3 = HTrans("Sentence")
Note:// Sentence is some English Language String

Paragraph Translator = Translate("Paragraph")
Note:// Paragraph are some English Language Strings separated by "."
Note:// All Paragraph Translates use the same system to call the function

=====================
Translation Quality:
----------------------
To use the Translation Quality the files in that folder are Copied to that of
the model and run by loading the Quality.py script. 
The Relevant Translator must be defined in the code before run.
~~~
The text files are as follows:
- Acy: Welsh Reference Sentences
- Aen: English Reference Sentences

- ResultsB: Collects Sentences in following pattern for BLEU:-
		English input	Translation	Reference Welsh 
- ResultsW: Collects Sentences in following pattern for WER:-
		English input	Translation	Reference Welsh 

- GT: List of translations for sentences via Google Transalte

-ResultsB: Collects all BLEU results for Sentences:
-ResultsW: Collects all WER results for Sentences:
~~~
The Python files are as follows:
- Quality: Script automatically runs and tests translator
 	   Contains BLEU and WER functions
	   Calls Matrix.py 
- Matrix: Previously Made general matrix module
	  used for transposition and matrix builder function

Note:// Spreadsheet contains all results.
=====================
Similarity:
----------------------
Spreadsheet contains RMSE calculations and source data
=====================
Presentation:
----------------------
The finial version of the presentation has been attached as the powerpoint file
