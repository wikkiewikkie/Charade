import copy
import elizabeth
import random
import sys


class Charade:

    def __init__(self, prefix="CHARADE", fill=6, start=1, size=500):
        self.prefix = prefix
        self.fill = fill
        self.start = start
        self.index = 1
        self.size = size

        self.language = 'en'

        self.people = [Person(self) for x in range(0, int(self.size/50) or 2)]

        print(self.people)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.size:
            random.seed()
            d = random.choice([Email(self), Email(self), Email(self), Email(self), File(self)])
            self.index += len(d) + 1
            return d
        else:
            raise StopIteration

    def __repr__(self):
        return "Charade({}, {}, {})".format(self.prefix, self.fill, self.start)


class GenericCollection:

    def __init__(self, instance, parent=None):
        self.instance = instance
        self.parent = parent

        self.index = 0
        self.start = copy.copy(self.instance.index)

        self.document_id = "{}{}".format(self.instance.prefix,
                                         str(self.index+self.start).zfill(self.instance.fill))

        if sys.version_info >= (3, 6):
            self.child_count = random.choices(range(0, 20),
                                              weights=[100, 50, 20, 10, 5,
                                                       5, 3, 3, 2, 1,
                                                       1, 1, 1, 1, 1,
                                                       1, 1, 1, 1, 1])
        else:
            self.child_count = random.randint(0, 20)

    def __iter__(self):
        return self

    def __len__(self):
        return self.child_count


class Email(GenericCollection):

    def __init__(self, instance, parent=None):
        super().__init__(instance, parent)

    def __repr__(self):
        return "Email({})".format(self.instance)

    def __next__(self):
        if self.child_count > 0 and self.index < self.child_count:
            self.index += 1
            return EmailAttachment(self, self.index+self.start)
        else:
            raise StopIteration


class EmailAttachment:

    def __init__(self, parent, start):
        self.parent = parent
        self.start = start

        self.document_id = "{}{}".format(self.parent.instance.prefix, str(start).zfill(self.parent.instance.fill))
        self.parent_id = self.parent.document_id

    def __repr__(self):
        return "EmailAttachment({}, {})".format(self.parent, self.start)

    def __len__(self):
        return 1


class File(GenericCollection):

    def __init__(self, instance, parent=None):
        super().__init__(instance, parent)

    def __next__(self):
        if self.child_count > 0 and self.index < self.child_count:
            self.index += 1
            return File(self.instance, parent=self)
        else:
            raise StopIteration

    def __repr__(self):
        return "File({})".format(self.instance)


class Image:

    def __init__(self, parent):
        self.parent = parent


class Person:

    def __init__(self, instance):
        self.instance = instance
        p = elizabeth.Personal(self.instance.language)

        self.email = p.email()
        self.name_first = p.name()
        self.name_last = p.surname()
        self.title = p.title()
        self.username = p.username()

        self.email_formatted = "{}, {} <{}>".format(self.name_last, self.name_first, self.email)



