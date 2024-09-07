from enum import Enum


class DocumentType(Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    READ = "READ"

# Enum으로 변환
def convert(enum_class, value):
    try:
        return enum_class(value.upper())
    except (ValueError, AttributeError):
        return None
