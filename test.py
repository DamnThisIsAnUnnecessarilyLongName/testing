import streamlit as st

st.title("Running Average Calculator")

# Initialize the session state to store numbers
if "numbers" not in st.session_state:
    st.session_state.numbers = []

# Input box for a new number
new_number = st.number_input("Enter a number:", step=1.0)

# Button to add number
if st.button("Add number"):
    st.session_state.numbers.append(new_number)

# Display running average
if st.session_state.numbers:
    total = sum(st.session_state.numbers)
    count = len(st.session_state.numbers)
    average = total / count
    st.write(f"Numbers entered: {st.session_state.numbers}")
    st.write(f"Running average: {average}")
else:
    st.write("No numbers entered yet.")


