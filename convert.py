import pandas
import numpy
import json

filepath = './Servers.xlsx'                         # Specify the excel filepath here.

excel_file_object = pandas.ExcelFile(filepath)      # Opens the file.
sheets = excel_file_object.sheet_names              # Get all sheet names from the excel file.

all_server_data = {}                                # Declare blank object, this will later be filled with the required info.

# Loop through the sheets.
for sheet in sheets:                                
    raw_sheet_data = pandas.read_excel(filepath, sheet_name=sheet, header=None)     # Get data from the current sheet.       
    
    # Loop through the rows to find the header row, we can do this by checking if the row contains the word 'Component'.
    for i, row in raw_sheet_data.iterrows():
        if 'Component' in row.values:
            refined_data = raw_sheet_data.iloc[(i+1):].reset_index(drop=True)       # Delete rows above this line.
            refined_data.columns = list(raw_sheet_data.iloc[i])                     # Make this line the column header.
            break
        
    refined_data['Component'] = refined_data['Component'].ffill()                   # Unmerge 'Component' column and fill all the cells with component name for each line.
    refined_data = refined_data[refined_data['Environment'].notna()]                # Delete duplicate rows where 'Environment' is unavailable or merged.
    sheet_data = refined_data.to_dict(orient='records')                             # Convert data into dictionary (Python equivalent of an object)

    # Loop through each entry and add it into the blank object we declared earlier.
    for item in sheet_data:
        comp = item['Component']
        env = item['Environment']
        url = item['Application URL']
        if numpy.isnan(url):
            url = None
        if comp not in all_server_data:
            all_server_data[comp] = {}
        all_server_data[comp][env] = url

target_filepath = './Server Data.json'              # The data will be output to this file in JSON form. 

with open(target_filepath, 'w') as f:               # Open the above file.
    json.dump(all_server_data, f, indent=4)         # Write all data into the file.

print(json.dumps(all_server_data, indent=2))        # Print the JSON in console.