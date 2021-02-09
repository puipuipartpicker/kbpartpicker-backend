from flask import jsonify

def handle_exception(error):
    print("I'm BEING calleD!!")
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
