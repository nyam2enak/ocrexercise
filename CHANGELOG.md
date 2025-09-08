# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-09-08

### Added

- **Enhanced OCR Pipeline**: Advanced image preprocessing with CLAHE and morphological operations
- **Web Interface**: Flask-based web application for document upload and processing
- **Multi-format Support**: Support for PDF, JPG, PNG, and other image formats
- **DataFrame Integration**: Structured data extraction into pandas DataFrames
- **Confidence Scoring**: OCR confidence scoring and quality assessment
- **Batch Processing**: Process multiple documents simultaneously
- **JSON Export**: Export processed data to JSON format
- **Setup Script**: Automated setup script for easy installation
- **Comprehensive Documentation**: Detailed README, CONTRIBUTING, and setup guides

### Changed

- **OCR Engine**: Upgraded to use Tesseract 5.x with improved accuracy
- **Code Structure**: Refactored into modular classes and functions
- **Error Handling**: Enhanced error handling and user feedback
- **Performance**: Optimized image processing and OCR performance

### Fixed

- **Memory Issues**: Fixed memory leaks in PDF processing
- **Encoding Issues**: Resolved text encoding problems
- **Path Handling**: Improved cross-platform path handling
- **Dependency Management**: Better dependency resolution

## [1.0.0] - 2025-09-01

### Added

- **Basic OCR Functionality**: Core OCR processing with Tesseract
- **PDF Processing**: Basic PDF to text conversion
- **Simple Web Interface**: Basic Flask web application
- **Data Extraction**: Basic pattern matching for invoice data
- **Jupyter Notebook**: Interactive notebook for testing OCR functions

### Technical Details

- **Python 3.8+** compatibility
- **Flask** web framework integration
- **OpenCV** image processing
- **Pandas** data manipulation
- **Basic error handling**

---

## Types of Changes

- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities

## Version Format

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 2.0.0)
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible
