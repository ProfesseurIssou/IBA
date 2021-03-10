# ICA (1.5.0)

## Configure file (lib/config.ib)
### Simple example
	...
	if "myWord" in %query%:
		goto "ConfigFilePath.ib"
	...

## Comment
	#Some text

## Data type
	String => "azerty" <=> 'azerty'
	Number => 15.0  0.5
	Integer => 15   0
	bool => true false
	None => None
	list => 0;5;"hello" => %MyList%[2] = "hello"

## Change data type
	%MyVar% = str(10)	#num/int -> str
	%MyVar% = num("10")	#str/int -> num
	%MyVar% = int("10") #num/str -> int

## Variables
	%MyVar%

## Set variable
	%MyVar% = 15
	%MyVar2% = "test"
	%MyVarList% = 1,2,"hello"

## Calcul priority
	%MyVar3% = (5+5)*2

## Condition
	if condition:
		#Some code

	Egal to: x == y
	Not egal to: x != y
	More than: x > y
	More egal than: x >= y
	Less than: x < y
	Less egal than: x <=y
	And: x AND y
	Or: x OR y
	In: x in y
	Not: not(x)

## Default variable
	%INDENTATION%	#Current condition level 	(int)
	%query%			#The first call words 		(string)
	%year%			#Current year				(int)
	%month%			#Current month				(int)
	%day%			#Current day				(int)
	%hour%			#Current hour				(int)
	%minute%		#Current minute				(int)
	%second%		#Current second				(int)
	%lang%			#Default language			(string)
	%username%		#User session name 			(string)

## Lang values
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

## Speak
	speak %MyText%
	speak "Hello World"

## Listen
	listen %InputText%

## Print
	print %MyText%
	print "Hello World"

## Wait
	wait(5.0) #Wait 5 second

## Execute file
	run("path/to/my/file.exe")

## Open web site on browser
	openBrowser("PathToTheBrowser","PUBLIC","URL")
	openBrowser("PathToTheBrowser","PRIVATE","URL")

## Saving data into database
	db_save("key",value)
## Load data from database
	%myVar% = db_load("key")
## Delete data from database
	db_del("key")
## If key exist in database
	db_exist("key") (return true or false)