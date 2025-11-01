# GitHub Upload Guide

## Step-by-Step Instructions to Upload This Project to GitHub

### Prerequisites
1. Install Git: https://git-scm.com/downloads
2. Create a GitHub account: https://github.com/signup
3. (Optional) Install GitHub Desktop: https://desktop.github.com/

### Method 1: Using Git Command Line

#### 1. Initialize Git Repository
Open PowerShell/Terminal in the project folder and run:

```bash
cd "C:\Users\chira\OneDrive\Desktop\SEM 7\NLP\Review-Analysis-and-Summarization-System-main"
git init
```

#### 2. Configure Git (First Time Only)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### 3. Create .gitignore (Already Done)
The `.gitignore` file is already configured to exclude:
- `config.py` (contains your API credentials)
- Model files (too large)
- Generated data files
- Python cache files

#### 4. Stage All Files
```bash
git add .
```

#### 5. Commit Changes
```bash
git commit -m "Initial commit: Review Analysis and Summarization System"
```

#### 6. Create Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `Review-Analysis-and-Summarization-System`
3. Description: `AI-powered system for detecting fake reviews and generating summaries`
4. Make it **Public** or **Private**
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

#### 7. Link Local Repository to GitHub
Copy the commands from GitHub (replace with your username):

```bash
git remote add origin https://github.com/YOUR_USERNAME/Review-Analysis-and-Summarization-System.git
git branch -M main
git push -u origin main
```

#### 8. Enter Credentials
- Enter your GitHub username
- For password, use a **Personal Access Token** (not your account password)
  - Generate token at: https://github.com/settings/tokens
  - Click "Generate new token (classic)"
  - Select scopes: `repo` (full control of private repositories)
  - Copy the token (you won't see it again!)

### Method 2: Using GitHub Desktop (Easier)

#### 1. Open GitHub Desktop
- Download from: https://desktop.github.com/

#### 2. Add Local Repository
- File → Add Local Repository
- Browse to: `C:\Users\chira\OneDrive\Desktop\SEM 7\NLP\Review-Analysis-and-Summarization-System-main`
- Click "Add Repository"

#### 3. Commit Changes
- You'll see all files listed
- Enter commit message: "Initial commit: Review Analysis and Summarization System"
- Click "Commit to main"

#### 4. Publish Repository
- Click "Publish repository" button
- Choose repository name: `Review-Analysis-and-Summarization-System`
- Add description
- Choose Public or Private
- **Uncheck** "Keep this code private" if you want it public
- Click "Publish Repository"

### Important: Before Uploading

✅ **Files to Upload:**
- All `.py` files
- `templates/` folder
- `static/` folder
- `README_NEW.md` (rename to README.md)
- `requirements.txt`
- `config_template.py`
- `.gitignore`
- `LICENSE`
- `CUSTOM_SUMMARIZER_README.md`

❌ **Files to EXCLUDE (Already in .gitignore):**
- `config.py` - **CONTAINS YOUR API CREDENTIALS**
- `data/*.csv` - Generated files
- `data/*.pdf` - Generated files
- `data/*.json` - Generated files
- `snlp/saved_models/*.pkl` - Model files (too large for GitHub)
- `__pycache__/` - Python cache

### After Upload

#### 1. Verify .gitignore Worked
Check your GitHub repository - you should NOT see:
- `config.py`
- Files in `data/` folder
- `.pkl` model files

#### 2. Update README
Replace the current `README.md` with `README_NEW.md`:

```bash
# On your local machine
Remove-Item README.md
Rename-Item README_NEW.md README.md
git add README.md
git commit -m "Update README with comprehensive documentation"
git push
```

#### 3. Add Repository Description
On GitHub:
1. Go to your repository
2. Click the ⚙️ gear icon next to "About"
3. Add description: "AI-powered review analysis system with fake detection and summarization"
4. Add topics: `python`, `machine-learning`, `nlp`, `sentiment-analysis`, `web-scraping`, `flask`, `review-analysis`
5. Save changes

#### 4. Create Releases (Optional)
1. Go to "Releases" → "Create a new release"
2. Tag: `v1.0.0`
3. Title: "Initial Release"
4. Description: List features and installation instructions
5. Publish release

### Common Issues

**Issue 1: File Too Large**
```
remote: error: File is too large
```
**Solution:** Model files (.pkl) are already in .gitignore. If you see this:
```bash
git rm --cached snlp/saved_models/*.pkl
git commit -m "Remove large model files"
git push
```

**Issue 2: Authentication Failed**
**Solution:** Use Personal Access Token instead of password
- Generate at: https://github.com/settings/tokens

**Issue 3: config.py Uploaded by Mistake**
**Solution:** Remove it immediately:
```bash
git rm --cached config.py
git commit -m "Remove config.py with credentials"
git push
```
Then change your API credentials on Oxylabs!

### Security Checklist

Before pushing:
- [ ] `config.py` is in `.gitignore`
- [ ] `config_template.py` has placeholder values
- [ ] No API keys in any committed files
- [ ] Model files are excluded (too large)
- [ ] Sample data is optional (can be regenerated)

### After Upload - User Instructions

Add this to your GitHub repository description:

```markdown
## Setup Instructions

1. Clone the repository
2. Copy `config_template.py` to `config.py`
3. Fill in your Oxylabs credentials in `config.py`
4. Install dependencies: `pip install -r requirements.txt`
5. Download/train the ML model and place in `snlp/saved_models/`
6. Run: `python app.py`
7. Visit: http://127.0.0.1:5000
```

### Need Help?

- Git Documentation: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com/
- GitHub Desktop Help: https://docs.github.com/en/desktop

---

**Ready to Upload?** Follow Method 1 (Command Line) or Method 2 (GitHub Desktop) above! 🚀
