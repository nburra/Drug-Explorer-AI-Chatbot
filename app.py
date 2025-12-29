# ---------- imports ----------
import mysql.connector
from groq import Groq
import streamlit as st 

# ---------- set up ----------
# import credentials
HOST = "XXXX"
USER = "XXXX"            
PASSWORD = "XXXX"
DATABASE = "XXXX"

# connect to db
conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)
cursor = conn.cursor(dictionary=True) 

# groq api call
GROQ_API_KEY = "XXXX"
client = Groq(api_key=GROQ_API_KEY)

# ---------- functions ----------
def get_med_names():
    """
    Get medicine names from db to populate streamlit dropdown list
    """
    # execute query
    cursor.execute(
    "SELECT DISTINCT `Medicine Name` FROM Medicine_Details ORDER BY `Medicine Name`"
    )
    # fetch all results
    results = cursor.fetchall()
    # return as list
    return [row["Medicine Name"] for row in results]

def get_med_details(med_name):
    """
    Get specific medicine info from db, parameter: med_name
    Return formatted string to be outputed to GROQ
    """
    # write query to get info from db
    query = """
    SELECT `Composition`, `Uses`, `Side_effects`, `Manufacturer`, `Image URL`,
           `Excellent Review %`, `Average Review %`, `Poor Review %`
    FROM Medicine_Details
    WHERE `Medicine Name` = %s
    """

    # execute query and fetch query results
    cursor.execute(query, (med_name,))
    query_results = cursor.fetchall()
    # return none if no medicine found
    if not query_results:
        return None
    
    # get first row of table
    db_first_row = query_results[0]

    # what columns to display in output
    cols = [
        f"- Composition: {db_first_row['Composition']}",
        f"- Uses: {db_first_row['Uses']}",
        f"- Side Effects: {db_first_row['Side_effects']}",
        f"- Manufacturer: {db_first_row['Manufacturer']}",
        f"- Excellent Review %: {db_first_row['Excellent Review %']}",
        f"- Average Review %: {db_first_row['Average Review %']}",
        f"- Poor Review %: {db_first_row['Poor Review %']}"
    ]

    # Return formatted string
    return f"structured data for {med_name}:\n" + "\n".join(cols)

def prompt_to_groq(prompt, med_name=None, history=None):
    """
    Send user prompt to GROW API, including structured data about medicine from db
    Logs chat history, parameter: history
    """

    # initialize chat history
    if history is None:
        history = []

    # system message for chatbot to respond to non-med related prompts
    system_message = {
        "role": "system",
        "content": (
            "You are a chatbot called Drug Explorer to interact with users and respond to prompts about medications."
            "Use the structured medicine data provided to answer questions about medicines. "
            "For general conversation, respond naturally and politely."
            "Ask them if they have any questions or need details about a mediciation."
        )
    }
    
    # log chats to history
    # copy previous chats to history
    chats = [system_message] + history.copy() 

    # include structured data to user prompt
    if med_name:
        med_data = get_med_details(med_name)
        if med_data:
            chats.append({"role": "system", "content": f"Structured Data:\n{med_data}"})

    # add current chat
    chats.append({"role": "user", "content": prompt})

    # groq api call
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=chats,
        temperature=0.7,
        max_completion_tokens=1024,
        top_p=1
    )

    # get ai response
    response = completion.choices[0].message.content

    # append ai response to history
    history.append({"role": "user", "content": prompt})
    history.append({"role": "assistant", "content": response})

    return response

# ---------- streamlit ----------

# page title
st.set_page_config(page_title="Drug Explorer Chatbot", layout="wide")
st.markdown('<h1 style="color:#77B1D4;">Drug Explorer Chatbot</h1>', unsafe_allow_html=True)

# ---------- page background ----------

# style block to change colors and reorient
st.markdown(
    """
    <style>
    /* background color */
    .stApp { background-color: #ADD8E6; }

    /* user prompts box */
    .user-prompts {
        background-color: #77B1D4;
        padding: 10px;
        border-radius: 8px;
        float: right;           
        clear: both;          
        margin-bottom: 10px;
    }

    /* response box */
    .response {
        background-color: #77B1D4;
        padding: 10px;
        border-radius: 8px;
        text-align: right;
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# change color of header
header_style = """
    <style>
    /* Change top header bar color */
    header {background-color: #77B1D4;}
    </style>
"""
st.markdown(header_style, unsafe_allow_html=True)

# welcome text
st.markdown(
    """
    **Welcome to the Drug Explorer Chatbot!  
    This AI chatbot answers your questions about specific medications using data from our database.
    Please select a medicine from the dropdown below to get started.**
    """
)

# initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# dropdown list for all med names
med_list = get_med_names()
selected_med = st.selectbox("**Select a medicine:**", med_list)

    # ---------- scroll for past chats ----------

# container for chats
container = st.empty()

# display chats
def display_chats():
    """
    display for user prompts and corresponding responses
    """
    with container.container():
        
    # loop through chat history
        for i in range(0, len(st.session_state.history), 2):
            # get user prompt
            user = st.session_state.history[i]["content"]
            # get ai response
            # tries to get next message in history, if no message output empty string
            response = st.session_state.history[i+1]["content"] if i+1 < len(st.session_state.history) else ""

            # create divider between chats
            st.markdown('<hr style="height:3px; background-color:#FFFFFF; border:none;">', unsafe_allow_html=True)

            # display user prompt on right side
            # first col empty, second contains message
            cols = st.columns([1, 3])
            with cols[1]:
                st.markdown(f"<div class='user-prompts'>{user}</div>", unsafe_allow_html=True)

                # space after message
                st.text("")

            # display response on left
            # first col empty, second contains message
            cols = st.columns([3, 1])
            with cols[0]:
                st.markdown(f"<div class='user-prompts'>{response}</div>", unsafe_allow_html=True)

                # space after message
                st.text("")

display_chats()
            
# text input box

def input_box():
    # get input
    user_prompt = st.session_state.user_input

    if user_prompt.strip() != "":

        # get ai response from groq
        response = prompt_to_groq(
            prompt=user_prompt,
            med_name=selected_med,
            history=st.session_state.history
    )

        # reload chat display
        st.session_state.user_input = ""
        container.empty()
        display_chats()

user_prompt = st.text_input("**Type your message here:**", key="user_input", on_change=input_box)