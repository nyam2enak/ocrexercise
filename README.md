# OCR Exercise Project

Proyek ini adalah implementasi sistem OCR (Optical Character Recognition) untuk ekstraksi data dari berbagai format dokumen seperti PDF, gambar, dan dokumen invoice. Sistem ini menggunakan teknologi AI untuk mengenali teks dari dokumen dan mengkonversinya ke format DataFrame untuk analisis lebih lanjut.

## 📋 Fitur Utama

- **Multi-format Document Processing**: Mendukung PDF, gambar (JPG, PNG), dan dokumen invoice
- **Advanced OCR**: Menggunakan Tesseract OCR dengan preprocessing gambar
- **Data Extraction**: Ekstraksi data terstruktur dari dokumen invoice
- **Web Interface**: Interface web untuk upload dan processing dokumen
- **DataFrame Output**: Output dalam format pandas DataFrame untuk analisis
- **Confidence Scoring**: Sistem penilaian keakuratan OCR

## 🛠️ Tech Stack

### Core Libraries

- **Python 3.8+**
- **Flask**: Web framework untuk interface
- **pandas**: Data manipulation dan DataFrame
- **numpy**: Komputasi numerik
- **OpenCV**: Image processing
- **Pillow (PIL)**: Image manipulation
- **Tesseract OCR**: Engine OCR utama
- **pdf2image**: PDF to image conversion

### Dependencies

```
flask==2.3.3
pandas==2.0.3
numpy==1.24.3
opencv-python==4.8.0.76
Pillow==10.0.0
pytesseract==0.3.10
pdf2image==1.17.0
```

## 🚀 Quick Start

### Automated Setup (Recommended)

```bash
# Run setup script (macOS/Linux)
./setup.sh

# Or run manually
chmod +x setup.sh && ./setup.sh
```

### Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install system dependencies
# macOS
brew install tesseract poppler

# Ubuntu/Debian
sudo apt-get install tesseract-ocr poppler-utils

# 4. Run the application
python ocr_modul.py
```

## � Documentation

- **[README.md](README.md)**: Main documentation
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Contribution guidelines
- **[CHANGELOG.md](CHANGELOG.md)**: Version history and changes
- **[LICENSE](LICENSE)**: MIT License

## 📁 File Structure

```
ocrexercise/
├── 📄 README.md                 # Main documentation
├── 📄 CONTRIBUTING.md          # Contribution guidelines
├── 📄 CHANGELOG.md             # Version history
├── 📄 LICENSE                  # MIT License
├── 🔧 setup.sh                 # Automated setup script
├── 📋 requirements.txt         # Python dependencies
├── ⚙️  .env.example           # Environment configuration
├── 📝 .gitignore              # Git ignore rules
├── 🐍 ocr_exercise.ipynb      # Main Jupyter notebook
├── 🐍 ocr_exercise2.ipynb     # Advanced notebook
├── 🐍 ocr_modul.py           # Main OCR module
├── 🌐 templates/              # Flask HTML templates
│   ├── upload.html           # Upload interface
│   └── result.html           # Results display
├── 📤 uploads/               # Uploaded files directory
├── 📊 processed/            # Processed data directory
└── 📄 *.pdf                  # Sample documents
```

## 🎯 Cara Penggunaan

### 1. Menjalankan Jupyter Notebook

#### Option A: Via Jupyter Notebook

```bash
jupyter notebook ocr_exercise.ipynb
```

#### Option B: Via VS Code

1. Buka VS Code
2. Buka folder `ocrexercise`
3. Klik kanan pada `ocr_exercise.ipynb`
4. Pilih "Open with Jupyter"

### 2. Menjalankan Web Application (ocr_modul.py)

#### Step 1: Jalankan Server

```bash
python ocr_modul.py
```

#### Step 2: Akses Web Interface

Buka browser dan akses: `http://localhost:5000`

#### Step 3: Upload Document

1. Klik "Choose File" untuk memilih dokumen
2. Pilih format: PDF atau Image
3. Klik "Upload and Process"
4. Lihat hasil ekstraksi di halaman result

### 3. Menggunakan OCR Functions

```python
from ocr_modul import AdvancedOCRPipeline

# Inisialisasi pipeline
pipeline = AdvancedOCRPipeline()

# Process PDF
result = pipeline.process_document('sample-invoice.pdf')
print(result)

# Extract text dari PDF
text = pipeline.extract_text_from_pdf('sample-invoice.pdf')
print(text)
```

## 📊 Output Format

### DataFrame Structure

```python
# Main Invoice Data
main_df = pd.DataFrame({
    'Field': ['Invoice Number', 'Invoice Date', 'Customer', 'Total Amount'],
    'Value': ['WMACCESS', '01.02.2024', 'Customer Name', '130.00 €']
})

# Service Items Data
items_df = pd.DataFrame({
    'Service_Description': ['Basic Fee wmView'],
    'Amount_Without_VAT': ['130,00 €'],
    'Quantity': ['1'],
    'Total_Amount': ['130,00 €']
})
```

## 🔧 Konfigurasi

### Environment Variables

```bash
# Set Tesseract path (jika perlu)
export TESSERACT_CMD=/usr/local/bin/tesseract

# Set Flask environment
export FLASK_ENV=development
```

### Custom Configuration

```python
# Dalam ocr_modul.py
class AdvancedOCRPipeline:
    def __init__(self):
        self.tesseract_config = r'--oem 3 --psm 6'
        self.dpi = 300
        self.confidence_threshold = 60
```

## 📈 Fitur Advanced

### 1. Image Preprocessing

- CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Morphological operations
- Noise reduction
- Resolution enhancement

### 2. Multi-strategy OCR

- Direct OCR
- Enhanced image OCR
- Table-specific OCR
- Confidence scoring

### 3. Data Validation

- Pattern matching untuk invoice data
- Amount validation
- Date format validation
- Service description extraction

## 🐛 Troubleshooting

### Common Issues

#### 1. Tesseract not found

```bash
# Check Tesseract installation
tesseract --version

# Set path manually in code
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
```

#### 2. PDF processing error

```bash
# Install poppler
brew install poppler  # macOS
sudo apt-get install poppler-utils  # Ubuntu
```

#### 3. Memory issues with large PDFs

```python
# Reduce DPI for large files
pages = convert_from_path(pdf_path, dpi=150)  # Instead of 300
```

#### 4. Flask port already in use

```bash
# Kill existing process
lsof -i :5000
kill -9 <PID>

# Or use different port
python ocr_modul.py  # Edit port in code
```

## 📝 Development

### Adding New Features

1. Fork repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Submit pull request

### Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

Jika Anda mengalami masalah atau memiliki pertanyaan:

1. Check [Issues](https://github.com/noviantochris/ocrexercise/issues) page
2. Create new issue dengan detail error
3. Contact: noviantochris@gmail.com

## 🔄 Updates

### Version 2.0 (Latest)

- Enhanced OCR with image preprocessing
- Web interface untuk upload dokumen
- Multi-format document support
- Confidence scoring system
- DataFrame output optimization

---

**Happy OCR Processing! 🚀**
