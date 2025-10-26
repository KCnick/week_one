import streamlit as st
from main import LLMApp
from config import env_config

st.set_page_config(
    page_title="Rnix Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("💬 Rnix Chatbot")
st.markdown("Chat with Rnix — your AI assistant powered by **Groq** or **OpenAI**!")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "llm_app" not in st.session_state:
    st.session_state.llm_app = None

with st.sidebar:
    st.header("⚙️ Configuration")

    provider = st.radio(
        "Select LLM Provider",
        options=["Groq", "OpenAI"],
        horizontal=True,
    )

    api_key = st.text_input(
        f"{provider} API Key",
        type="password",
        help=f"Enter your {provider} API key",
    )
    
    if not api_key:
        if provider == "Groq":
            api_key = env_config.groq_api_key
        else:
            api_key = env_config.openai_api_key

    if provider == "Groq":
        model = st.selectbox(
            "Model",
            ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
            help="Select the model to use",
        )
    else:
        model = st.selectbox(
            "OpenAI Model",
            ["gpt-5", "gpt-5-mini", "gpt-5-nano"],
            help="Select the model to use",
        )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1,
        help="Controls response randomness (higher = more creative)",
    )

    max_tokens = st.slider(
        "Max Tokens",
        min_value=256,
        max_value=2048,
        value=1024,
        step=256,
        help="Set the maximum response length",
    )

    base_prompt = (
        "You are Rnix, a helpful and knowledgeable AI assistant. "
        "If someone asks your name, respond with: 'My name is Rnix, your friendly assistant.' "
        "Always stay polite, concise, and informative."
    )

    custom_prompt = st.text_area(
        "Additional System Instructions (Optional)",
        placeholder="e.g., Focus on short and precise answers.",
        help="Set the context or behavior of the assistant",
    )

    system_prompt = f"{base_prompt}\n\n{custom_prompt}".strip()

    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if st.session_state.llm_app is None and api_key:
    try:
        st.session_state.llm_app = LLMApp(
            api_key=api_key, model=model, provider=provider.lower()
        )
    except Exception as e:
        st.error(f"Error initializing LLMApp: {e}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
    if not api_key:
        st.warning(f"Please enter your {provider} API key to start chatting.")
    elif st.session_state.llm_app is None:
        st.error("LLMApp is not initialized. Please check your API key.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.llm_app.chat(
                        user_message=prompt,
                        system_prompt=system_prompt,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )
                    st.markdown(response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                except Exception as e:
                    st.error(f"Error generating response: {e}")
