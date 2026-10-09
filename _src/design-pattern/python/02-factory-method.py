"""Factory Method – Python 3. Dùng abc.ABC để khai báo lớp/phương thức trừu tượng."""
from abc import ABC, abstractmethod


# ===== Product =====
class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...


class EmailNotification(Notification):
    def send(self, message): print(f"[EMAIL] {message}")


class SmsNotification(Notification):
    def send(self, message):
        text = message[:30] + "..." if len(message) > 30 else message
        print(f"[SMS]   {text}")


class ZaloNotification(Notification):
    def send(self, message): print(f"[ZALO]  {message} 👍")


# ===== Creator =====
class NotificationService(ABC):
    @abstractmethod
    def create_notification(self) -> Notification:
        """Factory Method – lớp con quyết định tạo đối tượng nào."""

    def notify_user(self, message: str) -> None:
        n = self.create_notification()
        print(f"{type(self).__name__} -> ", end="")
        n.send(message)


# ===== Concrete Creators =====
class EmailService(NotificationService):
    def create_notification(self): return EmailNotification()


class SmsService(NotificationService):
    def create_notification(self): return SmsNotification()


class ZaloService(NotificationService):
    def create_notification(self): return ZaloNotification()


if __name__ == "__main__":
    for service in (EmailService(), SmsService(), ZaloService()):
        service.notify_user("Lớp Design Pattern bắt đầu lúc 19h tối nay!")

    # Python: lớp là "first-class object" nên Simple Factory thường chỉ là một dict
    registry = {"email": EmailNotification, "sms": SmsNotification}
    registry["sms"]().send("Tạo đối tượng từ tên lớp lưu trong dict")
