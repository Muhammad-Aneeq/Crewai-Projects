import sys
import warnings
from datetime import datetime
from shoping_agent.crew import ShoppingAgentCrew
import streamlit as st
from shoping_agent.tools.dummy_data import dummy_products
from crewai import Task

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Initialize session state variables if not already set
if "conversation" not in st.session_state:
    st.session_state.conversation = []  # Stores messages like "User: ..." and "Agent: ..."
if "user_id" not in st.session_state:
    st.session_state.user_id = "user123"
if "crew_instance" not in st.session_state:
    st.session_state.crew_instance = ShoppingAgentCrew()

# Dummy inventory data
if "inventory" not in st.session_state:
    st.session_state.inventory = dummy_products

# Initialize phase if not set
if "phase" not in st.session_state:
    st.session_state.phase = "start"  # or "greeting" depending on your requirement

# Function to update conversation history
def update_conversation(role, message):
    if role.lower() == "user":
        prefix = "👤"
    else:
        prefix = "🤖"
    st.session_state.conversation.append(f"{prefix} {message}")

def display_conversation():
    st.write("### Conversation History:")
    for msg in st.session_state.conversation:
        st.write(msg)

def reset_conversation():
    st.session_state.conversation = []
    st.session_state.user_id = "user123"
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# Function to trigger orchestration
def process_order(inputs):
    with st.spinner("Processing your request..."):
        try:
            crew = st.session_state.crew_instance.crew()
            # Now the orchestrator dynamically decides which agent should take action
            crew_response = crew.kickoff(inputs=inputs)
        except Exception as e:
            crew_response = f"An error occurred: {e}"
    update_conversation("Agent", crew_response)
    return crew_response

def update_inventory(product_name, quantity):
    # Iterate through the inventory list to find the matching product by name
    for product in st.session_state.inventory:
        if product["name"] == product_name:
            # Update the quantity, ensuring it doesn't go below zero
            product["quantity"] -= quantity
            if product["quantity"] < 0:
                product["quantity"] = 0
            break
    else:
        st.warning(f"Product {product_name} not found in inventory.")

def show_inventory():
    st.write("### Inventory")
    # Display inventory in grid format for a cleaner look
    col1, col2, col3 = st.columns(3)
    with col1:
        for product in st.session_state.inventory[:7]:
            st.write(f"**{product['name']}**: {product['quantity']} in stock, Price: {product['price']}")
    
    with col2:
        for product in st.session_state.inventory[7:14]:
            st.write(f"**{product['name']}**: {product['quantity']} in stock, Price: {product['price']}")
    
    with col3:
        for product in st.session_state.inventory[14:]:
            st.write(f"**{product['name']}**: {product['quantity']} in stock, Price: {product['price']}")

def main():
    st.title("Shopping Assistant Chat")
    
    # Display inventory button
    if st.button("View Inventory"):
        show_inventory()

    # Always display conversation history at the top
    display_conversation()

    # Start Phase: Show "Start" button to begin the conversation
    if st.session_state.phase == "start":
        if st.button("Start Conversation"):
            st.session_state.phase = "greeting"
    
    # GREETING PHASE: The assistant sends a greeting message.
    if st.session_state.phase == "greeting":
        greeting_text = (
            "Hello there! I'm your personal shopping assistant, here to help you with your shopping needs. "
            "I can help you search for products, compare prices, and answer any questions you might have. "
            "Let's get started!"
        )
        update_conversation("Agent", greeting_text)
        st.session_state.phase = "input"
    
    # INPUT PHASE: Display a form for the user to enter dynamic details.
    if st.session_state.phase == "input":
        st.write("### Please Enter Your Details")
        with st.form(key="input_form", clear_on_submit=True):
            product_preference = st.text_input("Product Preference", "", help="e.g., Toothbrush, Laptop")
            user_query = st.text_input("Additional Details", "", help="Any extra information about your query")
            user_id = st.text_input("User ID", st.session_state.user_id, help="Your unique user identifier")
            submitted = st.form_submit_button("Submit")
        
        if submitted:
            st.session_state.user_id = user_id

            # Build the input dictionary
            inputs = {
                "product_preference": product_preference,
                "user_query": user_query,
                "user_id": st.session_state.user_id,
                "cart_action": "create",  # This creates an empty cart.
                "cart_data": []   
            }

            # Append the user submission to the conversation history.
            update_conversation("User", f"Product: '{product_preference}', Query: '{user_query}', User ID: '{user_id}'")

            # Process the order with the provided inputs using orchestration
            final_output = process_order(inputs)

            st.write("### Final Output:")
            st.markdown(final_output)

            # After the order, update the inventory
            update_inventory(product_preference, 1)  # Decrease the quantity by 1 for now (hardcoded to 1)

            # Show updated inventory after order
            st.write("### Updated Inventory:")
            show_inventory()

if __name__ == "__main__":
    main()


def run():
    """
    Run the shopping crew.
    """
    inputs = {
    'product_preference': "wireless headphones with noise-cancelling",  # Explicit value passed here
    'user_query': "Looking for a high-quality audio experience.",
    'user_id': "user123",
    "cart_action": "create",  # This creates an empty cart.
    "cart_data": []    
}
    
    try:
        ShoppingAgentCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        # If the exception indicates the product is not available, output that final result.
        if "Product not available" in str(e):
            print("Final Answer: The product you are looking for is not available. Please refine your search criteria.")
        else:
            raise Exception(f"An error occurred while running the crew: {e}")
    

def train():
    """
    Train the crew for a given number of iterations.
    """
 
    inputs = {
    'product_preference': "wireless headphones with noise-cancelling",  # Explicit value passed here
    'user_query': "Looking for a high-quality audio experience.",
    'user_id': "user123" 
}
    try:
        ShoppingAgentCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ShoppingAgentCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        ShoppingAgentCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_streamlit_app():
    import sys
    import streamlit.web.cli
    print("__file__>>>",__file__)
    # Prepare the sys.argv list so that Streamlit knows which file to run.
    sys.argv = ["streamlit", "run", __file__]
    streamlit.web.cli.main()
