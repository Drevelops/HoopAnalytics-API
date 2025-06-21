import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

export default function PlayersList() {
  const [players, setPlayers] = useState([])
  const [filteredPlayers, setFilteredPlayers] = useState([])
  const [loading, setLoading] = useState(true)
  
  // Filter states
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedTeam, setSelectedTeam] = useState('')
  const [selectedPosition, setSelectedPosition] = useState('')

  // Get unique teams and positions
  const uniqueTeams = [...new Set(players.map(p => p.team_name))].sort()
  const uniquePositions = [...new Set(players.map(p => p.position))].sort()

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/players/')
      .then(response => response.json())
      .then(data => {
        setPlayers(data)
        setFilteredPlayers(data)
        setLoading(false)
      })
      .catch(error => {
        console.error('API Error:', error)
        setLoading(false)
      })
  }, [])

  // Filter players
  useEffect(() => {
    let filtered = players

    if (searchTerm) {
      filtered = filtered.filter(player =>
        player.name.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (selectedTeam) {
      filtered = filtered.filter(player => player.team_name === selectedTeam)
    }

    if (selectedPosition) {
      filtered = filtered.filter(player => player.position === selectedPosition)
    }

    setFilteredPlayers(filtered)
  }, [searchTerm, selectedTeam, selectedPosition, players])

  const clearFilters = () => {
    setSearchTerm('')
    setSelectedTeam('')
    setSelectedPosition('')
  }

  if (loading) return <div className="container p-5">Loading players...</div>

  return (
    <div className="container">
      <h1 className="text-3xl font-bold text-gray-800 mb-5">
        NBA Players ({filteredPlayers.length} of {players.length})
      </h1>
      
      {/* Search and Filter Section */}
      <div className="filter-section">
        <h3 className="font-bold mb-4">Search & Filter Players</h3>
        
        <div className="grid grid-3 gap-4 mb-4">
          <div>
            <label className="font-bold mb-2" style={{ display: 'block' }}>
              Search by Name:
            </label>
            <input
              type="text"
              placeholder="Enter player name..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input"
            />
          </div>

          <div>
            <label className="font-bold mb-2" style={{ display: 'block' }}>
              Filter by Team:
            </label>
            <select
              value={selectedTeam}
              onChange={(e) => setSelectedTeam(e.target.value)}
              className="select"
            >
              <option value="">All Teams</option>
              {uniqueTeams.map(team => (
                <option key={team} value={team}>{team}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="font-bold mb-2" style={{ display: 'block' }}>
              Filter by Position:
            </label>
            <select
              value={selectedPosition}
              onChange={(e) => setSelectedPosition(e.target.value)}
              className="select"
            >
              <option value="">All Positions</option>
              {uniquePositions.map(position => (
                <option key={position} value={position}>{position}</option>
              ))}
            </select>
          </div>
        </div>

        <button onClick={clearFilters} className="btn btn-gray">
          Clear All Filters
        </button>
      </div>

      {/* Results */}
      {filteredPlayers.length === 0 ? (
        <div className="no-results">
          <h3>No players found</h3>
          <p>Try adjusting your search criteria or clear filters.</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {filteredPlayers.map(player => (
            <Link 
              key={player.id} 
              to={`/players/${player.id}`}
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              <div className="player-card">
                <h3 className="font-bold mb-2">{player.name}</h3>
                <p className="mb-1">Team: {player.team_name}</p>
                <p className="mb-1">Position: {player.position} | Height: {player.height} | Weight: {player.weight} lbs</p>
                <p className="text-gray-600" style={{ fontSize: '0.9rem' }}>
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