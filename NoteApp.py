import json
import os
from datetime import datetime

from Note import Note


class NotesApp:
    def __init__(self, file_path='notes.json'):
        self.file_path = file_path
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    notes_data = json.load(file)
                return [Note(**note_data) for note_data in notes_data]
            else:
                return []
        except json.JSONDecodeError:
            print(f'Ошибка при загрузке файла {self.file_path}. Файл поврежден или имеет неверный формат.')
            return []

    def save_notes(self):
        notes_data = [{'note_id': note.note_id, 'title': note.title, 'body': note.body, 'timestamp': note.timestamp} for
                      note in self.notes]
        try:
            with open(self.file_path, 'w') as file:
                json.dump(notes_data, file, indent=4)
        except IOError:
            print(f'Ошибка при сохранении файла {self.file_path}. Проверьте правильность доступа к файлу.')

    def add_note(self, title, body):
        note_id = len(self.notes) + 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_note = Note(note_id, title, body, timestamp)
        self.notes.append(new_note)
        self.save_notes()
        print(
            f'Заметка добавлена:\nID: {note_id}\nЗаголовок: {title}\nТело заметки: {body}\nВремя создания: {timestamp}')

    def view_notes(self):
        if self.notes:
            for note in self.notes:
                print(
                    f'ID: {note.note_id}\nЗаголовок: {note.title}\nТело заметки: {note.body}\nВремя создания: {note.timestamp}\n')
        else:
            print('Заметок нет.')

    def edit_note(self, note_id, title, body):
        for note in self.notes:
            if note.note_id == note_id:
                note.title = title
                note.body = body
                note.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_notes()
                print(
                    f'Заметка отредактирована:\nID: {note_id}\nНовый заголовок: {title}\nНовое тело заметки: {body}\nВремя редактирования: {note.timestamp}')
                return
        print(f'Заметка с ID {note_id} не найдена.')

    def delete_note(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                self.notes.remove(note)
                self.save_notes()
                print(f'Заметка удалена:\nID: {note_id}')
                return
        print(f'Заметка с ID {note_id} не найдена.')


def main():
    try:
        notes_app = NotesApp()

        while True:
            print("\nВыберите действие:")
            print("1. Просмотреть заметки")
            print("2. Добавить заметку")
            print("3. Редактировать заметку")
            print("4. Удалить заметку")
            print("5. Выйти")

            choice = input("Введите номер действия: ")

            if choice == '1':
                notes_app.view_notes()
            elif choice == '2':
                title = input("Введите заголовок заметки: ")
                body = input("Введите тело заметки: ")
                notes_app.add_note(title, body)
            elif choice == '3':
                try:
                    note_id = int(input("Введите ID заметки для редактирования: "))
                    title = input("Введите новый заголовок заметки: ")
                    body = input("Введите новое тело заметки: ")
                    notes_app.edit_note(note_id, title, body)
                except ValueError:
                    print("Ошибка: ID заметки должен быть числовым значением.")
            elif choice == '4':
                try:
                    note_id = int(input("Введите ID заметки для удаления: "))
                    notes_app.delete_note(note_id)
                except ValueError:
                    print("Ошибка: ID заметки должен быть числовым значением.")
            elif choice == '5':
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите существующее действие.")
    except Exception as e:
        print(f'Произошла ошибка: {e}')


if __name__ == "__main__":
    main()