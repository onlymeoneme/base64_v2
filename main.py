import requests
import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ─────────────────────────────────────────────
# НАСТРОЙКИ
# ─────────────────────────────────────────────

MIN_FILE_SIZE    = 200 * 1024   # 200 KB
MAX_FILE_SIZE    = 625 * 1024   # 625 KB
TARGET_FILE_SIZE = 400 * 1024   # ~400 KB — цель

ENCRYPT    = True         # True = шифровать, False = только base64
OUTPUT_DIR = "output"
KEY_FILE   = "secret.key" # 32 байта, AES-256

# ─────────────────────────────────────────────
# ИСТОЧНИКИ
# ─────────────────────────────────────────────

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
    "https://raw.githubusercontent.com/F0rc3Run/F0rc3Run/refs/heads/main/splitted-by-protocol/shadowsocks.txt",
]

PROTOCOLS = ["vmess://", "vless://", "trojan://", "ss://", "ssr://",
             "hy2://", "hysteria2://", "tuic://", "warp://"]


# ─────────────────────────────────────────────
# ПАРСИНГ
# ─────────────────────────────────────────────

def parse_content(content):
    result = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if any(line.startswith(p) for p in PROTOCOLS):
            result.append(line)
            continue
        try:
            padded = line + '=' * (-len(line) % 4)
            decoded = base64.b64decode(padded).decode('utf-8', errors='ignore')
            if any(p in decoded for p in PROTOCOLS):
                for dl in decoded.splitlines():
                    dl = dl.strip()
                    if dl and any(dl.startswith(p) for p in PROTOCOLS):
                        result.append(dl)
        except Exception:
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

    unique_configs = list(dict.fromkeys(final_config_list))

    print(f"\n{'='*50}")
    print(f"Источников успешно: {success_count} / {len(SOURCES)}")
    print(f"Источников с ошибкой: {fail_count}")
    print(f"Всего конфигов (с дублями): {len(final_config_list)}")
    print(f"Уникальных конфигов: {len(unique_configs)}")
    print(f"\nСтатистика по протоколам:")
    for p in PROTOCOLS:
        count = sum(1 for c in unique_configs if c.startswith(p))
        if count > 0:
            print(f"  {p:<15} {count}")
    print(f"{'='*50}\n")

    return unique_configs


# ─────────────────────────────────────────────
# РАЗБИВКА НА ЧАНКИ
# ─────────────────────────────────────────────

def split_into_chunks(configs):
    raw_target = int(TARGET_FILE_SIZE * 3 / 4)
    chunks = []
    current_chunk = []
    current_size = 0

    for config in configs:
        line_size = len(config.encode('utf-8')) + 1
        if current_size + line_size > raw_target and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_size = 0
        current_chunk.append(config)
        current_size += line_size

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


# ─────────────────────────────────────────────
# AES-256-GCM (совместимо с Android javax.crypto)
# ─────────────────────────────────────────────

def load_or_create_key() -> bytes:
    """
    Загружает ключ из KEY_FILE или создаёт новый 32-байтовый ключ.
    Ключ сохраняется в бинарном виде — 32 сырых байта.
    """
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as f:
            key = f.read()
        print(f"🔑 Ключ загружен из {KEY_FILE}")
    else:
        key = AESGCM.generate_key(bit_length=256)  # 32 байта
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
        # Дополнительно сохраняем base64-версию — удобно для вставки в Android
        key_b64 = base64.b64encode(key).decode('utf-8')
        with open(KEY_FILE + ".b64", 'w') as f:
            f.write(key_b64)
        print(f"🔑 Новый ключ создан и сохранён в {KEY_FILE}")
        print(f"   Base64 для Android: {key_b64}")
    return key


def encrypt_aes_gcm(data: bytes, key: bytes) -> bytes:
    """
    Шифрует данные AES-256-GCM.
    Формат результата: [12 байт nonce][зашифрованные данные + 16 байт GCM-тег]
    Android читает именно этот формат через javax.crypto.
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)          # случайный nonce на каждый файл
    ciphertext = aesgcm.encrypt(nonce, data, None)
    return nonce + ciphertext       # nonce прибит спереди


def decrypt_aes_gcm(data: bytes, key: bytes) -> bytes:
    """Расшифровывает данные зашифрованные encrypt_aes_gcm."""
    aesgcm = AESGCM(key)
    nonce      = data[:12]
    ciphertext = data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None)


# ─────────────────────────────────────────────
# СОХРАНЕНИЕ ФАЙЛОВ
# ─────────────────────────────────────────────

def save_chunks(chunks, key: bytes = None):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pad = len(str(len(chunks)))
    saved_files = []

    for idx, chunk in enumerate(chunks, 1):
        raw_text  = '\n'.join(chunk)
        raw_bytes = raw_text.encode('utf-8')

        # Шаг 1: base64
        b64_bytes = base64.b64encode(raw_bytes)

        # Шаг 2: AES-256-GCM шифрование (если включено)
        if key is not None:
            final_bytes = encrypt_aes_gcm(b64_bytes, key)
            ext = ".enc"
        else:
            final_bytes = b64_bytes
            ext = ".txt"

        filename = f"sub_{str(idx).zfill(pad)}{ext}"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, 'wb') as f:
            f.write(final_bytes)

        size_kb = len(final_bytes) / 1024
        in_range = "✓" if MIN_FILE_SIZE <= len(final_bytes) <= MAX_FILE_SIZE else "⚠"
        print(f"  {in_range} {filename}: {size_kb:.1f} KB ({len(chunk)} конфигов)")
        saved_files.append(filepath)

    return saved_files


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    print("Начинаем сбор конфигов...\n")
    configs = get_v2ray_sources()

    if not configs:
        print("Ошибка: не удалось собрать ни одного конфига!")
        return

    chunks = split_into_chunks(configs)
    print(f"Разбивка: {len(configs)} конфигов → {len(chunks)} файлов")
    print(f"Диапазон: {MIN_FILE_SIZE//1024}–{MAX_FILE_SIZE//1024} KB, цель ~{TARGET_FILE_SIZE//1024} KB\n")

    key = None
    if ENCRYPT:
        key = load_or_create_key()
        print("🔒 Шифрование: AES-256-GCM (совместимо с Android)\n")
        print("   ⚠  Не теряй secret.key — без него расшифровать невозможно!\n")

    print(f"Сохраняем в папку '{OUTPUT_DIR}/':")
    saved = save_chunks(chunks, key=key)

    print(f"\n{'='*50}")
    print(f"Готово! Сохранено файлов: {len(saved)}")
    if ENCRYPT:
        print(f"Бинарный ключ: {KEY_FILE}")
        print(f"Base64 ключ для Android: {KEY_FILE}.b64")
    print(f"{'='*50}")


# ─────────────────────────────────────────────
# УТИЛИТА: расшифровать файл вручную
# ─────────────────────────────────────────────

def decrypt_file(filepath: str, key_path: str = KEY_FILE):
    """
    Расшифровывает .enc файл и печатает конфиги.
    Использование: decrypt_file("output/sub_01.enc")
    """
    with open(key_path, 'rb') as f:
        key = f.read()

    with open(filepath, 'rb') as f:
        enc_data = f.read()

    b64_data = decrypt_aes_gcm(enc_data, key)
    raw_text = base64.b64decode(b64_data).decode('utf-8')
    print(raw_text)


if __name__ == "__main__":
    main()
