import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "İcra İnkar Tazminatı"

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
title_cell.value = "İCRA VE İFLAS KANUNU (İİK m. 67 & 68/a) %20 İCRA İNKAR TAZMİNATI HESAPLAYICI"
title_cell.fill = header_fill
title_cell.font = font_title
title_cell.alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 36

# Section 1: Girdi Parametreleri
ws["A3"] = "İcra Dosyası ve Takip Bilgileri"
ws["A3"].font = font_bold
ws["A3"].fill = sub_fill
ws.merge_cells("A3:B3")

inputs = [
    ("A4", "Takip / İcra Dosya No:", "B4", "2026/10452 Esas"),
    ("A5", "Takipteki Asıl Alacak Tutarı (TL):", "B5", 150000.00),
    ("A6", "Borçlunun İtiraz Ettiği Tutar (TL):", "B6", 120000.00),
    ("A7", "Kabul Edilen / İtiraz Edilmeyen Tutar (TL):", "B7", "=B5-B6"),
    ("A8", "İşlemiş Temerrüt Faizi (TL):", "B8", 14500.00),
    ("A9", "İcra Takip Masrafları (TL):", "B9", 1850.00),
    ("A10", "Yasal İcra İnkar Tazminatı Oranı (%):", "B10", 0.20)
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
    c_val.fill = highlight_fill if "B5" in val_pos or "B6" in val_pos else PatternFill(fill_type=None)
    if isinstance(val, (int, float)) or (isinstance(val, str) and val.startswith("=")):
        if "B10" in val_pos:
            c_val.number_format = "0.0%"
        else:
            c_val.number_format = "#,##0.00 TL"

# Section 2: Hesaplama Sonuçları
ws["D3"] = "Hükmedilen İtirazın İptali & Kaldırılması Dökümü"
ws["D3"].font = font_bold
ws["D3"].fill = sub_fill
ws.merge_cells("D3:E3")

outputs = [
    ("D4", "Tazminat Matrahı (İtiraz Edilen Kısım):", "E4", "=B6"),
    ("D5", "%20 İcra İnkar Tazminatı Tutarı:", "E5", "=E4*B10"),
    ("D6", "İtirazın Kaldırılması Vekalet Ücreti:", "E6", "=MAX(12000, MIN(E4, E4*0.16))"),
    ("D7", "Yargılama ve İcra Başvuru Harcı:", "E7", 650.00),
    ("D8", "İtiraz Edilmeyen Kesinleşen Kısım:", "E8", "=B7"),
    ("D9", "TOPLAM BORÇLU YÜKÜMLÜLÜĞÜ (TL):", "E9", "=B5+B8+B9+E5+E6+E7")
]

for label_pos, label_val, val_pos, val in outputs:
    c_lbl = ws[label_pos]
    c_lbl.value = label_val
    c_lbl.font = font_regular
    c_lbl.border = thin_border
    
    c_val = ws[val_pos]
    c_val.value = val
    c_val.font = font_result if "E9" in val_pos else font_bold
    c_val.border = thin_border
    if "E9" in val_pos:
        c_val.fill = result_fill
    if isinstance(val, (int, float)) or (isinstance(val, str) and val.startswith("=")):
        c_val.number_format = "#,##0.00 TL"

# Note footer
ws["A12"] = "Yasal Açıklama:"
ws["A12"].font = font_bold
ws["A13"] = "2004 sayılı İİK m. 67/2 ve m. 68/a uyarınca, borçlunun itirazının haksızlığına karar verilmesi durumunda, alacaklının talebiyle itiraz edilen veya hükmolunan tutarın asgari %20'si oranında icra inkar tazminatına hükmedilir."
ws["A13"].font = font_regular
ws.merge_cells("A13:E13")

# Auto-adjust column widths
ws.column_dimensions["A"].width = 38
ws.column_dimensions["B"].width = 24
ws.column_dimensions["C"].width = 4
ws.column_dimensions["D"].width = 38
ws.column_dimensions["E"].width = 24

wb.save("15_itirazin_iptali_ve_icra_inkar_tazminati_hesaplayici.xlsx")
print("Saved 15_itirazin_iptali_ve_icra_inkar_tazminati_hesaplayici.xlsx")
