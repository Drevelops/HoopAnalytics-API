import { BrowserRouter as Router, Routes, Route, Link, useParams } from 'react-router-dom'
import { useState, useEffect } from 'react'

function Dashboard() {
  return (
    <div style={{ padding: '20px' }}>
      <h1>🏀 NBA Analytics Dashboard</h1>
      <p>Welcome to your NBA analytics platform!</p>
    </div>
  )
}

function PlayerDetail() {
  const { player_id } = useParams()
  const [player, setPlayer] = useState(null)
  const [stats, setStats] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch player info and stats
    Promise.all([
      fetch(`http://localhost:8000/api/v1/players/${player_id}`),
      fetch(`http://localhost:8000/api/v1/players/${player_id}/stats`)
    ])
    .then(async ([playerResponse, statsResponse]) => {
      const playerData = await playerResponse.json()
      const statsData = await statsResponse.json()
      
      setPlayer(playerData)
      setStats(statsData)
      setLoading(false)
    })
    .catch(error => {
      console.error('Error fetching player data:', error)
      setLoading(false)
    })
  }, [player_id])

  if (loading) {
    return <div style={{ padding: '20px' }}>Loading player details...</div>
  }

  if (!player) {
    return <div style={{ padding: '20px' }}>Player not found</div>
  }

  return (
    <div style={{ padding: '20px', maxWidth: '800px' }}>
      {/* Back button */}
      <Link to="/players" style={{ 
        color: '#1f2937', 
        textDecoration: 'none', 
        marginBottom: '20px', 
        display: 'inline-block' 
      }}>
        ← Back to Players
      </Link>

      {/* Player Header */}
      <div style={{ 
        backgroundColor: '#f3f4f6', 
        padding: '30px', 
        borderRadius: '12px', 
        marginBottom: '30px' 
      }}>
        <h1 style={{ margin: '0 0 10px 0', fontSize: '2.5rem' }}>
          {player.name}
        </h1>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '15px' }}>
          <div>
            <p><strong>Team:</strong> {player.team_name}</p>
            <p><strong>Position:</strong> {player.position}</p>
            <p><strong>Height:</strong> {player.height}</p>
          </div>
          <div>
            <p><strong>Weight:</strong> {player.weight} lbs</p>
            <p><strong>Age:</strong> {player.age}</p>
            <p><strong>College:</strong> {player.college}</p>
          </div>
        </div>
      </div>

      {/* Player Stats */}
      {stats.length > 0 ? (
        <div>
          <h2 style={{ marginBottom: '20px' }}>Season Statistics</h2>
          {stats.map((stat, index) => (
            <div key={index} style={{ 
              border: '1px solid #e5e7eb', 
              padding: '20px', 
              borderRadius: '8px',
              marginBottom: '15px'
            }}>
              <h3 style={{ margin: '0 0 15px 0' }}>
                {stat.season} Season
              </h3>
              
              {/* Stats Grid */}
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(3, 1fr)', 
                gap: '15px' 
              }}>
                <div style={{ textAlign: 'center', padding: '10px', backgroundColor: '#fef3c7', borderRadius: '6px' }}>
                  <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#92400e' }}>
                    {stat.ppg}
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#78350f' }}>
                    Points per Game
                  </div>
                </div>
                
                <div style={{ textAlign: 'center', padding: '10px', backgroundColor: '#dbeafe', borderRadius: '6px' }}>
                  <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1e40af' }}>
                    {stat.rpg}
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#1e3a8a' }}>
                    Rebounds per Game
                  </div>
                </div>
                
                <div style={{ textAlign: 'center', padding: '10px', backgroundColor: '#dcfce7', borderRadius: '6px' }}>
                  <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#166534' }}>
                    {stat.apg}
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#14532d' }}>
                    Assists per Game
                  </div>
                </div>
                
                <div style={{ textAlign: 'center', padding: '10px', backgroundColor: '#fce7f3', borderRadius: '6px' }}>
                  <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#be185d' }}>
                    {(stat.fg_pct * 100).toFixed(1)}%
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#9d174d' }}>
                    Field Goal %
                  </div>
                </div>
                
                <div style={{ textAlign: 'center', padding: '10px', backgroundColor: '#f3e8ff', borderRadius: '6px' }}>
                  <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#7c3aed' }}>
                    {(stat.threept_pct * 100).toFixed(1)}%
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#6b21a8' }}>
                    3-Point %
                  </div>
                </div>
                
                <div style={{ textAlign: 'center', padding: '10px', backgroundColor: '#fef2f2', borderRadius: '6px' }}>
                  <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#dc2626' }}>
                    {stat.spg}
                  </div>
                  <div style={{ fontSize: '0.875rem', color: '#b91c1c' }}>
                    Steals per Game
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p>No stats available for this player.</p>
      )}
    </div>
  )
}

function PlayersList() {
  const [players, setPlayers] = useState([])
  const [filteredPlayers, setFilteredPlayers] = useState([])
  const [loading, setLoading] = useState(true)
  
  // Filter states
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedTeam, setSelectedTeam] = useState('')
  const [selectedPosition, setSelectedPosition] = useState('')

  // Get unique teams and positions for filter dropdowns
  const uniqueTeams = [...new Set(players.map(p => p.team_name))].sort()
  const uniquePositions = [...new Set(players.map(p => p.position))].sort()

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/players/')
      .then(response => response.json())
      .then(data => {
        setPlayers(data)
        setFilteredPlayers(data) // Initially show all players
        setLoading(false)
      })
      .catch(error => {
        console.error('API Error:', error)
        setLoading(false)
      })
  }, [])

  // Filter players whenever search term or filters change
  useEffect(() => {
    let filtered = players

    // Filter by search term (name)
    if (searchTerm) {
      filtered = filtered.filter(player =>
        player.name.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Filter by team
    if (selectedTeam) {
      filtered = filtered.filter(player => player.team_name === selectedTeam)
    }

    // Filter by position
    if (selectedPosition) {
      filtered = filtered.filter(player => player.position === selectedPosition)
    }

    setFilteredPlayers(filtered)
  }, [searchTerm, selectedTeam, selectedPosition, players])

  // Clear all filters
  const clearFilters = () => {
    setSearchTerm('')
    setSelectedTeam('')
    setSelectedPosition('')
  }

  if (loading) return <div style={{ padding: '20px' }}>Loading players...</div>

  return (
    <div style={{ padding: '20px' }}>
      <h1>NBA Players ({filteredPlayers.length} of {players.length})</h1>
      
      {/* Search and Filter Section */}
      <div style={{ 
        backgroundColor: '#f9fafb', 
        padding: '20px', 
        borderRadius: '8px', 
        marginBottom: '20px',
        border: '1px solid #e5e7eb'
      }}>
        <h3 style={{ marginTop: '0', marginBottom: '15px' }}>Search & Filter Players</h3>
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
          gap: '15px',
          marginBottom: '15px'
        }}>
          {/* Search by name */}
          <div>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
              Search by Name:
            </label>
            <input
              type="text"
              placeholder="Enter player name..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                width: '100%',
                padding: '8px 12px',
                border: '1px solid #d1d5db',
                borderRadius: '6px',
                fontSize: '14px'
              }}
            />
          </div>

          {/* Filter by team */}
          <div>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
              Filter by Team:
            </label>
            <select
              value={selectedTeam}
              onChange={(e) => setSelectedTeam(e.target.value)}
              style={{
                width: '100%',
                padding: '8px 12px',
                border: '1px solid #d1d5db',
                borderRadius: '6px',
                fontSize: '14px'
              }}
            >
              <option value="">All Teams</option>
              {uniqueTeams.map(team => (
                <option key={team} value={team}>{team}</option>
              ))}
            </select>
          </div>

          {/* Filter by position */}
          <div>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
              Filter by Position:
            </label>
            <select
              value={selectedPosition}
              onChange={(e) => setSelectedPosition(e.target.value)}
              style={{
                width: '100%',
                padding: '8px 12px',
                border: '1px solid #d1d5db',
                borderRadius: '6px',
                fontSize: '14px'
              }}
            >
              <option value="">All Positions</option>
              {uniquePositions.map(position => (
                <option key={position} value={position}>{position}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Clear filters button */}
        <button
          onClick={clearFilters}
          style={{
            backgroundColor: '#6b7280',
            color: 'white',
            border: 'none',
            padding: '8px 16px',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '14px'
          }}
          onMouseEnter={(e) => e.target.style.backgroundColor = '#4b5563'}
          onMouseLeave={(e) => e.target.style.backgroundColor = '#6b7280'}
        >
          Clear All Filters
        </button>

        {/* Active filters display */}
        {(searchTerm || selectedTeam || selectedPosition) && (
          <div style={{ marginTop: '15px', fontSize: '14px', color: '#6b7280' }}>
            <strong>Active filters:</strong>
            {searchTerm && <span style={{ marginLeft: '10px', padding: '2px 8px', backgroundColor: '#dbeafe', borderRadius: '4px' }}>Name: "{searchTerm}"</span>}
            {selectedTeam && <span style={{ marginLeft: '10px', padding: '2px 8px', backgroundColor: '#dcfce7', borderRadius: '4px' }}>Team: {selectedTeam}</span>}
            {selectedPosition && <span style={{ marginLeft: '10px', padding: '2px 8px', backgroundColor: '#fef3c7', borderRadius: '4px' }}>Position: {selectedPosition}</span>}
          </div>
        )}
      </div>

      {/* Results */}
      {filteredPlayers.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px', color: '#6b7280' }}>
          <h3>No players found</h3>
          <p>Try adjusting your search criteria or clear filters.</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '15px' }}>
          {filteredPlayers.map(player => (
            <Link 
              key={player.id} 
              to={`/players/${player.id}`}
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              <div style={{ 
                border: '1px solid #ccc', 
                padding: '15px', 
                borderRadius: '8px',
                backgroundColor: '#f9f9f9',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
              onMouseEnter={(e) => e.target.style.backgroundColor = '#f3f4f6'}
              onMouseLeave={(e) => e.target.style.backgroundColor = '#f9f9f9'}
              >
                <h3 style={{ margin: '0 0 8px 0' }}>{player.name}</h3>
                <p style={{ margin: '4px 0' }}>Team: {player.team_name}</p>
                <p style={{ margin: '4px 0' }}>Position: {player.position} | Height: {player.height} | Weight: {player.weight} lbs</p>
                <p style={{ margin: '4px 0', fontSize: '0.9rem', color: '#666' }}>
                  Age: {player.age} | College: {player.college} | Country: {player.country}
                </p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

function Navigation() {
  return (
    <nav style={{ 
      backgroundColor: '#1f2937', 
      padding: '15px',
      marginBottom: '0'
    }}>
      <div style={{ display: 'flex', gap: '20px' }}>
        <Link to="/" style={{ color: 'white', textDecoration: 'none', fontWeight: 'bold' }}>
          🏀 NBA Analytics
        </Link>
        <Link to="/players" style={{ color: 'white', textDecoration: 'none' }}>
          Players
        </Link>
        <Link to="/teams" style={{ color: 'white', textDecoration: 'none' }}>
          Teams
        </Link>
      </div>
    </nav>
  )
}

function App() {
  return (
    <Router>
      <div>
        <Navigation />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/players" element={<PlayersList />} />
          <Route path="/players/:player_id" element={<PlayerDetail />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App