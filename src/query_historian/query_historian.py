startTime = system.date.parse('2020-02-13 09:32:14.458', 'yyyy-MM-d k:m:s.S')
endTime = system.date.parse('2020-02-13 09:34:14.000', 'yyyy-MM-d k:m:s.S')
data = system.tag.queryTagHistory(paths=["[Data]HTX-FORM/WIT_130101_PV"],
                                  startDate=startTime,
                                  endDate=endTime,
                                  returnSize=0,
                                  aggregationMode="Average",
                                  returnFormat='Wide')
csv_data = str(system.dataset.toCSV(data)).replace('"','').replace(',','\t')
print(csv_data)

def calc_rate(historical_data, rollover=100000):
    pyds = system.dataset.toPyDataSet(historical_data)
    headers = list(pyds.getColumnNames())
    data = list()
    for row in range(len(pyds)-1):
        time_between = float(system.time.millisBetween(pyds[row]['t_stamp'], pyds[row + 1]['t_stamp'])) / (1000*60)
        if pyds[row + 1][1] >= pyds[row][1]:
            rate = (pyds[row + 1][1] - pyds[row][1]) / time_between
        else:
            rate = (pyds[row + 1][1] - pyds[row][1] + rollover) / time_between
        data.append([system.time.addMillis(pyds[row]['t_stamp'], int((time_between*1000*60*0.5))), rate])
    return system.dataset.toDataSet(headers, data)