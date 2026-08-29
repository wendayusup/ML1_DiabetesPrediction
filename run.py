import subprocess
import time
import socket
import shutil
import json
import urllib.request
from pyngrok import ngrok, conf

# 1. Konfigurasi Auth Token ngrok
NGROK_AUTH_TOKEN = "3IRWMUXeXGcFzsBpzabfliimk2o_2Qs8QiiFJwUnKrQacfMN5"

# Fungsi mencari port yang benar-benar kosong (bebas konflik)
def get_available_port(start_port=8501):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
            port += 1

PORT = get_available_port(8501)

# Gunakan binary resmi Windows ngrok.EXE
system_ngrok = shutil.which("ngrok")
if system_ngrok:
    conf.get_default().ngrok_path = system_ngrok

streamlit_process = None
ngrok_process = None
public_url = None

try:
    print(f"⏳ Menyalakan server Streamlit pada Port {PORT}...")
    # Menjalankan Streamlit pada port yang tersedia
    streamlit_process = subprocess.Popen([
        "streamlit", "run", "app.py",
        "--server.port", str(PORT),
        "--server.headless", "true"
    ])
    
    # Verifikasi server Streamlit sampai benar-benar aktif
    print("⏳ Menunggu server Streamlit siap...")
    max_wait = 15
    start_time = time.time()
    server_ready = False
    
    while time.time() - start_time < max_wait:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{PORT}", timeout=1) as response:
                if response.status == 200:
                    server_ready = True
                    break
        except Exception:
            time.sleep(1)
            
    if not server_ready:
        print(f"⚠️ Peringatan: Streamlit memerlukan waktu lebih lama, melanjutkan ke ngrok...")

    print(f"🌐 Membuka terowongan publik ngrok ke Port {PORT}...")
    
    # Coba via pyngrok dengan system binary
    try:
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)
        tunnel = ngrok.connect(PORT)
        public_url = tunnel.public_url
    except Exception:
        # Fallback via native ngrok.EXE langsung
        if system_ngrok:
            ngrok_process = subprocess.Popen([system_ngrok, "http", str(PORT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
            try:
                with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=5) as resp:
                    data = json.loads(resp.read().decode())
                    public_url = data["tunnels"][0]["public_url"]
            except Exception:
                public_url = "http://127.0.0.1:4040 (Cek dashboard ngrok)"
        else:
            raise RuntimeError("ngrok binary tidak ditemukan di PATH sistem.")

    print("\n" + "="*65)
    print("🚀 APLIKASI DIABETES DIAGNOSTIC STUDIO SUDAH ONLINE!")
    print(f"🔗 URL Akses Publik : {public_url}")
    print(f"🏠 URL Akses Lokal  : http://localhost:{PORT}")
    print("="*65)
    print("\n💡 Buka URL Akses Publik di browser HP atau Laptop lain.")
    print("💡 Tekan CTRL + C di terminal ini untuk mematikan server kapan saja.\n")
    
    # Jaga proses tetap berjalan
    streamlit_process.wait()

except KeyboardInterrupt:
    print("\n🛑 Menghentikan server Streamlit dan terowongan ngrok...")
    try:
        ngrok.kill()
    except Exception:
        pass
    if ngrok_process:
        ngrok_process.terminate()
    if streamlit_process:
        streamlit_process.terminate()
    print("✅ Server berhasil dimatikan dengan aman.")

except Exception as e:
    print(f"\n⚠️ Terjadi Kesalahan: {e}")
    if streamlit_process:
        streamlit_process.terminate()