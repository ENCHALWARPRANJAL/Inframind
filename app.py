from flask import Flask,render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap
from Modules.fetch_data import fetchData
from Modules.vader_sentiment import vaderSentiment
app=Flask(__name__,template_folder='template')
bootstrap = Bootstrap(app)
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
        return render_template("result.html",result=result)
@app.route('/pie_chart',methods=["POST","GET"])
def users():
    if request.method=='POST':
        result=request.form["firstname"]
        obj=fetchData()
        obj.createCsv(result)
        result=obj.operationHandling()
        obj.pie_chart()
        return render_template("pie_chart.html")



if __name__=='__main__':
    app.run(debug=True)

serve(app, host='0.0.0.0', port=8080, threads=1)    
