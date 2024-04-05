class Member:
    def __init__(self, surname=None, name=None, phone_number=None, from_line=None):
        if from_line is None:
            self.surname = surname
            self.name = name
            self.phone_number = phone_number
        else:
            self.surname = from_line.replace(" ", '').split("|")
            self.name = from_line.replace(" ", '').split("|")
            self.phone_number = from_line.replace(" ", '').split("|") 
    def input_characters(self):
        self.surname = input("Введите фамилию: ").capitalize()
        self.name = input("Введите имя: ").capitalize()
        self.phone_number = input("Введите номер телефона: ")

    def __str__(self):
        return ('{}, {}, {}'.format(self.surname, self.name, self.phone_number)) + '\n'

class Contacts:
    def find_member(self, query):
        with open('contact_book.txt') as file:
            for line in file:
                member = Member(from_line = line)
                if (member.surname, member.name) == query:
                    return member

#class Contacts:
#    def find_member(self, query = None):
#        with open("contact_book.txt", "r+") as file:
#            for line in file:
#                member = Member(from_line = line)
#                print(query)
#                if (member.surname, member.name) == query:
#                    return member

    def add_member(self):
        m = Member()
        m.input_characters()
        if c.find_member(query=(m.surname, m.name)) is None:
            f = open("contact_book.txt", "a")
            f.write('{}, {}, {}'.format(m.surname, m.name, m.phone_number) + '\n')
            print('\nКонтакт {SurName} {name} успешно добавлен\n'.format(SurName=m.surname, name=m.name) + '\n')
            f.close()
        else:
            print('Такой контакт уже есть')

    def delete_member(self, query):
        objects = []
        f = open("contact_book.txt", "r+")
        for line in f.readlines():
            member = Member(from_line=line)
            objects.append(member)
        for object in objects:
            if (member.name, member.name) != query:
                f.write(object.__str__())

    def show_all_contacts(self):
        with open("contact_book.txt", "r") as file:
            for line in file:
                member = Member(from_line=line)
                print(member)

def choice():
    selector = None
    try:
        selector = int(input('Введите "1" если хотите найти контакт\n' + \
                             'Введите "2" если хотите добавить новый контакт\n' + \
                             'Введите "3" если хотите удалить контакт\n' + \
                             'Введите "4" если хотите просмотреть всю адресную книгу\n' + \
                             '->:'))
    except ValueError:
        print('\n\nНе корректный ввод!\n')
        print('Необходимо ввести целое число!\n\n')
    return selector

c = Contacts()
while True:
    selector = choice()
    if selector == 1:
        query = ((input('Для поиска контакта введите фамилию: ').capitalize(),
                  input('Для поиска контакта введите имя: ').capitalize()))
        print(c.find_member(query))
    elif selector == 2:
        c.add_member()
    elif selector == 3:
        query = ((input('Для удаления контакта введите фамилию: ').capitalize(),
                  input('Для удаления контакта введите имя: ').capitalize()))
        c.delete_member(query)
    elif selector == 4:
        c.show_all_contacts()
    