#!/usr/bin/env python
import asyncio
from typing import List
import uuid
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from write_a_book_with_flows.crews.write_book_chapter_crew.write_book_chapter_crew import WriteBookChapterCrew
from write_a_book_with_flows.crews.outline_book_crew.outline_crew import OutlineCrew
from write_a_book_with_flows.types import Chapter, ChapterOutline
import asyncio
import streamlit as st


class BookState(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    title: str = "The Current State of AI in March 2025"
    book: List[Chapter] = []
    book_outline: List[ChapterOutline] = []
    topic: str = (
        "Exploring the latest trends in AI across different industries as of March 2025"
    )
    goal: str = """
        The goal of this book is to provide a comprehensive overview of the current state of artificial intelligence in March 2025.
        It will delve into the latest trends impacting various industries, analyze significant advancements,
        and discuss potential future developments. The book aims to inform readers about cutting-edge AI technologies
        and prepare them for upcoming innovations in the field.
    """


class BookFlow(Flow[BookState]):
    initial_state = BookState

    @start()
    def generate_book_outline(self):
        st.info("Generating Book Outline...")
        output = (
            OutlineCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic, "goal": self.state.goal})
        )

        chapters = output["chapters"]

        self.state.book_outline = chapters
        return chapters

    @listen(generate_book_outline)
    async def write_chapters(self):
        tasks = []

        async def write_single_chapter(chapter_outline):
            output = (
                WriteBookChapterCrew()
                .crew()
                .kickoff(
                    inputs={
                        "goal": self.state.goal,
                        "topic": self.state.topic,
                        "chapter_title": chapter_outline.title,
                        "chapter_description": chapter_outline.description,
                        "book_outline": [
                            chapter_outline.model_dump_json()
                            for chapter_outline in self.state.book_outline
                        ],
                    }
                )
            )
            title = output["title"]
            content = output["content"]
            chapter = Chapter(title=title, content=content)
            return chapter

        st.markdown("<h3 style='font-size: 24px;'>Book Outline</h3>", unsafe_allow_html=True)

        for chapter_outline in self.state.book_outline:
            st.write(f"Chapter Title: {chapter_outline.title}")
            st.write(f"Description: {chapter_outline.description}")
            # Schedule each chapter writing task
            task = asyncio.create_task(write_single_chapter(chapter_outline))
            tasks.append(task)

        # Await all chapter writing tasks concurrently
        st.info("Writing Book Chapters...")
        chapters = await asyncio.gather(*tasks)
        st.write(f"<h3 style='font-size: 24px;'>Newly generated chapters:</h3>", unsafe_allow_html=True)
        for chapter in chapters:
            st.write(f"Chapter Title: {chapter.title}")
            st.write(f"Content: {chapter.content}")
        self.state.book.extend(chapters)

    @listen(write_chapters)
    async def join_and_save_chapter(self):
        st.info("Joining and Saving Book Chapters...")
        # Combine all chapters into a single markdown string
        book_content = ""

        for chapter in self.state.book:
            # Add the chapter title as an H1 heading
            book_content += f"# {chapter.title}\n\n"
            # Add the chapter content
            book_content += f"{chapter.content}\n\n"

        # The title of the book from self.state.title
        book_title = self.state.title

        # Create the filename by replacing spaces with underscores and adding .md extension
        filename = f"./{book_title.replace(' ', '_')}.md"
        
        # Save the combined content into the file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(book_content)

        st.write(f"<h3 style='font-size: 24px;'>Book saved as {filename}</h4>", unsafe_allow_html=True)



# Define a helper function to run the asynchronous book flow using asyncio.
def run_book_flow(title: str, topic: str, goal: str):
    # Instantiate BookFlow and update the state with user-provided values.
    book_flow = BookFlow()
    book_flow.state.title = title
    book_flow.state.topic = topic
    book_flow.state.goal = goal

    # Run the asynchronous kickoff process.
    book_flow.kickoff()

    # Return the filename and the book content for display/download.
    filename = f"./{book_flow.state.title.replace(' ', '_')}.md"
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    return filename, content


def main():
    st.title("Dynamic AI Book Generator")
    st.write("Enter the details for your book and generate an AI-driven book on the current state of AI.")

    # Capture user input for title, topic, and goal
    title = st.text_input("Book Title", "The Current State of AI in March 2025")
    topic = st.text_area("Book Topic", "Exploring the latest trends in AI across different industries as of March 2025")
    goal = st.text_area(
        "Book Goal",
        """
        The goal of this book is to provide a comprehensive overview of the current state of artificial intelligence in March 2025.
        It will delve into the latest trends impacting various industries, analyze significant advancements,
        and discuss potential future developments. The book aims to inform readers about cutting-edge AI technologies
        and prepare them for upcoming innovations in the field.
        """
    )

    # When the button is pressed, create a new BookState and run the flow
    if st.button("Generate Book"):
        with st.spinner("Generating your book... This may take a few moments."):
            try:
                filename, content = run_book_flow(title, topic, goal)
                st.success("Book generation complete!")

                # Display the generated book content
                st.text_area("Generated Book", content, height=300)

                # Provide a download button for the markdown file.
                st.download_button("Download Book", content, file_name=filename.split("/")[-1])
            except Exception as e:
                st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

def kickoff():
    book_flow = BookFlow()
    book_flow.kickoff()

def run_streamlit_app():
    import sys
    import streamlit.web.cli
    print(__file__)
    # Prepare the sys.argv list so that Streamlit knows which file to run.
    sys.argv = ["streamlit", "run", __file__]
    streamlit.web.cli.main()


# def plot():
#     book_flow = BookFlow()
#     book_flow.plot()


# if __name__ == "__main__":
#     kickoff()