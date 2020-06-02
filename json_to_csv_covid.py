import json
import pandas as pd
from datetime import date
import os

def main():
	print("Hello World!")
	dt = date.today().strftime('%d-%B')
	print(dt)
	cmd = "scrapy crawl covid_counts -o " + "./data/" + dt +".json"
	print("scraping " + cmd)
	os.system(cmd)

	data = {}
	f = open('./data/' + dt + '.json')
	f_load = json.load(f)

	for i, line in enumerate(f_load):
		info = line['text']
		counties = ['Montgomery', 'Philadelphia']

		if info in counties:
			data[info+'_positive'] = int(f_load[i+1]['text'])
			data[info+'_negative'] = int(f_load[i+2]['text'])
			data[info+'_deaths'] = 0
			counties.remove(info)

		if info == 'Recovered***' and i < 50:
			data['Total_Positive'] = int(f_load[i+1]['text'].replace(",", ""))
			data['Total_Deaths'] = int(f_load[i+2]['text'].replace(",", ""))
			data['Total_Negative'] = int(f_load[i+3]['text'].replace(",", ""))

	master_table = pd.read_csv("./data/master_table.csv")
	days = len(master_table.index) - 1

	print(data)
	
	tests = data['Total_Positive'] + data['Total_Negative'] - int(master_table.loc[days]['Total Positive']) - int(master_table.loc[days]['Total Negative'])
	print(tests)
	positive = data['Total_Positive'] - int(master_table.loc[days]['Total Positive'])
	percent_positive = positive/tests
	negative = data['Total_Negative'] - int(master_table.loc[days]['Total Negative'])
	deaths = data['Total_Deaths'] - int(master_table.loc[days]['Total Deaths'])
	montco_new = data['Montgomery_positive'] - int(master_table.loc[days]['Montgomery County Positives'])
	philly_new = data['Philadelphia_positive'] - int(master_table.loc[days]['Philadelphia County Positives'])
	montco_14 = data['Montgomery_positive'] - int(master_table.loc[days-12]['Montgomery County Positives'])
	philly_14 = data['Philadelphia_positive'] - int(master_table.loc[days-12]['Philadelphia County Positives'])
	pa_14_deaths = data['Total_Deaths'] - int(master_table.loc[days-12]['Total Deaths']) 
	pa_14_postives = data['Total_Positive'] - int(master_table.loc[days-12]['Total Positive']) 

	new_row = [[dt, data['Total_Positive'], data['Total_Negative'], data['Total_Deaths'], tests, percent_positive, positive, negative, deaths, \
		 data['Montgomery_positive'], montco_new, data['Philadelphia_positive'], philly_new, montco_14, philly_14, 414, 792, pa_14_deaths, pa_14_postives]]

	print(new_row)

	master_table_p = master_table.append(pd.DataFrame(new_row, columns=master_table.columns), ignore_index=True)

	master_table_p.to_csv("./data/master_table.csv", index=False)

if __name__ == "__main__":
    main()