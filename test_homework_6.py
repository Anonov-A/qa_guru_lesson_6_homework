from datetime import date


# Часть A. Функции

# 1. Нормализация email адресов

def normalize_addresses(value: str) -> str:
    """
    Возвращает значение, в котором адрес приведен к нижнему регистру и очищен от пробелов по краям.
    """
    return value.strip().lower()

# 2. Сокращенная версия тела письма

def add_short_body(email: dict) -> dict:
    """
    Возвращает email с новым ключом email["short_body"] —
    первые 10 символов тела письма + "...".
    """
    body = email.get("body", "")
    short_body = body[:10] + "..." if len(body) > 10 else body
    email["short_body"] = short_body
    return email

# 3. Очистка текста письма

def clean_body_text(body: str) -> str:
    """
    Заменяет табы и переводы строк на пробелы.
    """
    return body.replace('\t', ' ').replace('\n', ' ')

# 4. Формирование итогового текста письма

def build_sent_text(email: dict) -> str:
    """
    Формирует текст письма в формате:

    Кому: {to}, от {from}
    Тема: {subject}, дата {date}
    {clean_body}
    """
    return f"Кому: {email.get('recipient', '')}, от {email.get('sender', '')}\nТема: {email.get('subject', '')}, дата {email.get('date', '')}\n{email.get('body', '')}"

# 5. Проверка пустоты темы и тела

def check_empty_fields(subject: str, body: str) -> tuple[bool, bool]:
    """
    Возвращает кортеж (is_subject_empty, is_body_empty).
    True, если поле пустое.
    """
    is_subject_empty = subject.strip() == ""
    is_body_empty = body.strip() == ""
    return (is_subject_empty, is_body_empty)

# 6. Маска email отправителя

def mask_sender_email(login: str, domain: str) -> str:
    """
    Возвращает маску email: первые 2 символа логина + "***@" + домен.
    """
    return login[:2] + "***@" + domain

# 7. Создать функцию которая проверит корректности email адресов. Адрес считается корректным, если:
# содержит символ @;
# оканчивается на один из доменов: .com, .ru, .net.

def get_correct_email(email_list: list[str]) -> list[str]:
    """
    Возвращает список корректных email.
    """
    valid_domains = ['.com', '.ru', '.net']
    return [
        email for email in email_list
        if '@' in email and any(email.endswith(domain) for domain in valid_domains)
    ]

# 8. Создание словаря письма

def create_email(sender: str, recipient: str, subject: str, body: str) -> dict:
    """
    Создает словарь email с базовыми полями:
    'sender', 'recipient', 'subject', 'body'
    """
    return {
        'sender': sender,
        'recipient': recipient,
        'subject': subject,
        'body': body
    }

# 9. Добавление даты отправки

def add_send_date(email: dict) -> dict:
    """
    Возвращает email с добавленным ключом email["date"] — текущая дата в формате YYYY-MM-DD.
    """
    email["date"] = date.today().isoformat()
    return email

# 10. Получение логина и домена

def extract_login_domain(address: str) -> tuple[str, str]:
    """
    Возвращает логин и домен отправителя.
    Пример: "user@mail.ru" -> ("user", "mail.ru")
    """
    if '@' in address:
        login, domain = address.split('@', 1)
        return login, domain
    return address, ""


# Часть B. Отправка письма

def sender_email(recipient_list: list[str], subject: str, message: str, *, sender="default@study.com") -> list[dict]:
    # 1. Проверить, что recipient_list не пустой
    if not recipient_list:
        return []

    # 2. Проверить корректность email отправителя и получателей
    valid_emails = get_correct_email([sender] + recipient_list)
    if sender not in valid_emails or not any(email in valid_emails for email in recipient_list):
        return []

    # 3. Проверить пустоту темы и тела письма
    is_subject_empty, is_body_empty = check_empty_fields(subject, message)
    if is_subject_empty or is_body_empty:
        return []

    # 4. Исключить отправку самому себе
    valid_recipients = [email for email in recipient_list if email != sender and email in valid_emails]

    # 5. Нормализация
    clean_subject = clean_body_text(subject)
    clean_body = clean_body_text(message)
    normalized_sender = normalize_addresses(sender)
    normalized_recipients = [normalize_addresses(recipient) for recipient in valid_recipients]

    sent_emails = []
    for recipient in normalized_recipients:
        # 6. Создать письмо для каждого получателя
        email_dict = create_email(normalized_sender, recipient, clean_subject, clean_body)

        # 7. Добавить дату отправки
        email_dict = add_send_date(email_dict)

        # 8. Замаскировать email отправителя
        login, domain = extract_login_domain(normalized_sender)
        email_dict['masked_sender'] = mask_sender_email(login, domain)

        # 9. Сохранить короткую версию
        email_dict = add_short_body(email_dict)

        # 10. Сформировать итоговый текст письма
        email_dict['sent_text'] = build_sent_text(email_dict)

        sent_emails.append(email_dict)

    # 11. Вернуть итоговый список писем
    return sent_emails


# Тестирование функции
test_emails = [
    "user@gmail.com",
    "admin@company.ru",
    "test_123@service.net",
    "Example.User@domain.com",
    " hello@corp.ru  ",
]

emails = sender_email(test_emails, "Крайне письмо",
                      "Уважаемый коллега, приглашаем вас на совещание которое состоится завтра в 10:00.")

# Вывод результата
for e in emails:
    print(e["sent_text"])
    print("---")