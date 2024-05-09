import streamlit as st
import pandas as pd
import pywhatkit
import requests
##pywhatkit.start_server()

# Data storage
user_data = pd.DataFrame(columns=["Name", "Mobile Number", "WhatsApp Number", "Email", "Locality", "Classification"])

# Streamlit app
def main():
    st.title("Shopkeeper Messaging Portal")
    
    # Form to collect user data
    st.subheader("User Information")
    name = st.text_input("Name")
    mobile_number = st.text_input("Mobile Number")
    whatsapp_number = st.text_input("WhatsApp Number")
    email = st.text_input("Email")
    locality = st.text_input("Locality")
    
    if st.button("Submit"):
        # Store user data
        global user_data
        new_user = pd.DataFrame({"Name": [name], "Mobile Number": [mobile_number], "WhatsApp Number": [whatsapp_number], "Email": [email], "Locality": [locality], "Classification": [""]})
        user_data = pd.concat([user_data, new_user], ignore_index=True)
        st.success("User data submitted successfully!")
        
    # Owner classification
    st.subheader("Owner Classification")
    classification_options = ['A', 'B', 'C']
    for index, user in user_data.iterrows():
        classification = st.selectbox(f"Classification for {user['Name']}", classification_options, key=f"classification_{index}")
        user_data.at[index, "Classification"] = classification
    st.success("User classification updated successfully!")
    
    # WhatsApp message sending functionality
    if st.button("Send WhatsApp Message"):
        for index, user in user_data.iterrows():
            if user['WhatsApp Number']:
                message = f"Hello {user['Name']}, thank you for being our customer! We have classified you as Class {user['Classification']}."
                send_whatsapp_message(user['WhatsApp Number'], message)
        st.success("WhatsApp messages sent successfully!")




def send_whatsapp_message(to_number, message):
    # Dummy implementation to simulate sending WhatsApp message
    # Replace this with your actual implementation

    # Format the message
    formatted_message = f"Sending message to {to_number}: {message}"

    # Print the formatted message
    print(formatted_message)
    
# Send a WhatsApp Message to a Contact at 1:30 PM
    pywhatkit.sendwhatmsg("+918928304380", "Hi", 22, 29)    
    # Simulate sending the message
    # In a real implementation, you would use an API to send WhatsApp messages
    # This is just a placeholder to demonstrate the function
    # Replace the URL with the actual API endpoint for sending WhatsApp messages
    # api_url = "https://your-whatsapp-api.com/send_message"
    # payload = {
    #     "to_number": to_number,
    #     "message": message
    # }
    # response = requests.post(api_url, json=payload)

    # # Check if the message was sent successfully
    # if response.status_code == 200:
    #     print("Message sent successfully!")
    # else:
    #     print("Failed to send message. Please check your implementation.")

if __name__ == "__main__":
    main()
