with open('BnL directory.txt', 'r') as fp:
	data = fp.readlines()

pagelen = 14
charlen = 243

rowdata = {}
row = 'ERR'
zrange = [0,0]
i = 0

#Read the file and build up formatted data
for line in [x.strip().split(':') for x in data if x.strip() != '']:
	if len(line) > 1:
		# COL : Z_BEG - Z_END
		row = line[0].strip()
		zrange = [int(x.strip()) for x in line[1].split('-')]
		rowdata[row] = {
			'beg': zrange[0],
			'end': zrange[1],
			'items': [],
		}
	else:
		rowdata[row]['items'] += [line[0].lower()]

prev = {}
ERRED = False
#Make sure text is all formatted correctly
for row in rowdata:
	data = rowdata[row]

	diff = len(data['items']) - (data['end'] - data['beg'] + 1)
	if diff > 0:
		print(f'ERROR: Row {row} has {diff} too many items in it!')
		ERRED = True
	elif diff < 0:
		print(f'WARNING: Row {row} has {-diff} unused slots.')

	maxlen = 17 # each line begins with "XYZ : ", so remaining space is only 17 chars
	i = data['beg']
	for item in data['items']:
		ix = f'{row}{i}'
		if item in prev:
			print(f'WARNING: Found "{item}" at {[ix]} but it already exists at {prev[item]}!')
		else:
			prev[item] = []

		prev[item] += [ix]
		i += 1

		if len(item) > maxlen:
			print(f'ERROR: Row {row}: "{item}" is {len(item)} chars long, max is {maxlen}!')
			ERRED = True

if ERRED:
	exit(1)


#Generate output text
outdata = []
for row in rowdata:
	zcoord = rowdata[row]['beg']
	for item in rowdata[row]['items']:
		outdata += [f'{row}{str(zcoord).zfill(2)} : {item}']
		zcoord += 1

#Sort output by item name
outdata = sorted(outdata, key=lambda item: item.split(' : ')[1])


#Add periodic line breaks based on MC book max line count and max chars per page
filedata = []
lineno = 0
chars = 0
for line in outdata:
	lineno += 1
	chars += len(line) + 1
	if chars > charlen:
		print(chars, len(line))
		filedata += ['\n']
		chars = 0
		lineno = 1
	filedata += [f'{line}\n']
	if lineno >= pagelen:
		filedata += ['\n']
		chars = 0
		lineno = 0

#Write to file
with open('Alpha BnL Directory.txt', 'w') as fp:
	fp.writelines(filedata)
