import csv


def create_tags():
	# open a system dialog to browse to the csv file.
	filepath = system.file.openFile('csv')
	#filepath = 'TagImport.csv'
	# check to make sure a filepath was selected.
	if filepath is not None:
		csv_data = csv.DictReader(open(filepath))

		# statically set the headers for tag configuration and the alarm configuration.
		tag_columns = ['name','tagGroup', 'tagType', 'valueSource', 'dataType', 'opcServer',
				  'opcItemPath', 'deadband', 'historicalDeadbandStyle', 'deadbandMode', 'scaleMode', 'rawHigh', 'rawLow', 'scaledHigh',
				  'scaledLow', 'historyEnabled', 'historyProvider', 'historicalDeadbandStyle', 'historicalDeadband',
				  'sampleMode', 'formatString', 'value','expression']
		alarm_columns = ['setpointA', 'notes', 'label', 'displayPath', 'priority', 'ackMode']

		# loop through the rows of the csv and create a dictionary structure.
		for row in csv_data:
			# initialize an empty dictionary to contain the tag configuration.
			tag_data = dict()

			# add the tag parameters to the tag_data
			for column in tag_columns:
				if row[column] != '':
					tag_data[column] = row[column]

			# this adds a single alarm in the format required tag_data ('alarms':[{setpointA:1....
			if row['alarms'] == '1':
				tag_data['alarms'] = list()
				tag_data['alarms'].append(dict())
				for column in alarm_columns:
					if column != 'label':
						tag_data['alarms'][0][column] = row[column]
					else:
						tag_data['alarms'][0][column] = {'bindType': 'Expression', 'value': '"' + row[column] + '"'}
				#manual row for alarm_name since 'name' is already used in the tag configuration.
				tag_data['alarms'][0]['name'] = row['alarm_name']

			# create the tag from the tagData dict.
			result = system.tag.configure(row['baseTagPath'], tag_data, 'o')
			#print(tag_data)
			print(result, tag_data['name'])


if __name__ == '__main__':
	create_tags()
