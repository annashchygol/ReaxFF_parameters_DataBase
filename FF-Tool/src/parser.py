import argparse

def printParsers(subparser_actions):
	# but better save than sorry
	for subparsers_action in subparsers_actions:
	    # get all subparsers and print help
	    for choice, subparser in subparsers_action.choices.items():
	        print("Subparser '{}'".format(choice))
	        print(subparser.format_help())


# create the top-level parser
parser = argparse.ArgumentParser(prog='PARSING PROGRAM')
parser.add_argument('--foo', action='store_true', help='foo help')
subparsers = parser.add_subparsers(help='sub-command help')

# create the parser for the "A" command
parser_a = subparsers.add_parser('A', help='A help')
parser_a.add_argument('--bar', type=int, help='bar help')

# create the parser for the "B" command
parser_b = subparsers.add_parser('B', help='B help')
parser_b.add_argument('--baz', '-b', choices='XYZ', help='baz help') #choices='XYZ'
# print main help

# create the parser for the command "KEY"
parser_key = subparsers.add_parser('KEY', help='KEY help')
parser_key.add_argument('-k', dest='key', help='Insert key(s): [YAML format]')

print(parser.format_help())

# retrieve subparsers from parser
subparsers_actions = [
    action for action in parser._actions 
    if isinstance(action, argparse._SubParsersAction)]
# there will probably only be one subparser_action,


#printParsers(subparsers_actions)
#________________________________
print('OLOLO')
options = parser.parse_args()
#if options.bar:
#	print('[From parser A]', 'bar = ', options.bar)
if options.baz:
	print('[From parser B]', 'baz = ', options.baz)