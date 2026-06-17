# 🏋️ Gym Management System - Complete Project Structure

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Backend Architecture](#backend-architecture)
4. [Frontend Architecture](#frontend-architecture)
5. [Database Design](#database-design)
6. [API Documentation](#api-documentation)
7. [Installation & Setup](#installation--setup)
8. [Working Modes](#working-modes)

---

## Project Overview

A complete, production-ready gym management platform with:
- **Backend**: FastAPI + PostgreSQL + SQLAlchemy
- **Frontend**: React.js + Redux + Material-UI
- **Mobile**: React Native (Optional)
- **Real-time**: WebSocket support
- **Payment**: Multiple gateway integration
- **Analytics**: Advanced reporting and dashboards

---

## Directory Structure

```
gym-management-system/
│
├── 📁 backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── config.py                  # Configuration & environment
│   │   │
│   │   ├── 📁 core/
│   │   │   ├── security.py            # JWT, OAuth2, password hashing
│   │   │   ├── dependencies.py        # FastAPI dependencies
│   │   │   ├── exceptions.py          # Custom exceptions
│   │   │   ├── constants.py           # App constants & enums
│   │   │   └── logger.py              # Logging configuration
│   │   │
│   │   ├── 📁 db/
│   │   │   ├── base.py                # SQLAlchemy base & session
│   │   │   ├── session.py             # Database session factory
│   │   │   ├── init_db.py             # Database initialization
│   │   │   └── models.py              # All database models
│   │   │
│   │   ├── 📁 models/                 # SQLAlchemy ORM Models
│   │   │   ├── user.py                # User, Role, Permission
│   │   │   ├── member.py              # Member, Membership
│   │   │   ├── trainer.py             # Trainer, Certification
│   │   │   ├── staff.py               # Staff, Schedule
│   │   │   ├── attendance.py          # Attendance tracking
│   │   │   ├── workout.py             # Workouts, Exercises
│   │   │   ├── nutrition.py           # Diet plans, Meals
│   │   │   ├── payment.py             # Payments, Invoices
│   │   │   ├── financial.py           # Revenue, Expenses
│   │   │   ├── inventory.py           # Equipment, Supplements
│   │   │   ├── notification.py        # Notifications, Logs
│   │   │   ├── branch.py              # Branch, Gym info
│   │   │   ├── class.py               # Group classes, Sessions
│   │   │   └── audit.py               # Audit logs
│   │   │
│   │   ├── 📁 schemas/                # Pydantic validation schemas
│   │   │   ├── user.py                # User schemas (in/out)
│   │   │   ├── member.py              # Member schemas
│   │   │   ├── trainer.py             # Trainer schemas
│   │   │   ├── attendance.py          # Attendance schemas
│   │   │   ├── workout.py             # Workout schemas
│   │   │   ├── payment.py             # Payment schemas
│   │   │   ├── pagination.py          # Pagination schemas
���   │   │   └── common.py              # Common schemas
│   │   │
│   │   ├── 📁 api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py          # Main API router
│   │   │       │
│   │   │       ├── 📁 auth/
│   │   │       │   ├── routes.py      # Auth endpoints
│   │   │       │   ├── dependencies.py # Auth dependencies
│   │   │       │   └── service.py     # Auth business logic
│   │   │       │
│   │   │       ├── 📁 users/
│   │   │       │   ├── routes.py
│   │   │       │   └── service.py
│   │   │       │
│   │   │       ├── 📁 members/
│   │   │       │   ├── routes.py
│   │   │       │   └── service.py
│   │   │       │
│   │   │       ├── 📁 trainers/
│   │   │       │   ├── routes.py
│   │   │       │   └── service.py
│   │   │       │
│   │   │       ├── 📁 staff/
│   │   │       │   ├── routes.py
│   │   │       │   └── service.py
│   │   │       │
│   │   │       ├── 📁 attendance/
│   │   │       │   ├── routes.py
│   │   │       │   └── service.py
│   │   │       │
│   │   │       ├── 📁 workouts/
│   │   │       │   ├── routes.py
│   │   │       │   └── service.py
│   │   │       │
│   │   │       ├── 📁 nutrition/
│   │   │       │   ├── routes.py
│   │   │       │   └── service.py
│   │   │       │
│   │   │       ├── 📁 payments/
│   │   │       │   ├── routes.py
│   │   │       │   └── service.py
│   │   │       │
│   │   │       ├── 📁 financial/
│   │   │       │   ├── routes.py
│   │   │       │   └── service.py
│   │   │       │
│   │   │       ├── 📁 inventory/
│   │   │       │   ├── routes.py
│   │   │       │   └── service.py
│   │   │       │
│   │   │       ├── 📁 reports/
│   │   │       │   ├── routes.py
│   │   │       │   └── service.py
│   │   │       │
│   │   │       ├── 📁 analytics/
│   │   │       │   ├── routes.py
│   │   │       │   └── service.py
│   │   │       │
│   │   │       ├── 📁 notifications/
│   │   │       │   ├── routes.py
│   │   │       │   └── service.py
│   │   │       │
│   │   │       ├── 📁 branches/
│   │   │       │   ├── routes.py
│   │   │       │   └── service.py
│   │   │       │
│   │   │       └── 📁 classes/
│   │   │           ├── routes.py
│   │   │           └── service.py
│   │   │
│   │   ├── 📁 services/               # Business logic layer
│   │   │   ├── auth_service.py
│   │   │   ├── member_service.py
│   │   │   ├── trainer_service.py
│   │   │   ├── attendance_service.py
│   │   │   ├── payment_service.py
│   │   │   ├── report_service.py
│   │   │   ├── notification_service.py
│   │   │   └── email_service.py
│   │   │
│   │   ├── 📁 tasks/                 # Celery tasks (async jobs)
│   │   │   ├── email_tasks.py
│   │   │   ├── notification_tasks.py
│   │   │   ├── report_tasks.py
│   │   │   ├── payment_tasks.py
│   │   │   └── scheduled_tasks.py
│   │   │
│   │   ├── 📁 utils/                 # Utility functions
│   │   │   ├── helpers.py
│   │   │   ├── validators.py
│   │   │   ├── formatters.py
│   │   │   ├── qr_code.py
│   │   │   ├── pdf_generator.py
│   │   │   ├── excel_generator.py
│   │   │   ├── payment_gateway.py
│   │   │   └── email_sender.py
│   │   │
│   │   ├── 📁 middleware/
│   │   │   ├── error_handler.py
│   │   │   ├── cors_middleware.py
│   │   │   ├── rate_limiter.py
│   │   │   └── request_logger.py
│   │   │
│   │   └── 📁 websocket/
│   │       ├── manager.py
│   │       ├── handlers.py
│   │       └── events.py
│   │
│   ├── 📁 migrations/                 # Alembic database migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │
│   ├── 📁 tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_members.py
│   │   ├── test_trainers.py
│   │   ├── test_payments.py
│   │   ├── test_attendance.py
│   │   └── fixtures/
│   │
│   ├── requirements.txt               # Python dependencies
│   ├── .env.example                  # Environment template
│   ├── docker-compose.yml            # Docker setup
│   ├── Dockerfile                    # Backend Docker image
│   ├── setup_db.py                   # Database initialization script
│   └── README.md
│
├── 📁 frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── assets/
│   │
│   ├── src/
│   │   ├── index.js                  # React entry point
│   │   ├── App.js                    # Root component
│   │   ├── App.css
│   │   │
│   │   ├── 📁 components/
│   │   │   ├── Layout/
│   │   │   │   ├── Header.js
│   │   │   │   ├── Sidebar.js
│   │   │   │   ├── Footer.js
│   │   │   │   └── MainLayout.js
│   │   │   │
│   │   │   ├── Auth/
│   │   │   │   ├── Login.js
│   │   │   │   ├── Register.js
│   │   │   │   ├── ForgotPassword.js
│   │   │   │   └── ProtectedRoute.js
│   │   │   │
│   │   │   ├── Dashboard/
│   │   │   │   ├── Dashboard.js
│   │   │   │   ├── StatCard.js
│   │   │   │   ├── RevenueChart.js
│   │   │   │   ├── AttendanceChart.js
│   │   │   │   ├── MemberGrowthChart.js
│   │   │   │   └── TopTrainersCard.js
│   │   │   │
│   │   │   ├── Members/
│   │   │   │   ├── MemberList.js
│   │   │   │   ├── MemberCreate.js
│   │   │   │   ├── MemberEdit.js
│   │   │   │   ├── MemberDetail.js
│   │   │   │   ├── MemberCard.js
│   │   │   │   └── QRCodeGenerator.js
│   │   │   │
│   │   │   ├── Trainers/
│   │   │   │   ├── TrainerList.js
│   │   │   │   ├── TrainerCreate.js
│   │   │   │   ├── TrainerEdit.js
│   │   │   │   ├── TrainerDetail.js
│   │   │   │   └── TrainerPerformance.js
│   │   │   │
│   │   │   ├── Attendance/
│   │   │   │   ├── AttendanceList.js
│   │   │   │   ├── CheckInOut.js
│   │   │   │   ├── QRScanner.js
│   │   │   │   ├── AttendanceReport.js
│   │   │   │   └── AttendanceAnalytics.js
│   │   │   │
│   │   │   ├── Workouts/
│   │   │   │   ├── WorkoutList.js
│   │   │   │   ├── WorkoutCreate.js
│   │   │   │   ├── ExerciseLibrary.js
│   │   │   │   ├── ProgressTracking.js
│   │   │   │   └── BeforeAfterPhotos.js
│   │   │   │
│   │   │   ├── Nutrition/
│   │   │   │   ├── DietPlanList.js
│   │   │   │   ├── DietPlanCreate.js
│   │   │   │   ├── Calculator.js
│   │   │   │   ├── MealPlans.js
│   │   │   │   └── NutritionTracking.js
│   │   │   │
│   │   │   ├── Payments/
│   │   │   │   ├── PaymentList.js
│   │   │   │   ├── PaymentCreate.js
│   │   │   │   ├── PaymentStatus.js
│   │   │   │   ├── InvoiceView.js
│   │   │   │   └── PaymentGateway.js
│   │   │   │
│   │   │   ├── Financial/
│   │   │   │   ├── RevenueReport.js
│   │   │   │   ├── ExpenseReport.js
│   │   │   │   ├── ProfitAnalysis.js
│   │   │   │   └── FinancialChart.js
│   │   │   │
│   │   │   ├── Inventory/
│   │   │   │   ├── InventoryList.js
│   │   │   │   ├── StockAdd.js
│   │   │   │   ├── StockMovement.js
│   │   │   │   └── InventoryValue.js
│   │   │   │
│   │   │   ├── Reports/
│   │   │   │   ├── ReportGenerator.js
│   │   │   │   ├── ExportOptions.js
│   │   │   │   ├── AttendanceReport.js
│   │   │   │   ├── MembershipReport.js
│   │   │   │   ├── RevenueReport.js
│   │   │   │   └── ReportScheduler.js
│   │   │   │
│   │   │   ├── Analytics/
│   │   │   │   ├── AnalyticsDashboard.js
│   │   │   │   ├── RevenueAnalytics.js
│   │   │   │   ├── MemberAnalytics.js
│   │   │   │   ├── TrainerAnalytics.js
│   │   │   │   └── ChurnAnalysis.js
│   │   │   │
│   │   │   ├── Notifications/
│   │   │   │   ├── NotificationCenter.js
│   │   │   │   ├── NotificationBell.js
│   │   │   │   └── NotificationSettings.js
│   │   │   │
│   │   │   ├── Classes/
│   │   │   │   ├── ClassList.js
│   │   │   │   ├── ClassSchedule.js
│   │   │   │   ├── ClassBooking.js
│   │   │   │   └── ClassAttendance.js
│   │   │   │
│   │   │   ├── Admin/
│   │   │   │   ├── UserManagement.js
│   │   │   │   ├── RolePermission.js
│   │   │   │   ├── BranchManagement.js
│   │   │   │   ├── SystemSettings.js
│   │   │   │   └── AuditLogs.js
│   │   │   │
│   │   │   └── Common/
│   │   │       ├── Modal.js
│   │   │       ├── Table.js
│   │   │       ├── Form.js
│   │   │       ├── Loading.js
│   │   │       ├── Error.js
│   │   │       ├── Pagination.js
│   │   │       ├── Filter.js
│   │   │       ├── SearchBox.js
│   │   │       └── ConfirmDialog.js
│   │   │
│   │   ├── 📁 pages/
│   │   │   ├── HomePage.js
│   │   │   ├── DashboardPage.js
│   │   │   ├── ProfilePage.js
│   │   │   ├── SettingsPage.js
│   │   │   ├── NotFoundPage.js
│   │   │   └── UnauthorizedPage.js
│   │   │
│   │   ├── 📁 redux/
│   │   │   ├── store.js
│   │   │   ├── rootReducer.js
│   │   │   │
│   │   │   ├── 📁 slices/
│   │   │   │   ├── authSlice.js
│   │   │   │   ├── memberSlice.js
│   │   │   │   ├── trainerSlice.js
│   │   │   │   ├── attendanceSlice.js
│   │   │   │   ├── paymentSlice.js
│   │   │   │   ├── uiSlice.js
│   │   │   │   └── notificationSlice.js
│   │   │   │
│   │   │   └── 📁 thunks/
│   │   │       ├── authThunks.js
│   │   │       ├── memberThunks.js
│   │   │       ├── paymentThunks.js
│   │   │       └── reportThunks.js
│   │   │
│   │   ├── 📁 services/
│   │   │   ├── api.js                 # Axios API instance
│   │   │   ├── authService.js
│   │   │   ├── memberService.js
│   │   │   ├── trainerService.js
│   │   │   ├── attendanceService.js
│   │   │   ├── paymentService.js
│   │   │   ├── reportService.js
│   │   │   └── analyticsService.js
│   │   │
│   │   ├── 📁 hooks/
│   │   │   ├── useAuth.js
│   │   │   ├── useFetch.js
│   │   │   ├── useForm.js
│   │   │   ├── useLocalStorage.js
│   │   │   ├── useDebounce.js
│   │   │   └── usePagination.js
│   │   │
│   │   ├── 📁 utils/
│   │   │   ├── axiosConfig.js
│   │   │   ├── constants.js
│   │   │   ├── formatters.js
│   │   │   ├── validators.js
│   │   │   ├── localStorage.js
│   │   │   ├── dateUtils.js
│   │   │   └── errorHandler.js
│   │   │
│   │   ├── 📁 styles/
│   │   │   ├── theme.js
│   │   │   ├── variables.css
│   │   │   ├── global.css
│   │   │   └── responsive.css
│   │   │
│   │   ├── 📁 assets/
│   │   │   ├── 📁 images/
│   │   │   ├── 📁 icons/
│   │   │   └── 📁 fonts/
│   │   │
│   │   └── index.css
│   │
│   ├── package.json
│   ├── .env.example
│   ├── .gitignore
│   └── README.md
│
├── 📁 mobile/                        # React Native App (Optional)
│   ├── app.json
│   ├── App.js
│   ├── package.json
│   ├── 📁 src/
│   │   ├── 📁 screens/
│   │   ├── 📁 components/
│   │   ├── 📁 navigation/
│   │   ├── 📁 redux/
│   │   ├── 📁 services/
│   │   ���── 📁 utils/
│   │
│   └── README.md
│
├── 📁 docs/                          # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── DATABASE_SCHEMA.md
│   ├── DEPLOYMENT.md
│   ├── SETUP_GUIDE.md
│   ├── API_EXAMPLES.md
│   └── TROUBLESHOOTING.md
│
├── 📁 docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── docker-compose.yml
│   └── nginx.conf
│
├── .gitignore
├── docker-compose.yml               # Main docker-compose
├── README.md                         # Project root README
└── STRUCTURE.md                      # This file

```

---

## Backend Architecture

### 1. **Layered Architecture**

```
HTTP Request
    ↓
Middleware (Auth, CORS, Error Handling)
    ↓
API Routes (FastAPI routers)
    ↓
Services (Business Logic)
    ↓
Models (SQLAlchemy ORM)
    ↓
Database (PostgreSQL)
    ↓
Response
```

### 2. **Core Components**

#### **Authentication & Authorization**
- JWT token-based authentication
- OAuth2 password flow
- Role-Based Access Control (RBAC)
- Permission management

#### **Database Layer**
- SQLAlchemy 2.0 ORM
- PostgreSQL with connection pooling
- Alembic migrations
- Event listeners for audit logging

#### **API Endpoints**
- RESTful API design
- Pagination support
- Filtering and sorting
- Response standardization

#### **Business Logic**
- Service layer for business rules
- Data validation
- Error handling
- Logging

#### **Async Tasks**
- Celery for background jobs
- Email notifications
- Report generation
- Payment processing

---

## Frontend Architecture

### 1. **Technology Stack**
- React 18.x
- Redux Toolkit for state management
- Material-UI for UI components
- Axios for API calls
- Chart.js for analytics
- React Router for navigation

### 2. **Application Structure**

```
Redux Store (Global State)
    ↓
Pages (Route components)
    ↓
Components (UI components)
    ↓
Services (API calls)
    ↓
Hooks (Custom logic)
    ↓
Utilities (Helpers)
```

### 3. **State Management**
- Redux for complex state
- Local state for UI components
- Redux Thunks for async operations
- Selectors for computed state

---

## Database Design

### **Core Tables**

#### Users & Authentication
- `users` - User accounts
- `roles` - User roles (Admin, Manager, Trainer, Member)
- `permissions` - Permissions
- `user_sessions` - Active sessions
- `audit_logs` - User activity logs

#### Organization
- `gyms` - Main gym entities
- `branches` - Branch information
- `branch_timings` - Operating hours

#### Members
- `members` - Member profiles
- `memberships` - Membership records
- `membership_history` - Membership changes
- `member_progress` - Progress tracking

#### Trainers
- `trainers` - Trainer profiles
- `certifications` - Trainer certifications
- `trainer_members` - Trainer-Member assignments
- `trainer_performance` - Performance metrics

#### Staff
- `staff` - Staff members
- `staff_roles` - Staff roles
- `staff_schedules` - Work schedules

#### Attendance
- `attendance` - Attendance records
- `qr_codes` - Member QR codes
- `rfid_cards` - RFID card mappings

#### Workouts & Fitness
- `exercises` - Exercise library
- `workout_plans` - Customized plans
- `workout_sessions` - Individual sessions
- `body_progress` - Progress tracking

#### Nutrition
- `diet_plans` - Diet plans
- `meals` - Meal records
- `nutrition_tracking` - Nutrition logs

#### Payments & Financial
- `payments` - Payment records
- `invoices` - Invoice generation
- `receipts` - Receipt records
- `revenue` - Revenue tracking
- `expenses` - Expense tracking

#### Inventory
- `inventory_items` - Equipment/Supplements
- `stock_movements` - Stock changes
- `stock_suppliers` - Supplier info

#### Communication
- `notifications` - Notification records
- `notification_templates` - Email/SMS templates
- `notification_logs` - Delivery logs

#### Classes
- `group_classes` - Class definitions
- `class_schedules` - Class schedules
- `class_enrollments` - Member enrollments
- `class_attendance` - Attendance tracking

---

## API Documentation

### Authentication Endpoints
```
POST   /api/v1/auth/register              Register new user
POST   /api/v1/auth/login                 User login
POST   /api/v1/auth/logout                User logout
POST   /api/v1/auth/refresh-token         Refresh JWT token
POST   /api/v1/auth/forgot-password       Password reset request
POST   /api/v1/auth/reset-password        Reset password with token
GET    /api/v1/auth/profile               Get current user
PUT    /api/v1/auth/profile               Update profile
```

### Member Management
```
GET    /api/v1/members                    List all members
POST   /api/v1/members                    Create member
GET    /api/v1/members/{id}               Get member details
PUT    /api/v1/members/{id}               Update member
DELETE /api/v1/members/{id}               Delete member
POST   /api/v1/members/{id}/suspend       Suspend membership
POST   /api/v1/members/{id}/freeze        Freeze membership
GET    /api/v1/members/{id}/qrcode        Generate QR code
GET    /api/v1/members/search             Search members
```

### Trainer Management
```
GET    /api/v1/trainers                   List trainers
POST   /api/v1/trainers                   Create trainer
GET    /api/v1/trainers/{id}              Get trainer details
PUT    /api/v1/trainers/{id}              Update trainer
GET    /api/v1/trainers/{id}/performance  Get performance metrics
GET    /api/v1/trainers/{id}/members      Get assigned members
POST   /api/v1/trainers/{id}/assign       Assign member
```

### Attendance System
```
POST   /api/v1/attendance/checkin         Member check-in
POST   /api/v1/attendance/checkout        Member check-out
GET    /api/v1/attendance                 Get attendance records
GET    /api/v1/attendance/reports         Attendance statistics
GET    /api/v1/attendance/daily           Daily attendance summary
GET    /api/v1/attendance/qr-scan         QR code scanning
```

### Workout Management
```
GET    /api/v1/workouts                   List workout plans
POST   /api/v1/workouts                   Create workout
GET    /api/v1/workouts/{id}              Get workout details
PUT    /api/v1/workouts/{id}              Update workout
GET    /api/v1/exercises                  Get exercise library
GET    /api/v1/workouts/{id}/progress     Track progress
POST   /api/v1/workouts/{id}/complete     Mark complete
```

### Nutrition Management
```
GET    /api/v1/diet-plans                 List diet plans
POST   /api/v1/diet-plans                 Create diet plan
GET    /api/v1/diet-plans/{id}            Get diet details
PUT    /api/v1/diet-plans/{id}            Update diet plan
POST   /api/v1/nutrition/calculate        Calculate BMI/BMR/TDEE
GET    /api/v1/nutrition/tracking         Track nutrition
```

### Payment Processing
```
GET    /api/v1/payments                   List payments
POST   /api/v1/payments                   Create payment
GET    /api/v1/payments/{id}              Get payment details
POST   /api/v1/payments/{id}/refund       Refund payment
GET    /api/v1/invoices                   List invoices
GET    /api/v1/invoices/{id}/download     Download PDF
```

### Financial Reports
```
GET    /api/v1/financial/revenue          Revenue report
GET    /api/v1/financial/expenses         Expense report
GET    /api/v1/financial/profit           Profit analysis
GET    /api/v1/financial/summary          Financial summary
GET    /api/v1/financial/export           Export financial data
```

### Inventory Management
```
GET    /api/v1/inventory                  List inventory
POST   /api/v1/inventory                  Add item
PUT    /api/v1/inventory/{id}             Update item
GET    /api/v1/inventory/stock            Stock levels
POST   /api/v1/inventory/movement         Record stock movement
```

### Reports & Analytics
```
GET    /api/v1/reports/attendance         Attendance report
GET    /api/v1/reports/members            Member report
GET    /api/v1/reports/revenue            Revenue report
GET    /api/v1/reports/expenses           Expense report
POST   /api/v1/reports/export             Export report
GET    /api/v1/analytics/dashboard        Dashboard metrics
GET    /api/v1/analytics/trends           Trend analysis
```

### Class Management
```
GET    /api/v1/classes                    List classes
POST   /api/v1/classes                    Create class
GET    /api/v1/classes/{id}               Get class details
POST   /api/v1/classes/{id}/enroll        Enroll member
GET    /api/v1/classes/{id}/attendance    Class attendance
```

### Admin Functions
```
GET    /api/v1/admin/users                List users
POST   /api/v1/admin/users                Create user
PUT    /api/v1/admin/users/{id}           Update user
DELETE /api/v1/admin/users/{id}           Delete user
GET    /api/v1/admin/audit-logs           Audit logs
GET    /api/v1/admin/settings             System settings
PUT    /api/v1/admin/settings             Update settings
```

---

## Installation & Setup

### Backend Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd gym-management-system/backend

# 2. Create virtual environment
python3.13 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Initialize database
python setup_db.py

# 6. Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 7. Access API
# Swagger: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Frontend Setup

```bash
# 1. Navigate to frontend
cd gym-management-system/frontend

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env
# Edit .env with API base URL

# 4. Start development server
npm start

# 5. Open in browser
# http://localhost:3000
```

### Docker Setup

```bash
# Build and run all services
docker-compose up -d

# Access services
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

---

## Working Modes

### 1. **Member Mode**
- Browse member profile
- Track fitness progress
- View assigned workouts
- Track nutrition
- View class schedules
- Book classes

### 2. **Trainer Mode**
- Manage assigned members
- Create/update workouts
- Track member progress
- Performance analytics
- Attendance management

### 3. **Staff Mode**
- Process check-in/checkout
- Manage attendance
- View schedules
- Process payments
- Manage inventory

### 4. **Manager Mode**
- Full member management
- Financial reports
- Revenue tracking
- Expense management
- Staff scheduling
- Analytics dashboard

### 5. **Admin Mode**
- System-wide administration
- User and role management
- Branch management
- System settings
- Audit logging
- Backup & Recovery

---

## Key Features Implementation

### ✅ Implemented Features
- Multi-branch gym management
- Member lifecycle management
- Trainer assignment system
- Attendance tracking (QR/RFID/Manual)
- Workout management with exercise library
- Nutrition planning and tracking
- Payment processing (Multiple gateways)
- Financial reporting and analytics
- Inventory management
- Email/SMS notifications
- Report generation (PDF/Excel)
- Role-based access control
- Audit logging

### 🔄 Real-time Features
- WebSocket connections for notifications
- Live attendance updates
- Real-time member tracking
- Instant payment confirmations

### 📊 Analytics & Reporting
- Revenue trends
- Member growth
- Trainer performance
- Attendance patterns
- Profit analysis
- Churn prediction

---

**Gym Management System** - Complete, Production-Ready Solution 💪
