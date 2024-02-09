from src.infrastructure.secure.services import PasslibPasswordService


def get_password_service():
    return PasslibPasswordService()
