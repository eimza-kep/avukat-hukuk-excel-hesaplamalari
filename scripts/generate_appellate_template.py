import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Kanun Yolu & Harç Hesaplayıcı"

# Ensure grid lines are visible
ws.views.sheetView[0].showGridLines = True

# Colors & Fonts
header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
sub_fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
highlight_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
result_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")

font_title = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=11, bold=True, color="1E293B")
font_regular = Font(name="Calibri", size=11, color="334155")
font_result = Font(name="Calibri", size=12, bold=True, color="15803D")

thin_border = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

# Title Row
ws.merge_cells("A1:E1")
title_cell = ws["A1"]
title_cell.value = "HMK & İİK KANUN YOLU (İSTİNAF / TEMYİZ) VE DAVA HARÇLARI HESAPLAYICI (2026)"
title_cell.fill = header_fill
title_cell.font = font_title
title_cell.alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 36

# Section 1: Girdi Parametreleri ve Parasal Kesinlik Sınırları
ws["A3"] = "Dava Değeri ve Yasal Kesinlik Eşikleri"
ws["A3"].font = font_bold
ws["A3"].fill = sub_fill
ws.merge_cells("A3:B3")

inputs = [
    ("A4", "Dava / Takip Değeri (TL):", "B4", 150000.00),
    ("A5", "HMK İstinaf Kesinlik Sınırı (m. 341):", "B5", 58520.00),
    ("A6", "HMK Temyiz Kesinlik Sınırı (m. 362):", "B6", 783760.00),
    ("A7", "HMK Senetle İspat Sınırı (m. 200):", "B7", 48580.00),
    ("A8", "İİK İstinaf Sınırı (İcra m. 363):", "B8", 136930.00),
    ("A9", "İİK Temyiz Sınırı (İcra m. 364):", "B9", 913380.00),
    ("A10", "HMK Duruşma İsteme Sınırı (m. 369):", "B10", 1175650.00),
]

for label_pos, label_val, val_pos, val in inputs:
    c_lbl = ws[label_pos]
    c_lbl.value = label_val
    c_lbl.font = font_regular
    c_lbl.border = thin_border
    
    c_val = ws[val_pos]
    c_val.value = val
    c_val.font = font_bold
    c_val.border = thin_border
    if val_pos == "B4":
        c_val.fill = highlight_fill
    if isinstance(val, (int, float)):
        c_val.number_format = "#,##0.00 TL"

# Section 2: HMK / İİK Kanun Yolu Durumu ve Dava Açılış Masrafları
ws["D3"] = "Kanun Yolu Durumu ve Peşin Harçlar"
ws["D3"].font = font_bold
ws["D3"].fill = sub_fill
ws.merge_cells("D3:E3")

outputs = [
    ("D4", "HMK İstinaf Kanun Yolu Durumu:", "E4", '=IF(B4<=B5,"KESİN (İstinafa Kapalı)","AÇIK (BAM İstinaf)"),'),  # will adjust formula
    ("D5", "HMK Temyiz Kanun Yolu Durumu:", "E5", '=IF(B4<=B6,"KESİN (Temyize Kapalı)","AÇIK (Yargıtay Temyiz)"),'),
    ("D6", "HMK m. 200 Senetle İspat Durumu:", "E6", '=IF(B4>B7,"Senet Zorunlu (Tanık Dinlenemez)","Tanıkla İspat Caiz"),'),
    ("D7", "Nispi Karar ve İlam Harcı (%6.831):", "E7", "=ROUND(B4*0.06831, 2)"),
    ("D8", "Peşin Nispi Harç (1/4 Oranında):", "E8", "=ROUND(E7/4, 2)"),
    ("D9", "Başvuru Harcı + Vekalet Pulu:", "E9", 764.00),
    ("D10", "HMK m. 120 Gider Avansı (2 Taraf):", "E10", 1850.00),
    ("D11", "TOPLAM DAVA AÇILIŞ MASRAFI (TL):", "E11", "=E8+E9+E10")
]

# Correct formulas without trailing syntax
outputs = [
    ("D4", "HMK İstinaf Kanun Yolu Durumu:", "E4", '=IF(B4<=B5,"KESİN (İstinafa Kapalı)","AÇIK (BAM İstinaf)")'),
    ("D5", "HMK Temyiz Kanun Yolu Durumu:", "E5", '=IF(B4<=B6,"KESİN (Temyize Kapalı)","AÇIK (Yargıtay Temyiz)")'),
    ("D6", "HMK m. 200 Senetle İspat Durumu:", "E6", '=IF(B4>B7,"Senet Zorunlu (Tanık Dinlenemez)","Tanıkla İspat Caiz")'),
    ("D7", "Nispi Karar ve İlam Harcı (%6.831):", "E7", "=ROUND(B4*0.06831, 2)"),
    ("D8", "Peşin Nispi Harç (1/4 Oranında):", "E8", "=ROUND(E7/4, 2)"),
    ("D9", "Başvuru Harcı + Vekalet Pulu:", "E9", 764.00),
    ("D10", "HMK m. 120 Gider Avansı (2 Taraf):", "E10", 1850.00),
    ("D11", "TOPLAM DAVA AÇILIŞ MASRAFI (TL):", "E11", "=E8+E9+E10")
]

for label_pos, label_val, val_pos, val in outputs:
    c_lbl = ws[label_pos]
    c_lbl.value = label_val
    c_lbl.font = font_regular
    c_lbl.border = thin_border
    
    c_val = ws[val_pos]
    c_val.value = val
    c_val.font = font_result if val_pos == "E11" else font_bold
    c_val.border = thin_border
    if val_pos == "E11":
        c_val.fill = result_fill
    if isinstance(val, (int, float)) or (isinstance(val, str) and (val.startswith("=ROUND") or val.startswith("=E8"))):
        c_val.number_format = "#,##0.00 TL"

# Note footer
ws["A13"] = "Mevzuat ve Hukuki Dayanak Notları:"
ws["A13"].font = font_bold
ws["A14"] = "1) 6100 sayılı HMK m. 200, m. 341 ve m. 362 ile 2004 sayılı İİK m. 363 ve m. 364 uyarınca parasal sınırlar her takvim yılı başında yeniden değerleme oranında artırılmaktadır."
ws["A14"].font = font_regular
ws.merge_cells("A14:E14")

ws["A15"] = "2) 492 sayılı Harçlar Kanunu uyarınca nispi harca tabi davalarda, nispi karar ve ilam harcının (binde 68,31) 1/4'ü dava açılırken peşin olarak tahsil edilir."
ws["A15"].font = font_regular
ws.merge_cells("A15:E15")

# Auto-adjust column widths
ws.column_dimensions["A"].width = 40
ws.column_dimensions["B"].width = 24
ws.column_dimensions["C"].width = 4
ws.column_dimensions["D"].width = 40
ws.column_dimensions["E"].width = 28

output_filename = "16_kanun_yolu_istinaf_temyiz_ve_kesinlik_sinirlari_hesaplayici.xlsx"
wb.save(output_filename)
print(f"Başarıyla kaydedildi: {output_filename}")
