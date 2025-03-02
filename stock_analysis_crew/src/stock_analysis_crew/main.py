import sys
from stock_analysis_crew.crew import StockAnalysisCrew
import streamlit as st
import time

def run(inputs):
    if inputs is None:

        inputs = {
            'query': 'What is the company you want to analyze?',
            'company_stock': 'AMZN',
        }
    return StockAnalysisCrew().crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'query': 'What is last years revenue',
        'company_stock': 'AMZN',
    }
    try:
        StockAnalysisCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
    

def main():
    st.title("Stock Analysis Crew App")
    st.write("Enter your company stock symbol to run the analysis.")

    # Input fields for query and company stock symbol
    # query = st.text_input("Query", "What is the company you want to analyze?")
    company_stock = st.text_input("Company Stock Symbol", "AMZN")
    
    if st.button("Run Analysis"):
        # Prepare inputs for the Crew AI agent
        inputs = {
            'query': "What is the company you want to analyze?",
            'company_stock': company_stock,
        }

        with st.spinner('The crew is analyzing the stock...'):
            # Simulate processing time if needed
            time.sleep(1)
            result = result = run(inputs)
            time.sleep(0.5)

        # Display the final report
        st.markdown("### Analysis Report")
        st.markdown(result)
        
        
        # # Call the agent and display the result
        # # result = StockAnalysisCrew().crew().kickoff(inputs=inputs)
        
        # st.markdown("### Analysis Report")
        # st.write(result)

if __name__ == "__main__":
    main()

def run_streamlit_app():
    import sys
    import streamlit.web.cli
    print(__file__)
    # Prepare the sys.argv list so that Streamlit knows which file to run.
    sys.argv = ["streamlit", "run", __file__]
    streamlit.web.cli.main()
# if __name__ == "__main__":
#     print("## Welcome to Stock Analysis Crew")
#     print('-------------------------------')
#     result = run()
#     print("\n\n########################")
#     print("## Here is the Report")
#     print("########################\n")
#     print(result)