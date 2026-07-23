#!/bin/bash

# ==========================================
# DarkForge - Advanced PDF & Image Exploitation Framework
# سكريبت التثبيت الكامل
# ==========================================

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${RED}"
echo "██████╗  █████╗ ██████╗ ██╗  ██╗███████╗ ██████╗ ██████╗  ██████╗ ███████╗"
echo "██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██╔════╝ ██╔══██╗██╔════╝ ██╔════╝"
echo "██║  ██║███████║██████╔╝█████╔╝ █████╗  ██║  ███╗██████╔╝██║  ███╗█████╗  "
echo "██║  ██║██╔══██║██╔══██╗██╔═██╗ ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  "
echo "██████╔╝██║  ██║██║  ██║██║  ██╗██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗"
echo "╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝"
echo -e "${NC}"
echo -e "${CYAN}  Advanced PDF & Image Exploitation Framework${NC}"
echo -e "${YELLOW}  للاستخدام في اختبارات الاختراق المصرح بها فقط${NC}"
echo ""

# التحقق من وجود Python
echo -e "${BLUE}[*] التحقق من المتطلبات...${NC}"

if command -v python3 &> /dev/null; then
    echo -e "${GREEN}[✓] Python 3 مثبت${NC}"
else
    echo -e "${RED}[✗] Python 3 غير مثبت!${NC}"
    echo -e "${YELLOW}  قم بتثبيته: pkg install python (Termux) أو apt install python3 (Linux)${NC}"
    exit 1
fi

# تحديث الحزم
echo -e "\n${BLUE}[*] تحديث الحزم...${NC}"

if [[ "$OSTYPE" == "linux-android"* ]] || [[ -d "/data/data/com.termux" ]]; then
    # Termux
    pkg update -y && pkg upgrade -y
    pkg install python python-pip git wget curl openssl -y
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    sudo apt update -y
    sudo apt install python3 python3-pip git wget curl -y
fi

echo -e "${GREEN}[✓] تم تحديث الحزم${NC}"

# تثبيت المكتبات المطلوبة
echo -e "\n${BLUE}[*] تثبيت المكتبات المطلوبة...${NC}"

pip3 install --upgrade pip
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[✓] تم تثبيت المكتبات بنجاح${NC}"
else
    echo -e "${RED}[✗] فشل في تثبيت بعض المكتبات${NC}"
    echo -e "${YELLOW}  جرب التثبيت اليدوي: pip3 install -r requirements.txt${NC}"
fi

# إنشاء المجلدات
echo -e "\n${BLUE}[*] إنشاء هيكل المشروع...${NC}"
mkdir -p output/pdf output/images output/payloads output/logs
mkdir -p examples templates

echo -e "${GREEN}[✓] تم إنشاء المجلدات${NC}"

# صلاحيات التشغيل
chmod +x darkforge/main.py 2>/dev/null
chmod +x darkforge/server/listener.py 2>/dev/null

# اختبار التثبيت
echo -e "\n${BLUE}[*] اختبار التثبيت...${NC}"

python3 -c "from PIL import Image; print('${GREEN}[✓] Pillow يعمل${NC}')" 2>/dev/null || echo "${YELLOW}[!] Pillow لم يعمل${NC}"
python3 -c "import Crypto; print('${GREEN}[✓] PyCryptodome يعمل${NC}')" 2>/dev/null || echo "${YELLOW}[!] PyCryptodome لم يعمل${NC}"
python3 -c "from colorama import Fore; print('${GREEN}[✓] Colorama يعمل${NC}')" 2>/dev/null || echo "${YELLOW}[!] Colorama لم يعمل${NC}"

# الاكتمال
echo -e "\n${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          Installation Complete!          ║${NC}"
echo -e "${GREEN}╠══════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║${NC}  Run: ${CYAN}python3 run.py${NC}                  ${GREEN}║${NC}"
echo -e "${GREEN}║${NC}  Help: ${CYAN}python3 run.py --help${NC}           ${GREEN}║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"

echo -e "\n${YELLOW}⚠️  تنبيه مهم:${NC}"
echo -e "${YELLOW}هذه الأداة مخصصة لاختبارات الاختراق المصرح بها فقط!${NC}"
