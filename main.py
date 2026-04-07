import requests
import base64
import json

# Список URL-адресов на raw-файлы в GitHub
SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vmess.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/trojan.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/ss.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/ssr.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/vmess.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/ss.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/ssr.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/trojan.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/filtered/subs/hysteria2.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/filtered/subs/vmess.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/filtered/subs/vless.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/filtered/subs/trojan.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/filtered/subs/ss.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/refs/heads/main/Protocols/ss.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/refs/heads/main/Protocols/trojan.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/refs/heads/main/Protocols/vless.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/refs/heads/main/Protocols/vmess.txt",
    "https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/refs/heads/main/config/all_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/vmess_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/trojan_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/ssr_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/refs/heads/main/ss_configs.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/app/sub.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_1.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_2.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_3.txt",
    "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_4.txt",
    "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/main/splitted/mixed",
    "https://raw.githubusercontent.com/onlymeoneme/v2ray_subs/refs/heads/main/list.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/refs/heads/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/refs/heads/main/nodes/ndnode.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/refs/heads/main/nodes/nodefree.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/refs/heads/main/nodes/v2rayshare.txt",
    "https://raw.githubusercontent.com/Barabama/FreeNodes/refs/heads/main/nodes/nodev2ray.txt",
    "https://raw.githubusercontent.com/Leon406/SubCrawler/refs/heads/main/sub/share/vless",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/refs/heads/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/peasoft/NoMoreWalls/refs/heads/master/list.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/V2RAY_RAW.txt",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/main/lite/subscriptions/xray/normal/mix",
    "https://raw.githubusercontent.com/arshiacomplus/v2rayExtractor/refs/heads/main/mix/sub.html",
    "https://raw.githubusercontent.com/Rayan-Config/C-Sub/refs/heads/main/configs/proxy.txt",
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity.txt",
    "https://raw.githubusercontent.com/Everyday-VPN/Everyday-VPN/main/subscription/main.txt",
    "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/xray/normal/reality",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/xray/normal/ss",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/xray/normal/trojan",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/xray/normal/tuic",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/xray/normal/vless",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/xray/normal/vmess",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/refs/heads/main/subscriptions/xray/normal/xhttp",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_SS%2BAll_RUS.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS.txt",
    "https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/refs/heads/main/githubmirror/new/all_new.txt",
    "https://raw.githubusercontent.com/F0rc3Run/F0rc3Run/refs/heads/main/splitted-by-protocol/vmess.txt",
    "https://raw.githubusercontent.com/F0rc3Run/F0rc3Run/refs/heads/main/splitted-by-protocol/vless.txt",
    "https://raw.githubusercontent.com/F0rc3Run/F0rc3Run/refs/heads/main/splitted-by-protocol/trojan.txt",
    "https://raw.githubusercontent.com/F0rc3Run/F0rc3Run/refs/heads/main/splitted-by-protocol/shadowsocks.txt"
]

# Поддерживаемые протоколы
PROTOCOLS = ["vmess://", "vless://", "trojan://", "ss://", "ssr://",
             "hy2://", "hysteria2://", "tuic://", "warp://"]

# Метка для всех конфигов
LABEL = "V Team"


def strip_label(config: str) -> str:
    """
    Удаляет оригинальный лейбл и заменяет на LABEL.
    Корректно обрабатывает vmess (через JSON) и обычные протоколы (отрезая хвост после #).
    """
    if config.startswith("vmess://"):
        try:
            # Извлекаем base64 строку (всё после vmess://)
            base64_data = config[8:]
            # Восстанавливаем паддинг, если он был утерян
            padded = base64_data + '=' * (-len(base64_data) % 4)
            # Декодируем и парсим JSON
            json_data = base64.b64decode(padded).decode('utf-8', errors='ignore')
            config_dict = json.loads(json_data)
            
            # Меняем название сервера (ключ 'ps')
            config_dict['ps'] = LABEL
            
            # Собираем обратно без лишних пробелов для экономии места
            new_json = json.dumps(config_dict, separators=(',', ':'))
            new_base64 = base64.b64encode(new_json.encode('utf-8')).decode('utf-8')
            return f"vmess://{new_base64}"
        except Exception:
            # Если vmess повреждён или нестандартный, оставляем как есть
            return config
    else:
        # Для остальных протоколов отрезаем всё после ПОСЛЕДНЕГО '#'
        base_config = config.rsplit('#', 1)[0]
        return f"{base_config}#{LABEL}"


def parse_content(content):
    """
    Построчно обрабатывает контент: и plain-text, и base64.
    """
    result = []

    for line in content.splitlines():
        line = line.strip()

        if not line or line.startswith('#'):
            continue

        # Строка уже является готовым конфигом
        if any(line.startswith(p) for p in PROTOCOLS):
            result.append(strip_label(line))
            continue

        # Пробуем декодировать строку как base64
        try:
            padded = line + '=' * (-len(line) % 4)
            decoded = base64.b64decode(padded).decode('utf-8', errors='ignore')

            # Проверяем, появились ли протоколы после декодирования
            if any(p in decoded for p in PROTOCOLS):
                for decoded_line in decoded.splitlines():
                    decoded_line = decoded_line.strip()
                    if decoded_line and any(decoded_line.startswith(p) for p in PROTOCOLS):
                        result.append(strip_label(decoded_line))
        except Exception:
            # Не base64 и не конфиг — просто пропускаем
            pass

    return result


def get_v2ray_sources():
    final_config_list = []
    success_count = 0
    fail_count = 0

    for i, url in enumerate(SOURCES, 1):
        short = url.split('/')[-1] or url.split('/')[-2]
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            content = response.text.strip()

            if not content:
                print(f"[{i}/{len(SOURCES)}] ⚠ Пусто: {short}")
                continue

            lines = parse_content(content)
            final_config_list.extend(lines)
            success_count += 1
            print(f"[{i}/{len(SOURCES)}] ✓ {short}: {len(lines)} конфигов")

        except Exception as e:
            fail_count += 1
            print(f"[{i}/{len(SOURCES)}] ✗ {short}: {e}")

    # Дедупликация (удаление повторяющихся серверов с сохранением порядка)
    seen = set()
    unique_configs = []
    for c in final_config_list:
        if c not in seen:
            seen.add(c)
            unique_configs.append(c)

    # Вывод статистики в консоль
    print(f"\n{'='*50}")
    print(f"Источников успешно: {success_count} / {len(SOURCES)}")
    print(f"Источников с ошибкой: {fail_count}")
    print(f"Всего конфигов (до дедупликации): {len(final_config_list)}")
    print(f"Уникальных конфигов (после):    {len(unique_configs)}")

    print(f"\nСтатистика по протоколам:")
    for p in PROTOCOLS:
        count = sum(1 for c in unique_configs if c.startswith(p))
        if count > 0:
            print(f"  {p:<15} {count}")
    print(f"{'='*50}\n")

    return '\n'.join(unique_configs)


def main():
    print("Начинаем сбор конфигов...\n")
    content = get_v2ray_sources()

    if not content.strip():
        print("Ошибка: не удалось собрать ни одного конфига!")
        return

    # Кодируем финальный объединённый список обратно в Base64 (формат подписки)
    output_bytes = base64.b64encode(content.encode('utf-8'))
    output_str = output_bytes.decode('utf-8')

    # Сохраняем в файл
    output_file = 'sub.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_str)

    print(f"Готово! Закодированный список сохранён в {output_file}")


if __name__ == "__main__":
    main()
