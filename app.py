import pandas as pd
import os
import warnings # <-- Import modul warnings

# Nonaktifkan FutureWarning dari Pandas secara spesifik
warnings.filterwarnings('ignore', category=FutureWarning) 

# --- Inisialisasi Data dan Konfigurasi ---
output_filename = 'pembayaran_fotografi.csv'

# Inisialisasi DataFrame
def inisialisasi_data(filename):
    """Memuat data dari file CSV atau membuat DataFrame baru."""
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)
            df['Jumlah'] = pd.to_numeric(df['Jumlah'], errors='coerce')
            df.dropna(subset=['Jumlah'], inplace=True)
            print(f"Data dimuat dari '{filename}'.")
            return df
        except Exception as e:
            print(f"Gagal memuat file CSV: {e}. Membuat DataFrame baru.")
            return pd.DataFrame(columns=['Nama Siswa', 'Tanggal Pembayaran', 'Jumlah'])
    else:
        print("Membuat DataFrame pembayaran baru.")
        return pd.DataFrame(columns=['Nama Siswa', 'Tanggal Pembayaran', 'Jumlah'])

# Inisialisasi DataFrame saat program mulai
df_payments = inisialisasi_data(output_filename)

# --- Fungsi-fungsi Program ---

def tambah_pembayaran(df, nama, tanggal, jumlah_str):
    """Menambahkan pembayaran baru ke DataFrame setelah memvalidasi jumlah."""
    try:
        # 1. Konversi jumlah ke tipe float
        jumlah = float(jumlah_str.replace('.', '').replace(',', ''))
        
        # 2. Buat baris data baru sebagai Dictionary
        data_baru = {
            'Nama Siswa': nama, 
            'Tanggal Pembayaran': tanggal, 
            'Jumlah': jumlah
        }
        
        # 3. Gunakan .loc untuk menambahkan data baru, yang merupakan cara yang disarankan (tanpa FutureWarning)
        # Ambil indeks berikutnya
        next_index = len(df)
        df.loc[next_index] = data_baru
        
        # Mengembalikan df yang sudah diperbarui
        print(f"\n✅ Pembayaran untuk **{nama}** sebesar **Rp {jumlah:,.2f}** berhasil ditambahkan.")
        return df
    except ValueError:
        print("\n❌ Error: Jumlah Pembayaran harus berupa angka yang valid.")
        return df

def tampilkan_pembayaran(df):
    """Menampilkan semua pembayaran dan menghitung totalnya."""
    if df.empty:
        print("\nBelum ada data pembayaran.")
        return

    print("\n## 📋 Daftar Semua Pembayaran Fotografi")
    df_display = df.copy()
    df_display['Jumlah'] = df_display['Jumlah'].apply(lambda x: f"Rp {x:,.2f}")
    
    print(df_display.to_string(index=False))

    total = df['Jumlah'].sum()
    print("\n" + "="*50)
    print(f"💰 **TOTAL KESELURUHAN PEMBAYARAN: Rp {total:,.2f}**")
    print("="*50)

def simpan_data(df, filename):
    """Menyimpan DataFrame ke file CSV."""
    df.to_csv(filename, index=False)
    print(f"\n💾 Data pembayaran berhasil disimpan ke '{filename}'.")

# --- Program Utama ---
while True:
    print("\n--- Menu Pembayaran Fotografi ---")
    print("1. Tambah Pembayaran Baru")
    print("2. Tampilkan Semua Pembayaran (dan Total)")
    print("3. Simpan dan Keluar")

    pilihan = input("Masukkan pilihan Anda (1/2/3): ").strip()

    if pilihan == '1':
        print("\n--- Tambah Pembayaran ---")
        nama = input("Masukkan Nama Siswa: ").strip()
        if not nama:
            print("Nama Siswa tidak boleh kosong.")
            continue
            
        tanggal = input("Masukkan Tanggal Pembayaran (YYYY-MM-DD): ").strip()
        jumlah_str = input("Masukkan Jumlah Pembayaran (cth: 150000 atau 150.000): ").strip()
        
        df_payments = tambah_pembayaran(df_payments, nama, tanggal, jumlah_str)
        
    elif pilihan == '2':
        tampilkan_pembayaran(df_payments)
        
    elif pilihan == '3':
        simpan_data(df_payments, output_filename)
        print("Terima kasih! Program berakhir.")
        break
        
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
