import csv

from dataclasses import dataclass
from typing import Dict, List


PAGE_SIZE = 3
BOOK_NAME = 'contactbook.csv'


@dataclass
class Contact:
    """Представляет контакт в телефонной книге."""
    full_name: str
    organization: str
    work_number: str
    personal_number: str

    def to_dict(self) -> Dict[str, str]:
        """Преобразует объект Contact в словарь."""
        return {
            'ФИО': self.full_name,
            'Организация': self.organization,
            'Рабочий номер': self.work_number,
            'Личный номер': self.personal_number
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Contact':
        """Создает объект Contact из словаря."""
        return cls(
            full_name=data['ФИО'],
            organization=data['Организация'],
            work_number=data['Рабочий номер'],
            personal_number=data['Личный номер']
        )

    def edit(self) -> None:
        """Позволяет редактировать поля контакта."""
        print('Какое поле хотите изменить?')
        print('1. ФИО;')
        print('2. Организация;')
        print('3. Рабочий номер;')
        print('4. Личный номер;')
        print('5. Выход')
        field = input('Введите цифру: ')
        if field == '1':
            self.full_name = input('Введите ФИО: ')
        elif field == '2':
            self.organization = input('Введите организацию: ')
        elif field == '3':
            self.work_number = input('Введите рабочий номер: ')
        elif field == '4':
            self.personal_number = input('Введите личный номер: ')
        elif field == '5':
            pass
        else:
            print('Попробуйте еще раз')


def get_contacts() -> List[Dict[str, str]]:
    """Читает контакты из csv-файла и возвращает список словарей контактов."""
    with open(BOOK_NAME, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        contacts = list(reader)
    return contacts


def update_contactbook(contacts: List[Dict[str, str]]) -> None:
    """Обновляет файл контактов с новыми данными."""
    with open(BOOK_NAME, 'w', newline='', encoding='utf-8') as file:
        headers = ['ФИО', 'Организация', 'Рабочий номер', 'Личный номер']
        writer = csv.DictWriter(file, fieldnames=headers)

        writer.writeheader()

        writer.writerows(contacts)


def show_page(contacts: List[Dict[str, str]], page_num: int) -> None:
    """Выводит на экран страницу контактов."""
    start_index = (page_num - 1) * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    for index, contact in enumerate(contacts[start_index:end_index],
                                    start=start_index + 1):
        print(f"Запись №{index}:")
        print(f"  ФИО: {contact['ФИО']}")
        print(f"  Организация: {contact['Организация']}")
        print(f"  Рабочий номер: {contact['Рабочий номер']}")
        print(f"  Личный номер: {contact['Личный номер']}")
        print("-" * 30)


def add_contact(contacts: List[Dict[str, str]], entry: Contact) -> None:
    """Добавляет новый контакт в список и обновляет файл."""
    new_contact = entry.to_dict()
    contacts.append(new_contact)
    update_contactbook(contacts)


def edit_contact(contacts: List[Dict[str, str]],
                 edited_contact: Contact,
                 index: int) -> None:
    """Редактирует существующий контакт в списке контактов и обновляет файл."""
    contacts[index] = edited_contact.to_dict()
    update_contactbook(contacts)


def search_contacts(contacts: List[Dict[str, str]],
                    search_field: str,
                    search_query: str) -> List[Dict[str, str]]:
    """Выполняет поиск контактов по указанному полю и запросу."""
    result = []
    for contact in contacts:
        if search_query.lower() in contact[search_field].lower():
            result.append(contact)
    return result


def search_process(search_field: str) -> None:
    """Логика поиска и редактирования записей в телефонной книге."""
    contacts = get_contacts()
    search_query = input('Введите запрос для поиска: ')
    search_results = search_contacts(
        contacts,
        search_field,
        search_query
        )

    if not search_results:
        print('\nНичего не найдено.')
        return

    page_num = 1

    while True:
        show_page(search_results, page_num)
        choice = input(
            "Введите 'n' для следующей страницы, 'p' для предыдущей, "
            "'r' для редактирования, или любую другую клавишу для выхода: "
            )
        if choice.lower() == 'n':
            page_num += 1
            if page_num > len(contacts) // PAGE_SIZE + 1:
                page_num = len(contacts) // PAGE_SIZE + 1

        elif choice.lower() == 'p' and page_num > 1:
            page_num -= 1

        elif choice.lower() == 'r':
            edit_index = (
                int(input('Введите номер записи для редактирования: ')) - 1
            )
            contact = Contact.from_dict(search_results[edit_index])
            if 0 <= edit_index < len(search_results):
                contact.edit()
                edit_contact(
                    contacts,
                    edited_contact=contact,
                    index=contacts.index(search_results[edit_index])
                    )
                update_contactbook(contacts)
            else:
                print('Некорректный номер записи')
        else:
            break


def main() -> None:
    while True:
        print('\nГлавное меню')
        print('\nВыберите действие: ')
        print('1. Вывести записи;')
        print('2. Добавить запись;')
        print('3. Поиск записей;')
        print('4. Выход.')
        option = input('Введите цифру: ')

        if option == '1':
            contacts = get_contacts()
            page_num = 1

            while True:
                show_page(contacts, page_num)
                choice = input(
                    "Введите 'n' для следующей страницы, 'p' для предыдущей, "
                    "'r' для редактирования,"
                    " или любую другую клавишу для выхода: "
                    )
                if choice.lower() == 'n':
                    page_num += 1
                    if page_num > len(contacts) // PAGE_SIZE + 1:
                        page_num = len(contacts) // PAGE_SIZE + 1

                elif choice.lower() == 'p' and page_num > 1:
                    page_num -= 1

                elif choice.lower() == 'r':
                    edit_index = (
                        int(input('Введите номер записи для редактирования: ')) - 1
                    )
                    contact = Contact.from_dict(contacts[edit_index])
                    if 0 <= edit_index < len(contacts):
                        contact.edit()
                        edit_contact(
                            contacts,
                            edited_contact=contact,
                            index=edit_index
                            )
                        update_contactbook(contacts)
                    else:
                        print('Некорректный номер записи')
                else:
                    break

        elif option == '2':
            while True:
                contacts = get_contacts()
                contact = Contact(
                    input('\nВведите ФИО: '),
                    input('Введите организацию: '),
                    input('Введите рабочий номер: '),
                    input('Введите личный номер: ')
                    )
                add_contact(contacts, contact)
                print('Запись успешно добавлена!')
                choice = input('\nДобавить еще одну запись? (y/n): ')
                if choice.lower() == 'n':
                    break

        elif option == '3':
            while True:
                contacts = get_contacts()
                print('\nПоиск записей')
                print('\nПо какому полю будем искать?')
                print('1. ФИО;')
                print('2. Организация;')
                print('3. Рабочий номер;')
                print('4. Личный номер;')
                print('5. Выход.')
                choice = input('Введите цифру: ')
                if choice in ('1', '2', '3', '4'):
                    search_field = {
                        '1': 'ФИО',
                        '2': 'Организация',
                        '3': 'Рабочий номер',
                        '4': 'Личный номер'
                    }[choice]
                    search_process(search_field)
                elif choice == '5':
                    break
                else:
                    print('\nТакой опции нет.')

        elif option == '4':
            break

        else:
            print('\nК сожалению, такого выбора нет.')


if __name__ == '__main__':
    main()
