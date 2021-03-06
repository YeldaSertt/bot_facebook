"""this code calculates the sum of the posts posted"""
import logging
import glob
import os
import csv
import sys
import pandas as pd

logging.basicConfig(stream=sys.stdout, format='%(message)s', level=logging.CRITICAL)
def sum_post(file_name):
    """SUM POST"""
    for filename in glob.glob(os.path.join(f"{file_name}", '*.csv')):
        csv_file = pd.read_csv(filename)
        csv_file.to_json(filename.replace("csv", "json"), orient="records")
        sum_like = 0
        try:
            for json_like in csv_file["Begeni"]:
                like = sum_like+int(json_like)
                sum_like = like
        except:# pylint: disable=bare-except
            pass

        sum_commnet = 0
        for com in csv_file["Yorum"]:
            comment = sum_commnet+int(com)
            sum_commnet = comment

        sum_share = 0
        for sha in csv_file["Yorum"]:
            share = sum_share+int(sha)
            sum_share = share

        header = ['ToplamBegeni', 'ToplamYorum', 'ToplamPaylasim']
        data = [sum_like, sum_commnet, sum_share]
        path = f"{file_name}/bot-facebook_sum.csv"
        with open(path, 'w') as write:
            writer = csv.writer(write)
            writer.writerow(header)
            writer.writerow(data)

if len(sys.argv[2]) != 3:
    logging.critical("CRITICAL : You entered a non-format input for example =>> python bot_facebook.py --dir DOM OR OCR")
else:
    sum_post(sys.argv[2])
