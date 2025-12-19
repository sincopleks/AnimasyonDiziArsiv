from flask import Flask, render_template, request, redirect, url_for
import fonklarvs as fonk
import trigger as trg

app = Flask(__name__)
def sayi_yap(deger, varsayilan=None):
    if not deger or deger.strip() == "":
        return varsayilan
    try:
        return int(deger)
    except:
        return varsayilan
    




@app.route('/', methods=['GET', 'POST'])
def index():
    aranan = ""
    if request.method == 'POST':
        aranan = request.form.get('aranan_kelime', '')

    sonuclar = fonk.dizileri_getir(aranan)
    return render_template('index.html', sonuclar=sonuclar, aranan=aranan)




@app.route('/ekle', methods=['GET', 'POST'])
def ekle():
    if request.method == 'POST':
        k_ad = request.form['ad']
        k_imdb = request.form['imdb']
        k_yil = request.form['yil']


        bitis = sayi_yap(request.form.get('bitis_yili'))
        janra = request.form.get('janra')
        teknik = request.form.get('teknik')
        sezon = sayi_yap(request.form.get('sezon'), 1)
        bolum = sayi_yap(request.form.get('bolum'), 0)
        oduller = request.form.get('oduller')
        yonetmen = request.form.get('yonetmen')
        platform = request.form.get('platform')





        hata_mesaji, temiz_ad, temiz_imdb, temiz_yil = trg.denetle(
            k_ad, k_imdb, k_yil, 
            islem_tipi="ekle", 
            bitis_yil=bitis, 
            sezon=sezon, 
            bolum=bolum
        )
        


        if hata_mesaji:
            eski_veri = (0, k_ad, k_imdb, k_yil, bitis, janra, teknik, sezon, bolum, oduller, yonetmen, platform)
            return render_template('form.html', islem="Ekle", hata=hata_mesaji, veri=eski_veri)
        




        try:
            fonk.dizi_ekle(temiz_ad, temiz_imdb, temiz_yil, bitis, janra, teknik, sezon, bolum, oduller, yonetmen, platform)
            return redirect(url_for('index'))
        except Exception as hata_sebebi:
            return f"Kayıt Hatası: {hata_sebebi}"
    



    return render_template('form.html', islem="Ekle")




@app.route('/sil/<int:id>')
def sil(id):
    fonk.dizi_sil(id)
    return redirect(url_for('index'))


@app.route('/guncelle/<int:id>', methods=['GET', 'POST'])
def guncelle(id):
    if request.method == 'POST':
        k_ad = request.form['ad']
        k_imdb = request.form['imdb']
        k_yil = request.form['yil']




        bitis = sayi_yap(request.form.get('bitis_yili'))
        janra = request.form.get('janra')
        teknik = request.form.get('teknik')
        sezon = sayi_yap(request.form.get('sezon'), 1)
        bolum = sayi_yap(request.form.get('bolum'), 0)
        oduller = request.form.get('oduller')
        yonetmen = request.form.get('yonetmen')
        platform = request.form.get('platform')

        
        hata_mesaji, temiz_ad, temiz_imdb, temiz_yil = trg.denetle(
            k_ad, k_imdb, k_yil, 
            islem_tipi="guncelle", 
            id=id,
            bitis_yil=bitis, 
            sezon=sezon, 
            bolum=bolum
        )




        if hata_mesaji:
            eski_veri = (id, k_ad, k_imdb, k_yil, bitis, janra, teknik, sezon, bolum, oduller, yonetmen, platform)
            return render_template('form.html', islem="Güncelle", hata=hata_mesaji, veri=eski_veri)

        try:
            fonk.dizi_guncelle(id, temiz_ad, temiz_imdb, temiz_yil, bitis, janra, teknik, sezon, bolum, oduller, yonetmen, platform)
            return redirect(url_for('index'))
        except Exception as hata_sebebi:
             return f"Güncelleme Hatası: {hata_sebebi}"







    veri = fonk.dizi_getir_id_ile(id)
    return render_template('form.html', islem="Güncelle", veri=veri)

if __name__ == '__main__':
    app.run(debug=True)