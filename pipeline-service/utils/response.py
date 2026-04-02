def success_response(data=None, message="success"):
    return {
        "status": "ok",
        "message": message,
        "data": data
    }

def error_response(message="error", details=None):
    return {
        "status": "error",
        "message": message,
        "details": details
    }
    
def pagination_response(data, message="success"):
    total_pages = (data['total'] + data['limit'] - 1)

    return {
        "status": "ok",
        "message": message,
        "data": data['data'],
        "meta": {
            "total": data['total'],
            "page": data['page'],
            "limit": data['limit'],
            "total_pages": total_pages
        }
    }