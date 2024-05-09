import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from twilio.rest import Client

# Database setup
DATABASE_URL = "sqlite:///app.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    mobile_number = Column(String)
    whatsapp_number = Column(String)
    email = Column(String)
    locality = Column(String)
    classification = Column(Enum('A', 'B', 'C'))

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Twilio setup
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_phone_number = 'your_twilio_phone_number'
client = Client(account_sid, auth_token)

# Streamlit app
def main():
    st.title("User Data Collection App")
    
    # Form to collect user data
    st.subheader("User Information")
    name = st.text_input("Name")
    mobile_number = st.text_input("Mobile Number")
    whatsapp_number = st.text_input("WhatsApp Number")
    email = st.text_input("Email")
    locality = st.text_input("Locality")
    
    if st.button("Submit"):
        # Store user data in the database
        db = SessionLocal()
        new_user = User(name=name, mobile_number=mobile_number, whatsapp_number=whatsapp_number, email=email, locality=locality)
        db.add(new_user)
        db.commit()
        st.success("User data submitted successfully!")
        
    # Owner classification
    st.subheader("Owner Classification")
    user_list = db.query(User).all()
    for user in user_list:
        classification = st.selectbox(f"Classification for {user.name}", ['A', 'B', 'C'])
        user.classification = classification
    db.commit()
    st.success("User classification updated successfully!")
    
    # WhatsApp message sending functionality
    if st.button("Send WhatsApp Message"):
        for user in user_list:
            if user.whatsapp_number:
                send_whatsapp_message(user.whatsapp_number, "Your Shop Card PDF: <PDF_Link_Here>")
        st.success("WhatsApp messages sent successfully!")

def send_whatsapp_message(to_number, message):
    message = client.messages.create(
        from_='whatsapp:' + twilio_phone_number,
        body=message,
        to='whatsapp:' + to_number
    )

if __name__ == "__main__":
    main()
