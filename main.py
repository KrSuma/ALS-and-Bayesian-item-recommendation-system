import numpy as np
import pandas as pd
import implicit
import time
import logging
import scipy
from scipy.sparse import coo_matrix, csr_matrix

log = logging.getLogger("implicit")

all_files = ['orders_export_1.csv', 'orders_export_2.csv', 'orders_export_3.csv']
df_from_each_file = (pd.read_csv(f) for f in all_files)
all_orders = pd.concat(df_from_each_file, ignore_index=True)

all_orders.info()

columns = ['Name', 'Email', 'Lineitem sku', 'Lineitem quantity']
columns2 = ['Vendor', 'Lineitem quantity', 'Email']

# all_orders = all_orders[columns]
# all_orders.rename(columns={'Lineitem sku':'Item', 'Lineitem quantity':'Quantity'}, inplace=True)
# all_orders.info()

all_orders = all_orders[columns2]

all_orders.rename(columns={'Lineitem quantity': 'Quantity'}, inplace=True)
all_orders.info()

all_orders.head()

# all_orders['Quantity'] = all_orders["Quantity"]
# all_orders["Email"] = all_orders["Email"].astype("category")
# all_orders["Item"] = all_orders["Item"].astype("category")
# all_orders["Name"] = all_orders["Name"].astype("category")

all_orders['Vendor'] = all_orders['Vendor'].astype("category")
all_orders['Email'] = all_orders['Email'].astype("category")

# all_orders.check_format(full_check=True)
all_orders.info()

all_orders.dropna(inplace=True)

order_matrix = coo_matrix \
        (
        (all_orders['Quantity'].astype(np.int32),
         (all_orders['Vendor'].cat.codes.copy(),
          all_orders['Email'].cat.codes.copy()))
    )
