import streamlit as st  # type: ignore
from taskflowai import Task, set_verbosity  # type: ignore
import re
import base64
from PIL import Image
import requests
from io import BytesIO
from Agents.travel_report_agent import TravelReportAgent
from Agents.travel_agent import TravelAgent
from Agents.web_research_agent import WebResearchAgent
from logger.logger_config import logging
from exception.custom_exception import CustomException

st.set_page_config(
    page_title="Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Set verbosity for debugging purposes
set_verbosity(True)

# RTL support for Arabic text
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

    /* Set images to LTR and center-align them */
    img {
        direction: ltr;
        display: block;
        margin-left: auto;
        margin-right: auto;
        max-width: 100%;
        height: auto;
    }
    </style>
""", unsafe_allow_html=True)

# First, simplify the CSS by removing the white backgrounds and fixing contrast
st.markdown("""
    <style>
    .block-container {
        padding: 1rem;
        max-width: 960px;
        margin: 0 auto;
    }
    .section-header {
        margin: 1.5rem 0 1rem;
        padding: 0.5rem;
        background-color: #1e3a8a;
        color: white;
        border-radius: 0.3rem;
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

# Simplify the image formatting function to preserve markdown
def format_markdown_images(markdown_text):
    """
    Keep markdown image syntax intact and just ensure URLs are properly formatted
    """
    import re
    
    # Only process markdown images without converting to HTML
    img_pattern = r'!\[(.*?)\]\((.*?)\)'
    
    def fix_url(match):
        alt_text, url = match.groups()
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = f"https:{url}" if url.startswith('//') else f"https://{url}"
        # Validate the URL (basic validation for image extensions)
        valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
        if not any(url.lower().endswith(ext) for ext in valid_extensions):
            # Attempt to fix by appending a valid extension (fallback to .jpg)
            url += ".jpg"
        return f'![{alt_text}]({url})'
    
    return re.sub(img_pattern, fix_url, markdown_text)


def research_destination(destination, interests):
    """Research destination with enhanced image handling"""
    instruction = (
        f"Research and generate a comprehensive travel report about {destination}.\n"
        f"- Use Wikipedia tools to find 2-3 high-quality images of major landmarks\n"
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
        f"- Format event images as: ![Event Name](https://full-image-url)\n"
        f"- Format images as: ![Description](https://full-image-url)\n"
        f"- Make sure image URLs start with http:// or https://\n"
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
            context=f"Destination Report: {destination_report}\n\n"
                    f"Events Report: {events_report}\n\n"
                    f"Weather Report: {weather_report}\n\n"
                    f"Flight Report: {flight_report}",
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

def download_link(data, filename, text):
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text}</a>'
    return href

def main():
    st.title("🌍 دليل السفر العربي")
    
    with st.container():
        st.subheader("📝 تفاصيل الرحلة")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_location = st.text_input("مدينة المغادرة", placeholder="أدخل نقطة البداية")
            destination = st.text_input("مدينة الوجهة", placeholder="أدخل وجهتك")
            
        with col2:
            #dates = st.text_input("تواريخ السفر", placeholder="20-31 ديسمبر 2025")
            dates = st.date_input("📅 اختر تواريخ السفر:", [])
            dates = [d.strftime("%Y-%m-%d") for d in dates]
            interests = st.text_input("اهتماماتك", placeholder="المتاحف، الطعام، المشي...")

    plan_button = st.button("🚀 خطط رحلتي", type="primary", use_container_width=True)

    if plan_button:
        if current_location and destination and dates:
            try:
                st.success("🎈 جاري بدء تخطيط رحلتك!")
                st.balloons()

                sections = {
                    "destination": ("📍 معلومات الوجهة", research_destination),
                    "events": ("🎯 الفعاليات والأنشطة", research_events),
                    "weather": ("☀️ توقعات الطقس", research_weather),
                    "flights": ("✈️ خيارات الرحلات الجوية", search_flights)
                }

                reports = {}

                for key, (title, func) in sections.items():
                    with st.container():
                        st.markdown(f"<div class='section-header'><h3>{title}</h3></div>", 
                                  unsafe_allow_html=True)
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
                                formatted_content = format_markdown_images(reports[key])
                                st.markdown(formatted_content)
                            except Exception as e:
                                st.error(f"خطأ في عرض المحتوى: {str(e)}")
                                st.markdown(reports[key])

                st.markdown("<div class='section-header'><h3>📋 خطة السفر الكاملة</h3></div>", 
                          unsafe_allow_html=True)
                with st.spinner("جاري إنشاء التقرير النهائي..."):
                    final_report = write_travel_report(
                        reports["destination"],
                        reports["events"],
                        reports["weather"],
                        reports["flights"]
                    )
                    try:
                        formatted_final_report = format_markdown_images(final_report)
                        st.markdown(formatted_final_report)
                    except Exception as e:
                        st.error(f"خطأ في عرض التقرير النهائي: {str(e)}")
                        st.markdown(final_report)
                
                st.download_button(
                    label="📥 تحميل خطة السفر الكاملة",
                    data=final_report,
                    file_name=f"خطة_السفر_{destination.lower().replace(' ', '_')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )

                st.markdown(download_link("Your travel plan content", "travel_plan.pdf", "📥 تحميل خطة السفر"), unsafe_allow_html=True)

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