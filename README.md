"""
    Gimbal'a komut paketi yollar.
    Protokole göre toplam uzunluk: 16 byte
    [0]  = 0xEB (sync1)
    [1]  = 0x90 (sync2)
    [2]  = Komut kodu (örn: 0x24 hareket, 0x25 zoom kontrol, 0x5A zoom oranı)
    [3-4] = Parametre X (örn: hız, açı, zoom oranı vs.)
    [5-6] = Parametre Y (örn: pitch açısı, hız vs.)
    [7]   = Parametre3 (çoğu durumda 0)
    [8]   = Zoom hızı (sadece 0x25 için geçerli)
    [9-14]= Reserved (0)
    [15]  = Checksum (ilk 15 byte’ın toplamı & 0xFF)
    """
