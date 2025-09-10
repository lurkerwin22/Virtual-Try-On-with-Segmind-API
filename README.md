# 👕 Virtual Try-On with Segmind API

This repository provides a Python script to generate **AI-powered virtual try-on images** using [Segmind’s Try-On Diffusion API](https://www.segmind.com/). The script takes a **person image** and a **clothing image**, then outputs a composite image showing the person wearing the selected clothing.

---

## 📂 Project Structure

```
.
├── modelo.py              # Main script
├── person.jpg             # Input: photo of the person (user-supplied)
├── clothing.png           # Input: clothing image (user-supplied)
├── output.jpg             # Output: generated try-on result
└── README.md              # Documentation
```

---

## ⚙️ Requirements

- Python 3.8+
- Dependencies:
  - `requests`
  - `Pillow` (PIL)

Install dependencies:

```bash
pip install requests pillow
```

---

## 🔑 API Setup

1. Create a free account at [Segmind](https://www.segmind.com/).
2. Get your API key from your dashboard.
3. Set the key as an environment variable:

```bash
export SEGMIND_API_KEY="your_api_key_here"
```

Alternatively, replace the placeholder in `modelo.py`:

```python
API_KEY = os.getenv("SEGMIND_API_KEY", "SG_df7a6586e3f59f08")
```

---

## 🚀 Usage

1. Place your **person image** (`person.jpg`) and **clothing image** (`clothing.png`) in the project directory.
   - Recommended size: **768×1024** pixels (the script automatically resizes).
2. Run the script:

```bash
python modelo.py
```

3. If successful, the result will be saved as `output.jpg` and displayed automatically.

---

## ⚡ Features

- Automatic **image preprocessing** (resize, format conversion).
- **Base64 encoding** for API compatibility.
- Retry mechanism for **rate-limiting and failures**.
- Adjustable parameters:
  - `category`: `"Upper body"`, `"Lower body"`, `"Dress"`
  - `num_inference_steps`: controls detail (default: `30`)
  - `guidance_scale`: faithfulness to input clothing (default: `8`)
  - `seed`: reproducibility

---

## 🛠️ Configuration

You can modify parameters inside `generate_tryon()`:

```python
payload = {
    "category": "Upper body",   # Try: "Lower body" or "Dress"
    "num_inference_steps": 30,
    "guidance_scale": 8,
    "seed": 42,
}
```

---

## 📸 Example

Input:  
- `person.jpg` → A standing person  
- `clothing.png` → T-shirt image  

Output:  
- `output.jpg` → Person wearing the T-shirt  

---

## 🚧 Improvements & To-Do

1. **Error Handling**  
   - Improve parsing of error responses (`resp.json()`) instead of just raw text.  
   - Handle invalid image formats gracefully.  

2. **Configuration File**  
   - Move constants (paths, parameters, API key) to a `config.json` or `.env` file.  

3. **CLI Arguments**  
   - Allow passing custom paths and parameters from the command line:  
     ```bash
     python modelo.py --person input.jpg --clothing jacket.png --category "Upper body"
     ```  

4. **Batch Processing**  
   - Extend to process multiple clothing items in one run.  

5. **Web/GUI Interface**  
   - Add a Flask or Streamlit front-end for interactive try-on.  

6. **Unit Tests**  
   - Add tests for image preprocessing and API response handling.  

7. **Documentation**  
   - Add real before/after example images in `README.md`.  
   - Provide benchmarking of different parameters (e.g., inference steps).  
