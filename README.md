# Subscription Manager

This is a subscription management application built with a Python (Flask) backend and a ReactJS frontend. It allows users to manage subscriptions, including adding, extending, ending subscriptions, and viewing revenue and subscriber statistics.

## Features

### Backend (Flask)
- Add new customers and products.
- Manage subscriptions with:
  - Adding a subscription.
  - Extending a subscription's end date.
  - Ending a subscription immediately.
- Validate active subscriptions to prevent duplicates.
- Provide revenue and subscriber statistics.

### Frontend (ReactJS)
- Interactive and responsive user interface.
- Manage customers, products, and subscriptions.
- Real-time data visualization using charts.
- Responsive navigation bar with smooth transitions.

---

## Technology Stack

### Backend
- **Flask**: Python web framework.
- **SQLite**: Database for storing customer, product, and subscription data.

### Frontend
- **ReactJS**: JavaScript library for building user interfaces.
- **Chart.js**: For graphical data visualization.

---

## Installation and Setup

### Backend (Flask)
1. Navigate to the `backend` folder.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt```

