import streamlit as st  # type: ignore
from taskflowai import Task, set_verbosity  # type: ignore
import base64
import re
import os
import requests
from PIL import Image
from io import BytesIO
from Agents.travel_report_agent import TravelReportAgent
from Agents.travel_agent import TravelAgent
from Agents.web_research_agent import WebResearchAgent
from logger.logger_config import logging
from exception.custom_exception import CustomException
import markdown2
from weasyprint import HTML
import tempfile

headers = {
    "authorization": st.secrets["GROQ_API_KEY",
                                "SERPER_API_KEY",
                                "AMADEUS_API_KEY",
                                "AMADEUS_API_SECRET",
                                "WEATHER_API_KEY",
                                "PEXELS_API_KEY"
                                ]
}

st.set_page_config(
    page_title="Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Set verbosity for debugging purposes
set_verbosity(True)


# First, simplify the CSS by removing the white backgrounds and fixing contrast
st.markdown("""
    <style>
    /* Set text direction to RTL */
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }
    .stTextInput>div>div>input {
        text-align: right;
    }
         
    /* Increase font size for text input labels */
    .stTextInput label {
        font-size: 2rem; /* Larger font size for labels */
        font-weight: bold; /* Make the labels bold */
    }

    /* Increase font size for date input labels */
    .stDateInput label {
        font-size: 2rem; /* Larger font size for labels */
        font-weight: bold; /* Make the labels bold */
    }

    .block-container {
        padding: 1rem;
        max-width: 960px;
        margin: 0 auto;
    }
    /* Set images to LTR and center-align them */
    .img {
        direction: ltr;
        display: block;
        margin-left: auto;
        margin-right: auto;
        max-width: 30%; /* Reduce the maximum width to 30% */
        height: 50%; /* Maintain aspect ratio */
        border-radius: 0.5rem; /* Add rounded corners for a polished look */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Add a subtle shadow */
    }
    /* Center section headers */
    .section-header {
        margin: 1.5rem 0 1rem;
        padding: 0.75rem;
        color: white;
        border-radius: 0.5rem;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center; /* Center-align the section header */
    }
    .content-section {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #e5e7eb;
        background-color: #1e293b;
        color: white;
    }
    .stTextInput {
        margin-bottom: 0.5rem;
    }
    .stButton button {
        margin: 1rem 0;
    }
    .stSuccess, .stError, .stWarning {
        padding: 0.75rem;
        border-radius: 0.3rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Define agents
reporter_agent = TravelReportAgent.initialize_travel_report_agent()
travel_agent = TravelAgent.initialize_travel_agent()
web_research_agent = WebResearchAgent.initialize_web_research_agent()


def generate_pdf(markdown_text, filename="trip_plan.pdf"):
    """
    Convert Markdown travel plan to a downloadable RTL PDF.
    """
    try:
        # Convert markdown to HTML
        html_content = markdown2.markdown(markdown_text)

        # Wrap HTML in a styled RTL container
        rtl_html = f"""
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    direction: rtl;
                    text-align: right;
                    font-family: 'Amiri', 'Cairo', 'Tahoma', sans-serif;
                    font-size: 14px;
                    line-height: 1.6;
                    margin: 2rem;
                }}
                h1, h2, h3, h4 {{
                    color: #1e3a8a;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                    display: block;
                    margin: 1rem auto;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Save PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            HTML(string=rtl_html).write_pdf(tmp_file.name)
            tmp_file.seek(0)
            pdf_data = tmp_file.read()

        return pdf_data

    except Exception as e:
        logging.error(f"❌ Failed to generate PDF: {e}")
        raise CustomException("حدث خطأ أثناء إنشاء ملف PDF")


# Function to display images or markdown content
def display_image_or_markdown(markdown_text):
    """
    Parses markdown for images and displays them safely.
    Falls back to st.image() if the markdown fails or URL is suspicious.
    """
    image_pattern = r'!\[(.*?)\]\((.*?)\)'
    parts = re.split(image_pattern, markdown_text)

    for i in range(0, len(parts), 3):
        try:
            # Regular text part
            st.markdown(parts[i], unsafe_allow_html=True)

            # If there's an image match
            if i + 2 < len(parts):
                alt_text = parts[i + 1]
                url = parts[i + 2].strip()

                if not url.startswith(("http://", "https://")):
                    if url.startswith("//"):
                        url = "https:" + url
                    else:
                        url = "https://" + url

                # Try to display using st.image() if suspicious
                if not any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']):
                    st.markdown(f"**{alt_text}**")
                    try:
                        response = requests.get(url, timeout=5)
                        image = Image.open(BytesIO(response.content))
                        new_image = image.resize((100, 50))
                        st.image(new_image)
                    except Exception as e:
                        st.warning(f"⚠️ تعذر تحميل الصورة: {alt_text}")
                else:
                    st.markdown(f"![{alt_text}]({url})", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"⚠️ حدث خطأ أثناء عرض جزء من المحتوى: {str(e)}")

def research_destination(destination, interests):
    """Research destination with enhanced image handling"""
    instruction = (
        f"Research and generate a comprehensive travel report about {destination}.\n"
        f"- Use Wikipedia tools to find 4-5 high-quality images of major landmarks\n"
        f"- Make sure that the query to the image tool is in english even if the user type it in arabic\n"
        f"- Ensure image links start with http:// or https://\n"
        f"- Format images as: ![Description](https://full-image-url)\n"
        f"- Add a short caption below each image\n"
        f"- Research attractions and activities related to: {interests}\n"
        f"- Organize the report with clear sections and headings\n"
        f"- Place images naturally in the content where relevant\n"
        f"- Include practical visitor information\n"
        f"- Format the entire response in clean Markdown\n"
        f"- **Important**: Write the final response entirely in Arabic."
    )
    try:
        task = Task.create(
            agent=web_research_agent,
            context=f"User Destination: {destination}\nUser Interests: {interests}",
            instruction=instruction
        )
        logging.info("Successfully created destination research task.")
        return task
    except Exception as e:
        logging.info(f"Failed to create destination research task: {str(e)}")
        raise CustomException(f"Error creating destination research task: {str(e)}")

def research_events(destination, dates, interests):
    """Research events with enhanced image handling"""
    instruction = (
        f"Search for events happening in {destination} during {dates} that match the following interests: {interests}.\n\n"
        f"For each event, include:\n"
        f"- Event name\n"
        f"- Date and time\n"
        f"- Venue/location\n"
        f"- Ticket information (if available)\n"
        f"- A short description of the event\n"
        f"- Make sure that the query to the image tool is in english even if the user type it in arabic\n"
        f"- Ensure image links start with http:// or https://\n"
        f"- Format event images as: ![Event Name](https://full-image-url)\n"
        f"- Format images as: ![Description](https://full-image-url)\n"
        f"- Ensure the information is accurate and up-to-date\n"
        f"- Place images naturally throughout the content where relevant\n"
        f"- Format the entire response in clean Markdown\n"
        f"- **Important**: Write the entire response in Arabic."
    )
    try:
        task = Task.create(
            agent=web_research_agent,
            context=f"Destination: {destination}\nDates: {dates}\nInterests: {interests}",
            instruction=instruction
        )
        logging.info("Successfully created events research task.")
        return task
    except Exception as e:
        logging.info(f"Failed to create events research task: {str(e)}")
        raise CustomException(f"Error creating events research task: {str(e)}")

def research_weather(destination, dates):
    """Research weather information"""
    try:
        task = Task.create(
            agent=travel_agent,
            context=f"Destination: {destination}\nDates: {dates}",
            instruction=(
                "Provide detailed weather information for the given destination and dates, including:\n"
                "1. Temperature ranges\n"
                "2. Precipitation chances\n"
                "3. General weather patterns\n"
                "4. Recommended clothing and gear\n"
                "\nRespond entirely in Arabic."
            )
        )
        logging.info("Successfully created weather research task.")
        logging.info(f"Weather task details: {task}")
        return task
    except Exception as e:
        logging.info(f"Failed to create weather research task: {str(e)}")
        raise CustomException(f"Error creating weather research task: {str(e)}")

def search_flights(current_location, destination, dates):
    """Search flight options"""
    try:
        task = Task.create(
            agent=travel_agent,
            context=f"Flights from {current_location} to {destination} on {dates}",
            instruction=(
                "Find the top 3 affordable and convenient flight options.\n"
                "Provide concise bullet-point information for each.\n"
                "Include airline, departure and arrival times, duration, and price if available.\n"
                "Respond entirely in Arabic."
            )
        )
        logging.info("Successfully created flight search task.")
        return task
    except Exception as e:
        logging.info(f"Failed to create flight search task: {str(e)}")
        raise CustomException(f"Error creating flight search task: {str(e)}")

def write_travel_report(destination_report, events_report, weather_report, flight_report):
    """Create final travel report"""
    try:
        task = Task.create(
            agent=reporter_agent,
            context=f"Flight Report: {flight_report}"
                    f"Weather Report: {weather_report}\n\n"
                    f"Destination Report: {destination_report}\n\n"
                    f"Events Report: {events_report}",
            instruction=(
                "Create a comprehensive travel report that includes the following:\n"
                "1. Retain all images from the destination and events reports.\n"
                "2. Organize the information clearly and logically.\n"
                "3. Maintain all markdown formatting.\n"
                "4. Ensure images are displayed correctly with captions.\n"
                "5. Include all essential details from each section.\n\n"
                "Respond entirely in Arabic."
            )
        )
        logging.info("Successfully created travel report.")
        return task
    except Exception as e:
        logging.info(f"Failed to create travel report: {str(e)}")
        raise CustomException(f"Error creating travel report: {str(e)}")

def main():
    st.markdown("""
    <h1 style='margin-top: 3rem; text-align: center;'>
        🌍 دليل السفر العربي
    </h1>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.subheader("📝 تفاصيل الرحلة")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_location = st.text_input("مدينة المغادرة", placeholder="أدخل نقطة البداية")
            destination = st.text_input("مدينة الوجهة", placeholder="أدخل وجهتك")
            
        with col2:
            dates = st.date_input("📅 اختر تواريخ السفر:", [])
            dates = [d.strftime("%Y-%m-%d") for d in dates]
            interests = st.text_input("اهتماماتك", placeholder="المتاحف، الطعام، المشي...")

    plan_button = st.button("🚀 خطط رحلتي", type="primary", use_container_width=True)

    if plan_button:
        if current_location and destination and dates:
            try:
                st.success("🎈 جاري بدء تخطيط رحلتك!")

                # Create tabs for each section
                tab_titles = ["📍 معلومات الوجهة", "🎯 الفعاليات والأنشطة", "☀️ توقعات الطقس", "✈️ خيارات الرحلات الجوية", "📋 خطة السفر الكاملة"]
                tabs = st.tabs(tab_titles)

                sections = {
                    "destination": ("📍 معلومات الوجهة", research_destination),
                    "events": ("🎯 الفعاليات والأنشطة", research_events),
                    "weather": ("☀️ توقعات الطقس", research_weather),
                    "flights": ("✈️ خيارات الرحلات الجوية", search_flights)
                }

                reports = {}

                # Populate each tab with its respective content
                for i, (key, (title, func)) in enumerate(sections.items()):
                    with tabs[i]:
                        st.markdown(f"<div class='section-header'><h3>{title}</h3></div>", unsafe_allow_html=True)
                        with st.spinner(f"جاري تحميل {title.lower()}..."):
                            if key == "destination":
                                reports[key] = func(destination, interests)
                            elif key == "events":
                                reports[key] = func(destination, dates, interests)
                            elif key == "weather":
                                reports[key] = func(destination, dates)
                            else:  # flights
                                reports[key] = func(current_location, destination, dates)

                            try:
                                display_image_or_markdown(reports[key])
                            except Exception as e:
                                st.error(f"خطأ في عرض المحتوى: {str(e)}")
                                st.markdown(reports[key])

                # Final travel plan tab
                with tabs[-1]:
                    st.markdown("<div class='section-header'><h3>📋 خطة السفر الكاملة</h3></div>", unsafe_allow_html=True)
                    with st.spinner("جاري إنشاء التقرير النهائي..."):
                        final_report = write_travel_report(
                            reports["flights"],
                            reports["weather"],
                            reports["destination"],
                            reports["events"]    
                        )
                        try:
                            display_image_or_markdown(final_report)
                        except Exception as e:
                            st.error(f"خطأ في عرض التقرير النهائي: {str(e)}")
                            st.markdown(final_report)

                    st.download_button(
                        label="📥 تحميل خطة السفر الكاملة (PDF)",
                        data=generate_pdf(final_report, f"خطة_السفر_{destination.lower().replace(' ', '_')}.pdf"),
                        file_name=f"خطة_السفر_{destination.lower().replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"🚨 حدث خطأ: {str(e)}")
                print(f"تفاصيل الخطأ: {str(e)}")
        else:
            st.warning("🔔 يرجى ملء جميع الحقول المطلوبة")

    st.markdown("""
        <p style='text-align: center; color: #666666; margin-top: 2rem;'>
            رحلة سعيدة! 🌟
        </p>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()