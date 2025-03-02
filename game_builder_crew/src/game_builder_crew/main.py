#!/usr/bin/env python

import sys
import yaml
from game_builder_crew.crew import GameBuilderCrew
import streamlit as st
import os



def run(inputs):
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    print("## Welcome to the Game Crew")
    print('-------------------------------')
    if inputs is None:

        with open('src/game_builder_crew/config/gamedesign.yaml', 'r', encoding='utf-8') as file:
            examples = yaml.safe_load(file)
    
        inputs = {
            'game' :  examples['example3_snake']
        }

    # Get the CrewAI output
    crew_output = GameBuilderCrew().crew().kickoff(inputs=inputs)
    
    # Extract the generated game code (Convert CrewOutput to string)
    if hasattr(crew_output, 'text'):
        return crew_output.text  # If CrewOutput has a `.text` attribute, return its string content
    else:
        return str(crew_output)  # Otherwise, convert it to string just in case

    # print("\n\n########################")
    # print("## Here is the result")
    # print("########################\n")
    # print("final code for the game:")
    # print(game)
    

def train():
    """
    Train the crew for a given number of iterations.
    """

    with open('src/game_builder_crew/config/gamedesign.yaml', 'r', encoding='utf-8') as file:
        examples = yaml.safe_load(file)

    inputs = {
        'game' : examples['example1_pacman']
    }
    try:
        GameBuilderCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
        

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
    


def main():
    st.set_page_config(page_title="Game Builder Crew", layout="wide")
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Game Builder Crew</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555;'>Generate your game code interactively</h3>", unsafe_allow_html=True)

    # Load game design examples
    try:
        with open('src/game_builder_crew/config/gamedesign.yaml', 'r', encoding='utf-8') as file:
            examples = yaml.safe_load(file)
    except Exception as e:
        st.error(f"Error loading YAML file: {e}")
        return

    example_keys = list(examples.keys())
    default_index = example_keys.index("example3_snake") if "example3_snake" in example_keys else 0
    selected_example_key = st.selectbox("Select a game design example", example_keys, index=default_index)

    st.markdown("### Selected Game Design")
    st.code(yaml.dump(examples[selected_example_key]), language="yaml")

    # Button to generate game code
    if st.button("Generate Game Code"):
        with st.spinner("Generating game code..."):
            inputs = {'game': examples[selected_example_key]}
            game_code = run(inputs)

            # Save the generated code to a file dynamically
            file_name = f"{selected_example_key}.py"
            file_path = os.path.join("generated_games", file_name)
            
            # Ensure the directory exists
            os.makedirs("generated_games", exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(game_code.strip())

            st.success(f"Game code generated successfully! The file has been saved as `{file_name}`")

            # Provide a download link for the generated file
            with open(file_path, "r", encoding="utf-8") as f:
                st.download_button(
                    label="Download Game Code",
                    data=f,
                    file_name=file_name,
                    mime="text/plain"
                )

            # Display instructions to run the game
            st.markdown("### How to Run the Game")
            st.markdown(f"""
                1. **Download** the generated `{file_name}` file.
                2. **Install Pygame** if you haven't already:  
                   ```
                   pip install pygame
                   ```
                3. **Run the game** using the command:  
                   ```
                   python {file_name}
                   ```
            """)

if __name__ == "__main__":
    main()


def run_streamlit_app():
    import sys
    import streamlit.web.cli
    print(__file__)
    # Prepare the sys.argv list so that Streamlit knows which file to run.
    sys.argv = ["streamlit", "run", __file__]
    streamlit.web.cli.main()