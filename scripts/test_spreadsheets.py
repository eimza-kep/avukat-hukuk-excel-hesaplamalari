#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_spreadsheets.py
--------------------
Repodaki tüm .xlsx Excel dosyalarını açar, şablon yapısını,
başlıkları ve formül içeriklerini denetler.
"""

import os
import sys
import glob
import openpyxl

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def test_repo_spreadsheets():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    xlsx_files = sorted(glob.glob(os.path.join(base_dir, "*.xlsx")))
    
    print(f"📊 Toplam test edilecek Excel dosyası: {len(xlsx_files)}")
    if len(xlsx_files) == 0:
        print("❌ HATA: Dizinde hiç .xlsx dosyası bulunamadı!")
        return 1

    errors = []
    for fp in xlsx_files:
        fn = os.path.basename(fp)
        try:
            wb = openpyxl.load_workbook(fp, data_only=False)
            sheet_names = wb.sheetnames
            if len(sheet_names) == 0:
                errors.append(f"[{fn}] Çalışma sayfası bulunamadı.")
                continue

            ws = wb.active
            if ws.max_row < 4:
                errors.append(f"[{fn}] Yetersiz satır sayısı ({ws.max_row}).")
            if ws.max_column < 3:
                errors.append(f"[{fn}] Yetersiz sütun sayısı ({ws.max_column}).")

            formulas = []
            for row in ws.iter_rows(values_only=True):
                for cell in row:
                    if isinstance(cell, str) and cell.startswith("="):
                        formulas.append(cell)

            if len(formulas) == 0:
                errors.append(f"[{fn}] Dosya içinde hiç Excel formülü bulunamadı!")

            print(f"  ✓ {fn} - Sayfa: '{ws.title}', Satır: {ws.max_row}, Sütun: {ws.max_column}, Formül: {len(formulas)}")
        except Exception as e:
            errors.append(f"[{fn}] Dosya açılamadı: {e}")

    if errors:
        print("\n⚠️ Doğrulama Hataları:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"\n🎉 {len(xlsx_files)} adet Excel dosyasının tamamı başarıyla doğrulandı!")
    return 0

if __name__ == "__main__":
    sys.exit(test_repo_spreadsheets())
