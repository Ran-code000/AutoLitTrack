import { BrowserRouter, Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import Search from "./pages/Search";
import Papers from "./pages/Paper";
import SchedulerStatus from "./pages/SchedulerStatus";

const App = () => {
  return (
    <BrowserRouter>
      <NavBar />
      <div className="min-h-screen bg-gray-100">
        <Routes>
          <Route path="/" element={<Search />} />
          <Route path="/papers" element={<Papers />} />
          <Route path="/scheduler" element={<SchedulerStatus />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;