# AutoLitTrack Frontend

## Overview
The `frontend` module of AutoLitTrack is a modern web application built with **React 18**, **Vite**, **Ant Design 5.24.8**, and **Tailwind CSS 4.1.4**. It provides an intuitive interface for searching academic papers, browsing literature lists, and monitoring scheduler status, interacting with a FastAPI backend at `http://127.0.0.1:8000`.

## Features
- **Search Page** (`/search`): Search papers by keywords with real-time arXiv integration.
- **Papers Page** (`/papers`): Display filtered literature lists in a responsive table.
- **Scheduler Status** (`/scheduler`): Monitor APScheduler task status.
- **Responsive Design**: Optimized for desktop and mobile using Tailwind CSS.

## Prerequisites
- **Node.js** ≥ 18
- **npm** ≥ 9
- **Backend**: FastAPI server running at `http://127.0.0.1:8000`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Ran-code000/AutoLitTrack.git
   cd AutoLitTrack/frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Ensure React 18 compatibility:
   ```bash
   npm install react@18.3.1 react-dom@18.3.1
   ```

## Usage
1. Start the development server:
   ```bash
   npm run dev
   ```
2. Open `http://localhost:5173` in your browser.
3. Navigate to:
   - `/search`: Enter keywords (e.g., "AI") to search papers.
   - `/papers`: View and filter literature lists.
   - `/scheduler`: Check scheduler status.

## Project Structure
```
frontend/
├── src/
│   ├── api/                # API client (Axios)
│   ├── components/         # Reusable UI components (e.g., NavBar)
│   ├── pages/              # Page components (Search, Papers, SchedulerStatus)
│   └── App.jsx             # Main app with routing
├── vite.config.js          # Vite configuration
└── package.json            # Dependencies and scripts
```

## Troubleshooting
- **Vite Import Errors** (e.g., `Failed to resolve import "./pages/Papers"`):
  - Verify `src/pages/Papers.jsx` exists and matches case.
  - Run `npm cache clean --force` and `npm install`.
- **API Timeouts** (e.g., `AxiosError: timeout of 15000ms exceeded`):
  - Ensure FastAPI runs at `http://127.0.0.1:8000`.
  - Test APIs with `curl http://127.0.0.1:8000/search?keyword=AI`.
  - Increase Axios timeout in `src/api/api.js` to `30000ms`.
- **Ant Design Compatibility**:
  - Use React 18.3.1 to avoid issues with Ant Design 5.24.8.

## Development
- **Linting**: Run `npm run lint` to check ESLint issues.
- **Build**: Run `npm run build` for production.
- **Debugging**: Use Chrome DevTools (Network tab) to inspect API requests.

## Contributing
Submit issues or pull requests to https://github.com/Ran-code000/AutoLitTrack. Ensure code follows ESLint rules and includes tests.

## License
MIT License