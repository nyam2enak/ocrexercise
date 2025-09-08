import os
import re
import pandas as pd
import numpy as np
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import json
from datetime import datetime

# OCR-related libraries
from PIL import Image, ImageEnhance, ImageFilter
import cv2  # OpenCV for computer vision and image manipulation
import pytesseract  # Python wrapper for Tesseract OCR engine
from pdf2image import convert_from_path  # Convert PDF pages to images

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Create necessary directories
for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

class EnhancedOCRProcessor:
    """Enhanced OCR processor with better preprocessing and data extraction."""
    
    def __init__(self):
        # Configure Tesseract OCR settings
        self.tesseract_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:|/\-+()[] '
        
    def enhance_image(self, image):
        """Apply advanced image enhancement techniques for better OCR accuracy."""
        # Convert PIL to OpenCV format
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # 1. Resize image for better OCR (if too small)
        height, width = img_cv.shape[:2]
        if width < 1800:  # Scale up small images
            scale_factor = 1800 / width
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            img_cv = cv2.resize(img_cv, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        # 2. Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # 3. Noise reduction
        denoised = cv2.medianBlur(gray, 3)
        
        # 4. Contrast enhancement using CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # 5. Binary thresholding with Otsu's method
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 6. Morphological operations to clean up the image
        kernel = np.ones((2,2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def process_pdf_to_text(self, pdf_path):
        """Enhanced PDF to text conversion with better preprocessing."""
        if not os.path.exists(pdf_path):
            return {"error": f"File '{pdf_path}' not found.", "text": ""}
        
        try:
            # Convert PDF to images with higher DPI for better quality
            images = convert_from_path(pdf_path, dpi=300, fmt='PNG')
            extracted_texts = []
            
            for i, image in enumerate(images):
                print(f"Processing page {i+1} with enhanced OCR...")
                
                # Apply image enhancement
                enhanced_image = self.enhance_image(image)
                
                # Perform OCR with custom configuration
                text = pytesseract.image_to_string(enhanced_image, config=self.tesseract_config)
                extracted_texts.append(text)
            
            full_text = "\n\n".join(extracted_texts)
            return {"error": None, "text": full_text, "pages": len(images)}
            
        except Exception as e:
            return {"error": str(e), "text": ""}

class DocumentDataExtractor:
    """Enhanced data extractor with better field detection and validation."""
    
    def __init__(self):
        # Predefined patterns for different document types
        self.patterns = {
            'po_document': {
                'supplier': [
                    r'Supplier\s*\|\s*(.+?)(?:\||$)',
                    r'From\s*[:]\s*(.+?)(?:\n|$)',
                    r'Vendor\s*[:]\s*(.+?)(?:\n|$)'
                ],
                'document_number': [
                    r'No\.?\s*PO\s*([A-Z0-9-]+)',
                    r'PO\s*Number\s*[:]\s*([A-Z0-9-]+)',
                    r'Purchase\s*Order\s*[:]\s*([A-Z0-9-]+)'
                ],
                'date': [
                    r'Date\s*(\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2})',
                    r'Date\s*[:]\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})',
                    r'(\d{4}-\d{2}-\d{2})'
                ],
                'status': [
                    r'Status\s*PO\s*\|\s*(.+?)(?:\n|$)',
                    r'Status\s*[:]\s*(.+?)(?:\n|$)'
                ],
                'address': [
                    r'(Jl\..+?)(?:\n|$)',
                    r'Address\s*[:]\s*(.+?)(?:\n|$)'
                ],
                'to': [
                    r'\|\s*To\s*(.+?)(?:\n|$)',
                    r'To\s*[:]\s*(.+?)(?:\n|$)',
                    r'Ship\s*To\s*[:]\s*(.+?)(?:\n|$)'
                ]
            }
        }
    
    def extract_field(self, text, field_patterns, default="Not found"):
        """Extract field using multiple pattern attempts."""
        for pattern in field_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                result = match.group(1).strip()
                # Clean up result
                result = re.sub(r'\s+', ' ', result)  # Replace multiple spaces
                result = result.split('|')[0].strip()  # Take first part if pipe-separated
                if result and result != "Not found":
                    return result
        return default
    
    def extract_main_fields(self, full_text, doc_type='po_document'):
        """Extract main document fields with validation."""
        patterns = self.patterns.get(doc_type, self.patterns['po_document'])
        
        extracted = {}
        for field, field_patterns in patterns.items():
            extracted[field] = self.extract_field(full_text, field_patterns)
        
        # Post-process and validate data
        extracted_clean = {
            'Supplier': extracted.get('supplier', 'Not found'),
            'Document Number': extracted.get('document_number', 'Not found'),
            'Date': self.normalize_date(extracted.get('date', 'Not found')),
            'Status': extracted.get('status', 'Not found'),
            'Address': extracted.get('address', 'Not found'),
            'To': extracted.get('to', 'Not found'),
            'Extracted At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return extracted_clean
    
    def normalize_date(self, date_str):
        """Normalize date to standard format."""
        if date_str == "Not found" or not date_str:
            return "Not found"
        
        # Try to parse different date formats
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',
            r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, date_str)
            if match:
                if len(match.groups()) == 1:
                    return match.group(1)
                elif len(match.groups()) == 3:
                    # Convert to YYYY-MM-DD format
                    if len(match.group(3)) == 4:  # DD/MM/YYYY or MM/DD/YYYY
                        return f"{match.group(3)}-{match.group(2).zfill(2)}-{match.group(1).zfill(2)}"
                    else:  # YYYY/MM/DD
                        return f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"
        
        return date_str  # Return as-is if no pattern matches

class ItemTableParser:
    """Enhanced item table parser with better structure detection."""
    
    def __init__(self):
        self.item_start_patterns = [
            r'^PRT\d*',
            r'^\d+\s+[A-Z]',
            r'^[A-Z]{2,}\d+'
        ]
    
    def parse_item_table(self, full_text):
        """Parse item table with enhanced structure detection."""
        lines = full_text.split('\n')
        items_raw = []
        current_item = []
        in_item_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect start of item section
            if not in_item_section and any(re.match(pattern, line) for pattern in self.item_start_patterns):
                in_item_section = True
            
            if in_item_section:
                # Check if this is a new item
                if any(re.match(pattern, line) for pattern in self.item_start_patterns):
                    if current_item:
                        items_raw.append(current_item)
                    current_item = [line]
                elif current_item:
                    # Add line to current item if it contains relevant data
                    if self.is_item_data_line(line):
                        current_item.append(line)
                    elif re.search(r'(?i)(subtotal|total|grand\s*total)', line):
                        # End of items section
                        break
        
        if current_item:
            items_raw.append(current_item)
        
        return self.process_raw_items(items_raw)
    
    def is_item_data_line(self, line):
        """Check if line contains item data."""
        indicators = [
            '/',  # Description separator
            re.search(r'\d+[\.,]\d+', line),  # Price patterns
            '|' in line,  # Column separator
            len(line) > 10  # Minimum length for meaningful data
        ]
        return any(indicators)
    
    def process_raw_items(self, items_raw):
        """Process raw item data into structured format."""
        table_items = []
        
        for item_lines in items_raw:
            if not item_lines:
                continue
                
            item_data = self.parse_single_item(item_lines)
            if item_data:
                table_items.append(item_data)
        
        # Filter out system rows
        filtered_items = []
        for item in table_items:
            desc = item.get('Description', '').lower()
            if not any(keyword in desc for keyword in ['subtotal', 'disc', 'amount tax', 'total']):
                filtered_items.append(item)
        
        # Split descriptions and add metadata
        enhanced_items = []
        for item in filtered_items:
            enhanced_item = self.enhance_item_data(item)
            enhanced_items.append(enhanced_item)
        
        return enhanced_items
    
    def parse_single_item(self, item_lines):
        """Parse a single item from multiple lines."""
        if not item_lines:
            return None
            
        # Extract item code from first line
        first_line = item_lines[0]
        parts = first_line.split(' ', 1)
        item_code = parts[0].strip().rstrip('-')
        base_description = parts[1] if len(parts) > 1 else ''
        
        # Combine all description lines
        full_description = base_description
        for line in item_lines[1:]:
            if '/' in line or not re.search(r'\d+[\.,]\d+', line):
                full_description += ' ' + line.strip()
        
        # Extract numeric values
        numeric_values = self.extract_numeric_values(item_lines)
        
        # Clean description (remove prices)
        clean_description = self.clean_description(full_description)
        
        return {
            'Item Code': item_code,
            'Description': clean_description,
            'Unit Cost': numeric_values.get('unit_cost', ''),
            'Discount': numeric_values.get('discount', ''),
            'Quantity': numeric_values.get('quantity', ''),
            'Total Cost': numeric_values.get('total_cost', ''),
            'Raw Lines': ' | '.join(item_lines)  # For debugging
        }
    
    def extract_numeric_values(self, item_lines):
        """Extract numeric values from item lines."""
        all_text = ' '.join(item_lines)
        
        # Find all price-like patterns
        price_patterns = [
            r'(\d+\.\d+,\d+)',  # 750.000,00
            r'(\d+,\d+)',       # 1,00
            r'(\d+\.\d+)'       # 750.000
        ]
        
        numbers = []
        for pattern in price_patterns:
            numbers.extend(re.findall(pattern, all_text))
        
        # Last line usually contains final prices
        last_line = item_lines[-1] if item_lines else ""
        last_numbers = re.findall(r'(\d+[\.,]\d+[\.,]\d+|\d+[\.,]\d+)', last_line)
        
        return {
            'total_cost': last_numbers[0] if len(last_numbers) > 0 else '',
            'discount': last_numbers[1] if len(last_numbers) > 1 else '',
            'quantity': last_numbers[2] if len(last_numbers) > 2 else '',
            'unit_cost': numbers[-1] if numbers and len(numbers) >= 3 else ''
        }
    
    def clean_description(self, description):
        """Clean and normalize description text."""
        # Remove price patterns
        cleaned = re.sub(r'\d+[\.,]\d+[\.,]\d+|\d+[\.,]\d+', '', description)
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned.strip()
    
    def enhance_item_data(self, item):
        """Split description and add structured fields."""
        description = item.get('Description', '')
        desc_parts = description.split('/')
        
        # Standardize field extraction
        enhanced = item.copy()
        enhanced.update({
            'Item Name': self.clean_field(desc_parts[0] if len(desc_parts) > 0 else ''),
            'Type': self.clean_field(desc_parts[1] if len(desc_parts) > 1 else ''),
            'Part Number': self.clean_field(desc_parts[2] if len(desc_parts) > 2 else ''),
            'Product Code': self.clean_field(desc_parts[3] if len(desc_parts) > 3 else ''),
            'Size': self.clean_field(desc_parts[4] if len(desc_parts) > 4 else ''),
            'Color': self.clean_field(desc_parts[5] if len(desc_parts) > 5 else ''),
            'Brand': self.clean_field(desc_parts[6] if len(desc_parts) > 6 else ''),
            'Description Parts Count': len(desc_parts),
            'Has Structured Description': len(desc_parts) > 3
        })
        
        return enhanced
    
    def clean_field(self, field):
        """Clean individual field data."""
        if not field:
            return ''
        
        # Remove extra whitespace and special characters
        cleaned = re.sub(r'[^\w\s\-\.]', '', field)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned.strip()

def process_pdf_to_text(pdf_path):
    """Enhanced wrapper function for backward compatibility."""
    processor = EnhancedOCRProcessor()
    result = processor.process_pdf_to_text(pdf_path)
    return result["text"]

def extract_main_fields(full_text):
    """Enhanced main fields extraction."""
    extractor = DocumentDataExtractor()
    return extractor.extract_main_fields(full_text)

def parse_item_table(full_text):
    """Enhanced item table parsing."""
    parser = ItemTableParser()
    items = parser.parse_item_table(full_text)
    return items

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Create enhanced processor instances
                ocr_processor = EnhancedOCRProcessor()
                data_extractor = DocumentDataExtractor()
                table_parser = ItemTableParser()
                
                # Process the file with enhanced OCR
                ocr_result = ocr_processor.process_pdf_to_text(filepath)
                
                if ocr_result["error"]:
                    return render_template('result.html', 
                                         main={}, 
                                         table=[], 
                                         error=f"OCR Error: {ocr_result['error']}")
                
                full_text = ocr_result["text"]
                
                if not full_text.strip():
                    return render_template('result.html', 
                                         main={}, 
                                         table=[], 
                                         error="No text could be extracted from the PDF.")
                
                # Extract structured data
                main_data = data_extractor.extract_main_fields(full_text)
                table_data = table_parser.parse_item_table(full_text)
                
                # Add processing metadata
                processing_info = {
                    'filename': filename,
                    'pages_processed': ocr_result.get("pages", 0),
                    'items_found': len(table_data),
                    'processing_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Save processed data to JSON for later analysis
                processed_data = {
                    'main_fields': main_data,
                    'items': table_data,
                    'processing_info': processing_info,
                    'raw_text': full_text[:1000] + "..." if len(full_text) > 1000 else full_text
                }
                
                processed_filename = f"processed_{filename.replace('.pdf', '.json')}"
                processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
                
                with open(processed_path, 'w', encoding='utf-8') as f:
                    json.dump(processed_data, f, indent=2, ensure_ascii=False)
                
                return render_template('result.html', 
                                     main=main_data, 
                                     table=table_data,
                                     processing_info=processing_info)
                                     
            except Exception as e:
                return render_template('result.html', 
                                     main={}, 
                                     table=[], 
                                     error=f"Processing Error: {str(e)}")
    
    return render_template('upload.html')

@app.route('/api/process', methods=['POST'])
def api_process():
    """API endpoint for programmatic access."""
    file = request.files.get('file')
    if not file or not file.filename:
        return jsonify({'error': 'No file provided'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process with enhanced classes
        ocr_processor = EnhancedOCRProcessor()
        data_extractor = DocumentDataExtractor()
        table_parser = ItemTableParser()
        
        ocr_result = ocr_processor.process_pdf_to_text(filepath)
        
        if ocr_result["error"]:
            return jsonify({'error': ocr_result["error"]}), 500
        
        main_data = data_extractor.extract_main_fields(ocr_result["text"])
        table_data = table_parser.parse_item_table(ocr_result["text"])
        
        return jsonify({
            'main_fields': main_data,
            'items': table_data,
            'pages_processed': ocr_result.get("pages", 0),
            'items_count': len(table_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_processed_data(filename):
    """Download processed data as JSON."""
    try:
        processed_filename = f"processed_{filename.replace('.pdf', '.json')}"
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
        
        if os.path.exists(processed_path):
            with open(processed_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            response = app.response_class(
                response=json.dumps(data, indent=2, ensure_ascii=False),
                status=200,
                mimetype='application/json'
            )
            response.headers['Content-Disposition'] = f'attachment; filename="{processed_filename}"'
            return response
        else:
            return jsonify({'error': 'File not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Enhanced OCR Flask Application...")
    print("📋 Features:")
    print("  - Advanced image preprocessing")
    print("  - Multiple pattern matching")
    print("  - Structured data extraction") 
    print("  - Clean web interface")
    print("  - JSON data export")
    print(f"\n🌐 Access the app at: http://127.0.0.1:5001/")
    app.run(debug=True, port=5001)
