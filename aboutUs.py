import streamlit as st
from PIL import Image
import os

def aboutUs():
    # Define team members
    team_members = [
        {"name": "\n", "role": "\n"},
        {"name": "Aagman Bhatia", "role": "Data Scientist"},
        {"name": "Aditi Jaiswal", "role": "Data Scientist"},
        {"name": "Gul Bansal", "role": "Data Scientist"},
        {"name": "Kaustubh Rastogi", "role": "Data Scientist"},
        {"name": "Kushal Matalia", "role": "Data Scientist"},
        {"name": "Yash Mathur", "role": "Data Scientist"}
    ]

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define sections content
    sections = [
        {
            "title": "About Us",
            "content": "Integrative Forecasting: Predicting Company Growth and Stock Trends through Multi-Source Analysis of News Headlines, Earnings Calls, Annual Reports and Social Media Trends"
        },
        {
            "title": "Our Team",
            "content": "\n".join([
                f"**<span style='color:black;'>{member['name']}</span>**\n"
                f"*<span style='color:black;'>{member['role']}</span>*\n"
                for member in team_members[0:]
            ])
        },
        {
            "title": "Our Mission and Values",
            "content":
                "To empower individuals and organizations with insightful analysis and innovative solutions at the intersection of financial expertise, data science, and natural language processing, driving informed decision-making and enabling success in dynamic markets.<br>1. Integrity: Upholding honesty and ethical conduct.<br>2. Innovation: Embracing creativity and continuous improvement.<br>3. Collaboration: Fostering teamwork and diverse perspectives.<br>4. Excellence: Committing to quality and exceeding expectations.<br>5. Customer Focus: Understanding and fulfilling customer needs.<br>6. Empowerment: Providing opportunities for growth and leadership.<br>7. Social Responsibility: Operating responsibly and contributing positively to society and the environment."
        },
        {
            "title": "Contact Us",
            "content": "Email: riseai@gmail.com<br>Phone: +911234567890<br>Address: Plaksha University, Mohali"
        }
    ]

    # Create a 2x3 grid layout
    col1, col2 = st.columns(2)
    for i, section in enumerate(sections):
        if i % 2 == 0:
            col = col1
        else:
            col = col2
            col.write("---")

        with col:
            st.markdown(
                f"""
                <div style="border-radius: 10px; padding: 20px; background-color: #f0f0f0; box-shadow: 2px 2px 5px grey;">
                    <h4 style="color: #333;">{section['title']}</h4>
                    <p style="line-height: 1.5; color: #666;">{section['content']}</p>
                </div>
                <br>
                """,
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    aboutUs()
