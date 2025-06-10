import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt
import numpy as np

# --- Fungsi Inti Kalkulasi ---
def hitung_properti_persegi(sisi: float) -> tuple[float, float]:
    """
    Menghitung keliling dan luas persegi.

    Args:
        sisi (float): Panjang sisi persegi.

    Returns:
        tuple[float, float]: Tuple berisi (keliling, luas) persegi.
    """
    if sisi <= 0:
        # Menangani input sisi yang tidak valid
        raise ValueError("Panjang sisi harus bernilai positif.")
    keliling = 4 * sisi
    luas = sisi * sisi
    return keliling, luas

# --- Fungsi Visualisasi ---
def gambar_persegi(sisi: float, ax: plt.Axes):
    """
    Menggambar persegi pada objek axes Matplotlib.

    Args:
        sisi (float): Panjang sisi persegi.
        ax (plt.Axes): Objek axes Matplotlib untuk menggambar.
    """
    ax.clear() # Membersihkan plot sebelumnya agar tidak menumpuk

    # Koordinat sudut persegi (misal, dimulai dari (0,0))
    x_coords = [0, sisi, sisi, 0, 0]
    y_coords = [0, 0, sisi, sisi, 0]

    # Menggambar sisi-sisi persegi
    ax.plot(x_coords, y_coords, 'b-', linewidth=2) # 'b-' untuk garis biru solid

    # Menambahkan label panjang sisi
    ax.text(sisi / 2, -0.1 * sisi, f'{sisi:.1f} cm', ha='center', va='top', color='black', fontsize=10)
    ax.text(sisi + 0.1 * sisi, sisi / 2, f'{sisi:.1f} cm', ha='left', va='center', color='black', fontsize=10, rotation=90)

    # Pengaturan tampilan plot
    margin = sisi * 0.2 # Menambahkan margin di sekitar persegi
    ax.set_xlim(-margin, sisi + margin)
    ax.set_ylim(-margin, sisi + margin)
    ax.set_aspect('equal', adjustable='box') # Memastikan skala x dan y sama agar persegi terlihat proporsional
    ax.set_title('Visualisasi Persegi', fontsize=14)
    ax.set_xlabel('X (cm)', fontsize=10)
    ax.set_ylabel('Y (cm)', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.6) # Menambahkan grid
    ax.tick_params(axis='both', which='major', labelsize=8) # Ukuran font untuk tick label

# --- Fungsi Callback untuk Interaksi Widget ---
def update_lab(change):
    """
    Fungsi callback yang dipanggil saat nilai slider berubah.
    Memperbarui perhitungan dan visualisasi.
    """
    with output_area:
        clear_output(wait=True) # Membersihkan output sebelumnya
        sisi = sisi_slider.value # Ambil nilai terbaru dari slider

        try:
            keliling, luas = hitung_properti_persegi(sisi)

            # Tampilkan Hasil Perhitungan
            print("--- **Hasil Perhitungan** ---")
            print(f"**Panjang Sisi:** {sisi:.1f} cm")
            print(f"**Keliling Persegi:** {keliling:.1f} cm")
            print(f"**Luas Persegi:** {luas:.1f} cm²")

            # Tampilkan Visualisasi
            print("\n--- **Visualisasi Persegi** ---")
            gambar_persegi(sisi, ax_plot) # Menggambar pada axes yang sudah ada
            fig_plot.canvas.draw_idle() # Memperbarui canvas Matplotlib
            display(fig_plot.canvas) # Tampilkan canvas Matplotlib
            plt.close(fig_plot) # Tutup figure agar tidak menumpuk di output Colab

        except ValueError as e:
            # Menangani error jika sisi tidak valid
            print(f"**Error:** {e}")
            ax_plot.clear()
            ax_plot.set_title("Input Sisi Tidak Valid", fontsize=14, color='red')
            ax_plot.text(0.5, 0.5, "Masukkan panjang sisi positif.", ha='center', va='center', transform=ax_plot.transAxes)
            ax_plot.set_xlim(0,1); ax_plot.set_ylim(0,1)
            ax_plot.set_aspect('equal')
            display(fig_plot.canvas)
            plt.close(fig_plot)

# --- Pengaturan Antarmuka Pengguna (Widgets) ---
sisi_slider = widgets.FloatSlider(
    value=5.0,  # Nilai awal slider
    min=0.1,    # Nilai minimum (hindari nol atau negatif)
    max=20.0,   # Nilai maksimum
    step=0.1,   # Langkah perubahan setiap geseran
    description='Panjang Sisi (cm):',
    orientation='horizontal',
    readout=True, # Menampilkan nilai saat ini
    readout_format='.1f', # Format tampilan nilai (satu desimal)
    continuous_update=True # Memperbarui output secara real-time saat digeser
)

# Area output untuk menampilkan teks hasil perhitungan dan plot Matplotlib
output_area = widgets.Output()

# Inisialisasi figure dan axes Matplotlib di awal.
# Ini lebih efisien daripada membuat figure baru setiap kali.
fig_plot, ax_plot = plt.subplots(figsize=(5, 5))
plt.close(fig_plot) # Tutup figure ini agar tidak langsung ditampilkan kosong

# Menghubungkan slider dengan fungsi update_lab
sisi_slider.observe(update_lab, names='value')

# --- Tampilan Lab ---
print("Selamat datang di **Virtual Lab Kalkulator Persegi**!")
print("Ini adalah alat interaktif untuk menghitung dan memvisualisasikan properti persegi.")
print("Geser slider di bawah untuk mengatur panjang sisi.")

# Menampilkan slider dan area output
display(sisi_slider, output_area)

# --- Inisialisasi Tampilan Awal ---
# Panggil fungsi update_lab sekali saat pertama kali dijalankan
# agar hasil default slider langsung ditampilkan.
update_lab({'new': sisi_slider.value})
