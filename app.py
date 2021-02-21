#!/usr/bin/python
from flask import Flask,render_template,redirect,url_for,request,Response,send_from_directory,send_file
import requests
from bs4 import BeautifulSoup
import pprint
import smtplib
from email.message import EmailMessage
import csv
import schedule
import time
from flask_bootstrap import Bootstrap
from Modules.fetch_data import fetchData
from flask_sqlalchemy import SQLAlchemy
from Modules.vader_sentiment import vaderSentiment
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
app=Flask(__name__,template_folder='template')
db=SQLAlchemy(app)
app.config['DEBUG'] = True
app.config["CLIENT_CSV"] = "F:/Inframind//file"

db.init_app(app)
bootstrap = Bootstrap(app)
df = pd.read_csv(
    "file-name.csv"
)
engine = create_engine('postgresql://postgres:root@localhost:5432/flaskmovie')
df.to_sql(
    'f', 
    engine,
    index=False, # Not copying over the index
    if_exists='replace'
)
con = psycopg2.connect(database="flaskmovie", user="postgres", password="root", host="127.0.0.1", port="5432")
cursor = con.cursor()
@app.route('/',methods=["POST","GET"])
def hello_world():   
    return render_template('home.html')
@app.route('/result',methods=["POST","GET"])
def user():
    if request.method=='POST':
        result=request.form["firstname"]
        obj=fetchData()
        obj.createCsv(result)
        result=obj.operationHandling()
        dats=obj.pie_chart()
        cursor.execute("select tweet from f")
        results = cursor.fetchall()
        sql = "COPY (SELECT * FROM f) TO STDOUT WITH CSV DELIMITER ';'"
        with open("file.csv", "w") as file: 
            cursor.copy_expert(sql, file)
        return render_template("result.html",result=result,dats=dats,da=results)             
@app.route('/download')
def download_file():
    p="file.csv"
    return send_file(p,as_attachment=True)

@app.route('/compare')
def hi():
    return render_template('compare.html')
x = 1
y=1
@app.route('/price',methods=['POST','GET'])
def input():  
    url = request.form['1']
    req_price = int(request.form['2'])
    email_user = request.form['3']
    global x
    if "flipkart" in url.lower() :
        print("Flipkart:\n")
        res = requests.get(f'{url}')
        soup = BeautifulSoup(res.text,'html.parser')
        name = soup.select('._35KyD6')[0].getText()
        price = soup.select('._3qQ9m1')[0].getText()
        price = int(price[1:].replace(",",""))
    elif "amazon" in url.lower():
        print("Amazon:\n")
        res = requests.get(url,headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        name = soup.select("#title")[0].getText().strip()
        try:
            price = soup.select("#priceblock_dealprice")[0].getText().strip()
        except:
            price = soup.select("#priceblock_ourprice")[0].getText().strip()
        price_num = price.replace("₹","")
        price_num = price_num.replace(",","")
        price = int(float(price_num))
    if (price <= req_price) :
            email = EmailMessage()
            email['from'] = 'Price tracker'
            email['to'] = email_user
            email['subject'] = 'The price of product is drop down to your requirment'

            email.set_content(f'Product Name: {name}\nPrice:{price}\n Link: "{url}"')
            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login('enchalwarpranjal@gmail.com','Pranjal@12345')
                smtp.send_message(email)
#             
            x=x+1
    else:
        global y
        print(y)
        if (y<=1):
            email = EmailMessage()
            email['from'] = 'Price tracker'
            email['to'] = email_user
            email['subject'] = 'Price Tracker'

            email.set_content(f'We Will Let You Know When The Price of the product dropped down to you requirement. \nProduct Name: {name}\nCurrent Price:{price}\n')
            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login('enchalwarpranjal@gmail.com','Pranjal@12345')
                smtp.send_message(email)
                y=y+1
                print("Email Send")
        else:
            print("Price Is Still Larger Than The Required Price")
    return render_template("compare_result.html",user=name,useremail=email_user,price=price,userprice=req_price,url=url)    

if __name__=='__main__':
    app.run(debug=True)

 
