from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():

    # USE URL OF MYSPEED (for api)
#----------------------------------------------------------------------------------
    url = "http://MYSPEED_URL/api/speedtests?hours=24"
#----------------------------------------------------------------------------------
    
    response = requests.get(url)
    if response.status_code != 200:
        return "Error", 500
    
    data = response.json()
    
    valid_results = [result for result in data if 'error' not in result]
    
    if not valid_results:
        return "None.", 500
    
    last_result = valid_results[0]

    download = last_result.get('download', 'N/A')
    upload = last_result.get('upload', 'N/A')
    ping = last_result.get('ping', 'N/A')


    # CHOISE TEMPLATE Large or Medium
#----------------------------------------------------------------------------------
    return render_template('large.html', download=download, upload=upload, ping=ping)
#----------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765)
