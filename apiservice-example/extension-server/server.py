from flask import Flask, jsonify

application = Flask(__name__)
application.url_map.strict_slashes = False


# the example does not include authentication and dynamic discovery information
# Note: in this extension approach resources do not translate into Kubernetes known resources
@application.route('/apis/example.com/v1alpha1', methods=['GET'])
def api_discovery0():
    return jsonify({
        "kind": "APIResourceList",
        "apiVersion": "v1alpha1",
        "groupVersion": "example.com/v1alpha1",
        "resources": [
            {
                "name": "cats",
                "singularName": "",
                "namespaced": True,
                "kind": "Cat",
                "verbs": ["get", "list"]
            }
        ]
    }), 200

@application.route('/apis/example.com/v1alpha1/cats', methods=['GET'])
def cats():
    return jsonify(["cat1", "cat2"]), 200

@application.route('/apis/example.com/v1alpha1/cats/<name>', methods=['GET'])
def cat(name):
    return jsonify({
        "name": name,
        "age": 3,
        "breed": "siamese"
    }), 200


if __name__ == '__main__':
    context = ('certs/server.crt', 'certs/server.key')
    application.run(debug=True, host='0.0.0.0', port=443, ssl_context=context)
