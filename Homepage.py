import streamlit as st

def app():
    st.title('Welcome to Melanoma_AI')
    st.markdown(
        """
        <div style='text-align: center; padding: 20px; background-color: #c52a4f; border-radius: 10px;'>
            <h2 style='color: #ffffff;'>Real-Time Melanoma Skin Cancer Detection</h2>
            <p style='color: #ffffff;'>Upload an image or use real-time detection to identify potential melanoma skin cancer.</p>
            <p style='color: #ffffff;'>Our advanced AI technology provides accurate and fast results to assist in early detection.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    choice = st.selectbox('Login/Signup',['Login','Sign Up'])

    if choice == 'Login':
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            try:
                # Authenticate user
                st.success('Login Successful')
            except:
                st.warning('Login failed')
    else:
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        username = st.text_input('Enter your unique username')
        if st.button('Create My Account'):
            # Create user account
            st.success('Account created successfully!')
            st.markdown('Please Login using your email and password')
            st.balloons()

# Call the app function
app()
