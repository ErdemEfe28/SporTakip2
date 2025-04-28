import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Sporcu:
    def __init__(self, ad, spor_dali):
        self.ad = ad
        self.spor_dali = spor_dali
        self.antrenmanlar = []
        self.takip_kayitlari = []

    def program_olustur(self, antrenman):
        self.antrenmanlar.append(antrenman)

    def ilerleme_kaydet(self, takip):
        self.takip_kayitlari.append(takip)

    def rapor_al(self):
        return f"Sporcu: {self.ad} - Toplam Antrenman Sayısı: {len(self.takip_kayitlari)}"

class Antrenman:
    def __init__(self, antrenman_adi, detaylar):
        self.antrenman_adi = antrenman_adi
        self.detaylar = detaylar

class Takip:
    def __init__(self, tarih, yapilan_antrenman, notlar):
        self.tarih = tarih
        self.yapilan_antrenman = yapilan_antrenman
        self.notlar = notlar

class SporTakipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spor Takip Uygulaması")
        self.sporcular = []

        tk.Label(root, text="Ad:").grid(row=0, column=0)
        self.txt_ad = tk.Entry(root)
        self.txt_ad.grid(row=0, column=1)

        tk.Label(root, text="Spor Dalı:").grid(row=1, column=0)
        self.txt_spor_dali = tk.Entry(root)
        self.txt_spor_dali.grid(row=1, column=1)

        self.btn_sporcu_ekle = tk.Button(root, text="Sporcu Ekle", command=self.sporcu_ekle)
        self.btn_sporcu_ekle.grid(row=2, column=0, columnspan=2)

        tk.Label(root, text="Sporcular:").grid(row=3, column=0)
        self.lst_sporcular = tk.Listbox(root)
        self.lst_sporcular.grid(row=3, column=1)
        self.lst_sporcular.bind("<<ListboxSelect>>", self.sporcu_secildi)

        tk.Label(root, text="Antrenman Adı:").grid(row=4, column=0)
        self.txt_antrenman_adi = tk.Entry(root)
        self.txt_antrenman_adi.grid(row=4, column=1)

        tk.Label(root, text="Detaylar:").grid(row=5, column=0)
        self.txt_detaylar = tk.Entry(root)
        self.txt_detaylar.grid(row=5, column=1)

        self.btn_antrenman_ekle = tk.Button(root, text="Antrenman Ekle", command=self.antrenman_ekle)
        self.btn_antrenman_ekle.grid(row=6, column=0, columnspan=2)

        tk.Label(root, text="Tarih (GG/AA/YYYY):").grid(row=7, column=0)
        self.txt_tarih = tk.Entry(root)
        self.txt_tarih.grid(row=7, column=1)

        tk.Label(root, text="Yapılan Antrenman:").grid(row=8, column=0)
        self.var_yapilan_antrenman = tk.StringVar(root)
        self.opt_yapilan_antrenman = tk.OptionMenu(root, self.var_yapilan_antrenman, "")
        self.opt_yapilan_antrenman.grid(row=8, column=1)

        tk.Label(root, text="Notlar:").grid(row=9, column=0)
        self.txt_notlar = tk.Entry(root)
        self.txt_notlar.grid(row=9, column=1)

        self.btn_ilerleme_kaydet = tk.Button(root, text="İlerleme Kaydet", command=self.ilerleme_kaydet)
        self.btn_ilerleme_kaydet.grid(row=10, column=0, columnspan=2)

        self.btn_rapor_al = tk.Button(root, text="Rapor Al", command=self.rapor_al)
        self.btn_rapor_al.grid(row=11, column=0, columnspan=2)

        self.lst_rapor = tk.Listbox(root, width=50)
        self.lst_rapor.grid(row=12, column=0, columnspan=2)

    def sporcu_ekle(self):
        ad = self.txt_ad.get()
        spor_dali = self.txt_spor_dali.get()
        if ad and spor_dali:
            yeni_sporcu = Sporcu(ad, spor_dali)
            self.sporcular.append(yeni_sporcu)
            self.lst_sporcular.insert(tk.END, ad)
            messagebox.showinfo("Başarılı", "Sporcu Eklendi!")
        else:
            messagebox.showerror("Hata", "Tüm alanları doldurun!")

    def secili_sporcu(self):
        secili = self.lst_sporcular.curselection()
        if secili:
            index = secili[0]
            return self.sporcular[index]
        return None

    def sporcu_secildi(self, event):
        sporcu = self.secili_sporcu()
        if sporcu:
            self.guncelle_antrenman_secimi(sporcu)

    def antrenman_ekle(self):
        sporcu = self.secili_sporcu()
        if sporcu:
            adi = self.txt_antrenman_adi.get()
            detay = self.txt_detaylar.get()
            if adi and detay:
                yeni_antrenman = Antrenman(adi, detay)
                sporcu.program_olustur(yeni_antrenman)
                self.guncelle_antrenman_secimi(sporcu)
                messagebox.showinfo("Başarılı", "Antrenman Eklendi!")
            else:
                messagebox.showerror("Hata", "Antrenman adı ve detaylar boş olamaz.")

    def guncelle_antrenman_secimi(self, sporcu):
        menu = self.opt_yapilan_antrenman["menu"]
        menu.delete(0, "end")
        for antrenman in sporcu.antrenmanlar:
            menu.add_command(label=antrenman.antrenman_adi, command=lambda value=antrenman.antrenman_adi: self.var_yapilan_antrenman.set(value))

    def ilerleme_kaydet(self):
        sporcu = self.secili_sporcu()
        if sporcu:
            try:
                tarih = datetime.strptime(self.txt_tarih.get(), "%d/%m/%Y")
                yapilan = self.var_yapilan_antrenman.get()
                notlar = self.txt_notlar.get()
                if not yapilan:
                    messagebox.showerror("Hata", "Yapılan antrenmanı seçin!")
                    return
                yeni_takip = Takip(tarih, yapilan, notlar)
                sporcu.ilerleme_kaydet(yeni_takip)
                messagebox.showinfo("Başarılı", "İlerleme Kaydedildi!")
            except ValueError:
                messagebox.showerror("Hata", "Tarih formatı yanlış! (GG/AA/YYYY)")

    def rapor_al(self):
        sporcu = self.secili_sporcu()
        if sporcu:
            self.lst_rapor.delete(0, tk.END)
            self.lst_rapor.insert(tk.END, sporcu.rapor_al())
            for takip in sporcu.takip_kayitlari:
                detay = self.detay_bul(sporcu, takip.yapilan_antrenman)
                self.lst_rapor.insert(tk.END, f"{takip.tarih.strftime('%d/%m/%Y')} - {takip.yapilan_antrenman} ({detay}) - {takip.notlar}")

    def detay_bul(self, sporcu, antrenman_adi):
        for antrenman in sporcu.antrenmanlar:
            if antrenman.antrenman_adi == antrenman_adi:
                return antrenman.detaylar
        return "Detay bulunamadı"

if __name__ == "__main__":
    root = tk.Tk()
    app = SporTakipApp(root)
    root.mainloop()
