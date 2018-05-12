from flask import Flask, jsonify

import pandas as pd

app = Flask(__name__)


@app.route('/api/lending_api', methods=['GET'])
def lending_api():
    # Load in raw df
    raw_df = pd.read_csv('LoanStats3a-clean.csv')

    # Manipulate data

    df_meets = raw_df.loc[
        raw_df['meets_credit_policy'] == 'Meets Credit Policy']
    df_doesnot = raw_df.loc[
        raw_df['meets_credit_policy'] == 'Does not meet the credit policy']

    df_meets_grouped = df_meets.groupby('sub_grade')['loan_amnt'].agg(
        {'meetsCount': 'count', 'meetsSum': sum})
    df_doesnot_grouped = df_doesnot.groupby('sub_grade')['loan_amnt'].agg(
        {'doesnotCount': 'count', 'doesnotSum': sum})

    df_grouped = pd.concat([df_meets_grouped, df_doesnot_grouped], axis=1)
    df_dict = df_grouped.reset_index().to_dict(orient='records')

    return jsonify(df_dict)


if __name__ == '__main__':
    app.run(debug=True)
