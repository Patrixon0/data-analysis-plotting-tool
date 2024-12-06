import numpy as np
import pandas as pd

def add_column_to_file(file_n, col_nr = None, col_name = 'new_col', Value = None, Formula = None, output_file_path = 'you_dummy_forgot_output_name.txt', result_length = 4):
    """ 
    The file adds an error of list_of_err[i] to the i element in the file
    Parameters: 
    file_n - relative path to file
    TBD
    """

    # parameters error catching
    if file_n == None:
        raise ValueError("You need to add a filename")
    if Value == None and Formula == None:
        raise ValueError("'Value' and 'Formula' cant both be 'None'")
    
    header = np.loadtxt(file_n, ndmin=1, max_rows=1, dtype='U20') # save header
    data = np.loadtxt(file_n, ndmin=1, skiprows=1, dtype='U20') # save data as type string
    df = pd.DataFrame(data, columns=header) 
    df = df.replace(',', '.', regex=True) # replace all , with .
    df = df.astype(float) # change data type to float

    if col_nr == None:
        df[col_name] = Value # adds column to the end
    else: df.insert(col_nr, col_name, Value) # inserts column at col_nr
    
    header = df.columns.tolist() # saves new header

    print('df.haed(): ')
    print(df.head())

    # save to file
    with open(output_file_path, 'w') as f:
        # Schreibe den Header
        f.write(f"{header}\n")
        # Schreibe die Ergebnisse
        np.savetxt(f, df.to_numpy(), fmt=f'%.{result_length}f', delimiter=' ')


