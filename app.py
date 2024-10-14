from flask import Flask, render_template, request
from script import product
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_product_details', methods=['POST'])
def get_product_details():
    urls = request.form.getlist('url')
    
    list_of_df = []

    for url in urls:
        list_of_df.append(product(url))

    feature = {}
    final = {}

    list_of_feature = []

    # Extracting features from each product's DataFrame
    for df in list_of_df:
        for index, rows in df.iterrows():
            if rows["Features"] not in feature:
                list_of_feature.append(rows["Features"])
                feature[rows["Features"]] = 1

    final["Features"] = list_of_feature

    # Creating column headings for the final DataFrame
    heading = 'Details of Product '
    for i in range(len(list_of_df)):
        final[heading + str(i+1)] = []

    # Populate the final DataFrame
    for f in list_of_feature:
        i = 0
        for df in list_of_df:
            flag = 0
            for index, rows in df.iterrows():
                if rows["Features"] == f:
                    flag = 1
                    final[heading + str(i+1)].append(rows["Details"])
            if flag == 0:
                final[heading + str(i+1)].append('NA')
            i += 1

    final_df = pd.DataFrame(data=final)

    # Saving the final DataFrame to an Excel file
    final_df.to_csv("data.csv", index=False)

    print("Success..!!")
    return "Success! Data saved to 'data.csv' file."

if __name__ == '__main__':
    app.run(debug=True)
