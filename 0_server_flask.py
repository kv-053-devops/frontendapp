from flask import Flask, request, render_template, url_for, redirect, flash
from forms import ChooseChart, SettingsOfCompany
import urllib.request, json
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = 'you-will-never-guess'
needed_values = ['symbol', 'name', 'price', 'price_open','day_high', 'day_low',  'market_cap', 'volume']

list_of_symbol_default = ["V","JNJ","AAPL","FB","MSFT","AMZN","GOOGL"]
list_of_dict = []
additional_data = None

def receive_data_for_table( list_of_symbol=None ):
    path_online_data="https://api.worldtradingdata.com/api/v1/stock"
    params_online_data_default = "?symbol=MSFT,AAPL,FB,GOOGL,AMZN&api_token=a5bU3AxoLKNcgBMMSqVJoLRYvPhyw6l2J55ucjjk2GQ9sTxT0t7YI8FdkxBo"
    if list_of_symbol is None or not isinstance(list_of_symbol, list):
        list_of_symbol = list_of_symbol_default
    try:
        url_full_path=path_online_data+"?symbol="
        for symbol in list_of_symbol:
            url_full_path += (str(symbol)+",")
        url_full_path = url_full_path[:-1:]+"&api_token=a5bU3AxoLKNcgBMMSqVJoLRYvPhyw6l2J55ucjjk2GQ9sTxT0t7YI8FdkxBo"
        with urllib.request.urlopen(url_full_path) as url:
            data = json.loads(url.read().decode())
        print (url_full_path, data)
    except:
        url_full_path = path_online_data+params_online_data_default
        print("Bad data for request. Use default url: " + url_full_path)
        with urllib.request.urlopen(url_full_path) as url:
            data = json.loads(url.read().decode())
        print(data)
    return data.get('data',[])



def receive_data_for_charts(userdata=None):
    path_intraday = "https://intraday.worldtradingdata.com/api/v1/intraday"
    params_intraday = "?symbol=AAPL&interval=60&range=10&api_token=a5bU3AxoLKNcgBMMSqVJoLRYvPhyw6l2J55ucjjk2GQ9sTxT0t7YI8FdkxBo"
    if userdata is None:
        userdata = additional_data
    try:
        userdata["symbol"] = str(userdata.get('symbol', "AAPL"))
        userdata["interval"] = str(userdata.get('interval', "60"))
        userdata["range"] = str(userdata.get('range', "30"))
        userdata["api_token"] = str(userdata.get("api_token", "a5bU3AxoLKNcgBMMSqVJoLRYvPhyw6l2J55ucjjk2GQ9sTxT0t7YI8FdkxBo"))
        # resp = requests.get(path_intraday, data=userdata)
        # data = resp.json()
        url_full_path=path_intraday+"?symbol="+userdata["symbol"]+"&interval="+userdata["interval"]+"&range="+userdata["range"]+"&api_token="+userdata["api_token"]
        with urllib.request.urlopen(url_full_path) as url:
            data = json.loads(url.read().decode())
        print (url_full_path, data)
    except:
        print("Bad data for request. Use default url: " + path_intraday+params_intraday)
        with urllib.request.urlopen(path_intraday+params_intraday) as url:
            data = json.loads(url.read().decode())
        print(data)
    return data

@app.route('/api/charts/', methods=['post', 'get'])
def draw_charts( userdata=None ): # not working parameters
    data = receive_data_for_charts( userdata=userdata )
    return render_template('chart_high_low.html', stock_data = data)

@app.route('/index', methods=('GET', 'POST'))
@app.route('/', methods=('GET', 'POST'))
def stock_app_main():
   form = ChooseChart()
   global additional_data, list_of_dict

   list_of_dict = receive_data_for_table()
   if request.method == 'GET':
       additional_data = None
       return render_template('main_table_with_chart.html', form = form , title='StockApp',
           list_of_dict=list_of_dict,  values = needed_values, additional_data = additional_data)
   elif request.method == 'POST':
       if form.validate() == False:
           # flash('Please, All fields are required.')
           return render_template('main_table_with_chart.html', form = form , title='StockApp',
                    list_of_dict=list_of_dict,  values = needed_values, additional_data = additional_data)
       else:
           additional_data = dict(symbol=form.symbols.data, interval=form.interval.data, range=form.range.data)
           print(form, additional_data)
           data = receive_data_for_charts( userdata=additional_data )
           return render_template('main_table_with_chart.html', form = form , title='StockApp',
                list_of_dict=list_of_dict,  values = needed_values, additional_data = additional_data, stock_data = data)
           # return redirect(url_for('draw_charts', userdata=dict(symbol=form.symbols.data, interval=form.interval.data, range=form.range.data) ))

@app.route('/settings', methods=('GET', 'POST'))
def settings():
   form = SettingsOfCompany()
   global list_of_symbol_default

   str_of_symbols = ""
   for symbol in list_of_symbol_default: #join to do
       str_of_symbols += (str(symbol)+",")
   # form.symbols_list.data = str_of_symbols[:-1:] # not working
   if request.method == 'GET':
       return render_template('settings.html', form = form , title='StockApp', start_symbols = str_of_symbols[:-1:])
   elif request.method == 'POST':
       print(form.symbols_list, list_of_symbol_default)
       if form.validate():
           list_of_symbol_default = form.symbols_list.data.replace(',', ' ').split()
           print(form.symbols_list.data, list_of_symbol_default)
           return redirect( url_for('stock_app_main') )
       else:
           return render_template('settings.html', form = form , title='StockApp')


@app.route('/hello')
def hello_world():
    return 'Task for flask-StockApp'


@app.route('/api/add', methods=['POST'])
def add():
    try:
        if request.method == 'POST':
            data = request.get_json()
            print(str(request) + "\n***********\n"+str(data)+"\n***********\n")
            list_of_dict.append(data)
    except:
        print("This didn't work.")
    print(str(list_of_dict)+"\n***********\n")
    return ""


@app.route('/api/list', methods=['GET'])
def return_all_jsons():
    return render_template("table.html",
                           title='Task for flask',
                           list_of_dict=list_of_dict,
                           values = needed_values)


if __name__ == '__main__':
    app.run()
