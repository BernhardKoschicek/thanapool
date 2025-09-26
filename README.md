# ThanaPool

This prototype was created in the course of the [Hack the Pool hackathon](https://info.kulturpool.at/hack-the-pool/) organized by [Kulturpool](https://kulturpool.at/).

The goal of ThanaPool is to combine cultural heritage data from an [OpenAtlas](https://openatlas.eu) database with relevant resources retrieved from the [Kulturpool API](https://api.kulturpool.at/docs#/) using the support of large language models (LLMs).

---

## Installation

### Requirements
- Python 3.9+
- [pip](https://pip.pypa.io/)
- An [OpenRouter](https://openrouter.ai/) API key for LLM access

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/thanapool.git
   cd thanapool

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate      # Windows

3. Install dependencies:
   ```bash
    pip install -r requirements.txt

4. Create a .env file in the project root with your OpenRouter API key:
    ```bash
   OPENROUTER_API_KEY='{your_token}'

5. Run the server:
    ```bash 
    python runserver.py
   
## Contributors

- [stefaneichert](https://github.com/stefaneichert)  
- [MelissaSheena](https://github.com/MelissaSheena)  
- [NotJona](https://github.com/NotJona)  
- [NinaBrundke](https://github.com/NinaBrundke)  
- [cureboyxxx](https://github.com/cureboyxxx)  
- [BernhardKoschicek](https://github.com/BernhardKoschicek)  

## License

This project is licensed under the MIT License.  

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the "Software"), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.
