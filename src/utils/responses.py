from flask import jsonify


def generic_response(code, data, message=None, params=None):
    return jsonify({
        "status": True if code == 200 else False,
        "data": data if code == 200 else {},
        "error_params": params if code != 200 else {},
        "error": message if code != 200 else {}
    }), code


def response_error(message, params=None, status_code=400):
    if params is None:
        params = {}
    return generic_response(status_code, None, message, params)


def response_success(data=None):
    if data is None:
        data = {}
    return generic_response(200, data)


def response_success_paging(items, total, pages, has_next, has_prev):
    return response_success({
        "meta": {
            "next": has_next,
            "prev": has_prev,
            "pages": pages,
            "total_items": total,
        },
        "items": items
    })
