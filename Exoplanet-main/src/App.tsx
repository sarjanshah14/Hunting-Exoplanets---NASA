import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Starfield } from './components/Starfield';
import { Dashboard } from './pages/Dashboard';
import { Specifications } from './pages/Specifications';
import { History } from './pages/History';
import { Explorer } from './pages/Explorer';
import { Learning } from './pages/Learning';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gradient-to-b from-gray-900 via-black to-gray-900 text-white relative overflow-x-hidden">
        <Starfield />
        <div className="relative z-10">
          <Navbar />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/specifications" element={<Specifications />} />
            <Route path="/history" element={<History />} />
            <Route path="/explorer" element={<Explorer />} />
            <Route path="/learning" element={<Learning />} />
          </Routes>
          <footer className="mt-20 py-8 border-t border-gray-800">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
                <p className="text-gray-400 text-sm text-center md:text-left">
                  AstroKit uses data from NASA's Kepler, K2, and TESS missions. All mission data is publicly available
                  through the NASA Exoplanet Archive.
                </p>
                <div className="flex space-x-6">
                  <a
                    href="https://github.com/nasa"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-gray-400 hover:text-cyan-400 transition-colors"
                  >
                    GitHub
                  </a>
                  <a
                    href="https://exoplanets.nasa.gov/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-gray-400 hover:text-cyan-400 transition-colors"
                  >
                    NASA
                  </a>
                </div>
              </div>
            </div>
          </footer>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
