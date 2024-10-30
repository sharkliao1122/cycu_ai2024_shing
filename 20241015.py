import pandas as pd

# 讀取原油價格 CSV 檔案
oil_price_file_path = r"C:\Users\User\OneDrive\桌面\資料庫應用\20241015\2024_01_02 ~ 2024_10_14國際原油價格.csv"
oil_df = pd.read_csv(oil_price_file_path, header=None)

# 重命名列名
oil_df.columns = ['DAY', 'WST', 'DUBAI', 'BRENT', 'EXCHANGE_RATE']

# 將日期中的 "-" 刪除
oil_df['DAY'] = oil_df['DAY'].astype(str).str.replace('-', '')

# 將 df 中 含有 "nan "的值改為 "NULL"
oil_df = oil_df.fillna('NULL')

# 生成原油價格的 SQL 語句
oil_sql_statements = []
for index, row in oil_df.iterrows():
    oil_sql_statements.append(f"INSERT INTO OIL_PRICE (DAY, WST, DUBAI, BRENT, EXCHANGE_RATE) VALUES ('{row['DAY']}', {row['WST']}, {row['DUBAI']}, {row['BRENT']}, {row['EXCHANGE_RATE']});")

# 將原油價格的 SQL 語句保存到文件
oil_sql_file_path = r"C:\Users\User\OneDrive\桌面\資料庫應用\20241015\insert_oil_price.sql"
with open(oil_sql_file_path, 'w') as file:
    file.write("\n".join(oil_sql_statements))

print(f"Oil price SQL statements have been saved to {oil_sql_file_path}")

# 讀取匯率 CSV 檔案
exchange_rate_file_path = r"C:\Users\User\OneDrive\桌面\資料庫應用\20241015\C31D5396-FDEA-49D9-A01D-7D1FA99920CC.csv"
exchange_df = pd.read_csv(exchange_rate_file_path, header=None)

# 檢查 CSV 檔案的列數
print(f"Number of columns in exchange rate CSV: {exchange_df.shape[1]}")

# 重命名列名
if exchange_df.shape[1] == 3:
    exchange_df.columns = ['DAY', 'USD_NTD', 'USD_JPY']
else:
    raise ValueError(f"Unexpected number of columns in exchange rate CSV: {exchange_df.shape[1]}")

# 將日期中的 "-" 刪除
exchange_df['DAY'] = exchange_df['DAY'].astype(str).str.replace('-', '')

# 將 df 中 含有 "nan "的值改為 "NULL"
exchange_df = exchange_df.fillna('NULL')

# 生成匯率的 SQL 語句
exchange_sql_statements = []
for index, row in exchange_df.iterrows():
    exchange_sql_statements.append(f"INSERT INTO EXCHANGE_RATE (DAY, USD_NTD, USD_JPY) VALUES ('{row['DAY']}', {row['USD_NTD']}, {row['USD_JPY']});")

# 將匯率的 SQL 語句保存到文件
exchange_sql_file_path = r"C:\Users\User\OneDrive\桌面\資料庫應用\20241015\insert_exchange_rate.sql"
with open(exchange_sql_file_path, 'w') as file:
    file.write("\n".join(exchange_sql_statements))

print(f"Exchange rate SQL statements have been saved to {exchange_sql_file_path}")

# 生成計算相對台幣和日幣油價最高與最低價格的 SQL 語句
calculate_max_min_price_sql = '''
-- 計算相對台幣油價最高與最低價格
SELECT 
    'NTD' AS CURRENCY,
    MAX(OIL_PRICE.WST * EXCHANGE_RATE.USD_NTD) AS MAX_WST_NTD,
    MIN(OIL_PRICE.WST * EXCHANGE_RATE.USD_NTD) AS MIN_WST_NTD,
    MAX(OIL_PRICE.DUBAI * EXCHANGE_RATE.USD_NTD) AS MAX_DUBAI_NTD,
    MIN(OIL_PRICE.DUBAI * EXCHANGE_RATE.USD_NTD) AS MIN_DUBAI_NTD,
    MAX(OIL_PRICE.BRENT * EXCHANGE_RATE.USD_NTD) AS MAX_BRENT_NTD,
    MIN(OIL_PRICE.BRENT * EXCHANGE_RATE.USD_NTD) AS MIN_BRENT_NTD
FROM 
    OIL_PRICE
INNER JOIN 
    EXCHANGE_RATE 
ON 
    OIL_PRICE.DAY = EXCHANGE_RATE.DAY

UNION ALL

-- 計算相對日幣油價最高與最低價格
SELECT 
    'JPY' AS CURRENCY,
    MAX(OIL_PRICE.WST * EXCHANGE_RATE.USD_JPY) AS MAX_WST_JPY,
    MIN(OIL_PRICE.WST * EXCHANGE_RATE.USD_JPY) AS MIN_WST_JPY,
    MAX(OIL_PRICE.DUBAI * EXCHANGE_RATE.USD_JPY) AS MAX_DUBAI_JPY,
    MIN(OIL_PRICE.DUBAI * EXCHANGE_RATE.USD_JPY) AS MIN_DUBAI_JPY,
    MAX(OIL_PRICE.BRENT * EXCHANGE_RATE.USD_JPY) AS MAX_BRENT_JPY,
    MIN(OIL_PRICE.BRENT * EXCHANGE_RATE.USD_JPY) AS MIN_BRENT_JPY
FROM 
    OIL_PRICE
INNER JOIN 
    EXCHANGE_RATE 
ON 
    OIL_PRICE.DAY = EXCHANGE_RATE.DAY;
'''

# 將計算油價最高與最低價格的 SQL 語句保存到文件
calculate_max_min_price_sql_file_path = r"C:\Users\User\OneDrive\桌面\資料庫應用\20241015\calculate_max_min_price.sql"
with open(calculate_max_min_price_sql_file_path, 'w') as file:
    file.write(calculate_max_min_price_sql)

print(f"Calculate max and min price SQL statement has been saved to {calculate_max_min_price_sql_file_path}")