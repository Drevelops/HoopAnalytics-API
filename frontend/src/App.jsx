import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navigation from './components/Navigation'
import Dashboard from './pages/Dashboard'
import PlayersList from './pages/PlayersList'
import PlayerDetail from './pages/PlayerDetail'
import TeamsList from './pages/TeamsList'

function App() {
  return (
    <Router>
      <div>
        <Navigation />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/players" element={<PlayersList />} />
          <Route path="/players/:player_id" element={<PlayerDetail />} />
          <Route path="/teams" element={<TeamsList />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App