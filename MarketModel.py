import os, feedparser, pandas as pd, requests, unicodedata, re, time, numpy as np, xlrd, csv, io, json, plotly.graph_objects as go,plotly.io as pio

from bs4 import BeautifulSoup
from pyhelpers.ops import is_downloadable
from datetime import datetime, timedelta
from dotenv import load_dotenv, dotenv_values, find_dotenv
from edgar import Company, set_identity 
from dash import Dash, dcc, html


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
### STOCK QUOTE FUNCTIONS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def get_EOD_data(key,symbol = "AAPL", exchange = "US", period = "d",from_ = "2024-01-01", to = "2024-05-02"): 
	
	url = "https://eodhd.com/api/eod/" + symbol +"."+ exchange +"?from="+ from_+"&to="+ to +"&period="+ period +"&api_token="+ key +"&fmt=json"

	data_type = 'EOD'

	r = requests.get(url)
	if r.status_code == requests.codes.ok: 

		data = r.json()
		df = pd.DataFrame(data)


		return df


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
### GRAPHING FUNCTIONS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def ohlc_plot(df):

	fig = go.Figure(data=go.Ohlc(x=df['date'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close']))
	fig.show()

def cndlstck_plot(df): 

	fig = go.Figure(data=[go.Candlestick(x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

	fig.show()


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
### GRAPHING FUNCTIONS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

### implementing a class for cashflows 

def calculate_IRR(stream): 
	# stream is an array of the cashflows annually EOY
	stream.reverse()
	# numpy polynomial solver 
	c = np.roots(stream).tolist()
	reals = []
	comps = []
	im = False

	for i in range(len(c)):
		root = (1/c[i]) - 1 
		
		if root.imag != 0:
			comps.append(root.real)

		else: 
			reals.append(root.real)


	if len(reals) != 0: 
		return [max(reals),im]

	else: 
		im = True
		nums = reals + comps
		return[max(nums),im]

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
### MAIN PROGRAM 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
### PROGRAM LOOP  
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def main(): 
	ProgramEnd = False 
	while not ProgramEnd:
		subloop_end = False
		user_input = input('Enter Function>')

		if user_input == 'end': 
			ProgramEnd = True
			break

		elif user_input == 'stocks': 
			while not subloop_end:
				user_input = input('Enter Stock Command>')
				if user_input == 'end': 
					subloop_end = True

				elif user_input == 'show':
					key = input('Enter API key>')
					symbol = input('Enter Ticker>')
					exchange = input('Enter Exchange>')
					period = input('Enter Period>')
					from_ = input('Enter Beginning Date (YYYY-MM-DD)>')
					to = input('Enter End Date (YYYY-MM-DD)>')
					plot_type = input('Enter Plot Type (ohlc,cndl)>')
					
					df = get_EOD_data(key,symbol, exchange, period,from_, to)

					if plot_type == 'ohlc':
						ohlc_plot(df)

					elif plot_type == 'cndl': 
						cndlstck_plot(df)

		elif user_input == 'cashflow':
			while not subloop_end:
				user_input = input('Enter CashFlow Command>')
				if user_input == 'end':
					subloop_end = True 

				elif user_input == 'IRR': 
					user_input = input('Enter CashFlow (x,x,x,...,x,x,x)>')
					user_input = user_input.split(',')
					for i in range(len(user_input)):
						user_input[i] = np.float64(user_input[i])
					
					IRR = calculate_IRR(user_input)

					print(str(np.round(IRR[0]*100,4))+'%')

main()