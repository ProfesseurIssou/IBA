# IBA (2.1.3)

## Configure file (lib/config.ib)
### Simple example
	...
	if "myWord" in query:
		goto("ConfigFilePath.ib")
	...

## Comment
	#Some text

## Data type
	String => "azerty" <=> 'azerty'
	Number => 15.0  0.5
	Integer => 15   0
	bool => true false
	none => none
	list => {0,5,"hello"} => MyList[2] = "hello"

## Variables
	MyVar1
	MyVar2

## Change data type
	MyVar = toStr(10)		#float/int -> str
	MyVar = toFloat("10")	#str/int -> float
	MyVar = toInt("10") 	#float/str -> int

## Get variables type
	type(MyVar)

## Set variable
	MyVar = 15
	MyVar2 = "test"
	MyVarList = {1,2,"hello"}

## Calcul priority
	MyVar3 = (5+5)*2

## Condition
	if condition:
		#Some code

	Egal to: x == y
	Not egal to: x != y
	More than: x > y
	More egal than: x >= y
	Less than: x < y
	Less egal than: x <=y
	And: x and y
	Or: x or y
	In: x in y
	Not: not(x)

## Default variable
	_INDENTATION_	#Current condition level 	(int)
	_CPATH_			#Current working path 		(string)
	_query_			#The first call words 		(string)
	_year_			#Current year				(int)
	_month_			#Current month				(int)
	_day_			#Current day				(int)
	_dayName_		#Name current day			(string)
	_hour_			#Current hour				(int)
	_minute_		#Current minute				(int)
	_second_		#Current second				(int)
	_lang_			#Default language			(string)
	_username_		#User session name 			(string)

## \_lang\_ values
| CODE          | language 	|
|---------------|-----------|
| bg_BG 		| Bulgarian |
| cs_CZ 		| Czech 	|
| da_DK			| Danish 	|
| de_DE 		| German 	|
| el_GR 		| Greek 	|
| en_US 		| English 	|
| es_ES 		| Spanish 	|
| et_EE 		| Estonian 	|
| fi_FI 		| Finnish 	|
| fr_FR 		| French 	|
| hr_HR 		| Croatian 	|
| hu_HU 		| Hungarian |
| it_IT 		| Italian 	|
| lt_LT 		| Lithuanian|
| lv_LV 		| Latvian 	|
| nl_NL 		| Dutch 	|
| no_NO 		| Norwegian |
| pl_PL 		| Polish 	|
| pt_PT 		| Portuguese|
| ro_RO 		| Romanian 	|
| ru_RU 		| Russian 	|
| sk_SK 		| Slovak 	|
| sl_SI 		| Slovenian |
| sv_SE 		| Swedish 	|
| tr_TR 		| Turkish 	|
| zh_CN 		| Chinese 	|

## Label
	lbl 'MyLabelName'
	#Some code
	#...
	jmp 'MyLabelName'

## Speak
	speak(MyText)
	speak("Hello World")

## Listen
	Text = listen()
	speak(listen())

## Print
	print(MyText)
	print("Hello World")

## Wait
	wait(5.0) #Wait 5 second

## Length of list or string
	listLen = len(MyList)
	msgLen = len(MyText)

## Replace characteres
    myText = replace("myText","targetCharacter","newCharacter")

## Split string into list
    myList = split("myString","delimiter")

## Execute file
	run("path/to/my/file.exe")

## Open web site on browser
	openBrowser("PathToTheBrowser","PUBLIC","URL")
	openBrowser("PathToTheBrowser","PRIVATE","URL")

# DataBase
## Saving data into database
	db_save("key",value)
## Load data from database
	myVar = db_load("key")
## Delete data from database
	db_del("key")
## If key exist in database
	db_exist("key") (return true or false)

# WordBank
## WordBank example
_WordBank/no.ibb_
```
no;No;non;Non
```
## Load WordBank
	wordList = loadWB("Path/WordBank.ibb") (return a list with all words)