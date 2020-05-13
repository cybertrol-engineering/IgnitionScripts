startTime = system.date.parse('2020-02-13 09:32:14.458', 'yyyy-MM-d k:m:s.S')
endTime = system.date.parse('2020-02-13 09:34:14.000', 'yyyy-MM-d k:m:s.S')
data = system.tag.queryTagHistory(paths=[
"[Data]HTX-FORM/WIT_130101_PV"],startDate=startTime, endDate=endTime, returnSize=0, aggregationMode="Average", returnFormat='Wide')
csv_data = str(system.dataset.toCSV(data)).replace('"','').replace(',','\t')
print(csv_data)