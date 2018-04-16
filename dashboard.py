import json
import requests
import sys
from copy import deepcopy

host = ''
port = ''
user = ''
password = ''
account = ''


def get_applications(host, port, user, password, account):
    url = 'https://{}:{}/controller/rest/applications'.format(host, port)
    auth = ('{}@{}'.format(user, account), password)
    print(auth)
    params = {'output': 'json'}

    print('Getting apps', url)
    r = requests.get(url, auth=auth, params=params)
    return sorted(r.json(), key=lambda k: k['name'])

def create_widgets_metric(APPS, widget_template):
    widgets = []
    counter = 0
    new_widget = widget_template
    new_dataSeries = new_widget['dataSeriesTemplates'][0]
    print(new_dataSeries)
    for application in APPS:
        app = application['name']
        app_id = application['id']
        print('Creating metrics for', app)
        if counter != 0:
            new_widget['dataSeriesTemplates'].append(deepcopy(new_dataSeries))

        
        new_widget['dataSeriesTemplates'][counter]['metricMatchCriteriaTemplate']['applicationName'] = app
        new_widget['dataSeriesTemplates'][counter]['applicationName'] = app
        new_widget['dataSeriesTemplates'][counter]['name'] = app

        counter += 1
    widgets.append(deepcopy(new_widget))
    return widgets


def process(dash):

    APPS = get_applications(host, port, user, password, account)
    new_dash = dash
    new_widgets = []
    for widget in new_dash['widgetTemplates']:

        if widget['widgetType'] == 'GraphWidget':
            
            new_widgets += create_widgets_metric(APPS,
                                                 widget)

    new_dash['widgetTemplates'] = new_widgets

    with open('new_dash_{}.json'.format(host), 'w') as outfile:
        json.dump(new_dash, outfile, indent=4, sort_keys=True)


def main():
    global host
    global port
    global user
    global password
    global account

    try:
        host = sys.argv[1] 
        port = sys.argv[2]
        user = sys.argv[3]
        password = sys.argv[4]
        account = sys.argv[5]

        with open('dashboard.json') as json_data:
            d = json.load(json_data)
            process(d)

    except:
        print 'dashboard.py <host> <port> <user> <password> <account>'
        sys.exit(2)

if __name__ == '__main__':
    main()
