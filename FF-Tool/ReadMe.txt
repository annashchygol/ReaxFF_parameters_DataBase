=== FF-Tool ===

FF-Tool is python module for convenient manipulations with ReaxFF force fields. [~ DataBase].
During force field optimisation - there are several scenarios for user to operate with the force fields(generating input, comparison, etc.); 
 

Requirements:
  * python 3.6.1 0 (>=3.5)
  * numpy 1.12.1 py36_0
  * pyparsing 2.2.0 py36_0
  * pyyaml 3.12 py36_0
  * yaml 0.1.6 0


How to start FF-Tool ?:
* File to be called: FF-Tool/src/taskManager.py
* Input options: cmd, yaml, or both;
* => To run FF-Tool: python <path to taskManager.py> <list of keys>

Functionality:
[1] Make a DataBase out of list of folders. It would be stored as a DataBase.yaml, as a more understandable format (numeric parameter keys are converted into corresponding atom types, more human-readable). 
    * Requesting a key ‘C-H' from DataBase is easier, doesn’t depend on the order in which parameters are present.
    * Detected on the fly:
        * ‘branch’,
        * ‘charge method’,
        * ‘Van der Waals type’, 
        * ‘DOI of the paper'
    * Message / Error about parameter inconsistencies is printed.

[2] Generating MCFF input files, based on the given input file and the DataBase [list of files, to form a DataBase].
    * There  are several favours for it: [min/max, quartiles, etc.]
	MCFF input [ffield_min, ffield_max, ffield_bool], based on:
	1. input force field: --inputFF, --forceField, --ff, -f
	2. DataBase of ff: --DBinput, --inputForDB, --dB, -i
	3. Keys to be optimised: --key, -k
	There are few options for generating ffield_min, field_max, depending on which key 	is specified in --ranges, '-r':
		1. Min, Max: 'minmax', 'M'
		2. Quartiles: [Q1-(Q3-Q1), Q3 + (Q3-Q1)]; 'quartiles', 'Q'
		3. Quartiles/2: [Q1 - (Q3-Q1)/2, Q3 + (Q3 -Q1/2)] , 'quartiles/2'
	
[3] COMPARISON OF FF(s):
    pair by pair comparison of FFs. They are taken from list of inputFF.
	—inputFF = <path to folder /file(s), to be compared > (—inputFF can be specified several times, for each new file),
	—compare= f (specify what to compare: f - refers to file)
 * For bonds, offdiagonal, angles, torsions blocks reverse keys are additionally compared.        For atoms, hydrogen blocks only direct key is checked.
 * Handling the case of several occurrences of the same key in one ff. => Sets of parameters can partly match (Ex: [[1,2,3],[5,6,7]] vs [5,6,7]) => keys are added to PART.MATCH KEYS,
	input example:
	python ../FF-Tool/src/taskManager.py --inputFF=/Users/anna/DataBase/ff/water/InnerWall\ +\ No\ Shielding/CHOLi.ff --inputFF=/Users/anna/DataBase/ff/water/InnerWall\ +\ No\ Shielding/CHOLi_copy.ff --compare=f
	output example [per block]:
	===ABSENT KEYS ===:
	in ff1: 'C-H-S', 'C-H-N'
	===SAME KEYS ===: 'N-H-O', 'S-H-S', 'O-H-N', 'N-H-N', 'O-H-S', 'S-H-O', 'S-H-N', 'N-H-S’
	===DIFF KEYS ===: 'O-H-O’
	===PART.MATCH KEYS===: 'C-H-N'

[4] FILTERS:
    Filters could be applied to DataBase, so one would work further only with the filtered ffs/data. 
    Filtering could be done by 'branch' 'charge method', etc. 
	Examples:
	 * flags: --filter, --fl, -F
	 * cmd: --filter = branch;
	 * yaml: filter: [branch, chargeMethod],
(argument 'branch', 'chargeMethod'' should be also specified as an input [ actions block], filter according to specified branch)

[5] Specific to MCFF forcefields [intermediate steps]:
    * Optimised parameters are gathered into a Matrix.
    * NormalizedMatrix is also computed.


More details: 
https://jira.scm.com:18080/browse/SCMSUITE-2909

