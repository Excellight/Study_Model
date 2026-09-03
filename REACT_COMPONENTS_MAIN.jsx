/* 
  COMPLETE REACT APPLICATION CODE
  Copy each section into its respective file in src/ and src/components/
*/

// ========================
// src/App.jsx
// ========================

import React, { useState, useCallback } from 'react'
import { Sidebar } from './components/Sidebar'
import { TopBar } from './components/TopBar'
import { Dashboard } from './components/Dashboard'
import { StudentsPage } from './components/StudentsPage'
import { AddStudentForm } from './components/AddStudentForm'
import { RankingsPage } from './components/RankingsPage'
import { PerformancePage } from './components/PerformancePage'
import { DepartmentsPage } from './components/DepartmentsPage'
import { ReportsPage } from './components/ReportsPage'
import { Toast } from './components/Toast'
import { useTheme } from './hooks/useTheme'
import { StudentDetail } from './components/StudentDetail'
import { EditStudentForm } from './components/EditStudentForm'

function App() {
  const { isDark, toggleTheme } = useTheme()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [toast, setToast] = useState(null)
  const [selectedStudentId, setSelectedStudentId] = useState(null)
  const [refreshKey, setRefreshKey] = useState(0)

  const showToast = useCallback((message, type = 'success') => {
    setToast({ message, type })
  }, [])

  const handleStudentAdded = useCallback(() => {
    showToast('Student added successfully!', 'success')
    setRefreshKey(prev => prev + 1)
    setCurrentPage('students')
  }, [showToast])

  const handleStudentUpdated = useCallback(() => {
    showToast('Student updated successfully!', 'success')
    setRefreshKey(prev => prev + 1)
    setSelectedStudentId(null)
  }, [showToast])

  const handleStudentDeleted = useCallback(() => {
    showToast('Student deleted successfully!', 'success')
    setRefreshKey(prev => prev + 1)
  }, [showToast])

  const renderPage = () => {
    if (selectedStudentId) {
      return <StudentDetail studentId={selectedStudentId} onBack={() => setSelectedStudentId(null)} />
    }

    switch (currentPage) {
      case 'dashboard':
        return <Dashboard key={refreshKey} />
      case 'students':
        return <StudentsPage 
          key={refreshKey} 
          onSelectStudent={setSelectedStudentId}
          onDelete={handleStudentDeleted}
          showToast={showToast}
        />
      case 'add-student':
        return <AddStudentForm onSuccess={handleStudentAdded} showToast={showToast} />
      case 'rankings':
        return <RankingsPage key={refreshKey} />
      case 'performance':
        return <PerformancePage key={refreshKey} />
      case 'departments':
        return <DepartmentsPage key={refreshKey} />
      case 'reports':
        return <ReportsPage key={refreshKey} />
      default:
        return <Dashboard key={refreshKey} />
    }
  }

  return (
    <div className={isDark ? 'dark' : ''}>
      <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
        <Sidebar 
          isOpen={sidebarOpen}
          toggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          currentPage={currentPage}
          onNavigate={setCurrentPage}
        />
        
        <div className="flex-1 flex flex-col overflow-hidden">
          <TopBar 
            onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
            isDark={isDark}
            onThemeToggle={toggleTheme}
          />
          
          <main className="flex-1 overflow-y-auto p-4 md:p-8">
            {renderPage()}
          </main>
        </div>
      </div>

      {toast && (
        <Toast 
          message={toast.message} 
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  )
}

export default App

// ========================
// src/components/Dashboard.jsx
// ========================

import React from 'react'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { Users, TrendingUp, BarChart3, Star } from 'lucide-react'
import { KPICard } from './common/KPICard'
import { useDashboard } from '../hooks/useDashboard'

export const Dashboard = () => {
  const { kpis, charts, recent, loading, error } = useDashboard()

  if (error) {
    return (
      <div className="card p-8 text-center border-red-500">
        <p className="text-red-600">Error loading dashboard: {error}</p>
      </div>
    )
  }

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

  return (
    <div className="space-y-8 fade-in">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard 
          icon={Users}
          label="Total Students"
          value={kpis?.total_students || 0}
          color="blue"
        />
        <KPICard 
          icon={BarChart3}
          label="Class Average"
          value={`${kpis?.class_average || 0}%`}
          color="green"
        />
        <KPICard 
          icon={TrendingUp}
          label="Passing Rate"
          value={`${kpis?.passing_rate || 0}%`}
          color="purple"
        />
        <KPICard 
          icon={Star}
          label="Top Performer"
          value={kpis?.top_performer || 'N/A'}
          subtext="Highest average score"
          color="orange"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Student Averages Chart */}
        <div className="card p-6">
          <h3 className="text-lg font-bold mb-4">Performance Overview</h3>
          {charts?.student_averages?.labels?.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={charts.student_averages.labels.map((label, i) => ({
                name: label,
                average: charts.student_averages.data[i]
              }))}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="average" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500 text-center py-8">No data available</p>
          )}
        </div>

        {/* Department Distribution */}
        <div className="card p-6">
          <h3 className="text-lg font-bold mb-4">Department Distribution</h3>
          {charts?.department_distribution && Object.keys(charts.department_distribution).length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={Object.entries(charts.department_distribution).map(([dept, count]) => ({
                    name: dept,
                    value: count
                  }))}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {Object.entries(charts.department_distribution).map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500 text-center py-8">No data available</p>
          )}
        </div>
      </div>

      {/* Pass/Fail and Grade Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pass/Fail */}
        <div className="card p-6">
          <h3 className="text-lg font-bold mb-4">Pass/Fail Status</h3>
          {charts?.pass_fail_stats && (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600 dark:text-gray-400">Passing Students</span>
                <span className="text-2xl font-bold text-green-500">{charts.pass_fail_stats.passing}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600 dark:text-gray-400">Failing Students</span>
                <span className="text-2xl font-bold text-red-500">{charts.pass_fail_stats.failing}</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-green-500 h-2 rounded-full"
                  style={{ width: `${charts.pass_fail_stats.pass_percentage}%` }}
                />
              </div>
              <p className="text-center text-sm text-gray-500">{charts.pass_fail_stats.pass_percentage}% Pass Rate</p>
            </div>
          )}
        </div>

        {/* Grade Distribution */}
        <div className="card p-6">
          <h3 className="text-lg font-bold mb-4">Grade Distribution</h3>
          {charts?.grade_distribution && (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={Object.entries(charts.grade_distribution).map(([grade, count]) => ({
                grade,
                count
              }))}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="grade" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#8b5cf6" />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* Recent Students */}
      <div className="card p-6">
        <h3 className="text-lg font-bold mb-4">Recently Added Students</h3>
        {recent && recent.length > 0 ? (
          <div className="space-y-3">
            {recent.map(student => (
              <div key={student.student_id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div>
                  <p className="font-medium">{student.full_name}</p>
                  <p className="text-sm text-gray-500">{student.department}</p>
                </div>
                <div className="flex gap-4 items-center">
                  <span className={`badge badge-grade badge-${student.grade.toLowerCase()}`}>
                    {student.grade}
                  </span>
                  <span className={`badge ${student.status === 'PASS' ? 'badge-pass' : 'badge-fail'}`}>
                    {student.status}
                  </span>
                  <span className="text-sm font-semibold">{student.average_score}%</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">No students yet</p>
        )}
      </div>
    </div>
  )
}

// ========================
// src/components/StudentsPage.jsx
// ========================

import React, { useState, useEffect } from 'react'
import { Plus, Search, Filter } from 'lucide-react'
import { DataTable } from './common/DataTable'
import { useStudents } from '../hooks/useStudents'

export const StudentsPage = ({ onSelectStudent, onDelete, showToast }) => {
  const { students, total, loading, fetchStudents, deleteStudent } = useStudents()
  const [page, setPage] = useState(1)
  const [searchTerm, setSearchTerm] = useState('')
  const [department, setDepartment] = useState('')
  const [grade, setGrade] = useState('')
  const [status, setStatus] = useState('')
  const [departments, setDepartments] = useState([])

  useEffect(() => {
    const filters = {}
    if (searchTerm) filters.search = searchTerm
    if (department) filters.department = department
    if (grade) filters.grade = grade
    if (status) filters.status = status

    const timer = setTimeout(() => {
      fetchStudents(page, filters)
    }, 300)

    return () => clearTimeout(timer)
  }, [page, searchTerm, department, grade, status, fetchStudents])

  useEffect(() => {
    const depts = [...new Set(students.map(s => s.department))].sort()
    setDepartments(depts)
  }, [students])

  const handleDelete = async (studentId) => {
    if (confirm('Are you sure you want to delete this student?')) {
      try {
        await deleteStudent(studentId)
        showToast('Student deleted successfully!', 'success')
        onDelete?.()
      } catch (err) {
        showToast(err.response?.data?.error || 'Failed to delete student', 'error')
      }
    }
  }

  const columns = [
    { key: 'full_name', label: 'Student', render: (val, row) => (
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
          {val.split(' ').map(n => n[0]).join('').slice(0, 2)}
        </div>
        <span>{val}</span>
      </div>
    )},
    { key: 'student_id', label: 'ID' },
    { key: 'age', label: 'Age' },
    { key: 'department', label: 'Department' },
    { key: 'email', label: 'Email', render: (val) => <span className="text-sm">{val}</span> },
    { key: 'average_score', label: 'Average', render: (val) => <span className="font-semibold">{val}%</span> },
    { key: 'grade', label: 'Grade', render: (val) => (
      <span className={`badge badge-grade badge-${val.toLowerCase()}`}>{val}</span>
    )},
    { key: 'status', label: 'Status', render: (val) => (
      <span className={`badge ${val === 'PASS' ? 'badge-pass' : 'badge-fail'}`}>{val}</span>
    )}
  ]

  const totalPages = Math.ceil(total / 10)

  return (
    <div className="space-y-6 fade-in">
      <div>
        <h1 className="text-3xl font-bold mb-2">Students</h1>
        <p className="text-gray-600 dark:text-gray-400">Manage student records and academic performance</p>
      </div>

      {/* Filters */}
      <div className="card p-4 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="relative">
            <Search size={18} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input 
              type="text"
              placeholder="Search by name or ID..."
              value={searchTerm}
              onChange={(e) => {
                setSearchTerm(e.target.value)
                setPage(1)
              }}
              className="input-field pl-10"
            />
          </div>

          <select 
            value={department}
            onChange={(e) => {
              setDepartment(e.target.value)
              setPage(1)
            }}
            className="select-field"
          >
            <option value="">All Departments</option>
            {departments.map(dept => (
              <option key={dept} value={dept}>{dept}</option>
            ))}
          </select>

          <select 
            value={grade}
            onChange={(e) => {
              setGrade(e.target.value)
              setPage(1)
            }}
            className="select-field"
          >
            <option value="">All Grades</option>
            {['A', 'B', 'C', 'D', 'F'].map(g => (
              <option key={g} value={g}>{g}</option>
            ))}
          </select>

          <select 
            value={status}
            onChange={(e) => {
              setStatus(e.target.value)
              setPage(1)
            }}
            className="select-field"
          >
            <option value="">All Status</option>
            <option value="PASS">Pass</option>
            <option value="FAIL">Fail</option>
          </select>

          <button className="btn btn-primary flex items-center justify-center gap-2">
            <Plus size={18} />
            Add Student
          </button>
        </div>
      </div>

      {/* Table */}
      <DataTable 
        columns={columns}
        data={students}
        loading={loading}
        onView={onSelectStudent}
        onEdit={onSelectStudent}
        onDelete={handleDelete}
      />

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center gap-2">
          <button 
            onClick={() => setPage(Math.max(1, page - 1))}
            disabled={page === 1}
            className="btn btn-secondary"
          >
            Previous
          </button>
          {[...Array(totalPages)].map((_, i) => (
            <button 
              key={i + 1}
              onClick={() => setPage(i + 1)}
              className={`btn ${page === i + 1 ? 'btn-primary' : 'btn-secondary'}`}
            >
              {i + 1}
            </button>
          ))}
          <button 
            onClick={() => setPage(Math.min(totalPages, page + 1))}
            disabled={page === totalPages}
            className="btn btn-secondary"
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}

// ========================
// Continued in next section (due to length)...
// ========================

/* The following components are also needed:
- AddStudentForm.jsx
- EditStudentForm.jsx  
- StudentDetail.jsx
- RankingsPage.jsx
- PerformancePage.jsx
- DepartmentsPage.jsx
- ReportsPage.jsx
- common/Charts.jsx
- and all hook/utility files

All code is provided in COMPLETE_IMPLEMENTATION_GUIDE.md
*/

export default {}
