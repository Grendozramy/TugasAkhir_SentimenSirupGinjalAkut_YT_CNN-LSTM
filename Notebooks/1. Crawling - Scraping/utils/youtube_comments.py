# Impor modul yang diperlukan: csv untuk menulis file CSV, dan datetime untuk mengambil tanggal hari ini
import csv
from datetime import datetime as dt

# Inisialisasi list kosong untuk menyimpan komentar
comments = []

# Dapatkan tanggal hari ini dalam format 'dd-mm-yyyy'
today = dt.today().strftime('%d-%m-%Y')

# Fungsi untuk memproses komentar dan opsional menyimpannya ke file CSV
def process_comments(response_items, csv_output=False):
    # Loop melalui setiap item dalam response_items
    for res in response_items:
        # Buat kamus kosong untuk menyimpan detail setiap komentar
        comment = {}
        # Simpan snippet dari komentar tingkat atas
        comment['snippet'] = res['snippet']['topLevelComment']['snippet']
        # Tidak ada parentId untuk komentar tingkat atas, jadi atur sebagai None
        comment['snippet']['parentId'] = None
        # Simpan ID dari komentar tingkat atas
        comment['snippet']['commentId'] = res['snippet']['topLevelComment']['id']
        # Tambahkan kamus 'snippet' ke list 'comments'
        comments.append(comment['snippet'])

    # Jika csv_output adalah True, simpan komentar ke file CSV
    if csv_output:
        make_csv(comments)

    # Cetak jumlah komentar yang diproses
    print(f'Finished processing {len(comments)} comments.')
    # Kembalikan list 'comments'
    return comments

# Fungsi untuk menyimpan komentar ke file CSV
def make_csv(comments, channelID=None):
    # Dapatkan kunci dari kamus pertama dalam 'comments' untuk digunakan sebagai header CSV
    header = comments[0].keys()

    # Atur nama file berdasarkan channelID dan tanggal hari ini
    if channelID:
        filename = f'comments_{channelID}_{today}.csv'
    else:
        filename = f'comments_{today}.csv'

    # Tulis komentar ke file CSV
    with open(filename, 'w', encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header, extrasaction='ignore')
        writer.writeheader()  # Tulis header
        writer.writerows(comments)  # Tulis baris komentar
