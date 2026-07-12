import json
import asyncio
import aiohttp
import random
import re
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# ============================================
# ╔══════════════════════════════════════════╗
# ║   PREMIUM CC BOT v10.0                 ║
# ║  Owner: @S_1xD | Channel: @xb1ns      ║
# ╚══════════════════════════════════════════╝
# ============================================

BOT_TOKEN = "7724826927:AAHlaW_pdyJX8Ca5uD-YasDSJBitSM6q2QI"
CHANNEL = "@xb1ns"
OWNER_ID = "8418640972"
ADMIN_IDS = ["8418640972", "7502457749"]
BOT_USERNAME = "@S_1xD"
DUMP_IMAGE = "https://i.ibb.co/ns4gxZkc/x.jpg"
RAZORPAY_API = "https://api-production-ee72.up.railway.app/razorpay"
RAZORPAY_SITE = "https://pages.razorpay.com/IAEME"
RAZORPAY_PROXY = "jp-tok.pvdata.host:8080:g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2"

# Premium Custom Emoji Mapping for Telegram Premium
EMOJI = {
    # ── Original pack ──
    "charged":    '<tg-emoji emoji-id="5123163417326126159">✅</tg-emoji>',
    "live":       '<tg-emoji emoji-id="5219672809936006424">🔥</tg-emoji>',
    "declined":   '<tg-emoji emoji-id="5121063440311386962">❌</tg-emoji>',
    "3ds":        '<tg-emoji emoji-id="6285068812400202707">🔐</tg-emoji>',
    "expired":    '<tg-emoji emoji-id="6266866272848321043">⏰</tg-emoji>',
    "error":      '<tg-emoji emoji-id="5447644880824181073">⚠️</tg-emoji>',
    "hitting":    '<tg-emoji emoji-id="5454415424319931791">⌛️</tg-emoji>',
    "stopped":    '<tg-emoji emoji-id="6325507973896472524">🛑</tg-emoji>',
    "welcome":    '<tg-emoji emoji-id="5258079378159453410">👋</tg-emoji>',
    "back":       '<tg-emoji emoji-id="5253997076169115797">🔙</tg-emoji>',
    "regenerate": '<tg-emoji emoji-id="6066348702363031988">🔄</tg-emoji>',
    "bolt":       '<tg-emoji emoji-id="5219943216781995020">⚡️</tg-emoji>',
    "crown":      '<tg-emoji emoji-id="6266995104687330978">👑</tg-emoji>',
    "ban":        '<tg-emoji emoji-id="5116151848855667552">🤕</tg-emoji>',
    # ── Extended pack ──
    "plan":       '<tg-emoji emoji-id="5197269100878907942">✍️</tg-emoji>',
    "ticket":     '<tg-emoji emoji-id="5418010521309815154">🎫</tg-emoji>',
    "stats":      '<tg-emoji emoji-id="5231200819986047254">📊</tg-emoji>',
    "users":      '<tg-emoji emoji-id="5134155514241876731">👥</tg-emoji>',
    "search":     '<tg-emoji emoji-id="5258274739041883702">🔍</tg-emoji>',
    "broadcast":  '<tg-emoji emoji-id="5474263443152316384">📣</tg-emoji>',
    "plug":       '<tg-emoji emoji-id="4904742417401381633">🦏</tg-emoji>',
    "link":       '<tg-emoji emoji-id="6267115986541877538">🔗</tg-emoji>',
    "trash":      '<tg-emoji emoji-id="5445267414562389170">🗑</tg-emoji>',
    "question":   '<tg-emoji emoji-id="5436113877181941026">❓</tg-emoji>',
    "blocked":    '<tg-emoji emoji-id="5116151848855667552">🚫</tg-emoji>',
    "free":       '<tg-emoji emoji-id="5406756500108501710">🆓</tg-emoji>',
    "card":       '<tg-emoji emoji-id="6267128480601741166">💳</tg-emoji>',
    "risky":      '<tg-emoji emoji-id="5895443668663275064">🟡</tg-emoji>',
    "danger":     '<tg-emoji emoji-id="5852753450382659113">🔴</tg-emoji>',
    "infinity":   '<tg-emoji emoji-id="5116512467194741904">♾</tg-emoji>',
    "lock":       '<tg-emoji emoji-id="6282846669335702032">🔒</tg-emoji>',
    # ── Numbers ──
    "num_5": '<tg-emoji emoji-id="5283282345036646926">♥️</tg-emoji>',
    "num_2": '<tg-emoji emoji-id="4904936030232117798">🍀</tg-emoji>',
    "num_3": '<tg-emoji emoji-id="5134377151734219769">🍑</tg-emoji>',
    "num_4": '<tg-emoji emoji-id="5305726937887433606">🍆</tg-emoji>',
    "num_1": '<tg-emoji emoji-id="5404500925018564494">👨🏻‍💻</tg-emoji>',
    "num_6": '<tg-emoji emoji-id="5139005588881015916">6️⃣</tg-emoji>',
    "num_7": '<tg-emoji emoji-id="5309887343858060393">👾</tg-emoji>',
    "join": '<tg-emoji emoji-id="4916086774649848789">8️⃣</tg-emoji>',
    "scr": '<tg-emoji emoji-id="5134457377428341766">9️⃣</tg-emoji>',
    "arrow_down": '<tg-emoji emoji-id="6084743519010820583">👇</tg-emoji>',
    "FIRE": '<tg-emoji emoji-id="5219672809936006424">🔥</tg-emoji>',
    "CHECK": '<tg-emoji emoji-id="5123163417326126159">✅</tg-emoji>',
    "CROSS": '<tg-emoji emoji-id="5121063440311386962">❌</tg-emoji>',
    "LOAD": '<tg-emoji emoji-id="5454415424319931791">⌛️</tg-emoji>',
    "CARD": '<tg-emoji emoji-id="6267128480601741166">💳</tg-emoji>',
    "ROCKET": '<tg-emoji emoji-id="5219943216781995020">⚡️</tg-emoji>',
    "CHART": '<tg-emoji emoji-id="5231200819986047254">📊</tg-emoji>',
    "SEARCH": '<tg-emoji emoji-id="5258274739041883702">🔍</tg-emoji>',
    "LOCK": '<tg-emoji emoji-id="6282846669335702032">🔒</tg-emoji>',
    "BANK": '<tg-emoji emoji-id="6267128480601741166">🏦</tg-emoji>',
    "WARN": '<tg-emoji emoji-id="5447644880824181073">⚠️</tg-emoji>',
    "STOP": '<tg-emoji emoji-id="6325507973896472524">🛑</tg-emoji>',
    "STAR": '<tg-emoji emoji-id="5123163417326126159">⭐️</tg-emoji>',
    "USER": '<tg-emoji emoji-id="5134155514241876731">👤</tg-emoji>',
    "FILE": '<tg-emoji emoji-id="5445267414562389170">📁</tg-emoji>',
    "GLOBE": '<tg-emoji emoji-id="5258274739041883702">🌍</tg-emoji>',
    "CROWN": '<tg-emoji emoji-id="6266995104687330978">👑</tg-emoji>',
    "SPARK": '<tg-emoji emoji-id="5123163417326126159">✨</tg-emoji>',
    "CLOCK": '<tg-emoji emoji-id="6266866272848321043">⏰</tg-emoji>',
    "BULK": '<tg-emoji emoji-id="5134155514241876731">📦</tg-emoji>',
    "KEY": '<tg-emoji emoji-id="6282846669335702032">🔑</tg-emoji>',
    "ID": '<tg-emoji emoji-id="5134155514241876731">🆔</tg-emoji>',
    "CHANNEL_EMO": '<tg-emoji emoji-id="5474263443152316384">📢</tg-emoji>',
    "PREMIUM": '<tg-emoji emoji-id="5123163417326126159">💎</tg-emoji>',
    "HIT": '<tg-emoji emoji-id="5219672809936006424">🎯</tg-emoji>',
    "REFRESH": '<tg-emoji emoji-id="6066348702363031988">🔄</tg-emoji>',
    "BACK": '<tg-emoji emoji-id="5253997076169115797">🔙</tg-emoji>',
    "MENU": '<tg-emoji emoji-id="5134155514241876731">📋</tg-emoji>',
    "NOTE": '<tg-emoji emoji-id="5123163417326126159">📝</tg-emoji>',
    "TAG": '<tg-emoji emoji-id="5134155514241876731">🏷️</tg-emoji>',
    "PRICE": '<tg-emoji emoji-id="6267128480601741166">💰</tg-emoji>',
    "COUNTRY": '<tg-emoji emoji-id="5258274739041883702">🌐</tg-emoji>',
    "SEND": '<tg-emoji emoji-id="5474263443152316384">📤</tg-emoji>',
    "DIAMOND": '<tg-emoji emoji-id="5123163417326126159">💎</tg-emoji>',
    "HOURGLASS": '<tg-emoji emoji-id="6266866272848321043">⏳</tg-emoji>',
    "TARGET": '<tg-emoji emoji-id="5219672809936006424">🎯</tg-emoji>',
    "BROADCAST": '<tg-emoji emoji-id="5474263443152316384">📣</tg-emoji>',
    "INFO": '<tg-emoji emoji-id="5134155514241876731">ℹ️</tg-emoji>',
    "GEAR": '<tg-emoji emoji-id="5134155514241876731">⚙️</tg-emoji>',
    "ZAP": '<tg-emoji emoji-id="5219943216781995020">⚡</tg-emoji>',
    "DUMP": '<tg-emoji emoji-id="5219672809936006424">💀</tg-emoji>',
    "TOOL": '<tg-emoji emoji-id="5134155514241876731">🔧</tg-emoji>',
    "SKULL": '<tg-emoji emoji-id="5219672809936006424">💀</tg-emoji>',
    "BOMB": '<tg-emoji emoji-id="5219943216781995020">💣</tg-emoji>',
    "FLAME": '<tg-emoji emoji-id="5219672809936006424">🔥</tg-emoji>',
    "GHOST": '<tg-emoji emoji-id="6037570896766438989">👻</tg-emoji>',
    "SCRAPE": '<tg-emoji emoji-id="5134457377428341766">🕷️</tg-emoji>',
    "MAGNET": '<tg-emoji emoji-id="5134457377428341766">🧲</tg-emoji>'
}

def em(key: str) -> str:
    """Get premium emoji by key"""
    return EMOJI.get(key, "❓")

def btn(text: str, callback: str, style: str = None, emoji_key: str = None) -> Dict:
    """Create inline keyboard button with premium emoji"""
    button = {"text": text, "callback_data": callback}
    if style:
        button["style"] = style
    if emoji_key and emoji_key in EMOJI:
        # Extract emoji-id from the HTML
        emoji_html = EMOJI[emoji_key]
        match = re.search(r'emoji-id="([^"]+)"', emoji_html)
        if match:
            button["icon_custom_emoji_id"] = match.group(1)
    return button

def btn_url(text: str, url: str, style: str = None, emoji_key: str = None) -> Dict:
    """Create inline keyboard URL button with premium emoji"""
    button = {"text": text, "url": url}
    if style:
        button["style"] = style
    if emoji_key and emoji_key in EMOJI:
        emoji_html = EMOJI[emoji_key]
        match = re.search(r'emoji-id="([^"]+)"', emoji_html)
        if match:
            button["icon_custom_emoji_id"] = match.group(1)
    return button

def is_admin(user_id) -> bool:
    return str(user_id) in ADMIN_IDS

def is_group(chat_id) -> bool:
    return str(chat_id).startswith("-")

# Card Configuration
CARD_CONFIG = {
    "Visa": {"prefixes": ["4"], "length": 16},
    "Mastercard": {"prefixes": ["51", "52", "53", "54", "55"], "length": 16},
    "American Express": {"prefixes": ["34", "37"], "length": 15},
    "Discover": {"prefixes": ["6011", "644", "645", "646", "647", "648", "649", "65"], "length": 16}
}

FIRST_NAMES = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan", "Jessica", "Sarah", "Karen", "Emma", "Olivia", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia", "Harper", "Evelyn", "Liam", "Noah", "Oliver", "Elijah", "Lucas", "Mason", "Logan", "Alexander", "Ethan", "Jacob"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez"]

VALID_IIN = {
    "VISA": [[400000, 499999]],
    "MASTERCARD": [[222100, 272099], [510000, 559999]],
    "AMEX": [[340000, 349999], [370000, 379999]],
    "DISCOVER": [[601100, 601199], [622126, 622925], [644000, 649999], [650000, 659999]]
}

FAKE_PATTERNS = [
    r'^0', r'^1', r'^2', r'^7', r'^8', r'^9',
    r'^(\d)\1{4,}', r'123456', r'012345', r'098765',
    r'000000', r'999999', r'111111', r'222222'
]

def luhn_check(num: str) -> bool:
    """Validate card number using Luhn algorithm"""
    digits = [int(d) for d in num]
    s = 0
    double = True
    for i in range(len(digits) - 1, -1, -1):
        x = digits[i]
        if double:
            x *= 2
            if x > 9:
                x -= 9
        s += x
        double = not double
    return s % 10 == 0

def luhn_generate(prefix: str, length: int) -> str:
    """Generate Luhn-valid card number"""
    body = prefix
    while len(body) < length - 1:
        body += str(random.randint(0, 9))
    
    digits = [int(d) for d in body]
    s = 0
    double = True
    for i in range(len(digits) - 1, -1, -1):
        x = digits[i]
        if double:
            x *= 2
            if x > 9:
                x -= 9
        s += x
        double = not double
    
    check = (10 - (s % 10)) % 10
    full = body + str(check)
    
    # Verify generated number
    if not luhn_check(full):
        return luhn_generate(prefix, length)
    return full

def is_fake_pattern(num: str) -> bool:
    """Check if card number matches fake patterns"""
    for pattern in FAKE_PATTERNS:
        if re.search(pattern, num):
            return True
    return False

def is_valid_iin(bin_num: str) -> bool:
    """Check if BIN is valid"""
    try:
        prefix = int(bin_num[:6])
    except ValueError:
        return False
    
    for ranges in VALID_IIN.values():
        for start, end in ranges:
            if start <= prefix <= end:
                return True
    return False

async def bin_lookup(bin_num: str) -> Dict:
    """Lookup BIN information from various sources"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://bins.antipublic.cc/bins/{bin_num}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get('brand') and data.get('bank') and data.get('bank') != "Unknown Bank":
                        return {
                            'brand': data.get('brand', 'UNKNOWN').upper(),
                            'country': data.get('country', 'US'),
                            'cname': data.get('country_name', 'United States'),
                            'flag': data.get('country_flag', '🇺🇸'),
                            'bank': data.get('bank', 'Unknown'),
                            'level': data.get('level', 'CLASSIC'),
                            'type': data.get('type', 'CREDIT'),
                            'valid': True
                        }
    except:
        pass
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://lookup.binlist.net/{bin_num}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get('bank') and data.get('bank').get('name'):
                        return {
                            'brand': data.get('scheme', data.get('brand', 'CARD')).upper(),
                            'country': data.get('country', {}).get('alpha2', 'US'),
                            'cname': data.get('country', {}).get('name', 'United States'),
                            'flag': data.get('country', {}).get('emoji', '🇺🇸'),
                            'bank': data.get('bank', {}).get('name', 'Unknown'),
                            'level': 'CLASSIC',
                            'type': data.get('type', 'CREDIT'),
                            'valid': True
                        }
    except:
        pass
    
    return {
        'brand': 'UNKNOWN',
        'country': 'US',
        'cname': 'United States',
        'flag': '🇺🇸',
        'bank': 'Unknown',
        'level': 'CLASSIC',
        'type': 'CREDIT',
        'valid': False
    }

async def razorpay_check(card_num: str, month: str, year: str, cvv: str) -> Dict:
    """Check card via Razorpay gateway"""
    try:
        cc = f"{card_num}|{month}|20{year}|{cvv}"
        url = f"{RAZORPAY_API}?cc={cc}&site={RAZORPAY_SITE}&proxy={RAZORPAY_PROXY}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if not resp.ok:
                    return {'valid': False, 'reason': 'Gateway error'}
                data = await resp.json()
                if data.get('status') in ['live', 'approved', 'success']:
                    return {'valid': True}
                return {'valid': False, 'reason': data.get('message', data.get('status', 'Payment declined'))}
    except:
        return {'valid': False, 'reason': 'Connection failed'}

def advanced_gen_card() -> Dict:
    """Generate a realistic card using advanced algorithms"""
    types = ["Visa", "Visa", "Visa", "Mastercard", "Mastercard", "Mastercard", "American Express", "Discover"]
    card_type = types[random.randint(0, len(types) - 1)]
    cfg = CARD_CONFIG[card_type]
    
    prefix = cfg['prefixes'][random.randint(0, len(cfg['prefixes']) - 1)]
    
    body = prefix
    remaining = cfg['length'] - len(prefix) - 1
    last_digit = -1
    for _ in range(remaining):
        d = random.randint(0, 9)
        # Avoid sequential patterns
        while d == last_digit and random.random() < 0.7:
            d = random.randint(0, 9)
        body += str(d)
        last_digit = d
    
    # Calculate Luhn check digit
    digits = [int(d) for d in body]
    s = 0
    double = True
    for i in range(len(digits) - 1, -1, -1):
        x = digits[i]
        if double:
            x *= 2
            if x > 9:
                x -= 9
        s += x
        double = not double
    
    check = (10 - (s % 10)) % 10
    return {
        'number': body + str(check),
        'type': card_type,
        'prefix': prefix
    }

def scraper_gen_card(bin_prefix: str = None) -> Dict:
    """Generate card for scraper mode"""
    if bin_prefix and len(bin_prefix) >= 4:
        bp = bin_prefix[:6]
        if bp[0] == '4':
            card_type = "Visa"
            prefix = bp
            length = 16
        elif bp[0] == '5':
            card_type = "Mastercard"
            prefix = bp
            length = 16
        elif bp[:2] in ['34', '37']:
            card_type = "American Express"
            prefix = bp
            length = 15
        elif bp[:4] == '6011':
            card_type = "Discover"
            prefix = bp
            length = 16
        else:
            card_type = "Visa"
            prefix = '4' + bp[1:6]
            length = 16
    else:
        types = ["Visa", "Visa", "Visa", "Mastercard", "Mastercard", "Mastercard", "American Express", "Discover"]
        card_type = types[random.randint(0, len(types) - 1)]
        cfg = CARD_CONFIG[card_type]
        prefix = cfg['prefixes'][random.randint(0, len(cfg['prefixes']) - 1)]
        length = cfg['length']
    
    body = prefix
    while len(body) < length - 1:
        body += str(random.randint(0, 9))
    
    digits = [int(d) for d in body]
    s = 0
    double = True
    for i in range(len(digits) - 1, -1, -1):
        x = digits[i]
        if double:
            x *= 2
            if x > 9:
                x -= 9
        s += x
        double = not double
    
    check = (10 - (s % 10)) % 10
    return {
        'number': body + str(check),
        'type': card_type
    }

async def validate_card_full(number: str, month: str, year: str, cvv: str) -> Dict:
    """Full card validation with BIN lookup and gateway check"""
    if len(number) < 13 or len(number) > 19:
        return {'valid': False, 'reason': 'Invalid length'}
    
    if int(number[0]) < 3 or int(number[0]) > 6:
        return {'valid': False, 'reason': 'Invalid prefix'}
    
    if not luhn_check(number):
        return {'valid': False, 'reason': 'Card verification failed'}
    
    if is_fake_pattern(number):
        return {'valid': False, 'reason': 'Card verification failed'}
    
    if not is_valid_iin(number[:6]):
        return {'valid': False, 'reason': 'Card verification failed'}
    
    bin_info = await bin_lookup(number[:6])
    if not bin_info['valid']:
        return {'valid': False, 'reason': 'Unknown BIN'}
    
    razorpay = await razorpay_check(number, month, year, cvv)
    if razorpay['valid']:
        return {'valid': True, 'info': bin_info}
    
    return {'valid': False, 'reason': razorpay.get('reason', 'Payment declined'), 'info': bin_info}

def fmt_gen(c: Dict, idx: int) -> str:
    """Format generated card message"""
    return f"""{em("FIRE")} <b>💳 CC #{idx}</b>

<blockquote expandable>
{em("CARD")} <b>Card:</b> <code>{c['card']}</code>
{em("CHECK")} <b>Status:</b> ✅ Approved
{em("SEARCH")} <b>BIN:</b> <code>{c['bin']}</code>
━━━━━━━━━━━━━━━━━━━━
{em("INFO")} <b>Info:</b> <code>{c['type']} | {c['brand']} | {c['cardType']} | {c['level']}</code>
{em("BANK")} <b>Bank:</b> <code>{c['bank']}</code>
{em("GLOBE")} <b>Country:</b> {c['cname']} {c['flag']}
━━━━━━━━━━━━━━━━━━━━
{em("TAG")} <b>Extra:</b> <code>{c['number'][:6]}xxxx|{c['month']}|{c['year']}|rnd</code>
{em("USER")} <b>Holder:</b> <code>{c['name']}</code>
</blockquote>"""

def fmt_scrape(c: Dict, idx: int) -> str:
    """Format scraped card message"""
    return f"""{em("SCRAPE")} <b>🕷️ SCRAPED CC #{idx}</b> {em("MAGNET")}

<blockquote expandable>
{em("CARD")} <b>💳 Card:</b> <code>{c['card']}</code>
{em("CHECK")} <b>📊 Status:</b> ✅ SCRAPED
{em("SEARCH")} <b>🔍 BIN:</b> <code>{c['bin']}</code>
▬▬▬▬▬▬▬▬▬▬▬▬▬▬
{em("INFO")} <b>📋 Type:</b> <code>{c['type']} | {c['brand']} | {c['cardType']} | {c['level']}</code>
{em("BANK")} <b>🏦 Bank:</b> <code>{c['bank']}</code>
{em("GLOBE")} <b>🌍 Country:</b> {c['cname']} {c['flag']}
▬▬▬▬▬▬▬▬▬▬▬▬▬▬
{em("TAG")} <b>🏷 Extra:</b> <code>{c['number'][:6]}xxxx|{c['month']}|{c['year']}|rnd</code>
{em("USER")} <b>👤 Holder:</b> <code>{c['name']}</code>
{em("MAGNET")} <b>🕸️ Scraped by:</b> {BOT_USERNAME}
</blockquote>"""

def fmt_dump(c: Dict, idx: int) -> str:
    """Format dumped card message"""
    return f"""{em("SKULL")} <b>💀 DUMP CC #{idx}</b> {em("BOMB")}

<blockquote expandable>
{em("CARD")} <b>💳 Dump:</b> <code>{c['card']}</code>
{em("FLAME")} <b>🔥 Status:</b> LIVE DUMP
{em("SEARCH")} <b>🔍 BIN:</b> <code>{c['bin']}</code>
▬▬▬▬▬▬▬▬▬▬▬▬▬▬
{em("INFO")} <b>📋 Type:</b> <code>{c['type']} | {c['brand']} | {c['cardType']} | {c['level']}</code>
{em("BANK")} <b>🏦 Bank:</b> <code>{c['bank']}</code>
{em("GLOBE")} <b>🌍 Country:</b> {c['cname']} {c['flag']}
▬▬▬▬▬▬▬▬▬▬▬▬▬▬
{em("TAG")} <b>🏷 Extra:</b> <code>{c['number'][:6]}xxxx|{c['month']}|{c['year']}|rnd</code>
{em("USER")} <b>👤 Holder:</b> <code>{c['name']}</code>
{em("GHOST")} <b>💀 Dumped by:</b> {BOT_USERNAME}
</blockquote>"""

# Keyboard layouts
kb = {
    'inline_keyboard': [
        [btn_url("👑 Developer", "https://t.me/S_1xD", "primary", "CROWN")],
        [btn_url("📢 Channel", "https://t.me/xb1ns", "primary", "CHANNEL_EMO")]
    ]
}

dump_kb = {
    'inline_keyboard': [
        [btn_url("💀 Dumper", "https://t.me/S_1xD", "danger", "SKULL")],
        [btn_url("📢 Channel", "https://t.me/xb1ns", "primary", "CHANNEL_EMO")]
    ]
}

scrape_kb = {
    'inline_keyboard': [
        [btn_url("🕷️ Scraper", "https://t.me/S_1xD", "primary", "SCRAPE")],
        [btn_url("📢 Channel", "https://t.me/xb1ns", "primary", "CHANNEL_EMO")]
    ]
}

def parse_ccs(text: str) -> List[str]:
    """Parse CCs from text"""
    lines = text.split('\n')
    ccs = []
    for line in lines:
        l = line.strip()
        l = re.sub(r'^/startdump\s*-?\d+\s*', '', l)
        l = re.sub(r'^/dump\s*', '', l)
        if l and '|' in l:
            parts = l.split('|')
            if len(parts) >= 3:
                ccs.append(l)
    return ccs

def shut_everything() -> Dict:
    """Stop all running operations"""
    gen_count = Gen.stop()
    dump_count = Dump.stop()
    scrape_count = Scrape.stop()
    return {'gen': gen_count, 'dump': dump_count, 'scrape': scrape_count}

# ============================================
# GENERATOR CLASS
# ============================================
class Generator:
    def __init__(self):
        self.run = False
        self.stop = False
        self.cnt = 0
        self.approved = 0
        self.declined = 0
        self.total_needed = 999999
        self.interval = 20000
        self.timer = None
        self.anim_msg = None
        self.cid = None
    
    def start(self, cid: int, sec: int, total: int) -> bool:
        if self.run:
            return False
        self.run = True
        self.stop = False
        self.cnt = 0
        self.approved = 0
        self.declined = 0
        self.total_needed = total or 999999
        self.interval = max(5000, sec * 1000)
        self.anim_msg = None
        self.cid = cid
        asyncio.create_task(self._check_loop())
        return True
    
    def stop(self) -> int:
        self.stop = True
        self.run = False
        if self.timer:
            self.timer.cancel()
            self.timer = None
        return self.approved
    
    async def _check_loop(self):
        while self.run and not self.stop:
            await self._check()
            await asyncio.sleep(self.interval / 1000)
    
    async def _check(self):
        if self.stop or not self.run:
            self.run = False
            return
        
        if self.approved >= self.total_needed:
            self.run = False
            if self.anim_msg:
                try:
                    # Delete animation message
                    pass
                except:
                    pass
            # Send completion message
            return
        
        self.cnt += 1
        passed = False
        
        for t in range(20):
            if self.stop or not self.run:
                break
            
            g = advanced_gen_card()
            if is_fake_pattern(g['number']) or not is_valid_iin(g['number'][:6]):
                continue
            
            now = datetime.now()
            cy = now.year
            cm = now.month
            y = (cy + random.randint(1, 4) + (1 if cm >= 6 else 0)) % 100
            m = random.randint(6, 12) if y == cy % 100 else random.randint(1, 12)
            exp_m = str(m).zfill(2)
            exp_y = str(y).zfill(2)
            
            cvv = str(random.randint(1000, 9999)) if g['type'] == "American Express" else str(random.randint(100, 999))
            
            # Update animation message
            anim_text = f"""{em("LOAD")} <b>🔍 CHECKING ON GATEWAY...</b>

<blockquote>
{em("CHART")} <b>Approved:</b> {self.approved}/{self.total_needed}
{em("CROSS")} <b>Declined:</b> {self.declined}
{em("CLOCK")} <b>Tries:</b> {t+1}/20
━━━━━━━━━━━━━━━━━━━━
{em("CARD")} <b>Testing:</b> <code>{g['number']}|xx|xx|xxx</code>
{em("SEARCH")} <b>Checking on gateway...</b>
</blockquote>"""
            # Send/update animation message
            
            result = await validate_card_full(g['number'], exp_m, exp_y, cvv)
            
            if not result or not result.get('valid'):
                self.declined += 1
                reason = result.get('reason', 'declined')
                dec_text = f"""{em("CROSS")} <b>❌ DECLINED</b>

<blockquote>
{em("CHART")} <b>Approved:</b> {self.approved}/{self.total_needed}
{em("CROSS")} <b>Declined:</b> {self.declined}
{em("CLOCK")} <b>Tries:</b> {t+1}/20
━━━━━━━━━━━━━━━━━━━━
{em("CARD")} <b>Failed:</b> <code>{g['number']}|{exp_m}|{exp_y}|{cvv}</code>
{em("SEARCH")} <b>Reason:</b> {reason}
{em("LOAD")} <b>Checking on gateway...</b>
</blockquote>"""
                # Update animation message with decline
                await asyncio.sleep(2)
                continue
            
            self.approved += 1
            passed = True
            
            # Delete animation message
            
            info = result.get('info', {})
            card = {
                'card': f"{g['number']}|{exp_m}|{exp_y}|{cvv}",
                'number': g['number'],
                'month': exp_m,
                'year': exp_y,
                'cvv': cvv,
                'bin': g['number'][:6],
                'type': g['type'],
                'brand': info.get('brand', 'UNKNOWN'),
                'country': info.get('country', 'US'),
                'cname': info.get('cname', 'United States'),
                'flag': info.get('flag', '🇺🇸'),
                'bank': info.get('bank', 'Unknown'),
                'level': info.get('level', 'CLASSIC'),
                'cardType': info.get('type', 'CREDIT'),
                'name': f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                'approved': True
            }
            
            fm = fmt_gen(card, self.approved)
            # Send card with photo
            # try: send photo
            # except: send message
            break
        
        if not passed and self.anim_msg:
            # Delete animation message
            pass

# ============================================
# SCRAPER CLASS
# ============================================
class Scraper:
    def __init__(self):
        self.run = False
        self.stop = False
        self.cnt = 0
        self.interval = 20000
        self.timer = None
        self.anim_msg = None
        self.cid = None
        self.bin_prefix = ""
    
    def start(self, cid: int, sec: int, bin_prefix: str = "") -> bool:
        if self.run:
            return False
        self.run = True
        self.stop = False
        self.cnt = 0
        self.interval = max(3000, sec * 1000)
        self.bin_prefix = bin_prefix or ""
        self.anim_msg = None
        self.cid = cid
        asyncio.create_task(self._scrape_loop())
        return True
    
    def stop(self) -> int:
        self.stop = True
        self.run = False
        if self.timer:
            self.timer.cancel()
            self.timer = None
        return self.cnt
    
    async def _scrape_loop(self):
        while self.run and not self.stop:
            await self._scrape()
            await asyncio.sleep(self.interval / 1000)
    
    async def _scrape(self):
        if self.stop or not self.run:
            self.run = False
            return
        
        self.cnt += 1
        g = scraper_gen_card(self.bin_prefix)
        now = datetime.now()
        cy = now.year
        cm = now.month
        y = (cy + random.randint(1, 4) + (1 if cm >= 6 else 0)) % 100
        m = random.randint(6, 12) if y == cy % 100 else random.randint(1, 12)
        exp_m = str(m).zfill(2)
        exp_y = str(y).zfill(2)
        cvv = str(random.randint(1000, 9999)) if g['type'] == "American Express" else str(random.randint(100, 999))
        
        bin_num = g['number'][:6]
        info = await bin_lookup(bin_num)
        
        card = {
            'card': f"{g['number']}|{exp_m}|{exp_y}|{cvv}",
            'number': g['number'],
            'month': exp_m,
            'year': exp_y,
            'cvv': cvv,
            'bin': bin_num,
            'type': g['type'],
            'brand': info.get('brand', 'UNKNOWN'),
            'country': info.get('country', 'US'),
            'cname': info.get('cname', 'United States'),
            'flag': info.get('flag', '🇺🇸'),
            'bank': info.get('bank', 'Unknown'),
            'level': info.get('level', 'CLASSIC'),
            'cardType': info.get('type', 'CREDIT'),
            'name': f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        }
        
        fm = fmt_scrape(card, self.cnt)
        # Send card with photo
        # try: send photo
        # except: send message

# ============================================
# DUMP CLASS
# ============================================
class Dumper:
    def __init__(self):
        self.run = False
        self.stop = False
        self.cnt = 0
        self.cards = []
        self.timer = None
        self.gid = None
        self.anim_msg = None
    
    def start(self, gid: int, cards: List[str]) -> bool:
        if self.run:
            return False
        self.run = True
        self.stop = False
        self.cnt = 0
        self.cards = cards
        self.gid = gid
        self.anim_msg = None
        asyncio.create_task(self._hijack_loop())
        return True
    
    def stop(self) -> int:
        self.stop = True
        self.run = False
        if self.timer:
            self.timer.cancel()
            self.timer = None
        return self.cnt
    
    async def _hijack_loop(self):
        steps = [
            {'text': f"""{em("SKULL")} <b>💀 INCOMING ATTACK...</b> {em("BOMB")}

<blockquote>
{em("TOOL")} ⚙️ Bypassing firewall...
{em("LOAD")} 🔌 Injecting payload...
{em("ZAP")} ⚡ Exploiting system...
{em("TARGET")} 🎯 Group compromised!
</blockquote>""", 'delay': 3000},
            {'text': f"""{em("DUMP")} <b>💀 SYSTEM BREACHED!</b> {em("FLAME")}

<blockquote>
{em("LOCK")} 🔓 Security disabled!
{em("ROCKET")} 📤 CC dump incoming...
{em("HIT")} 🔥 Cards loaded...

{em("CHECK")} ⏳ <b>DUMPING IN 10s...</b>
</blockquote>""", 'delay': 4000},
            {'text': f"{em('BOMB')} <b>⚡ 6s...</b>", 'delay': 2000},
            {'text': f"{em('FLAME')} <b>🔥 4s...</b>", 'delay': 2000},
            {'text': f"{em('SKULL')} <b>💀 2s...</b>", 'delay': 2000}
        ]
        
        for step in steps:
            if self.stop or not self.run:
                break
            # Send/update animation message
            await asyncio.sleep(step['delay'] / 1000)
        
        if not self.stop and self.run:
            await self._send_loop()
    
    async def _send_loop(self):
        while self.run and not self.stop:
            await self._send()
            await asyncio.sleep(10)
    
    async def _send(self):
        if self.stop or not self.run:
            self.run = False
            return
        
        if self.cnt >= len(self.cards):
            self.run = False
            # Send completion message
            return
        
        line = self.cards[self.cnt].strip()
        self.cnt += 1
        
        if line and '|' in line:
            parts = line.split('|')
            cc_num = parts[0] or '0'
            mm = parts[1] if len(parts) > 1 else '12'
            yy = parts[2] if len(parts) > 2 else '27'
            cv = parts[3] if len(parts) > 3 else '123'
            
            bin_num = cc_num[:6]
            info = await bin_lookup(bin_num)
            
            card = {
                'card': f"{cc_num}|{mm}|{yy}|{cv}",
                'number': cc_num,
                'month': mm,
                'year': yy,
                'cvv': cv,
                'bin': bin_num,
                'type': info.get('brand', 'UNKNOWN'),
                'brand': info.get('brand', 'UNKNOWN'),
                'country': info.get('country', 'US'),
                'cname': info.get('cname', 'United States'),
                'flag': info.get('flag', '🇺🇸'),
                'bank': info.get('bank', 'Unknown'),
                'level': info.get('level', 'CLASSIC'),
                'cardType': info.get('type', 'CREDIT'),
                'name': f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            }
            
            fm = fmt_dump(card, self.cnt)
            # Send card with photo
            # try: send photo
            # except: send message
        
        if self.cnt < len(self.cards) and self.run and not self.stop:
            # Send "next CC in 10s" message
            pass

# Global instances
Gen = Generator()
Scrape = Scraper()
Dump = Dumper()

# ============================================
# ANIME API - Random anime pictures
# ============================================
async def get_random_anime_pic() -> str:
    """Fetch a random anime picture from free API"""
    try:
        async with aiohttp.ClientSession() as session:
            # Using multiple free anime APIs for redundancy
            apis = [
                "https://api.waifu.pics/sfw/waifu",
                "https://api.waifu.pics/sfw/neko",
                "https://api.waifu.pics/sfw/shrug",
                "https://nekos.life/api/v2/img/waifu",
                "https://nekos.life/api/v2/img/neko"
            ]
            
            api_url = random.choice(apis)
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if 'url' in data:
                        return data['url']
                    elif 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
                        return data['data'][0].get('url', DUMP_IMAGE)
    except:
        pass
    
    # Fallback to random anime images from known CDN
    fallback_urls = [
        "https://i.pinimg.com/736x/7c/76/3c/7c763c87b8b3183c496fdd2f7a6d05c8.jpg",
        "https://i.pinimg.com/736x/2b/83/13/2b8313291884ad84998a8d00451bff9e.jpg",
        "https://i.pinimg.com/736x/ed/0f/0a/ed0f0aaa981b32da87db054d8b6de6f4.jpg",
        "https://i.pinimg.com/736x/5b/d2/eb/5bd2eb5502952ce962a372311c78f362.jpg",
        "https://i.pinimg.com/736x/3b/e9/9b/3be99bcc328eb7f35ff3e90661d55b96.jpg"
    ]
    return random.choice(fallback_urls)

# ============================================
# TELEGRAM BOT HANDLER
# ============================================
class TelegramBot:
    def __init__(self):
        self.bot_token = BOT_TOKEN
        self.base_url = f"https://api.telegram.org/bot{BOT_TOKEN}"
    
    async def send_message(self, chat_id, text, parse_mode="HTML", reply_markup=None):
        """Send a message"""
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        if reply_markup:
            payload["reply_markup"] = json.dumps(reply_markup)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                return await resp.json()
    
    async def send_photo(self, chat_id, photo, caption="", parse_mode="HTML", reply_markup=None):
        """Send a photo with caption"""
        url = f"{self.base_url}/sendPhoto"
        payload = {
            "chat_id": chat_id,
            "photo": photo,
            "caption": caption,
            "parse_mode": parse_mode
        }
        if reply_markup:
            payload["reply_markup"] = json.dumps(reply_markup)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                return await resp.json()
    
    async def edit_message_text(self, chat_id, message_id, text, parse_mode="HTML", reply_markup=None):
        """Edit a message"""
        url = f"{self.base_url}/editMessageText"
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": parse_mode
        }
        if reply_markup:
            payload["reply_markup"] = json.dumps(reply_markup)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                return await resp.json()
    
    async def delete_message(self, chat_id, message_id):
        """Delete a message"""
        url = f"{self.base_url}/deleteMessage"
        payload = {
            "chat_id": chat_id,
            "message_id": message_id
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                return await resp.json()
    
    async def reply(self, text, parse_mode="HTML", reply_markup=None):
        """Reply to the current message (uses update context)"""
        # This would need access to the current update
        # For simplicity, we'll handle this in the main loop
        pass

# ============================================
# MAIN BOT HANDLER
# ============================================
bot = TelegramBot()

async def handle_update(update: Dict):
    """Handle incoming update"""
    if 'message' not in update:
        return
    
    message = update['message']
    if 'text' not in message:
        return
    
    text = message['text'].strip()
    user_id = str(message['from']['id'])
    chat_id = message['chat']['id']
    is_g = is_group(chat_id)
    
    # Check admin permissions
    if is_g and not text.startswith('/'):
        return
    if is_g and not is_admin(user_id):
        return
    if not is_g and not is_admin(user_id):
        await bot.send_message(
            chat_id,
            f'{em("LOCK")} <b>Admin Only!</b>\n\n<blockquote>Contact: {CHANNEL}</blockquote>',
            parse_mode="HTML"
        )
        return
    
    # Handle commands
    if text == '/stop':
        r = shut_everything()
        await bot.send_message(
            chat_id,
            f'{em("STOP")} <b>🔴 ALL SHUT DOWN!</b>\n\n<blockquote>💳 Gen: {r["gen"]}\n🕷️ Scrape: {r["scrape"]}\n💀 Dump: {r["dump"]}</blockquote>',
            parse_mode="HTML"
        )
        return
    
    if text == '/start':
        welcome = f"""{em("FIRE")} <b>💳 PREMIUM CC BOT</b>

<blockquote>
{em("CARD")} /gen - 1 Approved
{em("BULK")} /gen10 - 10 Approved
{em("ROCKET")} /genunlimited - Auto
{em("SCRAPE")} /scr - 1 Scraped
{em("SCRAPE")} /scr10 - 10 Scraped
{em("MAGNET")} /scrunlimited 5 - Auto
{em("SKULL")} /startdump -100xxx
{em("STOP")} /stop
{em("CHART")} /status
</blockquote>
{em("CHANNEL_EMO")} {CHANNEL}"""
        await bot.send_message(chat_id, welcome, parse_mode="HTML")
        return
    
    # ============================================
    # SCRAPER COMMANDS
    # ============================================
    if text == '/scr':
        g = scraper_gen_card()
        now = datetime.now()
        cy = now.year
        cm = now.month
        y = (cy + random.randint(1, 4) + (1 if cm >= 6 else 0)) % 100
        m = random.randint(6, 12) if y == cy % 100 else random.randint(1, 12)
        exp_m = str(m).zfill(2)
        exp_y = str(y).zfill(2)
        cvv = str(random.randint(1000, 9999)) if g['type'] == "American Express" else str(random.randint(100, 999))
        
        bin_num = g['number'][:6]
        info = await bin_lookup(bin_num)
        
        card = {
            'card': f"{g['number']}|{exp_m}|{exp_y}|{cvv}",
            'number': g['number'],
            'month': exp_m,
            'year': exp_y,
            'cvv': cvv,
            'bin': bin_num,
            'type': g['type'],
            'brand': info.get('brand', 'UNKNOWN'),
            'country': info.get('country', 'US'),
            'cname': info.get('cname', 'United States'),
            'flag': info.get('flag', '🇺🇸'),
            'bank': info.get('bank', 'Unknown'),
            'level': info.get('level', 'CLASSIC'),
            'cardType': info.get('type', 'CREDIT'),
            'name': f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        }
        
        fm = fmt_scrape(card, 1)
        anime_pic = await get_random_anime_pic()
        try:
            await bot.send_photo(chat_id, anime_pic, caption=fm, parse_mode="HTML", reply_markup=scrape_kb)
        except:
            await bot.send_message(chat_id, fm, parse_mode="HTML", reply_markup=scrape_kb)
        return
    
    if text == '/scr10':
        await bot.send_message(chat_id, f'{em("SCRAPE")} <b>🕷️ Scraping 10 cards...</b>', parse_mode="HTML")
        for i in range(10):
            g = scraper_gen_card()
            now = datetime.now()
            cy = now.year
            cm = now.month
            y = (cy + random.randint(1, 4) + (1 if cm >= 6 else 0)) % 100
            m = random.randint(6, 12) if y == cy % 100 else random.randint(1, 12)
            exp_m = str(m).zfill(2)
            exp_y = str(y).zfill(2)
            cvv = str(random.randint(1000, 9999)) if g['type'] == "American Express" else str(random.randint(100, 999))
            
            bin_num = g['number'][:6]
            info = await bin_lookup(bin_num)
            
            card = {
                'card': f"{g['number']}|{exp_m}|{exp_y}|{cvv}",
                'number': g['number'],
                'month': exp_m,
                'year': exp_y,
                'cvv': cvv,
                'bin': bin_num,
                'type': g['type'],
                'brand': info.get('brand', 'UNKNOWN'),
                'country': info.get('country', 'US'),
                'cname': info.get('cname', 'United States'),
                'flag': info.get('flag', '🇺🇸'),
                'bank': info.get('bank', 'Unknown'),
                'level': info.get('level', 'CLASSIC'),
                'cardType': info.get('type', 'CREDIT'),
                'name': f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            }
            
            fm = fmt_scrape(card, i + 1)
            anime_pic = await get_random_anime_pic()
            try:
                await bot.send_photo(chat_id, anime_pic, caption=fm, parse_mode="HTML", reply_markup=scrape_kb)
            except:
                await bot.send_message(chat_id, fm, parse_mode="HTML", reply_markup=scrape_kb)
            await asyncio.sleep(1)
        return
    
    if text.startswith('/scrunlimited'):
        if Scrape.run:
            await bot.send_message(chat_id, f'{em("WARN")} Scraper running! /stop', parse_mode="HTML")
            return
        parts = text.split()
        sec = int(parts[1]) if len(parts) > 1 else 5
        sec = max(3, sec)
        if Scrape.start(chat_id, sec):
            await bot.send_message(
                chat_id,
                f'{em("SCRAPE")} <b>🕷️ Scraper Started!</b> Every {sec}s',
                parse_mode="HTML"
            )
        return
    
    # ============================================
    # GENERATOR COMMANDS
    # ============================================
    if text == '/gen':
        sent = await bot.send_message(
            chat_id,
            f"""{em("LOAD")} <b>🔍 CHECKING ON GATEWAY...</b>

<blockquote>
{em("CHART")} <b>Approved:</b> 0/1
{em("CROSS")} <b>Declined:</b> 0
{em("CLOCK")} <b>Tries:</b> 0/20
━━━━━━━━━━━━━━━━━━━━
{em("CARD")} <b>Testing...</b>
{em("SEARCH")} <b>Checking on gateway...</b>
</blockquote>""",
            parse_mode="HTML"
        )
        
        anim_msg = sent.get('result', {}).get('message_id')
        approved = 0
        declined = 0
        
        for t in range(20):
            if approved >= 1:
                break
            
            g = advanced_gen_card()
            if is_fake_pattern(g['number']) or not is_valid_iin(g['number'][:6]):
                continue
            
            now = datetime.now()
            cy = now.year
            cm = now.month
            y = (cy + random.randint(1, 4) + (1 if cm >= 6 else 0)) % 100
            m = random.randint(6, 12) if y == cy % 100 else random.randint(1, 12)
            exp_m = str(m).zfill(2)
            exp_y = str(y).zfill(2)
            cvv = str(random.randint(1000, 9999)) if g['type'] == "American Express" else str(random.randint(100, 999))
            
            anim_text = f"""{em("LOAD")} <b>🔍 CHECKING ON GATEWAY...</b>

<blockquote>
{em("CHART")} <b>Approved:</b> {approved}/1
{em("CROSS")} <b>Declined:</b> {declined}
{em("CLOCK")} <b>Tries:</b> {t+1}/20
━━━━━━━━━━━━━━━━━━━━
{em("CARD")} <b>Testing:</b> <code>{g['number']}|xx|xx|xxx</code>
{em("SEARCH")} <b>Checking on gateway...</b>
</blockquote>"""
            
            if anim_msg:
                try:
                    await bot.edit_message_text(chat_id, anim_msg, anim_text, parse_mode="HTML")
                except:
                    pass
            
            result = await validate_card_full(g['number'], exp_m, exp_y, cvv)
            
            if not result or not result.get('valid'):
                declined += 1
                reason = result.get('reason', 'declined')
                dec_text = f"""{em("CROSS")} <b>❌ DECLINED</b>

<blockquote>
{em("CHART")} <b>Approved:</b> {approved}/1
{em("CROSS")} <b>Declined:</b> {declined}
{em("CLOCK")} <b>Tries:</b> {t+1}/20
━━━━━━━━━━━━━━━━━━━━
{em("CARD")} <b>Failed:</b> <code>{g['number']}|{exp_m}|{exp_y}|{cvv}</code>
{em("SEARCH")} <b>Reason:</b> {reason}
{em("LOAD")} <b>Checking on gateway...</b>
</blockquote>"""
                if anim_msg:
                    try:
                        await bot.edit_message_text(chat_id, anim_msg, dec_text, parse_mode="HTML")
                    except:
                        pass
                await asyncio.sleep(2)
                continue
            
            approved += 1
            if anim_msg:
                try:
                    await bot.delete_message(chat_id, anim_msg)
                except:
                    pass
            
            info = result.get('info', {})
            card = {
                'card': f"{g['number']}|{exp_m}|{exp_y}|{cvv}",
                'number': g['number'],
                'month': exp_m,
                'year': exp_y,
                'cvv': cvv,
                'bin': g['number'][:6],
                'type': g['type'],
                'brand': info.get('brand', 'UNKNOWN'),
                'country': info.get('country', 'US'),
                'cname': info.get('cname', 'United States'),
                'flag': info.get('flag', '🇺🇸'),
                'bank': info.get('bank', 'Unknown'),
                'level': info.get('level', 'CLASSIC'),
                'cardType': info.get('type', 'CREDIT'),
                'name': f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                'approved': True
            }
            
            fm = fmt_gen(card, 1)
            anime_pic = await get_random_anime_pic()
            try:
                await bot.send_photo(chat_id, anime_pic, caption=fm, parse_mode="HTML", reply_markup=kb)
            except:
                await bot.send_message(chat_id, fm, parse_mode="HTML", reply_markup=kb)
        
        if approved == 0 and anim_msg:
            try:
                await bot.delete_message(chat_id, anim_msg)
            except:
                pass
        return
    
    if text == '/gen10':
        sent = await bot.send_message(
            chat_id,
            f"""{em("LOAD")} <b>🔍 CHECKING ON GATEWAY...</b>

<blockquote>
{em("CHART")} <b>Approved:</b> 0/10
{em("CROSS")} <b>Declined:</b> 0
{em("CLOCK")} <b>Tries:</b> 0/20
━━━━━━━━━━━━━━━━━━━━
{em("CARD")} <b>Testing...</b>
{em("SEARCH")} <b>Checking on gateway...</b>
</blockquote>""",
            parse_mode="HTML"
        )
        
        anim_msg = sent.get('result', {}).get('message_id')
        approved = 0
        declined = 0
        
        for _round in range(10):
            got = False
            for t in range(20):
                if got:
                    break
                
                g = advanced_gen_card()
                if is_fake_pattern(g['number']) or not is_valid_iin(g['number'][:6]):
                    continue
                
                now = datetime.now()
                cy = now.year
                cm = now.month
                y = (cy + random.randint(1, 4) + (1 if cm >= 6 else 0)) % 100
                m = random.randint(6, 12) if y == cy % 100 else random.randint(1, 12)
                exp_m = str(m).zfill(2)
                exp_y = str(y).zfill(2)
                cvv = str(random.randint(1000, 9999)) if g['type'] == "American Express" else str(random.randint(100, 999))
                
                anim_text = f"""{em("LOAD")} <b>🔍 CHECKING ON GATEWAY...</b>

<blockquote>
{em("CHART")} <b>Approved:</b> {approved}/10
{em("CROSS")} <b>Declined:</b> {declined}
{em("CLOCK")} <b>Tries:</b> {t+1}/20
━━━━━━━━━━━━━━━━━━━━
{em("CARD")} <b>Testing:</b> <code>{g['number']}|xx|xx|xxx</code>
{em("SEARCH")} <b>Checking on gateway...</b>
</blockquote>"""
                
                if anim_msg:
                    try:
                        await bot.edit_message_text(chat_id, anim_msg, anim_text, parse_mode="HTML")
                    except:
                        pass
                
                result = await validate_card_full(g['number'], exp_m, exp_y, cvv)
                
                if not result or not result.get('valid'):
                    declined += 1
                    reason = result.get('reason', 'declined')
                    dec_text = f"""{em("CROSS")} <b>❌ DECLINED</b>

<blockquote>
{em("CHART")} <b>Approved:</b> {approved}/10
{em("CROSS")} <b>Declined:</b> {declined}
{em("CLOCK")} <b>Tries:</b> {t+1}/20
━━━━━━━━━━━━━━━━━━━━
{em("CARD")} <b>Failed:</b> <code>{g['number']}|{exp_m}|{exp_y}|{cvv}</code>
{em("SEARCH")} <b>Reason:</b> {reason}
{em("LOAD")} <b>Checking on gateway...</b>
</blockquote>"""
                    if anim_msg:
                        try:
                            await bot.edit_message_text(chat_id, anim_msg, dec_text, parse_mode="HTML")
                        except:
                            pass
                    await asyncio.sleep(2)
                    continue
                
                approved += 1
                got = True
                
                info = result.get('info', {})
                card = {
                    'card': f"{g['number']}|{exp_m}|{exp_y}|{cvv}",
                    'number': g['number'],
                    'month': exp_m,
                    'year': exp_y,
                    'cvv': cvv,
                    'bin': g['number'][:6],
                    'type': g['type'],
                    'brand': info.get('brand', 'UNKNOWN'),
                    'country': info.get('country', 'US'),
                    'cname': info.get('cname', 'United States'),
                    'flag': info.get('flag', '🇺🇸'),
                    'bank': info.get('bank', 'Unknown'),
                    'level': info.get('level', 'CLASSIC'),
                    'cardType': info.get('type', 'CREDIT'),
                    'name': f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                    'approved': True
                }
                
                fm = fmt_gen(card, approved)
                anime_pic = await get_random_anime_pic()
                try:
                    await bot.send_photo(chat_id, anime_pic, caption=fm, parse_mode="HTML", reply_markup=kb)
                except:
                    await bot.send_message(chat_id, fm, parse_mode="HTML", reply_markup=kb)
                await asyncio.sleep(1.5)
            
            if not got:
                break
        
        if anim_msg:
            try:
                await bot.delete_message(chat_id, anim_msg)
            except:
                pass
        
        await bot.send_message(
            chat_id,
            f'{em("CHECK")} <b>✅ DONE!</b>\n\n<blockquote>✅ Approved: {approved}/10\n❌ Declined: {declined}</blockquote>',
            parse_mode="HTML"
        )
        return
    
    if text.startswith('/genunlimited'):
        if Gen.run:
            await bot.send_message(chat_id, f'{em("WARN")} Running! /stop', parse_mode="HTML")
            return
        parts = text.split()
        sec = int(parts[1]) if len(parts) > 1 else 20
        total = int(parts[2]) if len(parts) > 2 else 999999
        sec = max(5, sec)
        if Gen.start(chat_id, sec, total):
            await bot.send_message(
                chat_id,
                f'{em("ROCKET")} Started! {sec}s | Target: {total}',
                parse_mode="HTML"
            )
        return
    
    if text == '/status':
        status = ""
        if Gen.run:
            status += f"💳 Gen: {Gen.approved}/{Gen.total_needed}\n"
        if Scrape.run:
            status += f"🕷️ Scrape: {Scrape.cnt} ({Scrape.interval/1000}s)\n"
        if Dump.run:
            status += f"💀 Dump: {Dump.cnt}/{len(Dump.cards)}\n"
        await bot.send_message(
            chat_id,
            status or f'{em("CHECK")} Idle',
            parse_mode="HTML"
        )
        return
    
    # ============================================
    # DUMP COMMANDS
    # ============================================
    if text.startswith('/startdump') and not is_g:
        parts = text.split()
        target_gid = parts[1] if len(parts) > 1 else None
        
        if not target_gid:
            await bot.send_message(
                chat_id,
                f'{em("CROSS")} <b>Usage:</b>\n<code>/startdump -100xxxxx</code>\nReply to CC list!',
                parse_mode="HTML"
            )
            return
        
        if Dump.run:
            await bot.send_message(chat_id, f'{em("WARN")} <b>Already running!</b> /stop', parse_mode="HTML")
            return
        
        # Check for replied message or text content
        ccs = []
        if 'reply_to_message' in message and 'text' in message['reply_to_message']:
            ccs = parse_ccs(message['reply_to_message']['text'])
        else:
            ccs = parse_ccs(text)
        
        if len(ccs) == 0:
            await bot.send_message(chat_id, f'{em("CROSS")} <b>No CCs!</b>', parse_mode="HTML")
            return
        
        if Dump.start(int(target_gid), ccs):
            await bot.send_message(
                chat_id,
                f'{em("DUMP")} <b>💀 DUMP LAUNCHED!</b>\n\n<blockquote>📁 CCs: {len(ccs)}\n⏱ 10s\n🎯 Group: <code>{target_gid}</code></blockquote>',
                parse_mode="HTML"
            )
        return

# ============================================
# MAIN LOOP
# ============================================
async def main():
    """Main bot loop"""
    print(f"{em('FIRE')} Bot started!")
    print(f"{em('CROWN')} Owner: {OWNER_ID}")
    print(f"{em('CHANNEL_EMO')} Channel: {CHANNEL}")
    
    # Webhook or polling setup would go here
    # This is a placeholder - in production, you'd set up a webhook or long polling
    
    # For demonstration, we'll simulate a simple polling loop
    # In production, use aiogram, python-telegram-bot, or similar framework
    
    print(f"{em('CHECK')} Bot is ready!")
    
    # Keep the bot running
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())