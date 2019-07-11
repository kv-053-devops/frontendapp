from flask import Flask, request, render_template, url_for, redirect
from forms import ChooseChart

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
needed_values = ['symbol', 'price', 'price_open','day_high', 'day_low',  'market_cap', 'volume']
list_of_dict = []

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

@app.route('/api/filters/', methods=['post', 'get'])
def filters():
    message = ''
    if request.method == 'POST':
        symbols = request.form.get('symbols')
        date_start = request.form.get('date_start')
        if symbols != '' :
            message = "Filter by company :" + symbols
        else:
            message = "No filter by company"
    return render_template('filters.html', message=message,
                            title='Task for flask',
                            list_of_dict=list_of_dict)

@app.route('/api/forms/', methods=['post', 'get'])
def login():
    form = LoginForm()
    return render_template('forms.html', title='Sign In', form=form)
    form = LoginForm()
    if form.validate_on_submit():
         # flash('Login requested for user {}, remember_me={}'.format(
         #    form.username.data, form.remember_me.data))
        print("validate - ok ")
        return redirect('/api/forms/')
    return render_template('forms.html', title='Sign In', form=form)

@app.route('/hello')
def hello_world():
    return 'Task for flask'

@app.route('/', methods=('GET', 'POST'))
def online_table():
    form = ChooseChart()
    #return render_template('main_table.html', form=form , title='StockApp',
    #                     list_of_dict=list_of_dict,  values = needed_values)
    #form = ChooseChart()
    if form.validate_on_submit():
        # flash('validate - ok {}, {}, {}'.format(form.symbols.data, form.range.data, form.interval.data))
        print(form.symbols.data)

        return redirect('/')
    return render_template('main_table.html', form=form , title='StockApp',
                            list_of_dict=list_of_dict,  values = needed_values)



if __name__ == '__main__':
    app.run()
