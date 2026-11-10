"""Lỗi nghiệp vụ. Tầng API chịu trách nhiệm ánh xạ chúng sang mã HTTP."""


class DomainError(Exception):
    """Lớp cha của mọi lỗi nghiệp vụ."""


class NotFoundError(DomainError):
    """Không có dữ liệu cho mã được yêu cầu."""
