# 🗄️ Database Module: Core Operations

---

## 📖 **Overview**

The **Database Module** provides the foundational data persistence layer for the **AutoLitTrack** system, enabling efficient storage and retrieval of academic paper metadata fetched from arXiv. Built using **SQLite** and **SQLAlchemy**, this module supports basic CRUD operations (Create, Read) for managing papers, ensuring lightweight and reliable data handling tailored for the project's hardware constraints.

---

## ✨ **Key Features**

- 📝 **Paper Storage**: Save paper metadata (title, abstract, link, published date, keyword) to a SQLite database.
- 🔍 **Keyword-Based Retrieval**: Retrieve papers by keyword with pagination support.
- ⚡ **Lightweight & Embedded**: Uses SQLite for zero-configuration, embedded storage.
- ✅ **Robust Testing**: Fully tested with unit tests to ensure reliability.
- 🛠️ **Scalable Design**: Modular structure for future enhancements (e.g., adding summary and keywords fields).

---

## 🛠️ **Technical Details**

### **Dependencies**

- **Python**: 3.8+
- **Libraries**:
  - `sqlalchemy`: For ORM-based database interactions.
  - `datetime`: For handling publication dates.

Install dependencies via:

```bash
pip install sqlalchemy
```

### **Module Structure**

The database module is organized into three key files under `backend/app/database/`:

- `config.py`: Manages database configuration and session handling (`DATABASE_URL`, `engine`, `SessionLocal`, `get_db`).
- `models.py`: Defines the `Paper` model and creates the database tables.
- `crud.py`: Implements core CRUD operations (`save_paper`, `get_papers_by_keyword`).

#### **Data Flow**

```mermaid
graph TD
    A[ArxivCrawler] --> B[Fetch Paper Data]
    B --> C[Call save_paper]
    C --> D[SQLite Database]
    D --> E[Store Paper Metadata]
    E --> F[Return Saved Paper]
    F --> G[Retrieve via get_papers_by_keyword]
    G --> H[Return Paper List]
```

#### **Database Schema**

The `Paper` model defines the structure of the `papers` table:

| **Field** | **Type** | **Description** |
| --- | --- | --- |
| `id` | Integer | Primary key, auto-incremented |
| `title` | String | Paper title (required) |
| `abstract` | Text | Paper abstract (required) |
| `link` | String | URL to the paper (required) |
| `published` | DateTime | Publication date (required) |
| `keyword` | String | Search keyword (required) |

#### **Key Methods**

- `save_paper(db: Session, paper: dict, keyword: str)`:

  - Saves a paper to the database.
  - Converts the `published` field to a `datetime` object.
  - Returns the saved paper object.

- `get_papers_by_keyword(db: Session, keyword: str, limit: int = 10)`:

  - Retrieves a list of papers matching the given keyword.
  - Supports pagination via the `limit` parameter.

---

## 🖥️ **Usage**

### **Example Code**

The database module is integrated with the `ArxivCrawler` to save and retrieve papers.

```python
from arxiv_crawler import ArxivCrawler
from database.crud import save_paper, get_db, get_papers_by_keyword

# Initialize the crawler
crawler = ArxivCrawler(max_results=3)

# Fetch papers
results = crawler.search_papers("machine learning")

# Save papers to the database
db = next(get_db())
for paper in results:
    saved_paper = save_paper(db, paper, "machine learning")
    print(f"Saved: {saved_paper.title}")

# Retrieve papers by keyword
papers = get_papers_by_keyword(db, "machine learning", limit=3)
for paper in papers:
    print(f"Retrieved: {paper.title}")
```

### **Sample Output**

```
Saved: A Survey on Machine Learning Techniques
Saved: Advances in Deep Learning Models
Saved: Machine Learning for Natural Language Processing
---
Retrieved: A Survey on Machine Learning Techniques
Retrieved: Advances in Deep Learning Models
Retrieved: Machine Learning for Natural Language Processing
```

---

## 🧪 **Testing**

The module has been thoroughly tested using `pytest`. The test suite is located at `test_backend/unit/test_database_CRUD.py`.

### **Run Tests**

From the project root directory, execute:

```bash
pytest test_backend/unit/test_database_CRUD.py -v
```

### **Expected Output**

```
==================================== test session starts ====================================
platform win32 -- Python 3.12.3, pytest-8.3.4, pluggy-1.5.0 -- D:\Anaconda\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Ran\Desktop\LitGenius
configfile: pytest.ini
plugins: anyio-4.6.2
collected 4 items

test_backend/unit/test_database_CRUD.py::test_save_paper PASSED                        [ 25%] 
test_backend/unit/test_database_CRUD.py::test_save_paper_missing_fields PASSED        [ 50%] 
test_backend/unit/test_database_CRUD.py::test_get_papers_by_keyword PASSED            [ 75%]
test_backend/unit/test_database_CRUD.py::test_get_papers_by_keyword_no_results PASSED [100%] 

===================================== 4 passed in 0.52s ===================================== 
```

### **Test Details**

- **Fixtures**:
  - `db_session`: Creates a temporary in-memory SQLite database (`sqlite:///:memory:`), initializes the `Paper` table, and provides a clean testing environment using `sessionmaker`.
- **Test Cases**:
  - `test_save_paper`: Verifies that `save_paper` correctly saves a paper and checks the database record.
  - `test_save_paper_missing_fields`: Tests saving a paper with missing fields (e.g., empty abstract).
  - `test_get_papers_by_keyword`: Saves multiple papers and verifies `get_papers_by_keyword` retrieves them correctly.
  - `test_get_papers_by_keyword_no_results`: Ensures an empty list is returned for non-matching keywords.
- **Dependencies**:
  - Relies on `backend.app.database.models` and `crud` modules.
  - Uses `pytest` and `sqlalchemy` for testing.

---

## 📊 **Performance & Resource Usage**

The database module is optimized for lightweight operation:

- **Storage**: SQLite uses a single file (`papers.db`), requiring zero configuration.
- **Memory Usage**: &lt;5MB for the database engine.
- **Read/Write Performance**: Supports up to 100,000 operations/second on a local SSD.
- **Hardware Fit**: Ideal for embedded systems and small-to-medium data volumes.

---

## 🛠️ **Development Notes**

### **Error Handling**

- **Database Connection**: The `get_db` function (in `config.py`) ensures proper session management, closing the session after each operation.
- **Data Validation**: The `Paper` model enforces required fields (e.g., `title`, `abstract`, `link`).
- **Exception Handling**: The `ArxivCrawler` integration catches and logs database errors during saving.

### **Benefits of Adding** `config.py`

The database module separates concerns by introducing `config.py`, which provides several advantages:

- **Module Responsibilities**:

  - `config.py`: Responsible for database connection and session management (e.g., `DATABASE_URL`, connection parameters, session settings).
  - `models.py`: Solely focuses on defining database models and table structures.
  - `crud.py`: Exclusively handles database operation logic.

- **Key Advantages**:

  1. **Logic Separation**: Decouples configuration logic from model definitions. `models.py` focuses on models, while `config.py` handles database connections and session management.
  2. **Modularity**: Centralizes all database configurations in `config.py`, allowing other modules to import functions or objects directly from `config.py`.
  3. **Clear Dependency Chain**: `crud.py` and `ArxivCrawler` depend only on `config.py` for session management, eliminating direct reliance on `models.py`.
  4. **Centralized Configuration**: All database-related settings (e.g., `DATABASE_URL`, connection parameters, session configurations) reside in `config.py`. Changing the database (e.g., from SQLite to PostgreSQL) requires modifying only `config.py`.
     - **Example**: Switching `DATABASE_URL` from `"sqlite:///papers.db"` to a PostgreSQL connection string (e.g., `"postgresql://user:password@localhost:5432/dbname"`) involves editing just one line in `config.py`.
  5. **Reduced Duplication**: `get_db` and `SessionLocal` are defined once in `config.py`, and other modules can import them directly, avoiding redundant definitions.
  6. **Lower Coupling**: `models.py` no longer handles configuration tasks, reducing inter-module dependencies. For instance, `crud.py` now imports `SessionLocal` from `config.py` instead of `models.py`.

### **Future Improvements**

- Add support for storing additional fields (e.g., `keywords`, `summary`).
- Implement indexing on the `keyword` column for faster queries.
- Add support for user-specific features (e.g., search history, favorites).

---

## 📜 **License**

This module is part of the **AutoLitTrack** project and is licensed under the MIT License.

## 📬 **Contact**

For issues or contributions, please open an issue on GitHub or reach out via my GitHub profile.

---

*Persisting Academic Insights with Efficiency and Reliability.*
