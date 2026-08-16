import json
import base64
from datetime import datetime, timezone

def process_config(config_file, output_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Ошибка чтения файла {config_file}: {e}")
        return

    # Парсим дату окончания (UTC)
    expire_str = data.get('expire_date', '2000-01-01 00:00:00')
    expire_dt = datetime.strptime(expire_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    now_dt = datetime.now(timezone.utc)

    lines = []

    # Шапка подписки (Название и контакты)
    title_node = f"vless://00000000-0000-0000-0000-000000000000@127.0.0.1:1080?type=tcp#📌 {data.get('profile_title', 'VPN Sub')}"
    tg_node = f"vless://00000000-0000-0000-0000-000000000000@127.0.0.1:1080?type=tcp#💬 Поддержка: {data.get('telegram_support', '')}"

    lines.append(title_node)
    lines.append(tg_node)

    # Проверка времени с точностью до минут
    if now_dt < expire_dt:
        # Время ЕЩЁ НЕ вышло -> добавляем рабочие VLESS ключи
        time_left_node = f"vless://00000000-0000-0000-0000-000000000000@127.0.0.1:1080?type=tcp#⏳ Активно до: {expire_str} UTC"
        lines.append(time_left_node)
        lines.extend(data.get('active_keys', []))
    else:
        # Время ВЫШЛО -> заменяем на сообщение об ошибке
        expired_info = f"vless://00000000-0000-0000-0000-000000000000@127.0.0.1:1080?type=tcp#⛔ Подписка закончилась {expire_str}"
        lines.append(expired_info)
        lines.extend(data.get('expired_keys', []))

    # Собираем и кодируем в Base64
    raw_payload = "\n".join(lines)
    b64_payload = base64.b64encode(raw_payload.encode('utf-8')).decode('utf-8')

    # Записываем итоговый файл подписки
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(b64_payload)

    print(f"Файл {output_file} успешно обновлен!")

if __name__ == '__main__':
    # Генерация основной подписки
    process_config('sub_8400749643_premium.json', 'sub_8400749643')
