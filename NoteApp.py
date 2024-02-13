import json
import os
from datetime import datetime
from Note import Note  # Импортируем класс Note из другого модуля


class NotesApp:
    def __init__(self, file_path='notes.json'):
        """
        Конструктор класса NotesApp.
        Инициализирует file_path и загружает заметки из файла.
        """
        self.file_path = file_path
        self.notes = self.load_notes()

    def load_notes(self):
        """
        Загружает заметки из JSON-файла.
        """
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    notes_data = json.load(file)
                return [Note(**note_data) for note_data in notes_data]
            else:
                return []
        except FileNotFoundError:
            print(f'Файл {self.file_path} не найден.')
            return []
        except json.JSONDecodeError:
            print(f'Ошибка при загрузке файла {self.file_path}. Файл поврежден или имеет неверный формат.')
            return []

    def save_notes(self):
        """
        Сохраняет заметки в JSON-файл.
        """
        notes_data = [{'note_id': note.note_id, 'title': note.title, 'body': note.body, 'timestamp': note.timestamp} for
                      note in self.notes]
        try:
            with open(self.file_path, 'w') as file:
                json.dump(notes_data, file, indent=4)
        except IOError:
            print(f'Ошибка при сохранении файла {self.file_path}. Проверьте правильность доступа к файлу.')

    def add_note(self, title, body):
        """
        Добавляет новую заметку с указанным заголовком и содержимым.
        """
        note_id = len(self.notes) + 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_note = Note(note_id, title, body, timestamp)
        self.notes.append(new_note)
        self.save_notes()
        print(
            f'Заметка добавлена:\nID: {note_id}\nЗаголовок: {title}\nТело заметки: {body}\nВремя создания: {timestamp}')

    def view_notes(self, filter_date=None):
        """
        Выводит все заметки.
        Если указана filter_date, выводит только заметки, созданные после этой даты.
        """
        if self.notes:
            for note in self.notes:
                if filter_date is None or datetime.strptime(note.timestamp, "%Y-%m-%d %H:%M:%S") >= filter_date:
                    print(
                        f'ID: {note.note_id}\nЗаголовок: {note.title}\nТело заметки: {note.body}\n'
                        f'Время создания: {note.timestamp}\n')
        else:
            print('Заметок нет.')

    def edit_note(self, note_id, title, body):
        """
        Редактирует заметку с указанным ID, обновляя заголовок, содержимое и временную метку.
        """
        try:
            note = next(note for note in self.notes if note.note_id == note_id)
            note.title = title
            note.body = body
            note.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_notes()
            print(
                f'Заметка отредактирована:\nID: {note_id}\nНовый заголовок: {title}\n'
                f'Новое тело заметки: {body}\nВремя редактирования: {note.timestamp}')
        except StopIteration:
            print(f'Заметка с ID {note_id} не найдена.')

    def delete_note(self, note_id):
        """
        Удаляет заметку с указанным ID.
        """
        try:
            note = next(note for note in self.notes if note.note_id == note_id)
            self.notes.remove(note)
            # Переупорядочиваем ID для оставшихся заметок
            for index, note in enumerate(self.notes, start=1):
                note.note_id = index
            self.save_notes()
            print(f'Заметка удалена:\nID: {note_id}')
        except StopIteration:
            print(f'Заметка с ID {note_id} не найдена.')

    def view_note_by_id(self, note_id):
        """
        Выводит заметку с указанным ID на экран, если она существует.
        """
        try:
            note = next(note for note in self.notes if note.note_id == note_id)
            print(
                f'ID: {note.note_id}\nЗаголовок: {note.title}\nТело заметки: {note.body}\n'
                f'Время создания: {note.timestamp}\n')
        except StopIteration:
            print(f'Заметка с ID {note_id} не найдена.')


def main():
    try:
        notes_app = NotesApp()
        while True:
            print("\nВыберите действие:")
            print("1. Просмотреть все заметки")
            print("2. Просмотреть заметки после определенной даты")
            print("3. Просмотреть заметку с указанным ID")
            print("4. Добавить заметку")
            print("5. Редактировать заметку")
            print("6. Удалить заметку")
            print("7. Выйти")

            choice = input("Введите номер действия: ")

            if choice == '1':
                notes_app.view_notes()
            elif choice == '2':
                try:
                    date_str = input("Введите дату в формате YYYY-MM-DD HH:MM:SS: ")
                    filter_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    notes_app.view_notes(filter_date)
                except ValueError:
                    print("Ошибка: Некорректный формат даты.")
            elif choice == '3':
                try:
                    note_id = int(input("Введите ID заметки для просмотра: "))
                    notes_app.view_note_by_id(note_id)
                except ValueError:
                    print("Ошибка: ID заметки должен быть числовым значением.")
            elif choice == '4':
                title = input("Введите заголовок заметки: ")
                body = input("Введите тело заметки: ")
                notes_app.add_note(title, body)
            elif choice == '5':
                try:
                    note_id = int(input("Введите ID заметки для редактирования: "))
                    title = input("Введите новый заголовок заметки: ")
                    body = input("Введите новое тело заметки: ")
                    notes_app.edit_note(note_id, title, body)
                except ValueError:
                    print("Ошибка: ID заметки должен быть числовым значением.")
            elif choice == '6':
                try:
                    note_id = int(input("Введите ID заметки для удаления: "))
                    notes_app.delete_note(note_id)
                except ValueError:
                    print("Ошибка: ID заметки должен быть числовым значением.")
            elif choice == '7':
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите существующее действие.")
    except Exception as e:
        print(f'Произошла ошибка: {e}')


if __name__ == "__main__":
    main()
