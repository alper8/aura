# 🌌 Aura  
*Automated Universal Row Augmenter*  

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-brightgreen.svg)](https://www.python.org/)  
[![OpenAI API](https://img.shields.io/badge/OpenAI_API-Required-orange.svg)](https://openai.com/)  

**Aura** automates the translation and description of database attributes (e.g., English → Turkish) using OpenAI’s GPT models. Designed for data engineers and analysts, it streamlines documentation with consistent, human-like outputs.  

---

## ✨ Features  
- **AI-Powered Descriptions**: Generates natural-language descriptions for attributes (e.g., `CustomerID` → `Müşteri Tekil Anahtarı`).  
- **Chunk Processing**: Handles large files by splitting input into manageable chunks.  
- **Customizable Prompts**: Optimize outputs for your domain (e.g., finance, healthcare).  
- **Progress Tracking**: Real-time progress bar and incremental saves.  
- **Debug Mode**: Fine-tune models, prompts, and chunk sizes for advanced use.  

---

## 🚀 Quick Start  

### Prerequisites  
- OpenAI API key (set as `OPENAI_API_KEY` environment variable).  
- Python 3.8+.  

### Installation  
```bash
git clone https://github.com/alper8/aura.git
cd aura\cli
pip install -r requirements.txt
```

### Usage  
#### Basic (Pre-configured for Turkish descriptions):  
```bash
(manual)
python AddDesc.py

(with arguments)
python AddDesc.py attr.txt desc.txt
```  
#### Debug Mode (Customize AI behavior):  
```bash
python AddDesc.py --debug

python AddDesc.py input.txt output.txt --debug --model gpt-4o --chunk_size 50
```  

#### Input Example (`input_attributes.txt`):  
```plaintext
CustomerID  
OrderDate  
KVKKFlag  
```  

#### Output Example (`output_descriptions.txt`):  
```plaintext
CustomerID: Müşteri Tekil Anahtarı  
OrderDate: Sipariş Tarihi  
KVKKFlag: KVKK Bilgisi  
```  

---

## 🛠️ Customization  
### Modify the AI Prompt  
Edit the `--prompt` argument in `AddDesc.py` to change output language/style:  
```python  
prompt = "Sen bir veri modelleme uzmanısın..."  # Current Turkish prompt  
```  
Example for English:  
```python  
prompt = "You are a data modeling expert. Write 2-3 word descriptions for each attribute (e.g., 'CustomerID: Unique client identifier')."  
```  

---

## 🤝 Contributing  
1. **Fork** the repository.  
2. Add new CLI scripts (e.g., `AddTranslations.py` etc.) to expand Aura’s capabilities.  
3. Submit a **Pull Request** with clear documentation.  

---

## 📜 License  
Copyright 2025 © [Alper Baykara](https://github.com/alper8).  
Please open an issue with your e-mail address for private licensing deals.

---

## 🌟 Roadmap  
- [ ] Public API
- [ ] Frontend
- [ ] Custom LLM support

---

**💡 Tip**: Run with `--debug` to test different GPT models or prompts!  

--- 
