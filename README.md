# QUIZIFY — Academic Examination & Rotating QR Attendance Platform

**Quizify** is a college and university academic examination and attendance platform. It enforces server-authoritative role-based access control (RBAC), rotating cryptographic QR attendance, timetable synchronization, automated and subjective quiz evaluation, and multi-format report exports.

---

## 🏛️ Architecture Overview

```
                                      QUIZIFY SYSTEM ARCHITECTURE
                                      
               ┌────────────────────────────────────────────────────────┐
               │              React + Vanilla CSS Frontend              │
               │   • Dynamic Accent Token Colorizer (Dark & Light)      │
               │   • Mobile / Desktop In-Browser Camera QR Scanner      │
               │   • Distraction-Free Live Examination HUD              │
               │   • Private AI Doubt Solver & Faculty Assistant        │
               └───────────────────────────┬────────────────────────────┘
                                           │  REST APIs / JWT
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │              Node.js + Express 5 Backend               │
               │   • Strict Server-Side RBAC (Admin, Teacher, Student)  │
               │   • Authoritative Countdown Exam Timers                │
               │   • Rotating QR Cryptographic Token & Hash Generator   │
               │   • Document Classification (PDF/DOCX Exam vs Concept) │
               │   • Pluggable AI Service Adapter (Gemini & Fallback)   │
               │   • Multi-Format Exporter (PDFKit, DOCX, ExcelJS, CSV) │
               │   • Real-Time Security & Compliance Audit Logger       │
               └───────────────────────────┬────────────────────────────┘
                                           │  ACID Transactions
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │          SQLite 3 Database (WAL Mode Enabled)          │
               │   • Strict Foreign Keys, Unique & Check Constraints    │
               │   • Explicit Division-Batch Hierarchical Ties          │
               │   • Raw Attendance Counts as Source of Truth           │
               └────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Requirements
- **Node.js**: v18+ (tested on Node v24.18.0)
- **NPM**: v9+

### 2. Installation
Dependencies are already installed in root and `frontend/`:
```bash
npm install
cd frontend && npm install && cd ..
```

### 3. Database Initialization & Seeding
```bash
npm run seed
```

### 4. Running the Platform
```bash
# Starts the backend server (serves API and production React bundle on http://localhost:5000)
npm start
```
For local frontend development with instant Hot Module Replacement:
```bash
cd frontend
npm run dev
# Accessible on http://localhost:5173 (proxied to backend on port 5000)
```

### 5. Running Automated Security & Integration Tests
```bash
npm test
# Executes 14 comprehensive tests covering cryptographic QR rotation, RBAC,
# wrong division rejection, duplicate scan prevention, authoritative quiz timer,
# tab-switch auto-submit, and multi-format reports.
```

---

## 🔐 Credentials & Roles

The system is pre-seeded with realistic institutional test accounts:

| Role | Identifier / Login | Password | Description |
| :--- | :--- | :--- | :--- |
| **ADMIN** | `ADM-1` | `1-NOTADM` | Full platform authority, timetable scheduling, faculty assignments, attendance corrections, and audit logs. |
| **TEACHER** | `prof.sharma` | `TeacherPass@2026` | Assigned to CEP (CS501) and ADS (CS502) for Divisions A1 & A2. Can launch rotating QR sessions, author quizzes, and view live monitors. |
| **TEACHER** | `dr.verma` | `TeacherPass@2026` | Assigned to DBMS (CS503) for Division A1. |
| **STUDENT** | `2026CSE001` | `StudentPass@2026` | Aarav Patel — Division A1, Batch B1. Eligible for CEP Theory and ADS Practical. |
| **STUDENT** | `2026CSE002` | `StudentPass@2026` | Diya Sen — Division A1, Batch B2. |
| **STUDENT** | `2026CSE004` | `StudentPass@2026` | Ananya Gupta — Division A2, Batch B1. |

> **Security Note:** In accordance with prompt requirements, the initial administrator credentials are authenticated against the database hash and never hardcoded in the frontend.

---

## ⚙️ Core Technical Features

### 1. Rotating QR Code Attendance (Section 37–40, 58–59)
- **Cryptographic Rotation**: Every session generates unique random tokens and 6-character backup codes.
- **SHA-256 Storage**: Hashes are stored on the server (`qr_generations`).
- **Rotation Invalidation**: When generation $N+1$ activates, generation $N$ is immediately invalidated on the server.
- **Single-Marking Constraint**: Handled at the database level via `UNIQUE(attendance_session_id, student_id)`.
- **Anti-Bypass Validations**: Rejects expired tokens, old tokens, students from mismatched divisions or batches, and inactive accounts.

### 2. Raw Count Attendance Calculations (Section 47–49)
- **Mathematical Accuracy**: Always calculates `(total_present / total_conducted) * 100`.
- **Theory vs Practical**: Explicitly tracks Theory and Practical separately. Overall cumulative metrics are calculated directly from raw counts—never by averaging percentages.

### 3. Authoritative Live Quiz & Timer Engine (Section 21–30)
- **Server Timer**: Expiration is calculated as `start_time + duration_minutes` on the server. Client clock tampering is rendered completely ineffective.
- **Tab / Window Switch Monitoring**: Detects `visibilitychange` and window `blur`. The server logs violation numbers, duration, and auto-submits attempts when the threshold is exceeded with status `AUTO_SUBMITTED_VIOLATION`.
- **Question Types**:
  - **MCQ**: Auto-graded against verified choices.
  - **Numerical**: Supports exact decimals or configurable tolerance ($\pm \epsilon$) and precision.
  - **Subjective**: Student enters written analysis; instructor grades via the evaluation portal.
- **Result Release Control**: Students cannot see results or correct answers until the teacher-configured `result_release_time`.

### 4. Pluggable AI Service Adapter (Section 13–15, 76)
- Implements the official `@google/genai` SDK for Gemini models when `GEMINI_API_KEY` is present.
- Seamlessly falls back to an internal pedagogical generator that produces valid structured JSON schemas without hardcoding question banks.
- **Private Histories**: Student AI Doubt Solver conversations are isolated per user (`WHERE user_id = ?`).

### 5. Multi-Format Report Engine (Section 31, 50, 71)
- Downloads downloadable files across 4 enterprise formats:
  - **PDF**: Formatted via `PDFKit` with header banners, metadata boxes, and pagination.
  - **Word DOCX**: Formatted via `docx` library with styled tables and headers.
  - **Excel XLSX**: Created via `ExcelJS` with auto-column width calculations.
  - **CSV**: RFC-compliant CSV strings with escaped delimiters.

### 6. Design System & Custom Accent Picker (Section 60–63)
- Fully vanilla CSS tokens (`--accent-primary`, `--accent-glow`, `--accent-light`, `--accent-border`).
- **Layout Invariance**: Switching themes or selecting custom hex accents dynamically updates styling tokens without altering component layouts, spacing, or navigation.

---

## 🧪 Automated Test Suite

Run the full security test suite:
```bash
node tests/test_all_security.js
```
Verifies:
1. Admin bootstrap password hashing.
2. Role separation & student profile constraints.
3. Division/batch restrictions on faculty.
4. Cryptographic generation of rotating QR & backup codes.
5. Eligible student scan verification.
6. Rejection of duplicate scans.
7. Rejection of mismatched divisions.
8. Rejection of mismatched batches.
9. Invalidation of old QR tokens on rotation.
10. Raw-count attendance calculation formula.
11. Attendance eligibility gating on linked quizzes.
12. Server-authoritative auto-submission on tab-switch violations.
13. Numerical question tolerance evaluation.
14. Generation of valid PDF, DOCX, CSV, and Excel reports.

Run the end-to-end API test:
```bash
node tests/test_e2e_api.js
```
Verifies real HTTP requests for authentication, starting attendance, student QR submission, quiz creation, and PDF generation against the running server.
