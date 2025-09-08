# Contributing to OCR Exercise

Terima kasih atas minat Anda untuk berkontribusi pada proyek OCR Exercise! Kami sangat menghargai kontribusi dari komunitas.

## 🚀 Cara Berkontribusi

### 1. Fork Repository

1. Fork repository ini ke akun GitHub Anda
2. Clone fork Anda: `git clone https://github.com/YOUR_USERNAME/ocrexercise.git`
3. Buat branch baru: `git checkout -b feature/AmazingFeature`

### 2. Setup Development Environment

```bash
cd ocrexercise
./setup.sh  # Jalankan setup script
source .venv/bin/activate
```

### 3. Make Changes

- Ikuti PEP 8 style guide
- Tambahkan docstrings untuk fungsi baru
- Test perubahan Anda
- Pastikan tidak ada error

### 4. Commit Changes

```bash
git add .
git commit -m "Add: Amazing new feature"
git push origin feature/AmazingFeature
```

### 5. Create Pull Request

1. Buka repository fork Anda di GitHub
2. Klik "New Pull Request"
3. Pilih branch Anda
4. Berikan deskripsi yang jelas tentang perubahan
5. Submit Pull Request

## 📋 Development Guidelines

### Code Style

- **Python**: Ikuti [PEP 8](https://pep8.org/)
- **Docstrings**: Gunakan format Google-style docstrings
- **Naming**: Gunakan snake_case untuk variable/fungsi, PascalCase untuk class
- **Imports**: Group imports (standard library, third-party, local)

### Commit Messages

Format: `Type: Description`

Types:

- `Add:` - Fitur baru
- `Fix:` - Perbaikan bug
- `Update:` - Update fitur existing
- `Docs:` - Dokumentasi
- `Style:` - Formatting, missing semi colons, etc
- `Refactor:` - Code refactoring
- `Test:` - Adding tests

### Testing

```bash
# Run basic tests
python -m pytest

# Test OCR functionality
python -c "from ocr_modul import EnhancedOCRProcessor; print('OCR test passed')"
```

## 🐛 Reporting Bugs

### Template Bug Report

```
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. macOS 12.0]
 - Python Version: [e.g. 3.9]
 - Tesseract Version: [e.g. 5.0.0]

**Additional context**
Add any other context about the problem here.
```

## 💡 Feature Requests

### Template Feature Request

```
**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

## 📚 Documentation

### Adding Documentation

- Update README.md untuk perubahan signifikan
- Tambahkan docstrings untuk fungsi baru
- Update comments dalam code
- Buat example usage jika diperlukan

### Documentation Standards

- Gunakan bahasa Indonesia untuk dokumentasi utama
- Sertakan English translation jika memungkinkan
- Berikan contoh code yang bisa dijalankan
- Jelaskan parameter dan return value

## 🔧 Development Setup

### Required Software

- Python 3.8+
- Tesseract OCR 4.0+
- Poppler (for pdf2image)
- Git

### Recommended Tools

- VS Code dengan Python extension
- Jupyter Notebook
- GitHub Desktop (optional)

## 📞 Getting Help

Jika Anda membutuhkan bantuan:

1. Check [Issues](https://github.com/noviantochris/ocrexercise/issues)
2. Buat issue baru dengan label `question`
3. Contact maintainer: noviantochris@gmail.com

## 📋 Code of Conduct

### Our Standards

- **Respectful**: Gunakan bahasa yang sopan dan menghargai
- **Inclusive**: Terbuka untuk semua kontributor
- **Collaborative**: Bekerja sama untuk improvement
- **Patient**: Bersabar dengan kontributor baru

### Enforcement

Pelanggaran Code of Conduct dapat dilaporkan dengan membuat issue atau contact maintainer.

---

**Terima kasih atas kontribusi Anda! 🎉**
