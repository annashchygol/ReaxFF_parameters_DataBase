# This class is ment to filter out database, based on the rule/input flag / key.
# This could be:
#  - branch 		| {water }  <- this one would be speciified in the KEY(s)
#  - charge model 	|
#  - vdW type		|

# Think: does it mean I specify everything twice ??? 
# MAYbe, but this way it's much more transparent!
# Think over.

import logging

def applyFilters(options, dataBase):
	# in: unfiltered DataBase
	# out: filetered DataBase
	print ('>', 'DB: len=', len(dataBase))

	logging.info('{}'.format('Applying filters'))
	filterRules = options.filter

	print('Filtering by:', filterRules)
	logging.debug('{} {}'.format('FilterRules', filterRules))

	for filtName in filterRules:
		
		# 1.Get the list of filters; =filterRules;
		# 2.Find what they were equal to in the input key for actions block: [ex. branch = ?, chargeMethod = ?}
		#   Basically  just compare it to actions keys in options;
		# Silly solution | could be done much smarter, by matching the names:

		filterCriteria = ''
		if filtName == 'branch' and options.branch:
			filterCriteria = options.branch
		elif filtName == 'chargeMethod' and options.chargeMethod:
			filterCriteria = options.chargeMethod
		elif filtName == 'vdWtype' and options.vanDerWaals:
			filterCriteria = options.vanDerWaals

		#Add more filtering conditions, if needed, 
		dataBase = list(filter(lambda ff: ff['info'][filtName]==filterCriteria, dataBase))
		print()
		print ('>', 'DB: len=', len(dataBase), ', filter criteria:', filtName, '=',filterCriteria)
		for it in dataBase:
			print(it['info'][filtName], it['info']['name'])

		logging.debug('{} {} {}'.format('Filtered DB:', it['info'][filtName], it['info']['name']))
	return