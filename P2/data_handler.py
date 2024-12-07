import numpy as np
import pandas as pd

def add_column_to_file(file_n, col_nr = None, col_name = 'new_col', Value = None, Formula = None, output_file_path = 'you_dummy_forgot_output_name.txt', result_length = 4, per_cent_error_col_name_and_val = None):
    """ 
    The file adds an error of list_of_err[i] to the i element in the file
    Parameters: 
    file_n - relative path to file
    TBD
    """

    # parameters error catching
    if file_n == None:
        raise ValueError("You need to add a filename")
    if Value == None and Formula == None and per_cent_error_col_name_and_val == None:
        raise ValueError("'Value', 'Formula' and 'per_cent_error_col_and_val' cant all be 'None'")
    
    header = np.loadtxt(file_n, ndmin=1, max_rows=1, dtype='U20') # save header
    data = np.loadtxt(file_n, ndmin=1, skiprows=1, dtype='U20') # save data as type string
    df = pd.DataFrame(data, columns=header) 
    df = df.replace(',', '.', regex=True) # replace all , with .
    df = df.astype(float) # change data type to float

    if Value != None:
        if col_nr == None:
            df[col_name] = Value # adds column to the end
        else: df.insert(col_nr, col_name, Value) # inserts column at col_nr
    elif per_cent_error_col_name_and_val != None:
        for i in range(len(header)):
            if header[i] == per_cent_error_col_name_and_val[0]:
                col_nr = i + 1
                break

        col_name = per_cent_error_col_name_and_val[0] + '_error'
        df.insert(col_nr, col_name, df[per_cent_error_col_name_and_val[0]] * per_cent_error_col_name_and_val[1]) # inserts column at col_nr

    header = df.columns.tolist() # saves new header

    print('df.haed(): ')
    print(df.head())

    # save to file
    with open(output_file_path, 'w') as f:
        # Schreibe den Header
        f.write(f"{header}\n")
        # Schreibe die Ergebnisse
        np.savetxt(f, df.to_numpy(), fmt=f'%.{result_length}f', delimiter=' ')


