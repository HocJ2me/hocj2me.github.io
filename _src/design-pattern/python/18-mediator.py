"""Mediator – Python 3."""


class ClassChatRoom:                                # Concrete Mediator
    def __init__(self, name):
        self.name, self.users = name, []

    def join(self, user):
        self.users.append(user)
        print(f"[{self.name}] {user.name} đã tham gia")

    def broadcast(self, msg, sender):
        tag = "📌 " if isinstance(sender, Teacher) else ""
        for u in self.users:
            if u is not sender:
                u.receive(tag + msg, sender.name)

    def send_private(self, msg, sender, to):
        for u in self.users:
            if u.name == to:
                u.receive("(riêng) " + msg, sender.name)


class User:                                         # Colleague
    def __init__(self, name, room):
        self.name, self.room = name, room
        room.join(self)

    def send(self, msg):
        print(f"{self.name} gửi: {msg}")
        self.room.broadcast(msg, self)

    def send_private(self, to, msg):
        print(f"{self.name} nhắn riêng {to}: {msg}")
        self.room.send_private(msg, self, to)

    def receive(self, msg, sender):
        print(f"    -> {self.name} nhận từ {sender}: {msg}")


class Student(User): pass
class Teacher(User): pass


if __name__ == "__main__":
    room = ClassChatRoom("Lớp 10A1")
    teacher = Teacher("Thầy Tuyền", room)
    an, binh, chi = Student("An", room), Student("Bình", room), Student("Chi", room)
    an.send("Mọi người làm bài tập Builder chưa?")
    teacher.send("Hạn nộp là 20h tối nay nhé!")
    binh.send_private("Chi", "Cho mình mượn vở ghi với")
    chi.send("Bài này dài quá :(")
