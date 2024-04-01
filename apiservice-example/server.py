from flask import Flask

application = Flask(__name__)


@application.route('/cats', methods=['GET'])
def gauge():
    return [{'color': 'calico'}], 200


if __name__ == '__main__':
    context = ('certs/server.crt', 'certs/server.key')
    application.run(debug=True, host='0.0.0.0', port=443, ssl_context=context)
