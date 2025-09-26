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
