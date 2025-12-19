import psycopg2

def baglanti_kur():
    try:
        return psycopg2.connect(
            host="localhost",
            database="AnimasyonDiziVerileri",
            user="postgres",
            password="159357", 
            port="5432"
        )
    except Exception as e:
        print("Bağlantı Hatası:", e)
        return None

def dizileri_getir(aranan=""):
    conn = baglanti_kur()
    cur = conn.cursor()
    


    base_sql = """
        SELECT AnimasyonID, Ad, IMDB_Puani, YayinYili_Baslangic, 
               YayinYili_Bitis, Janra, Teknik, SezonSayisi, BolumSayisi, 
               Oduller, Yonetmenler, Platformlar 
        FROM AnimasyonDizileri
    """
    
    if aranan:
        cur.execute(base_sql + " WHERE Ad ILIKE %s", ('%' + aranan + '%',))
    else:
        cur.execute(base_sql + " ORDER BY Ad ASC")
    
    sonuclar = cur.fetchall()
    cur.close()
    conn.close()
    return sonuclar





def dizi_getir_id_ile(id):
    conn = baglanti_kur()
    cur = conn.cursor()
    sql = """
        SELECT AnimasyonID, Ad, IMDB_Puani, YayinYili_Baslangic, 
               YayinYili_Bitis, Janra, Teknik, SezonSayisi, BolumSayisi, 
               Oduller, Yonetmenler, Platformlar 
        FROM AnimasyonDizileri WHERE AnimasyonID = %s
    """
    cur.execute(sql, (id,))
    veri = cur.fetchone()
    cur.close()
    conn.close()
    return veri



def dizi_ekle(ad, imdb, yil, bitis, janra, teknik, sezon, bolum, oduller, yonetmen, platform):
    conn = baglanti_kur()
    cur = conn.cursor()

    cur.execute("SELECT DiziEkle(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                (ad, imdb, yil, bitis, janra, teknik, sezon, bolum, oduller, yonetmen, platform))
    conn.commit()
    cur.close()
    conn.close()



def dizi_sil(id):
    conn = baglanti_kur()
    cur = conn.cursor()
    cur.execute("SELECT DiziSil(%s)", (id,))
    conn.commit()
    cur.close()
    conn.close()



def dizi_guncelle(id, ad, imdb, yil, bitis, janra, teknik, sezon, bolum, oduller, yonetmen, platform):
    conn = baglanti_kur()
    cur = conn.cursor()
    cur.execute("SELECT DiziGuncelle(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                (id, ad, imdb, yil, bitis, janra, teknik, sezon, bolum, oduller, yonetmen, platform))
    conn.commit()
    cur.close()
    conn.close()



def isim_var_mi(ad, haric_id=None):
    conn = baglanti_kur()
    cur = conn.cursor()
    
    sql = "SELECT Count(*) FROM AnimasyonDizileri WHERE LOWER(Ad) = LOWER(%s)"
    params = [ad]
    
    if haric_id is not None:
        sql += " AND AnimasyonID != %s"
        params.append(haric_id)
        
    cur.execute(sql, tuple(params))
    sayi = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    return sayi > 0