import { BrowserRouter, Routes, Route } from "react-router-dom";
import "@/App.css";
import Dashboard from "@/pages/Dashboard";
import NewScan from "@/pages/NewScan";
import ReportView from "@/pages/ReportView";
import { Toaster } from "@/components/ui/sonner";

function App() {
  return (
    <div className="App">
      <Toaster position="top-right" />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/scan/new" element={<NewScan />} />
          <Route path="/report/:reportId" element={<ReportView />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
