import json
import os
import urllib.request
import urllib.parse
from pathlib import Path

# Tạo folder
paper_dir = Path('paper')
paper_dir.mkdir(exist_ok=True)

# Đọc references.json
ref_path = Path('references.json')
if not ref_path.exists():
    print('Không tìm thấy references.json')
    exit()

with open(ref_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Tìm thấy {len(data.get('papers', []))} paper. Đang tiến hành tải...")

headers = {'User-Agent': 'Mozilla/5.0'}

for p in data.get('papers', []):
    doi = p.get('doi')
    pid = p.get('id', 'UNKNOWN')
    title = p.get('title', 'Unknown Title').replace('/', '_').replace(':', '_').replace('?', '_')[:50]
    
    if not doi:
        print(f"[-] {pid} không có DOI, bỏ qua.")
        continue
        
    print(f"[*] Đang kiểm tra Open Access cho {pid} (DOI: {doi})...")
    try:
        # Check Unpaywall API cho Open Access PDF
        upw_url = f"https://api.unpaywall.org/v2/{doi}?email=student@fpt.edu.vn"
        req = urllib.request.Request(upw_url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            upw_data = json.loads(resp.read().decode('utf-8'))
            
        pdf_url = None
        if upw_data.get('best_oa_location'):
            pdf_url = upw_data['best_oa_location'].get('url_for_pdf')
            
        if pdf_url:
            print(f"  -> Đã tìm thấy PDF mở: {pdf_url}")
            pdf_path = paper_dir / f"{pid} - {title}.pdf"
            
            # Fetch PDF
            try:
                pdf_req = urllib.request.Request(pdf_url, headers=headers)
                with urllib.request.urlopen(pdf_req, timeout=30) as pdf_resp:
                    with open(pdf_path, 'wb') as pdf_file:
                        pdf_file.write(pdf_resp.read())
                print(f"  [+] Tải thành công: {pdf_path.name}")
            except Exception as e_pdf:
                print(f"  [x] Lỗi khi tải PDF: {e_pdf}. Đang tạo file text link thay thế.")
                pdf_url = None # Fallback to txt
        
        if not pdf_url:
            print(f"  [!] Paper này bị khóa (Paywall) hoặc lỗi tải. Đang tạo file meta...")
            txt_path = paper_dir / f"{pid} - {title}.txt"
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(f"Title: {p.get('title')}\n")
                txt_file.write(f"Authors: {', '.join(p.get('authors', []))}\n")
                txt_file.write(f"DOI: {doi}\n")
                txt_file.write(f"Link: https://doi.org/{doi}\n")
                txt_file.write(f"Tình trạng: Paper này không có bản Open Access (PDF miễn phí) hoặc link PDF không khả dụng.\n")
            print(f"  [+] Đã lưu thông tin: {txt_path.name}")
            
    except Exception as e:
        print(f"  [x] Lỗi khi xử lý {pid}: {e}")

print("\nHoàn tất!")
