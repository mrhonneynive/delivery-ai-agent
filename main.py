import os
import signal
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
# HATA ÇÖZÜMÜ: ClientTool yerine ClientTools import edildi
from elevenlabs.conversational_ai.conversation import Conversation, ClientTools
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

# 1. Ortam değişkenlerini yükle
load_dotenv()

# --- MOCK DATA (Geliştirme Test Verileri) ---
order_db = {
    "12345": {
        "status": "True",
        "latency": "Gecikmedi",
        "preparing_date": "05.02.2026",
        "shipping_date": "07.02.2026",
        "delivery_info": "Henüz teslim edilmedi",
        "cargo_name": "Yurtiçi Kargo"
    },
    "67890": {
        "status": "True",
        "latency": "Gecikti - Yoğunluk nedeniyle",
        "preparing_date": "01.02.2026",
        "shipping_date": "03.02.2026",
        "delivery_info": "04.02.2026 tarihinde Ali Veli'ye teslim edildi",
        "cargo_name": "Aras Kargo"
    }
}

# --- TOOL CALLBACK FONKSİYONLARI ---
def get_order_callback(parameters):
    # Parametre güvenliği için .get kullanımı
    oid = parameters.get("order_id")
    print(f"\n[TOOL TETİKLENDİ] get_order -> Sipariş No: {oid}")
    
    # Sipariş veritabanında var mı kontrol et
    record = order_db.get(oid)
    if record:
        return "True"
    return "False"

def preparing_callback(parameters):
    oid = parameters.get("order_id")
    print(f"[TOOL TETİKLENDİ] preparing -> {oid}")
    date = order_db.get(oid, {}).get("preparing_date", "Bilinmiyor")
    cargo = order_db.get(oid, {}).get("cargo_name", "")
    return f"Tahmini kargo tarihi: {date}, Kargo Firması: {cargo}"

def shipped_callback(parameters):
    oid = parameters.get("order_id")
    print(f"[TOOL TETİKLENDİ] shipped -> {oid}")
    date = order_db.get(oid, {}).get("shipping_date", "Bilinmiyor")
    cargo = order_db.get(oid, {}).get("cargo_name", "")
    return f"Tahmini teslim tarihi: {date}, Kargo Firması: {cargo}"

def delivered_callback(parameters):
    oid = parameters.get("order_id")
    print(f"[TOOL TETİKLENDİ] delivered -> {oid}")
    info = order_db.get(oid, {}).get("delivery_info", "Bilgi bulunamadı")
    return info

def latency_status_callback(parameters):
    oid = parameters.get("order_id")
    print(f"[TOOL TETİKLENDİ] latency_status -> {oid}")
    return order_db.get(oid, {}).get("latency", "Gecikme bilgisi yok")

# --- ANA ÇALIŞTIRICI ---
def main():
    agent_id = os.getenv("AGENT_ID")
    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not agent_id or not api_key:
        print("HATA: .env dosyasında AGENT_ID veya ELEVENLABS_API_KEY eksik.")
        return

    client = ElevenLabs(api_key=api_key)

    client_tools = ClientTools()
    client_tools.register("get_order", get_order_callback)
    client_tools.register("preparing", preparing_callback)
    client_tools.register("shipped", shipped_callback)
    client_tools.register("delivered", delivered_callback)
    client_tools.register("latency_status", latency_status_callback)

    conversation = Conversation(
        client=client,
        agent_id=agent_id,
        client_tools=client_tools, 
        requires_auth=True,
        audio_interface=DefaultAudioInterface(),
        callback_agent_response=lambda resp: print(f"Asistan: {resp}"),
        callback_user_transcript=lambda transcript: print(f"Müşteri: {transcript}"),
    )

    signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())

    print(">>> Asistan aktif. (Konuşmayı bitirmek için Ctrl+C)")
    print(">>> Test için: '12345' (Gecikmedi) veya '67890' (Gecikti) diyebilirsin.")
    
    conversation.start_session()
    
    session_id = conversation.wait_for_session_end()
    print(f"Oturum sonlandı. ID: {session_id}")

if __name__ == "__main__":
    main()