from flask import Flask, jsonify

application = Flask(__name__)
application.url_map.strict_slashes = False


@application.route('/', methods=['GET'])
def root():
    return {'status': 'success'}, 200


@application.route('/cats', methods=['GET'])
def cats():
    return [{'color': 'calico'}], 200


@application.route('/apis/example.com/v1alpha1', methods=['GET'])
def api_discovery0():
    # Adjust this response based on your specific API's resources and requirements
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
@application.route('/example.com/v1alpha1', methods=['GET'])
def api_discovery():
    # Adjust this response based on your specific API's resources and requirements
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


@application.route('/v1alpha1', methods=['GET'])
def api_discovery2():
    # Adjust this response based on your specific API's resources and requirements
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


if __name__ == '__main__':
    context = ('certs/server.crt', 'certs/server.key')
    application.run(debug=True, host='0.0.0.0', port=443, ssl_context=context)
