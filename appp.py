from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    # --- PROSES DATA ANALYSIS ---
    df = pd.read_csv('jualan.csv')
    
    # 1. Kira jumlah jualan (Kuantiti x Harga)
    df['Jumlah_Jualan'] = df['Kuantiti'] * df['Harga_Sebunit']
    
    # 2. Cari jumlah besar (Total Revenue)
    total_revenue = df['Jumlah_Jualan'].sum()
    
    # 3. Cari produk paling laku
    produk_top = df.groupby('Produk')['Kuantiti'].sum().idxmax()
    
    # Tukar data jadi HTML table untuk paparan web
    jadual_html = df.to_html(classes='table table-striped', index=False)

    # --- PAPARAN UI ---
    return render_template_string(f"""
    <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        </head>
        <body class="container mt-5">
            <h1 class="mb-4">📊 Laporan Analisis Jualan</h1>
            
            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="card p-3 bg-primary text-white">
                        <h3>Total Pendapatan: RM {total_revenue}</h3>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card p-3 bg-success text-white">
                        <h3>Produk Top: {produk_top}</h3>
                    </div>
                </div>
            </div>

            <h3>Data Mentah (Data Entry):</h3>
            {jadual_html}
        </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True)