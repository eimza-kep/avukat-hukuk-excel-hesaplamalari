#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hukuk ve Avukatlık Hesaplama CLI Motoru v2.0 (2026/2027 AAÜT & İİK Güncellemesi)
================================================================================
- AAÜT Nispi ve Maktu Vekalet Ücreti (2026/2027 ve 2024/2025 Tarife Seçimi)
- AAÜT m. 13/2 Alacak Tutarını Aşmama Kuralı ve Mahkeme Maktu Ücretleri
- İcra Dosya Kapak Hesabı (Tahsil ve Cezaevi Harcı)
- İİK m. 67 & 68/a İtirazın Kaldırılması ve %20 İcra İnkar Tazminatı Hesabı
- 6325 sayılı Kanun Uyarınca Arabuluculuk Asgari Ücreti
- 3095 sayılı Kanun Kanuni Faiz ve Ticari Temerrüt Faizi Hesabı

Yazar: E-İmza & Dijital Dönüşüm Portalı (https://uyapteknikdestek.site/)
Lisans: MIT
"""

import sys
import json

# Force UTF-8 stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 2026/2027 Dönemi Resmi Gazete AAÜT Üçüncü Kısım Nispi Kademe Baremleri
AAUT_BRACKETS_2026_2027 = [
    (400000, 0.16),           # İlk 400.000 TL için %16
    (400000, 0.15),           # Sonraki 400.000 TL için %15 (800.000 TL'ye kadar)
    (800000, 0.14),           # Sonraki 800.000 TL için %14 (1.600.000 TL'ye kadar)
    (1200000, 0.11),          # Sonraki 1.200.000 TL için %11 (2.800.000 TL'ye kadar)
    (1600000, 0.08),          # Sonraki 1.600.000 TL için %8 (4.400.000 TL'ye kadar)
    (2000000, 0.05),          # Sonraki 2.000.000 TL için %5 (6.400.000 TL'ye kadar)
    (2400000, 0.03),          # Sonraki 2.400.000 TL için %3 (8.800.000 TL'ye kadar)
    (float('inf'), 0.02)      # 8.800.000 TL'den yukarısı için %2
]

# Önceki Dönem (2024/2025) AAÜT Nispi Baremleri
AAUT_BRACKETS_2024_2025 = [
    (100000, 0.16),
    (100000, 0.15),
    (200000, 0.14),
    (500000, 0.11),
    (1000000, 0.08),
    (float('inf'), 0.05)
]

# 2026/2027 AAÜT İkinci Kısım İkinci Bölüm Maktu Ücret Tarifesi
COURT_MINIMUM_FEES_2026 = {
    "icra_dairesi": 6000.0,
    "icra_mahkemesi": 12000.0,
    "sulh_hukuk": 18000.0,
    "asliye_hukuk": 30000.0,
    "asliye_ticaret": 30000.0,
    "is_mahkemesi": 30000.0,
    "tuketici": 15000.0,
    "agir_ceza": 48000.0,
    "istinaf": 25000.0,
    "temyiz": 40000.0
}

COURT_MINIMUM_FEES_2024 = {
    "icra_dairesi": 3000.0,
    "icra_mahkemesi": 6000.0,
    "sulh_hukuk": 10700.0,
    "asliye_hukuk": 17900.0,
    "asliye_ticaret": 17900.0,
    "is_mahkemesi": 17900.0,
    "tuketici": 9000.0,
    "agir_ceza": 29800.0,
    "istinaf": 15000.0,
    "temyiz": 24000.0
}


def calculate_aaut_fee(alacak_tutari: float, kdv_orani: float = 0.20, year: int = 2026, mahkeme: str = None) -> dict:
    """
    AAÜT (Avukatlık Asgari Ücret Tarifesi) vekâlet ücretini hesaplar:
    - Yıla göre baremler: 2026/2027 veya 2024/2025
    - Mahkeme maktu ücreti ve AAÜT m. 13/2 (alacak miktarını aşmama kuralı) kontrolü
    """
    year = int(year)
    if year >= 2026:
        kademeler = AAUT_BRACKETS_2026_2027
        maktu_tablosu = COURT_MINIMUM_FEES_2026
        tarife_adi = "2026/2027 Dönemi AAÜT"
    else:
        kademeler = AAUT_BRACKETS_2024_2025
        maktu_tablosu = COURT_MINIMUM_FEES_2024
        tarife_adi = f"{year} Öncesi AAÜT"

    kalan = max(0.0, float(alacak_tutari))
    vekalet_ucreti = 0.0
    dilimler = []

    for limit, oran in kademeler:
        if kalan <= 0:
            break
        dilim_tutar = min(kalan, limit)
        dilim_ucret = dilim_tutar * oran
        vekalet_ucreti += dilim_ucret
        dilimler.append({
            "dilim_tutar": dilim_tutar,
            "oran": oran,
            "ucret": round(dilim_ucret, 2)
        })
        kalan -= dilim_tutar

    maktu_ucret = 0.0
    uygulanan_maktu = False
    alacak_siniri_uygulandi = False

    if mahkeme and mahkeme in maktu_tablosu:
        maktu_ucret = maktu_tablosu[mahkeme]
        if vekalet_ucreti < maktu_ucret:
            # AAÜT m. 13/2: Ancak vekalet ücreti alacak tutarını geçemez!
            if alacak_tutari < maktu_ucret:
                vekalet_ucreti = alacak_tutari
                alacak_siniri_uygulandi = True
            else:
                vekalet_ucreti = maktu_ucret
                uygulanan_maktu = True

    kdv_tutari = vekalet_ucreti * kdv_orani
    toplam = vekalet_ucreti + kdv_tutari

    return {
        "alacak_tutari": round(alacak_tutari, 2),
        "tarife_yili": year,
        "tarife_adi": tarife_adi,
        "mahkeme": mahkeme,
        "maktu_asgari_ucret": round(maktu_ucret, 2) if mahkeme else None,
        "uygulanan_maktu": uygulanan_maktu,
        "alacak_siniri_uygulandi": alacak_siniri_uygulandi,
        "net_vekalet_ucreti": round(vekalet_ucreti, 2),
        "kdv_orani": kdv_orani,
        "kdv_tutari": round(kdv_tutari, 2),
        "toplam_ucret": round(toplam, 2),
        "dilimler": dilimler
    }


def calculate_inkar_tazminati(
    asil_alacak: float,
    itiraz_edilen_tutar: float = None,
    faiz: float = 0.0,
    masraf: float = 0.0,
    tazminat_orani: float = 0.20,
    year: int = 2026,
    mahkeme: str = "icra_mahkemesi"
) -> dict:
    """
    2004 sayılı İcra ve İflas Kanunu (İİK) Madde 67 ve 68/a Uyarınca:
    - İtiraz edilen alacak üzerinden asgari %20 İcra İnkar Tazminatı
    - Dava/Talep vekâlet ücreti (AAÜT 2026/2027)
    - Başvuru ve tebligat harçları
    - Kısmi itiraz ve toplam borçlu yükümlülüğü hesabı
    """
    asil_alacak = float(asil_alacak)
    itiraz_tutari = float(itiraz_edilen_tutar) if itiraz_edilen_tutar is not None else asil_alacak
    itiraz_tutari = min(itiraz_tutari, asil_alacak)
    kabul_edilen_tutar = max(0.0, asil_alacak - itiraz_tutari)

    # %20 İcra İnkar Tazminatı (İtiraz edilen asıl alacak üzerinden hesaplanır)
    inkar_tazminati = itiraz_tutari * tazminat_orani

    # Dava / Talep konusu itiraz edilen tutar üzerinden vekalet ücreti
    vekalet_res = calculate_aaut_fee(itiraz_tutari, year=year, mahkeme=mahkeme)
    vekalet_ucreti = vekalet_res["toplam_ucret"]

    # Maktu yargılama ve icra harçları
    basvuru_harci = 427.60
    tebligat_gideri = 250.00
    toplam_masraf = masraf + basvuru_harci + tebligat_gideri

    alacak_toplami = asil_alacak + faiz
    toplam_borclu_yukumlulugu = alacak_toplami + inkar_tazminati + vekalet_ucreti + toplam_masraf

    return {
        "asil_alacak": round(asil_alacak, 2),
        "itiraz_edilen_tutar": round(itiraz_tutari, 2),
        "kabul_edilen_tutar": round(kabul_edilen_tutar, 2),
        "faiz": round(faiz, 2),
        "masraf": round(toplam_masraf, 2),
        "tazminat_orani": tazminat_orani,
        "icra_inkar_tazminati": round(inkar_tazminati, 2),
        "vekalet_ucreti": round(vekalet_ucreti, 2),
        "toplam_borclu_yukumlulugu": round(toplam_borclu_yukumlulugu, 2),
        "yasal_dayanak": "2004 sayılı İİK m. 67 ve m. 68/a (%20 İcra İnkar Tazminatı)"
    }


def calculate_icra_kapak(asil_alacak: float, faiz: float = 0.0, masraf: float = 0.0, year: int = 2026) -> dict:
    """
    İcra dairesi dosya kapak hesabı:
    - Asıl Alacak + İşlemiş Faiz + Masraflar
    - İcra Vekâlet Ücreti (Kademeli AAÜT)
    - Tahsil Harcı (%9.10 - Hacizli/Satışsız tahsilat)
    - Cezaevi Harcı (%2)
    """
    alacak_toplami = asil_alacak + faiz + masraf
    vekalet_res = calculate_aaut_fee(asil_alacak, year=year, mahkeme="icra_dairesi")
    vekalet_ucreti = vekalet_res["toplam_ucret"]

    ara_toplam = alacak_toplami + vekalet_ucreti
    tahsil_harci = ara_toplam * 0.0910
    cezaevi_harci = asil_alacak * 0.0200
    genel_toplam = ara_toplam + tahsil_harci + cezaevi_harci

    return {
        "asil_alacak": round(asil_alacak, 2),
        "faiz": round(faiz, 2),
        "masraf": round(masraf, 2),
        "alacak_toplami": round(alacak_toplami, 2),
        "icra_vekalet_ucreti": round(vekalet_ucreti, 2),
        "tahsil_harci": round(tahsil_harci, 2),
        "cezaevi_harci": round(cezaevi_harci, 2),
        "dosya_kapak_bakiyesi": round(genel_toplam, 2)
    }


def calculate_mediation_fee(anlasilan_tutar: float, kdv_orani: float = 0.20) -> dict:
    """
    6325 sayılı Kanun uyarınca Arabuluculuk Asgari Ücret Tarifesi (Nispi Ücret)
    """
    kademeler = [
        (100000, 0.06),
        (160000, 0.05),
        (340000, 0.04),
        (500000, 0.03),
        (1000000, 0.02),
        (float('inf'), 0.01)
    ]

    kalan = max(0.0, float(anlasilan_tutar))
    ucret = 0.0
    for limit, oran in kademeler:
        if kalan <= 0:
            break
        dilim = min(kalan, limit)
        ucret += dilim * oran
        kalan -= dilim

    kdv = ucret * kdv_orani
    return {
        "anlasilan_tutar": anlasilan_tutar,
        "net_arabuluculuk_ucreti": round(ucret, 2),
        "kdv_tutari": round(kdv, 2),
        "toplam_ucret": round(ucret + kdv, 2)
    }


def calculate_yasal_faiz(tutar: float, gun_sayisi: int, faiz_orani: float = 0.24) -> dict:
    """
    3095 Sayılı Kanuni Faiz ve Temerrüt Faizi Hesabı
    """
    tutar = float(tutar)
    gun = int(gun_sayisi)
    oran = float(faiz_orani)
    faiz = tutar * oran * (gun / 365.0)
    toplam = tutar + faiz
    return {
        "asil_alacak": round(tutar, 2),
        "gun_sayisi": gun,
        "yillik_faiz_orani": oran,
        "faiz_tutari": round(faiz, 2),
        "toplam_alacak": round(toplam, 2)
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Hukuk ve Avukatlık Hesaplama Motoru v2.0 (2026/2027 AAÜT & İİK Güncellemesi)")
    parser.add_argument("--json", action="store_true", help="JSON formatında çıktı ver")
    parser.add_argument("--markdown", action="store_true", help="Markdown formatında rapor üret")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # AAÜT
    p_aaut = subparsers.add_parser("aaut", help="AAÜT Nispi ve Maktu Vekalet Ücreti Hesapla")
    p_aaut.add_argument("tutar", type=float, help="Dava veya icra alacak tutarı (TL)")
    p_aaut.add_argument("--year", type=int, default=2026, choices=[2024, 2025, 2026, 2027], help="Tarife Yılı (Varsayılan: 2026)")
    p_aaut.add_argument("--mahkeme", type=str, default=None,
                        choices=["icra_dairesi", "icra_mahkemesi", "sulh_hukuk", "asliye_hukuk", "asliye_ticaret", "is_mahkemesi", "tuketici", "agir_ceza", "istinaf", "temyiz"],
                        help="Mahkeme Türü Maktu Kontrolü (AAÜT m. 13/2)")

    # İİK m. 67 & 68/a İcra İnkar Tazminatı
    p_inkar = subparsers.add_parser("inkar", help="İİK m. 67 ve 68/a İtirazın Kaldırılması & %20 İcra İnkar Tazminatı")
    p_inkar.add_argument("alacak", type=float, help="Takipteki Asıl Alacak Tutarı (TL)")
    p_inkar.add_argument("--itiraz", type=float, default=None, help="Borçlunun İtiraz Ettiği Tutar (Belirtilmezse tüm alacak sayılır)")
    p_inkar.add_argument("--faiz", type=float, default=0.0, help="İşlemiş Faiz Tutarı")
    p_inkar.add_argument("--masraf", type=float, default=0.0, help="Takip Masrafları")
    p_inkar.add_argument("--oran", type=float, default=0.20, help="İcra İnkar Tazminatı Oranı (Varsayılan: 0.20 / %%20)")
    p_inkar.add_argument("--year", type=int, default=2026, choices=[2024, 2025, 2026, 2027], help="AAÜT Tarife Yılı")

    # İcra Kapak
    p_icra = subparsers.add_parser("icra", help="İcra Dosya Kapak Hesabı")
    p_icra.add_argument("alacak", type=float, help="Asıl alacak tutarı (TL)")
    p_icra.add_argument("--faiz", type=float, default=0.0, help="İşlemiş faiz tutarı")
    p_icra.add_argument("--masraf", type=float, default=0.0, help="Takip masrafları")
    p_icra.add_argument("--year", type=int, default=2026, help="Tarife yılı")

    # Arabuluculuk
    p_med = subparsers.add_parser("arabuluculuk", help="Arabuluculuk Asgari Ücreti Hesapla")
    p_med.add_argument("tutar", type=float, help="Uyuşmazlıkta anlaşılan bedel (TL)")

    # Yasal Faiz
    p_faiz = subparsers.add_parser("faiz", help="3095 s. Kanuni ve Temerrüt Faizi Hesaplayıcı")
    p_faiz.add_argument("tutar", type=float, help="Asıl Alacak Tutarı (TL)")
    p_faiz.add_argument("gun", type=int, help="Geçen Gün Sayısı")
    p_faiz.add_argument("--oran", type=float, default=0.24, help="Yıllık faiz oranı (Varsayılan: 0.24 / %%24)")

    args = parser.parse_args()

    if args.command == "aaut":
        res = calculate_aaut_fee(args.tutar, year=args.year, mahkeme=args.mahkeme)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
            return
        if args.markdown:
            print(f"# AAÜT Vekalet Ücreti Raporu ({res['tarife_adi']})\n\n"
                  f"- **Dava Değeri:** {res['alacak_tutari']:,.2f} TL\n"
                  f"- **Net Ücret:** {res['net_vekalet_ucreti']:,.2f} TL\n"
                  f"- **KDV:** {res['kdv_tutari']:,.2f} TL\n"
                  f"- **Toplam Vekalet Ücreti:** **{res['toplam_ucret']:,.2f} TL**\n"
                  f"- **Maktu Kontrolü:** {res['maktu_asgari_ucret'] or 'Uygulanmadı'}")
            return
        print("=" * 65)
        print(f"      AAÜT VEKALET ÜCRETİ HESAP TABLOSU ({res['tarife_adi']})")
        print("=" * 65)
        print(f"Alacak / Dava Değeri    : {res['alacak_tutari']:,.2f} TL")
        if res['mahkeme']:
            print(f"Mahkeme Türü            : {res['mahkeme']} (Maktu: {res['maktu_asgari_ucret']:,.2f} TL)")
            if res['alacak_siniri_uygulandi']:
                print("⚠️  UYARI: AAÜT m. 13/2 uyarınca vekalet ücreti dava değerini aşamaz!")
        print(f"Net Vekalet Ücreti      : {res['net_vekalet_ucreti']:,.2f} TL")
        print(f"KDV (%{int(res['kdv_orani']*100)})                 : {res['kdv_tutari']:,.2f} TL")
        print(f"TOPLAM VEKALET ÜCRETİ   : {res['toplam_ucret']:,.2f} TL")
        print("=" * 65)

    elif args.command == "inkar":
        res = calculate_inkar_tazminati(args.alacak, args.itiraz, args.faiz, args.masraf, args.oran, args.year)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
            return
        if args.markdown:
            print(f"# İİK m. 67 & 68/a İcra İnkar Tazminatı Raporu\n\n"
                  f"- **Takipteki Asıl Alacak:** {res['asil_alacak']:,.2f} TL\n"
                  f"- **İtiraz Edilen Kısım:** {res['itiraz_edilen_tutar']:,.2f} TL\n"
                  f"- **%%20 İcra İnkar Tazminatı:** **{res['icra_inkar_tazminati']:,.2f} TL**\n"
                  f"- **İtirazın Kaldırılması Vekalet:** {res['vekalet_ucreti']:,.2f} TL\n"
                  f"- **Toplam Borçlu Yükümlülüğü:** **{res['toplam_borclu_yukumlulugu']:,.2f} TL**")
            return
        print("=" * 65)
        print("      İİK m. 67 & 68/a %20 İCRA İNKAR TAZMİNATI HESABI")
        print("=" * 65)
        print(f"Takipteki Asıl Alacak      : {res['asil_alacak']:,.2f} TL")
        print(f"Borçlunun İtiraz Ettiği    : {res['itiraz_edilen_tutar']:,.2f} TL")
        print(f"Kabul Edilen Kısım         : {res['kabul_edilen_tutar']:,.2f} TL")
        print(f"%%{int(res['tazminat_orani']*100)} İcra İnkar Tazminatı   : {res['icra_inkar_tazminati']:,.2f} TL")
        print(f"İtiraz Kaldırma Vekalet    : {res['vekalet_ucreti']:,.2f} TL")
        print(f"Harç ve Yargılama Gideri   : {res['masraf']:,.2f} TL")
        print("-" * 65)
        print(f"TOPLAM BORÇLU YÜKÜMLÜLÜĞÜ  : {res['toplam_borclu_yukumlulugu']:,.2f} TL")
        print("=" * 65)

    elif args.command == "icra":
        res = calculate_icra_kapak(args.alacak, args.faiz, args.masraf, args.year)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
            return
        if args.markdown:
            print(f"# İcra Dosya Kapak Raporu\n\n- **Asıl Alacak:** {res['asil_alacak']:,.2f} TL\n- **İcra Vekalet:** {res['icra_vekalet_ucreti']:,.2f} TL\n- **Tahsil Harcı:** {res['tahsil_harci']:,.2f} TL\n- **Kapak Bakiyesi:** **{res['dosya_kapak_bakiyesi']:,.2f} TL**")
            return
        print("=" * 65)
        print("        İCRA DOSYA KAPAK HESAP ÇIKTISI v2.0")
        print("=" * 65)
        print(f"Asıl Alacak          : {res['asil_alacak']:,.2f} TL")
        print(f"İşlemiş Faiz         : {res['faiz']:,.2f} TL")
        print(f"Takip Masrafları     : {res['masraf']:,.2f} TL")
        print(f"İcra Vekalet Ücreti  : {res['icra_vekalet_ucreti']:,.2f} TL")
        print(f"Tahsil Harcı (%9.10) : {res['tahsil_harci']:,.2f} TL")
        print(f"Cezaevi Fonu (%2)    : {res['cezaevi_harci']:,.2f} TL")
        print("-" * 65)
        print(f"DOSYA KAPAK BAKİYESİ : {res['dosya_kapak_bakiyesi']:,.2f} TL")
        print("=" * 65)

    elif args.command == "arabuluculuk":
        res = calculate_mediation_fee(args.tutar)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
            return
        print("=" * 65)
        print("     ARABULUCULUK ASGARİ ÜCRET HESAP TABLOSU v2.0")
        print("=" * 65)
        print(f"Anlaşılan Bedel      : {res['anlasilan_tutar']:,.2f} TL")
        print(f"Net Arabuluculuk     : {res['net_arabuluculuk_ucreti']:,.2f} TL")
        print(f"KDV                  : {res['kdv_tutari']:,.2f} TL")
        print(f"TOPLAM ÜCRET         : {res['toplam_ucret']:,.2f} TL")
        print("=" * 65)

    elif args.command == "faiz":
        res = calculate_yasal_faiz(args.tutar, args.gun, args.oran)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
            return
        if args.markdown:
            print(f"# Yasal Faiz Hesap Raporu\n\n- **Asıl Alacak:** {res['asil_alacak']:,.2f} TL\n- **Gün:** {res['gun_sayisi']}\n- **Yıllık Faiz:** %{res['yillik_faiz_orani']*100:.2f}\n- **İşlemiş Faiz:** {res['faiz_tutari']:,.2f} TL\n- **Toplam Alacak:** **{res['toplam_alacak']:,.2f} TL**")
            return
        print("=" * 65)
        print("        YASAL FAİZ VE TEMERRÜT FAİZİ HESAP TABLOSU")
        print("=" * 65)
        print(f"Asıl Alacak Tutarı   : {res['asil_alacak']:,.2f} TL")
        print(f"İşlemiş Gün Sayısı   : {res['gun_sayisi']} gün")
        print(f"Uygulanan Faiz Oranı : %{res['yillik_faiz_orani']*100:.2f}")
        print(f"Hesaplanan Faiz      : +{res['faiz_tutari']:,.2f} TL")
        print("-" * 65)
        print(f"TOPLAM ALACAK TUTARI : {res['toplam_alacak']:,.2f} TL")
        print("=" * 65)


if __name__ == "__main__":
    main()
