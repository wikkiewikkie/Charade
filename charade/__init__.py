import copy
import csv
import elizabeth
import io
import random
import sys

sys_random = random.SystemRandom()


class Charade:

    def __init__(self, prefix="CHARADE", fill=6, size=500):
        self.prefix = prefix
        self.fill = fill
        self.index = 1
        self.size = size

        self.language = 'en'

        self.people = [Person(self) for x in range(0, int(self.size/50))]
        while len(self.people) < 15:
            self.people.append(Person(self))

        self.custodian = random.choice(self.people)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index <= self.size:
            random.seed()
            if self.index % 250 == 0:
                self.custodian = random.choice(self.people)
            d = random.choice([Email(self), Email(self), Email(self), Email(self), File(self)])
            self.index += len(d) + 1
            return d
        else:
            raise StopIteration

    def __repr__(self):
        return "Charade(prefix='{}', fill={}, size={})".format(self.prefix, self.fill, self.size)

    def delimited(self, delimiter="\x14", quote="\xfe"):
        file = io.StringIO()
        writer = csv.writer(file, delimiter=delimiter, quotechar=quote)
        for doc in self:
            writer.writerow([doc.document_id, doc.parent_id])
            for att in doc:
                writer.writerow([att.document_id, att.parent_id])
        file.seek(0)
        return file


class GenericDocument:

    def __init__(self, instance, parent=None):
        self.instance = instance
        self.parent = parent

        self.index = copy.copy(self.instance.index)

        self.document_id = "{}{}".format(self.instance.prefix, str(self.index).zfill(self.instance.fill))

        if parent:
            self.parent_id = self.parent.document_id
        else:
            self.parent_id = self.document_id

        self.delimited_fields = ['document_id', "parent_id"]
        if sys.version_info >= (3, 6):
            self.child_count = sys_random.choices(range(0, 20),
                                                  weights=[100, 50, 20, 10, 5,
                                                           5, 3, 3, 2, 1,
                                                           1, 1, 1, 1, 1,
                                                           1, 1, 1, 1, 1])[0]
        else:
            self.child_count = sys_random.randint(0, 20)

    def __iter__(self):
        return self

    def __len__(self):
        return self.child_count


class Email(GenericDocument):

    def __init__(self, instance, parent=None):
        super().__init__(instance, parent)

        self.authors = set()
        self.recipients = set()
        self.copyees = set()
        self.blind_copyees = set()

        available = set(self.instance.people)

        for attrib, mn, mx in [("authors", 1, 1),
                               ("recipients", 1, 5),
                               ("copyees", 0, 5),
                               ("blind_copyees", 0, 2)]:
            setattr(self, attrib, set(sys_random.sample(list(available), k=sys_random.randint(mn, mx))))
            available = available.difference(getattr(self, attrib))

        self.sent = elizabeth.Datetime().date()
        self.subject = elizabeth.Text().title()

    def __repr__(self):
        return "Email({})".format(self.instance)

    def __str__(self):
        return "From:\t{}\nTo:\t{}\nCC:\t{}\nBCC:\t{}\n\n{}".format("; ".join([str(x) for x in self.authors]),
                                                                    "; ".join([str(x) for x in self.recipients]),
                                                                    "; ".join([str(x) for x in self.copyees]),
                                                                    "; ".join([str(x) for x in self.blind_copyees]),
                                                                    list(self.authors)[0].email_signature)

    def __next__(self):
        if self.child_count > 0 and self.index < self.child_count:
            self.index += 1
            return EmailAttachment(self, self.index)
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


class File(GenericDocument):

    def __init__(self, instance, parent=None):
        super().__init__(instance, parent)

        self.author = random.choice(self.instance.people)

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

        self.company = elizabeth.Business(self.instance.language).company()
        self.phone = p.telephone()
        self.email = p.email()
        self.name_first = p.name()
        self.name_last = p.surname()
        self.title = p.occupation()
        self.username = p.username()

        self.email_formatted = "{}, {} <{}>".format(self.name_last, self.name_first, self.email)
        self.email_signature = "{} {}\n{}\n{}\n\n{}\n{}".format(self.name_first,
                                                                self.name_last,
                                                                self.title,
                                                                self.company,
                                                                self.email,
                                                                self.phone)

    def __str__(self):
        return self.email_formatted

