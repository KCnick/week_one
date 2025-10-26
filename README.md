# 💬 Rnix Chatbot

Rnix Chatbot is a **multi-provider AI chat application** built with **Streamlit**, supporting both **Groq** and **OpenAI** LLMs.  
It provides a user-friendly interface for interacting with advanced models like `llama-3.3-70b-versatile` and `gpt-5o`.

---

##  Features

 Switch between **Groq** and **OpenAI** providers  
 Select from multiple **LLM models**  
 Adjust **temperature** and **max tokens**  
 Customizable **system prompt**  
 Persistent **chat history** during session  
 Built-in chatbot personality: **Rnix**  
 Clean, interactive **Streamlit UI**


##  Tech Stack

- **Frontend:** Streamlit  
- **Backend/Logic:** Python
- **LLM Providers:** Groq API & OpenAI API  
- **Configuration:** Environment-based API key management  


## Create and activate a virtual environment

`python3 -m venv .venv`
`source .venv/bin/activate`


## Install dependencies
`pip install -r requirements.txt`

## Environment Configuration
Create a `.env` file in the project root:
`GROQ_API_KEY=your-groq-api-key`
`OPENAI_API_KEY=your-openai-api-key`

## Running the APP
 `streamlit run streamlit_app.py`



