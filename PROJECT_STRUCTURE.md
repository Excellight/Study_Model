# Student Management System Pro - Modern Dashboard

## Project Structure

```
project/
├── backend/
│   ├── app.py              (Flask application)
│   ├── student.py          (Student and StudentManager classes)
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── src/
│       ├── main.jsx
│       ├── api.js
│       ├── App.jsx
│       ├── components/
│       │   ├── Layout.jsx
│       │   ├── Sidebar.jsx
│       │   ├── TopBar.jsx
│       │   ├── Dashboard.jsx
│       │   ├── StudentsPage.jsx
│       │   ├── StudentDetail.jsx
│       │   ├── AddStudentForm.jsx
│       │   ├── EditStudentForm.jsx
│       │   ├── RankingsPage.jsx
│       │   ├── PerformancePage.jsx
│       │   ├── DepartmentsPage.jsx
│       │   ├── ReportsPage.jsx
│       │   ├── Toast.jsx
│       │   ├── Modal.jsx
│       │   └── common/
│       │       ├── KPICard.jsx
│       │       ├── DataTable.jsx
│       │       └── Charts.jsx
│       └── hooks/
│           ├── useStudents.js
│           ├── useDashboard.js
│           └── useTheme.js
└── README.md
```

## Installation & Setup

### Backend Setup

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Run Flask server:
```bash
python app.py
```
The API will be available at: http://localhost:5000/api

### Frontend Setup

1. Install Node dependencies:
```bash
cd frontend
npm install
```

2. Run development server:
```bash
npm run dev
```
The app will be available at: http://localhost:3000

## Key Features

✅ Modern, responsive dashboard  
✅ Real-time reactive updates  
✅ Dark/Light mode support  
✅ Student management (CRUD)  
✅ Performance analytics  
✅ Student rankings  
✅ Department statistics  
✅ Charts and visualizations  
✅ Pagination, filtering, sorting  
✅ Toast notifications  
✅ Professional UI/UX  

## API Endpoints

### Dashboard
- GET /api/dashboard - KPI cards
- GET /api/dashboard/charts - Chart data
- GET /api/dashboard/recent-students - Recent students

### Students  
- GET /api/students - List with pagination/filters
- GET /api/students/{id} - Student details
- POST /api/students - Create student
- PUT /api/students/{id} - Update student
- DELETE /api/students/{id} - Delete student

### Rankings
- GET /api/rankings - Ranked students

### Performance
- GET /api/performance/analytics - Analytics

### Departments
- GET /api/departments - Department stats

### Reports
- GET /api/reports/class-performance - Class report
- GET /api/reports/student/{id} - Student report

## Technical Stack

### Backend
- Flask 2.3.2
- Flask-CORS
- Python 3.8+

### Frontend  
- React 18.2
- Vite 4.3
- Tailwind CSS 3.3
- Chart.js 4.3
- Lucide React (Icons)
- Axios

## Folder Structure Notes

All source files will be created in the workspace files directory. The backend and frontend can run independently:

- Backend runs on port 5000
- Frontend runs on port 3000 (with proxy to backend API)
- All files use modern, clean code practices
- Separation of concerns: API layer, components, hooks, utilities
- Dark mode support throughout
- Fully responsive design

## Next Steps

1. Create backend files (app.py and student.py)
2. Create frontend structure with React components
3. Test API endpoints
4. Ensure real-time reactivity
5. Deploy or package for distribution

All functionality from the original CLI program is preserved and enhanced with a modern UI.
