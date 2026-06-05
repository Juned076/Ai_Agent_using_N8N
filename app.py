import streamlit as st
import requests

N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/1b87af39-c011-4706-802c-cc37cf1d5819"

# Page title
st.title("🤝 Your Personal Assistant")
st.subheader("What can your personal assistant do?")

st.markdown("""
1. Answer questions on various topics.   
2. Arrange Calendar events and meetings.  
3. Read your emails and send replies, can even summarize them for you.
4. Manage your tasks and to-do lists.
5. Take quick notes for you.
6. Track your expenses and budgeting.
""")

st.subheader("💬 Chat with your assistant")

# Session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_message = st.chat_input("Type your message here...")

if user_message:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    # Send to n8n and get response
    ai_response = None
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={"message": user_message},
            timeout=60  # wait up to 60 seconds for AI to respond
        )

        # Debug: show raw response if something goes wrong
        if response.status_code != 200:
            ai_response = f"⚠️ n8n returned status {response.status_code}. Make sure your workflow is active."
        
        elif response.text.strip() == "":
            ai_response = "⚠️ n8n returned an empty response. Check your 'Respond to Webhook' node."
        
        else:
            data = response.json()

            # Handle different n8n response shapes
            if isinstance(data, list) and len(data) > 0:
                item = data[0]
                if "output" in item:
                    ai_response = item["output"]
                elif "text" in item:
                    ai_response = item["text"]
                elif "message" in item:
                    ai_response = item["message"]
                else:
                    ai_response = str(item)

            elif isinstance(data, dict):
                if "output" in data:
                    ai_response = data["output"]
                elif "text" in data:
                    ai_response = data["text"]
                elif "message" in data:
                    ai_response = data["message"]
                else:
                    ai_response = str(data)
            else:
                ai_response = str(data)

    except requests.exceptions.ConnectionError:
        ai_response = "⚠️ Could not connect to n8n. Make sure n8n is running on localhost:5678 and the workflow is active."
    except requests.exceptions.Timeout:
        ai_response = "⚠️ Request timed out. The AI is taking too long to respond. Try again."
    except requests.exceptions.JSONDecodeError:
        ai_response = f"⚠️ n8n returned invalid JSON. Raw response: {response.text[:300]}"
    except Exception as e:
        ai_response = f"⚠️ Unexpected error: {str(e)}"

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})