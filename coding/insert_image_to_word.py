# filename: insert_image_to_word.py

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from docx import Document
from docx.shared import Inches

# fetching the data
nvda = yf.download('NVDA', start=pd.to_datetime('today').replace(month=1,day=1), end=pd.to_datetime('today'))
tesla = yf.download('TSLA', start=pd.to_datetime('today').replace(month=1,day=1), end=pd.to_datetime('today'))

# plot figure
plt.figure(figsize=(14,7))
plt.plot(nvda.index, nvda.Close, label='NVIDIA')
plt.plot(tesla.index, tesla.Close, label='TESLA')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.title('NVIDIA vs TESLA Stock Price YTD')
plt.legend()
plt.grid()
plt.savefig('stocks.png')

# create Word document and add the image
doc = Document()
doc.add_picture('stocks.png', width=Inches(6.0))
doc.save('Stocks.docx')