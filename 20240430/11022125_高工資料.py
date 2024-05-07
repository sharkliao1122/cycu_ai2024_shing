

# 設定 CSV 檔案的 URL
# 以迴圈方式幫我從 https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20240429/00/TDCS_M03A_20240429_000000.csv  https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20240429/00/TDCS_M03A_20240429_000500.csv 到 https://tisvcloud.freeway.gov.tw/history/TDCS/M03A/20240429/23/TDCS_M03A_20240429_235500.csv 這個網址下載所有的檔案
import os
import pandas as pd
import requests
import io

import os
import io
import pandas as pd
import requests
