# Smart Failure Detection with Machine Learning

##  Project Overview

Smart Failure Detection with Machine Learning is an AI-powered web application developed as part of the **Infosys Springboard Internship Program**. The system assists startup founders, entrepreneurs, and business analysts in evaluating the potential success or failure of a project by combining project data, market intelligence, competitor analysis, and machine learning-based recommendations.

The application collects project information from users, stores it securely in a PostgreSQL database, performs market and competitor analysis, and provides insights that support informed business decision-making.

---

##  Problem Statement

Many startups and business projects fail due to insufficient market research, poor planning, lack of competitor analysis, and ineffective risk assessment. Entrepreneurs often make decisions without understanding market trends or evaluating potential risks.

This project addresses these challenges by providing an intelligent system that analyzes project information, market conditions, and competitors to generate meaningful recommendations that help reduce project failure risk.

---

##  Features

- Project Submission Form
- PostgreSQL Database Integration
- Market Intelligence Dashboard
- Industry Overview Analysis
- Market Demand Analysis
- Competitor Analysis
- SWOT Analysis
- AI-Based Insights and Recommendations
- Risk Assessment Module
- Responsive and Interactive Dashboard

---

##  Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend Programming |
| Flask | Web Framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Flask-Migrate | Database Migration |
| HTML5 | Frontend Structure |
| CSS3 | Styling |
| JavaScript | Client-side Interactivity |
| Scikit-learn | Machine Learning |
| Pandas | Data Processing |
| NumPy | Numerical Computation |
| Matplotlib | Data Visualization |
| ReportLab | PDF Report Generation |
| Font Awesome | Icons |

---

##  Project Structure

```text
Smart-Failure-Detection-ML
│
├── database/
├── ml/
├── models/
├── routes/
├── services/
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── icons/
├── templates/
├── utils/
├── app.py
├── config.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

##  Installation

### Clone the Repository

```bash
git clone <repository-url>
cd Smart-Failure-Detection-ML
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure PostgreSQL

Create a PostgreSQL database and update the database configuration in `config.py`.

### Run the Application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Workflow

1. User submits project details.
2. Project information is stored in PostgreSQL.
3. The system performs market analysis.
4. Competitor information is analyzed.
5. SWOT analysis is generated.
6. AI generates insights and recommendations.
7. Results are displayed through an interactive dashboard.

---

##  Target Users

- Startup Founders
- Entrepreneurs
- Business Analysts
- Investors
- Business Mentors
- Incubation Centers

---

##  Output Screenshots

The following screenshots are included in the project documentation:

- Dashboard
- Project Submission Form
- Risk Assessment
- Recommendations
- Market Intelligence
- Competitor Analysis
- PostgreSQL Database
- Final Output

---

## Future Enhancements

- Real-time market data integration
- Advanced machine learning models
- User authentication
- Cloud deployment
- AI chatbot assistance
- Predictive analytics dashboard
- PDF report generation
- Data visualization enhancements

---

##  Developed By

**Shivani Tangudu**

B.Tech - Artificial Intelligence & Machine Learning

Infosys Springboard Internship Project

---

##  License

This project was developed for educational and internship purposes as part of the Infosys Springboard Internship Program.