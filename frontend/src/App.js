import { BrowserRouter, Routes, Route } from "react-router-dom";
import "@/App.css";
import Dashboard from "@/pages/Dashboard";
import NewScan from "@/pages/NewScan";
import ReportView from "@/pages/ReportView";
import RepoScanUpload from "@/pages/RepoScanUpload";
import RepoScanResults from "@/pages/RepoScanResults";
import { Toaster } from "@/components/ui/sonner";

function App() {
  return (
    <div className="App">
      <Toaster position="top-right" />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/scan/new" element={<NewScan />} />
          <Route path="/scan/repo" element={<RepoScanUpload />} />
          <Route path="/scan/repo/:scanId" element={<RepoScanResults />} />
          <Route path="/report/:reportId" element={<ReportView />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
