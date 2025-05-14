# Arabic Travel Guide 🌍✈️

Travel Guide is a web-based application built with Streamlit that helps Arabic users plan their trips efficiently. It provides features like destination research, weather forecasts, flight options, and a complete travel itinerary. The app is designed with a user-friendly interface and supports right-to-left (RTL) text for Arabic users.

---

## Architecture Diagram

The system follows a modular agent-based structure as shown in the figure below:

![image](https://github.com/user-attachments/assets/960fc026-98dc-4180-a4f1-df3952c12b8d)

---

## User Interface Preview

![image](https://github.com/user-attachments/assets/c87a7923-6c7e-43cd-b785-0a919befd5f8)

---

## Sample Output

Here’s some examples of the generated travel report:

![image](https://github.com/user-attachments/assets/ac3251ae-3b17-41f8-95cd-2dd27e673e6c)
![image](https://github.com/user-attachments/assets/16b6ac0a-226f-433f-97c2-0c1e45d36b57)
![image](https://github.com/user-attachments/assets/f6ca1ee1-689a-4ec2-9b95-d462ad7e833d)
![image](https://github.com/user-attachments/assets/071fc869-0253-4d9e-a774-a068ac2c6edd)
![image](https://github.com/user-attachments/assets/f4e00120-0f2a-4725-a66f-80b999c8cc5d)

---

## Features

- **Destination Information**: Get detailed information about your travel destination.
- **Event Suggestions**: Discover activities and events happening at your destination for your travel period.
- **Weather Forecasts**: View weather predictions for your travel dates.
- **Flight Options**: Search for flights between your departure and destination cities.
- **Travel Itinerary**: Generate and download a complete travel plan in PDF format.
- **Image Search**: Fetch relevant images for your destination using Pexels API.
- **Web Research**: Perform web searches for additional information.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/sandysamiir/Arabic-Travel-Guide.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
- Create a `.env` file in the root directory.
- Add the following keys:
  ```env
  GROQ_API_KEY="your_groq_api_key"
  SERPER_API_KEY="your_serper_api_key"
  AMADEUS_API_KEY="your_amadeus_api_key"
  AMADEUS_API_SECRET="your_amadeus_api_secret"
  WEATHER_API_KEY="your_weather_api_key"
  PEXELS_API_KEY="your_pexels_api_key"
  ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```
---

## Project structure
- Arabic-Travel-Guide/
  - Agents/
    - travel_agent.py
    - travel_report_agent.py
    - web_research_agent.py
  - exception/
    - custom_exception.py
  - logger/
    - logger_config.py
  - tools/
    - search_flights.py
    - search_articles.py
    - serper_search.py
    - get_weather_data.py
    - search_images.py
  - utils/
    - main_utils.py
  - app.py
  - requirements.txt
  - README.md

### Key files

| File | Description |
|------|-------------|
| `app.py` | Main application file for the Streamlit app. |
| `Agents/` | Contains agent classes for handling specific tasks like travel planning and web research. |
| `tools/` | Includes tools for fetching flights, weather data, articles, and images. |
| `exception` | Custom exception handling logic. |
| `logger/` | Logging configuration for debugging and monitoring. |
| `utils/` | Utility functions and environment variable validation. |

---

## Usage

1. Open the app in your browser after running it with streamlit run app.py.
2. Fill in the required fields:
   - مدينة المغادرة
   - مدينة الوجهة
   - اختر تواريخ السفر
   - اهتماماتك (مثل: المتاحف، الطعام، الشواطئ...)
4. Click on the "🚀 خطط رحلتي" button to generate your travel plan.
5. Explore the tabs for 📍 معلومات الوجهة 🎯 الفعاليات والأنشطة ☀️ توقعات الطقس and ✈️ خيارات الرحلات الجوية.
6. Download the complete travel itinerary as a PDF.

---

## Future Enhancements

- Add support for more APIs (e.g., hotel booking, car rentals).
- Improve the UI/UX with additional themes and layouts.
- Add multi-language support for more languages.
