# 🤰 Prenatal Care Web-Application for Expectant Mothers

## 📌 Overview
This is a specialized web application designed to support expectant mothers throughout their pregnancy journey.  
The platform provides **personalized health tracking**, **nutrition guidance**, **pregnancy journaling**, **AI-powered assistance**, and **educational resources** — all in one easy-to-use interface.

Users can:
- Securely sign up and log in.
- Track important health metrics such as blood group, address, and expected birth date.
- Access tailored nutrition and fitness recommendations.
- Maintain a pregnancy journal.
- Get instant guidance from an AI chatbot.
- Use a built-in calendar to track appointments.
- Browse FAQs and educational materials for pregnancy wellness.

---

## 🚀 Features
👩‍⚕️ **Health Tracking** – Record blood group, expected birth date, and personal details.  
🥗 **Nutrition & Fitness** – Personalized wellness tips through the NutriFit module.  
📓 **Pregnancy Journal** – Private space for notes and reflections.  
🤖 **AI Chatbot** – Get immediate assistance for pregnancy-related queries.  
📅 **Calendar** – Keep track of medical appointments and key dates.  
📚 **Educational Resources** – FAQs, articles, and wellness guidance.  
🎵 **Relaxation Resources** – Music and book recommendations for stress relief.  
🔐 **User Authentication** – Secure signup/login system with SQLite database.  

---

## 🛠️ Tech Stack
**Frontend:** HTML5, CSS3, JavaScript  
**Backend:** Python (Flask Framework)  
**Database:** SQLite (persistent user data storage)  
**Other:** Flask-CORS for cross-origin requests  

---

## 📂 Project Structure
├── main.html
├── login.html
├── signup.html
├── calendar.html
├── health tracker page.html
├── NutriFit.html
├── journal.html
├── chatbot page.html
├── education.html
├── music and books page.html
├── faqs page.html
├── login.py
└── users.db

## ⚙️ Installation & Setup
1. Clone the Repository
git clone https://github.com/mahaksgoel-byte/Prenatal-Care-Web-Application-for-Expectant-Mothers.git
cd Prenatal-Care-Web-Application-for-Expectant-Mothers

2. Install Dependencies
pip install flask flask-cors

3. Run the Server
python login.py

Server runs on: http://127.0.0.1:5000

4. Open the Application
Open main.html or other pages via a local server (not directly from file://).

🐞 Challenges Faced
User Authentication Setup
Initially struggled to implement secure signup/login using SQLite.
Resolved by designing proper database schemas with unique email constraints.
Frontend–Backend Integration
Forms weren’t sending data because the Flask backend wasn’t running or API paths were wrong.
Fixed by aligning API routes and ensuring the backend server was active.
CORS Issues
Fetch requests failed when opening HTML directly from the file system.
Solved by adding flask-cors and serving the site from a local HTTP server.
Database Path Errors
Backend couldn’t locate users.db when run from different directories.
Fixed by using absolute paths and consistent working directories.

📸 Screenshots
(Add screenshots of key pages here — dashboard, health tracker, chatbot, etc.)

💡 Future Improvements
Push notifications for appointment reminders.
Encrypted password storage.

📜 License
This project is licensed under the Apache License.

🔗 GitHub Repository: https://github.com/mahaksgoel-byte/Prenatal-Care-Web-Application-for-Expectant-Mothers
