from flask import Flask, request, render_template, url_for, redirect, flash
from forms import ChooseChart, SettingsOfCompany
import urllib.request, json
import requests, sys

###
import os
app_run_address = os.environ.get('APP_ADDRESS', '0.0.0.0')
app_run_port = os.environ.get('APP_PORT', '5001')
app_query_url = os.environ.get('APP_QUERY_URL', 'http://127.0.0.1:5002/logic/query_data')
app_settings_url = os.environ.get('APP_SETTINGS_URL', 'http://127.0.0.1:5004/start')
app_settings_save_url  = os.environ.get('APP_SETTINGS_SAVE_URL', 'http://127.0.0.1:5004/save')
# app_is_cheat = os.environ.get('APP_IS_CHEAT', False) 
app_is_cheat =  'APP_IS_CHEAT' in os.environ

app = Flask(__name__)

### run : python3 server_flask.py 0.0.0.0 5001 http://127.0.0.1:5002/logic/query_data http://127.0.0.1:5004/start http://127.0.0.1:5004/save
# if run python3 server_flask.py 0.0.0.0 - it is a cheat-mod (queires to worldtradingdata ) test
# app_run_address = '0.0.0.0'  if len(sys.argv) < 2 else sys.argv[1]
# app_run_port = '5001'  if len(sys.argv) < 3 else sys.argv[2]
# app_query_url = "http://127.0.0.1:5002/logic/query_data" if len(sys.argv) < 4 else sys.argv[3]
# app_settings_url = "http://127.0.0.1:5004/start" if len(sys.argv) < 5 else sys.argv[4]
# app_settings_save_url  = "http://127.0.0.1:5004/save"  if len(sys.argv) < 6 else sys.argv[5]
# app_is_cheat = True if  len(sys.argv) <= 2 and app_run_address == '0.0.0.0' else False

app.config['SECRET_KEY'] = 'you-will-never-guess'
needed_values = ['symbol', 'name', 'price', 'price_open','day_high', 'day_low',  'market_cap', 'volume']

list_of_symbol_default = ["V","JNJ","WMT","PG"]
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
        if app_is_cheat:
            with urllib.request.urlopen(url_full_path) as url:
                data = json.loads(url.read().decode())
        else:
            data_loaded = {"symbols":list_of_symbol_default,"query_type":"realtime"}
            print("data_loaded=",type(json.dumps(data_loaded)))
            post_req = requests.post(app_query_url, json=data_loaded)
            data = post_req.json()
    except Exception as err:
        print(err)
        url_full_path = path_online_data+params_online_data_default
        print("Bad data for request. Use default url: " + url_full_path)
        with urllib.request.urlopen(url_full_path) as url:
            data = json.loads(url.read().decode())
    print (url_full_path, data)
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
        url_full_path=path_intraday+"?symbol="+userdata["symbol"]+"&interval="+userdata["interval"]+"&range="+userdata["range"]+"&api_token="+userdata["api_token"]

        if app_is_cheat:
            with urllib.request.urlopen(url_full_path) as url:
                data = json.loads(url.read().decode())
        else:
            data_loaded = {"symbols":userdata["symbol"],"query_type":"intraday", "day_range":userdata["range"],"time_interval":userdata["interval"]}
            print("data_loaded=",type(json.dumps(data_loaded)))
            post_req = requests.post(app_query_url, json=data_loaded)
            data = post_req.json()
        print (url_full_path, data)
    except:
        print("Bad data for request. Use default url: " + path_intraday+params_intraday)
        with urllib.request.urlopen(path_intraday+params_intraday) as url:
            data = json.loads(url.read().decode())
        print(data)
    return data

def receive_symbol_list_from_settings_db():
    global list_of_symbol_default
    try:
        res = requests.get(app_settings_url)
        str_of_symbols=json.loads(res.text)[0].get("symbol")
        list_of_symbol_default = str_of_symbols.replace(',', ' ').split()
        print("Success reading from db: ",str_of_symbols, list_of_symbol_default)
    except Exception as err:
        print("Using default value. Error during restoring from  ConfigMGR:", err, list_of_symbol_default)
    return


@app.route('/api/charts/', methods=['post', 'get'])
def draw_charts( userdata=None ): # not working parameters
    data = receive_data_for_charts( userdata=userdata )
    return render_template('chart_high_low.html', stock_data = data)

@app.route('/index', methods=('GET', 'POST'))
@app.route('/', methods=('GET', 'POST'))
def stock_app_main():
   form = ChooseChart()
   global additional_data, list_of_dict

   receive_symbol_list_from_settings_db()
   list_of_dict = receive_data_for_table()
   if request.method == 'GET':
       additional_data = None
       return render_template('main_table_with_chart.html', form = form , title='StockApp',
           list_of_dict=list_of_dict,  values = needed_values, additional_data = additional_data)
   elif request.method == 'POST':
       if form.validate() == False:
           # flash('Please, All fields are required.')
           additional_data = None
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
       try:
           # res = requests.get(app_settings_url)
           # str_of_symbols=json.loads(res.text)[0].get("symbol")+" "
           pass
       except Exception as err:
           print("Error during restoring from  ConfigMGR:", err)
       return render_template('settings.html', form = form , title='StockApp', start_symbols = str_of_symbols[:-1:])
   elif request.method == 'POST':
       print(form.symbols_list, list_of_symbol_default)
       if form.validate():
           list_of_symbol_default = form.symbols_list.data.replace(',', ' ').split()
           print(form.symbols_list.data, list_of_symbol_default)
           try:
               res = requests.put(app_settings_save_url, json = {"symbol":form.symbols_list.data})
           except Exception as err:
               print("Error during saving to ConfigMGR:", err)
           return redirect( url_for('stock_app_main') )
       else:
           return render_template('settings.html', form = form , title='StockApp')


@app.route('/hello')
def hello_world():
    return 'Task for flask-StockApp-canary'


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
    print(app_query_url, app_is_cheat)
    app.run( host=app_run_address, port=app_run_port )
