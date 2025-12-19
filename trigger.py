from datetime import datetime
import fonklarvs as fonk


def denetle(ad, imdb, yil, islem_tipi="ekle", id=None, bitis_yil=None, sezon=None, bolum=None):
    
    hata = None

    if not ad or str(ad).strip() == "":
        return "Hata: Dizi adı boş olamaz.", None, None, None

    temiz_ad = str(ad).strip().title()

    try:

        imdb_str = str(imdb).replace(",", ".")




        temiz_imdb = float(imdb_str)
        if temiz_imdb < 0 or temiz_imdb > 10:
            return "Hata: IMDB puanı 0 ile 10 arasında olmalıdır.", None, None, None
    except ValueError:
         return "Hata: Puan sayı olmalıdır.", None, None, None




    try:
        temiz_yil = int(yil)
        suanki_yil = datetime.now().year
             
        if temiz_yil > suanki_yil + 5:
            return f"Hata: Çok ileri bir tarih ({temiz_yil}) girilemez!", None, None, None
            
    except ValueError:
        return "Hata: Yıl sayı olmalıdır!", None, None, None


    if bitis_yil is not None:
        try:
            temiz_bitis = int(bitis_yil)
            if temiz_bitis < temiz_yil:
                return f"Hata: Bitiş yılı ({temiz_bitis}), başlangıç yılından ({temiz_yil}) önce olamaz.", None, None, None
        except:
            pass 





    if sezon is not None:
        if int(sezon) < 0:
            return "Hata: Sezon sayısı 0'dan küçük olamaz.", None, None, None
    
    if bolum is not None:
        if int(bolum) < 0:
             return "Hata: Bölüm sayısı 0'dan küçük olamaz.", None, None, None


    if fonk.isim_var_mi(temiz_ad, haric_id=id):
        return f"Hata: '{temiz_ad}' zaten listede var.", None, None, None

    return None, temiz_ad, temiz_imdb, temiz_yil