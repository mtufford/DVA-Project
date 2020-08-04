import sys
import json
sys.path.insert(1, './lib') # add lib directory to path to import modules used in ml.py

from datetime import datetime
import sqlite3
import config
import pandas as pd
import json
from flask import Flask, jsonify, request, g, render_template, Response
from lib.ml import MLRandomForestCause, MLRandomForestSizeClass, MLKnnCause, MLKnnSizeClass,\
                   MLAdaBoostCause, MLAdaBoostSizeClass, MLHistGradientBoostingCause,\
                   MLHistGradientBoostingSizeClass
from lib.process_query import convert_causes

app = Flask(__name__)
# app.config.from_object(config.DevelopmentConfig)
app.config.from_object(config.TestingConfig)

model_list = ['RF', 'KNN', 'ADABOOST', 'HISTGRADBOOST']

def dict_factory(cursor, row):
    # row reader for reading query results
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db(ret_type='None'):
    db = getattr(g, '_database', None)
    if db is None:
        db = Flask._database = sqlite3.connect(app.config.get("DATABASE"))
        if ret_type == 'dict':
            db.row_factory = dict_factory
    return db


#def do_raw_query(query):
#    cur = get_db('dict').cursor()
#    cur.execute(query)
#    result = cur.fetchall()
#    # print(result)
#    table = STable(result)
#    table.border = True
#    return table


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/', methods=['GET'])
def home():
    return app.send_static_file('frontend/index.html')


@app.route('/api/fires', methods=['GET'])
def query_fires():
    # return fires by year, state, or year and state
    # /api/fires?year={YYYY}&state={XX}

    query_parameters = request.args
    year = query_parameters.get('year')
    state = query_parameters.get('state')

    query = 'SELECT FOD_ID, FIRE_NAME, FIRE_SIZE, FIRE_SIZE_CLASS, LATITUDE, LONGITUDE, STAT_CAUSE_DESCR, date(DISCOVERY_DATE) AS DISCOVERY_DATE FROM Fires WHERE'
    to_filter = []

    if year:
        query += ' FIRE_YEAR=? AND'
        to_filter.append(year)
    if state:
        query += ' STATE=? AND'
        to_filter.append(state)
    if not (year or state):
        return page_not_found(404)
    query = query[:-4] + ';'  # remove last " AND" from query

    conn = get_db('dict')
#    cur = conn.cursor()
#    result = cur.execute(query, to_filter).fetchall()
#    return jsonify(result)

    data = pd.read_sql(query, conn, params=to_filter)
    result = convert_causes(data).to_json(orient='records')

    close_connection(None)

    return Response(response=result, status=200, mimetype="application/json")


@app.route('/api/firedetail', methods=['GET'])
def fire_detail():
    # return fire detail by fod_id
    # /api/firedetail?fod_id={}

    query_parameters = request.args
    fod_id = query_parameters.get('fod_id')

    query = 'SELECT FOD_ID, FIRE_NAME, FIRE_SIZE, FIRE_SIZE_CLASS, LATITUDE, LONGITUDE, STAT_CAUSE_DESCR, date(DISCOVERY_DATE) AS DISCOVERY_DATE, DISCOVERY_TIME, date(CONT_DATE) AS CONT_DATE, CONT_TIME, COUNTY, STATE FROM Fires WHERE'
    to_filter = []

    if fod_id:
        query += ' FOD_ID=?;'
        to_filter.append(fod_id)
    else:
        return page_not_found(404)

    conn = get_db('dict')
#    cur = conn.cursor()
#    result = cur.execute(query, to_filter).fetchall()
#    return jsonify(result)

    data = pd.read_sql(query, conn, params=to_filter)
    result = convert_causes(data).to_json(orient='records')

    return Response(response=result, status=200, mimetype='application/json')


@app.route('/api/predict', methods=['POST'])
def predict_cause_class():
    # return prediction of cause and/or fire-class-size
    # /api/predict?model={}&lat={}&long={}&date={mm-dd-yyyy}

    # parameters:
    #     model: in model_list
    #     lat: latitude
    #     long: longitude
    #     date: date in format of mm-dd-yyyy

    # initialize response dictionary
    response = {}

    # extract parameters
    query_parameters = json.loads(request.data.decode("utf-8"))
    print(query_parameters)
    model = query_parameters.get('model')
    lat_raw = query_parameters.get('latitude')
    long_raw = query_parameters.get('longitude')
    date_raw = query_parameters.get('date')

    # convert lat and long to floats
    lat = float(lat_raw)
    long = float(long_raw)

    # parse date
    date = datetime.strptime(date_raw, '%m-%d-%Y')

    # identify year, month, day-of-week
    year = date.year
    month = date.month
    day_of_week = date.weekday()

    # call model for prediction
    if model in model_list:
        response['cause'] = models[model]['CAUSE'].predict(lat, long, year, month, day_of_week)
        response['cause_model_accuracy'] = models[model]['CAUSE'].estimator.accuracy_
        response['size_class'] = models[model]['SIZE_CLASS'].predict(lat, long, year, month, day_of_week)
        response['size_class_model_accuracy'] = models[model]['SIZE_CLASS'].estimator.accuracy_
    else:
        return Response(response='Model not available.', status=400, mimetype='text/plain')

    # return prediction with model's accuracy
    return jsonify(response)


if __name__ == '__main__':
    # to use, change to (above) app.config.from_object(config.TestingConfig)
    if app.config.get("TESTING"):

        # load models to predict wildfire cause and class_size
        models = {}
        for model in model_list:
            models[model] = {}
            if model == 'RF':
                models[model]['CAUSE'] = MLRandomForestCause()
                models[model]['SIZE_CLASS'] = MLRandomForestSizeClass()
            elif model == 'KNN':
                models[model]['CAUSE'] = MLKnnCause()
                models[model]['SIZE_CLASS'] = MLKnnSizeClass()
            elif model == 'ADABOOST':
                models[model]['CAUSE'] = MLAdaBoostCause()
                models[model]['SIZE_CLASS'] = MLAdaBoostSizeClass()
            elif model == 'HISTGRADBOOST':
                models[model]['CAUSE'] = MLHistGradientBoostingCause()
                models[model]['SIZE_CLASS'] = MLHistGradientBoostingSizeClass()

            try:
                models[model]['CAUSE'].load()
            except FileNotFoundError:
                print('ERROR -- Missing file: {}\n'.format(models[model]['CAUSE'].file_name))
            try:
                models[model]['SIZE_CLASS'].load()
            except FileNotFoundError:
                print('ERROR -- Missing file: {}\n'.format(models[model]['SIZE_CLASS'].file_name))


    # begin running app
    app.run()
