import os

ITEMS_FUNCT = """

% Query
items2([A, B], CalTotal) :- 
	calories(A, Cal_A), 
	calories(B, Cal_B), 
	A \= B,
	Sum is Cal_A + Cal_B,
	Sum == CalTotal.

items3([A, B, C], CalTotal) :-
	calories(A, Cal_A),
	calories(B, Cal_B),
	calories(C, Cal_C),
	A \= B, A \= C, B \= C,
	Sum is Cal_A + Cal_B + Cal_C,
	Sum == CalTotal.

items4([A, B, C, D], CalTotal) :-
	calories(A, Cal_A),
	calories(B, Cal_B),
	calories(C, Cal_C),
	calories(D, Cal_D),
	A \= B, A \= C, A \= D, B \= C, B \= D, C \= D,
	Sum is Cal_A + Cal_B + Cal_C + Cal_D,
	Sum == CalTotal.
"""

def gen_prolog(menu):

	# build a dictionary of ("itemN", item_name)
	item_ids = {}
	i = 0
	for item, cals in menu.iteritems():
		item_ids["item" + str(i)] = (item, cals)
		i += 1

	item_kwnoledge = ""
	for item_id in item_ids:
		# print item_id, item_ids[item_id][1]
		item_kwnoledge += "calories(%s, %d).\n" % (item_id, item_ids[item_id][1])

	with open("pymenu.pl", 'w') as f:
		f.write(item_kwnoledge)
		f.write(ITEMS_FUNCT)

	return item_ids

def read_items():
	with open("out.txt", "r") as f:
		content = f.read()
		if not content: return []
		return content[1:][:-1].split(',')

def get_items_2(nb_calories):
	os.system('swipl -s pymenu.pl -g "items2(Items,' + str(nb_calories) + '), write(Items)." -t halt. > out.txt')
	return read_items()

def get_items_3(nb_calories):
	os.system('swipl -s pymenu.pl -g "items3(Items,' + str(nb_calories) + '), write(Items)." -t halt. > out.txt')
	return read_items()

def get_items_4(nb_calories):
	os.system('swipl -s pymenu.pl -g "items4(Items,' + str(nb_calories) + '), write(Items)." -t halt. > out.txt')
	return read_items()

def get_items(menu, nb_items, nb_calories):
	""" Returns nb_items items with their sum of calories equal to total_cals
		menu must be a dictionnary of item_name, nb_calories """

	item_ids = gen_prolog(menu)

	if nb_items == 2:
		items =  get_items_2(nb_calories)
	if nb_items == 3:
		items =  get_items_3(nb_calories)
	if nb_items == 4:
		items = get_items_4(nb_calories)

	res = []
	for item in items:
		res.append(item_ids[item][0])
	return res


menu = { "burger": 1000, "pepsi": 500, "fries": 600, "pizza": 1100 }
print get_items(menu, 4, 3200)