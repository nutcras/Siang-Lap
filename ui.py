import os
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, 
                            QWidget, QLabel, QFileDialog, QLineEdit, 
                            QMessageBox)
from crypto_utils import generate_key
from voice_utils import record_and_convert_to_text

class VoiceEncryptApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("โปรแกรมเข้ารหัสไฟล์ด้วยเสียง")
        self.setGeometry(100, 100, 400, 300)
        self.selected_file = None
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # ปุ่มเลือกไฟล์
        self.btn_select = QPushButton("เลือกไฟล์")
        self.btn_select.clicked.connect(self.select_file)
        layout.addWidget(self.btn_select)
        
        # แสดงชื่อไฟล์ที่เลือก
        self.lbl_file = QLabel("ยังไม่ได้เลือกไฟล์")
        layout.addWidget(self.lbl_file)
        
        # ช่องใส่รหัสผ่าน
        self.lbl_pass = QLabel("รหัสผ่าน (ภาษาไทย):")
        layout.addWidget(self.lbl_pass)
        
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Normal)
        layout.addWidget(self.txt_password)
        
        # ปุ่มเข้ารหัส
        self.btn_encrypt = QPushButton("เข้ารหัสไฟล์")
        self.btn_encrypt.clicked.connect(self.encrypt_file)
        layout.addWidget(self.btn_encrypt)
        
        # ปุ่มถอดรหัสด้วยเสียง
        self.btn_decrypt = QPushButton("ถอดรหัสด้วยเสียง")
        self.btn_decrypt.clicked.connect(self.decrypt_with_voice)
        layout.addWidget(self.btn_decrypt)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "เลือกไฟล์")
        if file_path:
            self.selected_file = file_path
            self.lbl_file.setText(os.path.basename(file_path))
    
    def encrypt_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "คำเตือน", "กรุณาเลือกไฟล์ก่อน")
            return
        
        password = self.txt_password.text()
        if not password:
            QMessageBox.warning(self, "คำเตือน", "กรุณากรอกรหัสผ่าน")
            return
        
        try:
            with open(self.selected_file, 'rb') as f:
                original_data = f.read()
            
            key = generate_key(password)
            encrypted_data = key.encrypt(original_data)
            
            output_file = self.selected_file + '.enc'
            with open(output_file, 'wb') as f:
                f.write(encrypted_data)
            
            QMessageBox.information(self, "สำเร็จ", f"เข้ารหัสไฟล์สำเร็จ!\nไฟล์ที่เข้ารหัส: {output_file}")
        except Exception as e:
            QMessageBox.critical(self, "ข้อผิดพลาด", f"เกิดข้อผิดพลาดขณะเข้ารหัส: {str(e)}")
    
    def decrypt_with_voice(self):
        if not self.selected_file or not self.selected_file.endswith('.enc'):
            QMessageBox.warning(self, "คำเตือน", "กรุณาเลือกไฟล์ที่เข้ารหัส (.enc)")
            return
        
        QMessageBox.information(self, "ข้อมูล", "กรุณาพูดรหัสผ่านเป็นภาษาไทย")
        password_text = record_and_convert_to_text()
        
        if not password_text:
            QMessageBox.warning(self, "คำเตือน", "ไม่สามารถรับรู้เสียงได้ กรุณาลองอีกครั้ง")
            return
        
        try:
            key = generate_key(password_text)
            
            with open(self.selected_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = key.decrypt(encrypted_data)
            
            output_file = self.selected_file[:-4]  # ลบ .enc ออก
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
            
            QMessageBox.information(self, "สำเร็จ", f"ถอดรหัสไฟล์สำเร็จ!\nไฟล์ที่ถอดรหัส: {output_file}")
        except Exception as e:
            QMessageBox.critical(self, "ข้อผิดพลาด", "ถอดรหัสล้มเหลว - รหัสผ่านไม่ถูกต้องหรือไฟล์เสียหาย")