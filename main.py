import csv
import re
import pandas as pd

# Функция для нормализации ФИО
def normalize_name(row):
    full_name = " ".join(row[:3]).split()
    row[:3] = full_name + [""] * (3 - len(full_name))
    return row

# Функция для нормализации телефона
def normalize_phone(phone):
    pattern = re.compile(
        r"(\+7|8)?\s*\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})(?:\s*(доб.)\s*(\d+))?"
    )
    replacement = r"+7(\2)\3-\4-\5 \6\7".strip()
    return pattern.sub(replacement, phone)

# Основная функция обработки
def process_contacts(input_path, output_path):
    with open(input_path, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter="\t")
        contacts_list = list(rows)

    # Заголовки таблицы
    headers = contacts_list[0]
    contacts_list = contacts_list[1:]

    # Нормализация данных
    normalized_contacts = []
    for contact in contacts_list:
        contact = normalize_name(contact)
        contact[5] = normalize_phone(contact[5])
        normalized_contacts.append(contact)

    # Слияние дубликатов
    merged_contacts = {}
    for contact in normalized_contacts:
        key = (contact[0], contact[1])  # lastname + firstname
        if key not in merged_contacts:
            merged_contacts[key] = contact
        else:
            for i in range(len(contact)):
                if not merged_contacts[key][i]:
                    merged_contacts[key][i] = contact[i]

    # Преобразование результата в список
    final_contacts = [headers] + list(merged_contacts.values())

    # Сохранение результата
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerows(final_contacts)

    # Вывод в консоль в виде датафрейма
    df = pd.DataFrame(final_contacts[1:], columns=final_contacts[0])
    print(df)

# Пути к файлам
input_path = "phonebook_raw.csv"  # Замените на путь к вашему исходному файлу
output_path = "phonebook.csv"

# Запуск обработки
process_contacts(input_path, output_path)

