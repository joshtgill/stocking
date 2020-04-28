import yfinance as yf
import pandas


top100Symbols = ['AGI', 'ALNY', 'AMD', 'APLS', 'APLT', 'APTO', 'ARCT', 'ARVN', 'ATLC', 'AU', 'AUDC', 'AUY', 'AVDL', 'AXSM', 'BASI', 'BLDP', 'BLU', 'BNTX', 'BTG', 'CATS', 'CDLX', 'CGEN', 'CJJD', 'CLSD', 'COE', 'CUE', 'CVM', 'CYTK', 'DEAC', 'DEACU', 'DKNG', 'DOCU', 'DRD', 'DXCM', 'EBS', 'EGO', 'ELA', 'ENPH', 'EQX', 'FATE', 'FIVN', 'FNV', 'FRTA', 'GFI', 'GOLD', 'GSX', 'HEBT', 'ICAD', 'IGMS', 'IMVTW', 'INFU', 'INSG', 'IOVA', 'KDMN', 'KGC', 'KOD', 'KPTI', 'KRMD', 'LPTX', 'LUNA', 'MEDS', 'MHH', 'MTA', 'MTEM', 'NBSE', 'NEM', 'NG', 'NVRO', 'OBCI', 'PAAS', 'PDD', 'PETS', 'PLMR', 'PRPL', 'PRTS', 'QDEL', 'RLMD', 'RVP', 'SAND', 'SAVA', 'SBSW', 'SCPH', 'SE', 'SEDG', 'SGEN', 'SHOP', 'SILV', 'TDOC', 'TRIL', 'TSLA', 'VERU', 'VNET', 'VSTM', 'VTIQW', 'VXRT', 'WPM', 'ZEAL', 'ZLAB', 'ZM', 'ZYXI']

pandas.set_option('display.max_rows', None, 'display.max_columns', None)

tsla = yf.Ticker('TSLA')
data = tsla.history(start='2020-04-28', interval='1m')
for label in data:
    print('{}\t'.format(label), end='')
print()

# Open, High, Low, Close
for i in range(len(data)) :
    # print('{}\t{}\t{}\t{}'.format(data.iloc[i, 0], data.iloc[i, 1], data.iloc[i, 2], data.iloc[i, 3]))

print(data)
# print(tsla.history(start='2020-04-28', interval='1m'))
