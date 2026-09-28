#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hukuk ve Avukatlık Hesaplama CLI Motoru v1.2
============================================
AAÜT Nispi Vekalet Ücreti, İcra Dosya Kapak Hesabı ve Arabuluculuk
Asgari Ücret Tarifesi (AAÜT) Hesaplayıcı Motoru.

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

def calculate_aaut_fee(alacak_tutari: float, kdv_orani: float = 0.20) -> dict:
    """
    AAÜT (Avukatlık Asgari Ücret Tarifesi) nispi vekâlet ücretini kademeli olarak hesaplar:
    - İlk 100.000 TL için: %16
    - Sonraki 100.000 TL için: %15
    - Sonraki 200.000 TL için: %14
    - Sonraki 500.000 TL için: %11
    - Sonraki 1.000.000 TL için: %8
    - 1.900.000 TL üzeri için: %5
    """
    kademeler = [
        (100000, 0.16),
        (100000, 0.15),
        (200000, 0.14),
        (500000, 0.11),
        (1000000, 0.08),
        (float('inf'), 0.05)
    ]

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

    kdv_tutari = vekalet_ucreti * kdv_orani
    toplam = vekalet_ucreti + kdv_tutari

    return {
        "alacak_tutari": alacak_tutari,
        "net_vekalet_ucreti": round(vekalet_ucreti, 2),
        "kdv_orani": kdv_orani,
        "kdv_tutari": round(kdv_tutari, 2),
        "toplam_ucret": round(toplam, 2),
        "dilimler": dilimler
    }

def calculate_icra_kapak(asil_alacak: float, faiz: float = 0.0, masraf: float = 0.0) -> dict:
    """
    İcra dairesi dosya kapak hesabı:
    - Asıl Alacak + İşlemiş Faiz + Masraflar
    - İcra Vekâlet Ücreti (Kademeli AAÜT)
    - Tahsil Harcı (%9.10 - Hacizli/Satışsız tahsilat)
    - Cezaevi Harcı (%2)
    """
    alacak_toplami = asil_alacak + faiz + masraf
    vekalet_res = calculate_aaut_fee(asil_alacak)
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
    6325 sayılı Kanun uyarınca Arabuluculuk Asgari Ücret Tarifesi (Nispi Ücret):
    - İlk 100.000 TL için: %6
    - Sonraki 160.000 TL için: %5
    - Sonraki 340.000 TL için: %4
    - Sonraki 500.000 TL için: %3
    - Sonraki 1.000.000 TL için: %2
    - Kalan tutar için: %1
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

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Hukuk ve Avukatlık Hesaplama Motoru v1.2")
    parser.add_argument("--json", action="store_true", help="JSON formatında çıktı ver")
    parser.add_argument("--markdown", action="store_true", help="Markdown formatında rapor üret")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # AAÜT
    p_aaut = subparsers.add_parser("aaut", help="AAÜT Nispi Vekalet Ücreti Hesapla")
    p_aaut.add_argument("tutar", type=float, help="Dava veya icra alacak tutarı (TL)")

    # İcra
    p_icra = subparsers.add_parser("icra", help="İcra Dosya Kapak Hesabı")
    p_icra.add_argument("alacak", type=float, help="Asıl alacak tutarı (TL)")
    p_icra.add_argument("--faiz", type=float, default=0.0, help="İşlemiş faiz tutarı")
    p_icra.add_argument("--masraf", type=float, default=0.0, help="Takip masrafları")

    # Arabuluculuk
    p_med = subparsers.add_parser("arabuluculuk", help="Arabuluculuk Asgari Ücreti Hesapla")
    p_med.add_argument("tutar", type=float, help="Uyuşmazlıkta anlaşılan bedel (TL)")

    args = parser.parse_args()

    if args.command == "aaut":
        res = calculate_aaut_fee(args.tutar)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
            return
        if args.markdown:
            print(f"# AAÜT Nispi Vekalet Ücreti Raporu\n\n- **Dava Değeri:** {res['alacak_tutari']:,.2f} TL\n- **Net Ücret:** {res['net_vekalet_ucreti']:,.2f} TL\n- **KDV:** {res['kdv_tutari']:,.2f} TL\n- **Toplam Vekalet Ücreti:** **{res['toplam_ucret']:,.2f} TL**")
            return
        print("=" * 60)
        print("      AAÜT NİSPİ VEKALET ÜCRETİ HESAP TABLOSU v1.2")
        print("=" * 60)
        print(f"Alacak / Dava Değeri : {res['alacak_tutari']:,.2f} TL")
        print(f"Net Vekalet Ücreti   : {res['net_vekalet_ucreti']:,.2f} TL")
        print(f"KDV (%{int(res['kdv_orani']*100)})              : {res['kdv_tutari']:,.2f} TL")
        print(f"TOPLAM VEKALET ÜCRETİ: {res['toplam_ucret']:,.2f} TL")
        print("=" * 60)

    elif args.command == "icra":
        res = calculate_icra_kapak(args.alacak, args.faiz, args.masraf)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
            return
        if args.markdown:
            print(f"# İcra Dosya Kapak Raporu\n\n- **Asıl Alacak:** {res['asil_alacak']:,.2f} TL\n- **İcra Vekalet:** {res['icra_vekalet_ucreti']:,.2f} TL\n- **Tahsil Harcı:** {res['tahsil_harci']:,.2f} TL\n- **Kapak Bakiyesi:** **{res['dosya_kapak_bakiyesi']:,.2f} TL**")
            return
        print("=" * 60)
        print("        İCRA DOSYA KAPAK HESAP ÇIKTISI v1.2")
        print("=" * 60)
        print(f"Asıl Alacak          : {res['asil_alacak']:,.2f} TL")
        print(f"İşlemiş Faiz         : {res['faiz']:,.2f} TL")
        print(f"Takip Masrafları     : {res['masraf']:,.2f} TL")
        print(f"İcra Vekalet Ücreti  : {res['icra_vekalet_ucreti']:,.2f} TL")
        print(f"Tahsil Harcı (%9.10) : {res['tahsil_harci']:,.2f} TL")
        print(f"Cezaevi Fonu (%2)    : {res['cezaevi_harci']:,.2f} TL")
        print("-" * 60)
        print(f"DOSYA KAPAK BAKİYESİ : {res['dosya_kapak_bakiyesi']:,.2f} TL")
        print("=" * 60)

    elif args.command == "arabuluculuk":
        res = calculate_mediation_fee(args.tutar)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
            return
        print("=" * 60)
        print("     ARABULUCULUK ASGARİ ÜCRET HESAP TABLOSU v1.2")
        print("=" * 60)
        print(f"Anlaşılan Bedel      : {res['anlasilan_tutar']:,.2f} TL")
        print(f"Net Arabuluculuk     : {res['net_arabuluculuk_ucreti']:,.2f} TL")
        print(f"KDV                  : {res['kdv_tutari']:,.2f} TL")
        print(f"TOPLAM ÜCRET         : {res['toplam_ucret']:,.2f} TL")
        print("=" * 60)

if __name__ == "__main__":
    main()
