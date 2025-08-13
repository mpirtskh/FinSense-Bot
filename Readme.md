# GenAI ასისტენტი TBC-ისთვის [MVP] [created on MacOS]

### ბოტთან კომუნიკაციის მაგალითები:
- "რა სახის ანგარიშები გაქვთ?"
- "რა საკომისიოები არის ბარათებზე?"
- "მიჩვენე სავალუტო კურსები"
- "რამდენი ლარია 100 დოლარი?"
- "გადაიყვანე 50 ევრო ლარში"
- "რომელი საათია თბილისში?"
- "როგორი ამინდიa ბათუმში?"
- "ანგარიშის გახსნა მინდა"

## 🚀 ინსტალაცია

### 1. რეპოზიტორიის კლონირება
```bash
git clone <your-repo-url>
cd TBC_GenAIbot
```

### 2. ვირტუალური გარემოს შექმნა
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# ან
.venv\Scripts\activate  # Windows
```

### 3. დამოკიდებულებების ინსტალაცია
```bash
pip install -r requirements.txt
```

### 4. გარემოს ცვლადების დაყენება
```env
OPENAI_API_KEY=*api_key*
OPENAI_MODEL=gpt-4o-mini
BANK_NAME=for ex. "TBC Bank"
```

## 🎯 გამოყენება

### ბოტის გაშვება
```bash
python -m app.main
```

## Tools

### 1. **get_time** - დრო და თარიღი

### 2. **get_weather** - ამინდის ინფორმაცია
- **API:** Open-Meteo (უფასო, API გასაღები არ სჭირდება)

### 3. **get_exchange_rates** - სავალუტო კურსები
- **API:** ExchangeRate-API

### 4. **convert_currency** - ვალუტის კონვერტაცია

### 5. **search_banking_faq** - ბანკინგის კითხვები

### 6. **ანგარიშის გახსნა** 
- ** : მიწერეთ ბოტს "ანგარიშის გახსნა მინდა"**


## 🌐 API ინტეგრაციები

### OpenAI API
- **მოდელი:** GPT-4o-mini
### Open-Meteo (ამინდი)
### ExchangeRate-API (სავალუტო კურსები)

---

# GenAI Assistant for TBC [MVP]

TBC Bank's virtual assistant that uses artificial intelligence and LangGraph to answer questions.

### Example Questions:
- "რა სახის ანგარიშები გაქვთ?" (What types of accounts do you have?)
- "რა საკომისიოები არის ბარათებზე?" (What fees are on cards?)
- "მიჩვენე სავალუტო კურსები" (Show me exchange rates)
- "რამდენი ლარია 100 დოლარი?" (How many Lari is 100 Dollars?)
- "გადაიყვანე 50 ევრო ლარში" (Convert 50 Euro to Lari)
- "რომელი საათია თბილისში?" (What time is it in Tbilisi time?)
- "როგორი ამინდია ბათუმში?" (How's the weather in Batumi?)

## 
- **LangGraph** - for conversation agent
- **LangChain** - for LLM integration
- **OpenAI GPT-4o** - for natural language processing
- **Python 3.10+** - main programming language
- **Pydantic** - for data validation


## 🚀 Installation

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd TBC_GenAIbot
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
BANK_NAME=TBC Bank
```

## 🎯 Usage

### Run the Bot
```bash
python -m app.main
```

## 🔧Created Tools

### 1. **get_time** - Time and Date

### 2. **get_weather** - Weather Information

### 3. **get_exchange_rates** - Exchange Rates

### 4. **convert_currency** - Currency Conversion

### 5. **search_banking_faq** - Banking Questions

### 6. **Multi-step account opening process** 
## 🌐 API Integrations

### OpenAI API
- **Model:** GPT-4o-mini
### Open-Meteo (Weather)
### ExchangeRate-API (Exchange Rates)
