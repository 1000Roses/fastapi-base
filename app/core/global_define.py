from app.schemas.base import BaseResponse
class ErrorResponse:
    # System Messages
    DEFAULT = {
        "status": 400,
        "msg": "Chưa hiển thị được thông tin, vui lòng thử lại sau.",
        "detail": None
    }

class SystemMessages():
    DB_FAILED = BaseResponse.response(status=300, msg="Kết nối hệ thống lỗi, vui lòng thử lại sau ít phút")
    WRONG_PARAMS = BaseResponse.response(status=400, msg="Sai thông tin đầu vào, vui lòng kiểm tra lại thông tin")
    RATE_LIMIT = BaseResponse.response(status=401, msg="Bạn truy cập quá nhanh.")
    TOKEN_REQUIRED=BaseResponse.response(status=1003, msg="Token không tồn tại")
    TOKEN_EXPIRED=BaseResponse.response(status=1001, msg="Token hết hạn")
    INVALID_TOKEN=BaseResponse.response(status=1002, msg="Token không hợp lệ")
    SYSTEM_BUSY=BaseResponse.response(status=300, msg="Hệ thống đang bận, vui lòng thử lại sau ít phút")
    SYSTEM_ERROR=BaseResponse.response(status=301, msg="Có lỗi trong quá trình xử lý, vui lòng thử lại sau ít phút")