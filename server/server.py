from flask import Flask, request, url_for
import requests
import os
import json
app = Flask(__name__)

# from OpenSSL import SSL
# context = SSL.Context(SSL.SSLv23_METHOD)
# context.use_privatekey_file(os.getcwd()+'/server/server.key')
# context.use_certificate_file(os.getcwd()+'/server/server.crt')

@app.route('/')
def hello_world():
    return 'Hello, World'

@app.route('/verifybait', methods=['POST', 'GET'])
def verify():
    if request.method == 'POST':
        #print request.form.get('title')
        print request.form.get('link')

        # do computation with title and link
        result = "not bait"

        # send a post request to extention
        # r = requests.post('http://extentionhere.com', data = {'result': result})
        url = "https://explaintome.herokuapp.com/api/v1.0/summary"
        headers = {'Content-Type': "application/json", 'Accept': '*/*'}
        data = {
            "url": request.form.get('link'),
            "max_sent": 1,
            "lang": "en"
        }
        
        r = requests.post(url, headers=headers, data=json.dumps(data))
        d = json.loads(r.text)
        
        newtitle = d["meta"]["opengraph"]["description"]
        summary = d["summary"][0]
        
        print "Title:", newtitle
        print "Summary:", summary

        # return 'verified\n'
        return "{'title': newtitle, 'summary': summary, 'clickbait': 1}\n"

    if request.method == 'GET':
        return 'Please make a POST request to get summary, corrected title and clickbait'

if __name__ == '__main__':
    context = (os.getcwd()+'/../server.crt', os.getcwd()+'/../server.key')
    app.run(host='0.0.0.0', port=5000, ssl_context=context, threaded=True, debug=True)