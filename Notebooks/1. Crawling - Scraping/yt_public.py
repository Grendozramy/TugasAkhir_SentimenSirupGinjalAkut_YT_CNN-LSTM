# Mengimpor modul yang diperlukan
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from iteration_utilities import unique_everseen

# Mengimpor fungsi process_comments dan make_csv yang telah dimodifikasi
from utils.youtube_comments import process_comments, make_csv

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Mengambil API Key dari variabel lingkungan
API_KEY = os.getenv("API_KEY")

# Membangun layanan API YouTube v3
youtube = build("youtube", "v3", developerKey=API_KEY)

def comment_threads(videoId, to_csv=True):
    comments_list = []

    # Mengambil komentar menggunakan API YouTube
    request = youtube.commentThreads().list(
        part='id,snippet',
        videoId=videoId,
    )
    # Menjalankan permintaan dan mendapatkan respons
    response = request.execute()

    # Memproses komentar dalam respons dan menambahkannya ke dalam daftar
    comments_list.extend(process_comments(response['items'], csv_output=False))

    # Melanjutkan pengambilan komentar jika nextPageToken ada
    while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
            part='id,snippet',
            videoId=videoId,
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))

    # Menghapus duplikat dari daftar komentar
    comments_list = list(unique_everseen(comments_list))

    print(f"Selesai mengambil komentar untuk {videoId}. {len(comments_list)} komentar ditemukan.")

    # Menyimpan komentar ke file CSV jika to_csv adalah True
    if to_csv:
        make_csv(comments_list, videoId)

    # Mengembalikan daftar komentar
    return comments_list

if __name__ == '__main__':
    # Mendefinisikan ID dari video untuk mengambil komentar
    videoId = 'yiffzzl7EFY'
    # Mengambil komentar dan mencetaknya
    response = comment_threads(videoId)
    print(response)

