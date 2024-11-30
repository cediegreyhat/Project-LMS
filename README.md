# **Learner's Management System**

## **Table of Contents**
- [Introduction](#introduction)
- [Motivations](#motivations)
- [Features](#features)
- [Roadmap](#roadmap)
- [Project Structure](#project-structure)
- [Installation and Usage](#installation-and-usage)
- [Technology Stack](#technology-stack)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)

---

## **Introduction**
The **Tool Management System** is a full-stack project designed to streamline inventory management for tools. It supports functionalities like tool borrowing, returning, tracking, and maintaining tool conditions. This system ensures ease of use for both admins and users while providing reliable database storage with an intuitive interface.

---

## **Motivations**
This project was developed as part of a final assessment for a **Computer Engineering course** to apply knowledge of software engineering, databases, and user interface design. 

The motivation stems from:
1. The need for efficient tracking of tool inventory in educational and workplace settings.
2. Addressing real-world challenges like misplaced tools, insufficient quantities, and manual record-keeping.
3. Providing a professional and collaborative learning experience for team members with varying skill levels.

---

## **Features**
### Functional Requirements
1. **User Roles**:
   - **Admin**: Manage inventory (add, delete, update tools).
   - **Regular Users**: View and borrow tools.
2. **Tool Management**:
   - Add, edit, delete, and search tools.
   - Track tool quantities and conditions.
3. **Transaction Management**:
   - Borrow and return tools.
   - Record transactions with timestamps.
4. **Database**:
   - SQLite-based database for persistent and offline storage.
5. **GUI**:
   - Future integration of a user-friendly interface for interaction.

### Non-Functional Requirements
1. **Local Execution**:
   - Entirely offline functionality for secure and reliable operations.
2. **Simplicity**:
   - Clean design focusing on ease of use and functionality.

---

## **Roadmap**
### Week 1: Development Timeline
| Day  | Task                          | Details                                                                 | Deliverables                     |
|------|-------------------------------|-------------------------------------------------------------------------|----------------------------------|
| 1    | Project Setup                 | Define the database schema, initialize environment.                    | `inventory.db` with schema      |
| 2    | Backend Development           | Implement CRUD operations for tool management.                         | Functional backend               |
| 3    | Basic Interface               | Create GUI layout and implement basic forms (e.g., add tool).          | GUI for tool addition            |
| 4    | Borrow/Return Features        | Add borrow/return logic and integrate into the database.               | Borrow/return functionality      |
| 5    | Search and Reporting          | Search tools, generate basic reports (e.g., overdue tools).            | Search and reporting features    |
| 6    | Testing and Debugging         | Comprehensive testing, bug fixes, and sample data validation.          | Stable system                    |
| 7    | Documentation and Final Touches | Prepare user manual, project report, and final presentation.           | Complete project documentation   |

---

## **Project Structure**
```plaintext
/main
  ├── main.py          # Main backend logic
  ├── database.py      # Database interactions and CRUD operations
  ├── gui.py           # Frontend GUI
/db
  └── inventory.db     # SQLite database file
/docs
  ├── User_manual.pdf  # User manual documentation
  ├── project_report.pdf # Project report
```

## **Installation and Usage**
Prerequisites

    Python 3.x installed on your system.
    SQLite pre-installed (comes with Python).

Setup Instructions

   Clone this repository:
```
git clone [https://github.com/cediegreyhat/Project-LMS/.git](https://github.com/cediegreyhat/Project-LMS)
cd Project-LMS
```
Install required Python libraries:
```
pip install pandas
```

Run the project:

    python3 main/main.py

## **Technology Stack**

    Backend: Python (SQLite for database management)
    Database: SQLite (file-based)
    Future Plans for Frontend: Tkinter or PyQt for GUI

## **Future Enhancements**

    QR/Barcode Integration:
        Use QR codes for easy tool tracking and transactions.
    Analytics and Reporting:
        Visualize tool usage statistics with charts.
    Multi-User Authentication:
        Add login/logout functionality for admins and users.
    Enhanced GUI:
        Create a visually appealing interface with Tkinter or PyQT

## **Contributors**
Team Members:

    Lhord Cedrick T. Delos Santos (Team Leader): Backend Development, Database Integration
    Luis Fernandez: Basic GUI Development
    Warren Dollendo: Basic GUI Development
    Dan Angelo Domagsang: Basic GUI Development
    Charles Benedict Rafols: Database Development/Debug
    Charles Allen Lacsa: Documentation
    Brix Baldiray: Documentation
    Dylan Guliquey: Testing and Bug Fixing

Feel free to contribute or raise issues in the repository! 🚀




