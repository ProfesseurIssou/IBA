# ICA (1.2.1)

## Configure file (lib/Default.json)
	"MyTriggerWord":"ConfigFilePath.ib",

## Comment
	#Some text

## Data type
	String => "azerty" <=> 'azerty'
	Number => 15 => 0.5
	None => None

## Change data type
	%MyVar% = str(10)	#num->str
	%MyVar% = num("10")	#str->num

## Variables
	%MyVar%

## Set variable
	%MyVar% = 15
	%MyVar2% = "test"

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

## Default variable
	%INDENTATION%	#Current condition level 	(int)
	%query%			#The first call words 		(string)
	%year%			#Current year				(int)
	%month%			#Current month				(int)
	%day%			#Current day				(int)
	%hour%			#Current hour				(int)
	%minute%		#Current minute				(int)
	%second%		#Current second				(int)

## Speak
	speak %MyText%
	speak "Hello World"

## Listen
	listen %InputText%

## Execute file
	run("path/to/my/file.exe")

## Open web site on browser
	openBrowser("PathToTheBrowser","PUBLIC","URL")
	openBrowser("PathToTheBrowser","PRIVATE","URL")