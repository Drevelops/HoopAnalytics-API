import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

export default function TeamsList() {
  const [teams, setTeams] = useState([])
  const [filteredTeams, setFilteredTeams] = useState([])
  const [loading, setLoading] = useState(true)
  
  // Filter states
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedConference, setSelectedConference] = useState('')
  const [selectedDivision, setSelectedDivision] = useState('')

  // Get unique conferences and divisions
  const uniqueConferences = [...new Set(teams.map(t => t.conference))].sort()
  const uniqueDivisions = [...new Set(teams.map(t => t.division))].sort()

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/v1/teams/`)
      .then(response => response.json())
      .then(data => {
        setTeams(data)
        setFilteredTeams(data)
        setLoading(false)
      })
      .catch(error => {
        console.error('API Error:', error)
        setLoading(false)
      })
  }, [])

  // Filter teams
  useEffect(() => {
    let filtered = teams

    if (searchTerm) {
      filtered = filtered.filter(team =>
        team.team_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        team.city.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (selectedConference) {
      filtered = filtered.filter(team => team.conference === selectedConference)
    }

    if (selectedDivision) {
      filtered = filtered.filter(team => team.division === selectedDivision)
    }

    setFilteredTeams(filtered)
  }, [searchTerm, selectedConference, selectedDivision, teams])

  const clearFilters = () => {
    setSearchTerm('')
    setSelectedConference('')
    setSelectedDivision('')
  }

  if (loading) return <div className="container p-5">Loading teams...</div>

  return (
    <div className="container">
      <h1 className="text-3xl font-bold text-gray-800 mb-5">
        NBA Teams ({filteredTeams.length} of {teams.length})
      </h1>
      
      {/* Search and Filter Section */}
      <div className="filter-section">
        <h3 className="font-bold mb-4">Search & Filter Teams</h3>
        
        <div className="grid grid-3 gap-4 mb-4">
          <div>
            <label className="font-bold mb-2" style={{ display: 'block' }}>
              Search by Team or City:
            </label>
            <input
              type="text"
              placeholder="Enter team or city name..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input"
            />
          </div>

          <div>
            <label className="font-bold mb-2" style={{ display: 'block' }}>
              Filter by Conference:
            </label>
            <select
              value={selectedConference}
              onChange={(e) => setSelectedConference(e.target.value)}
              className="select"
            >
              <option value="">All Conferences</option>
              {uniqueConferences.map(conference => (
                <option key={conference} value={conference}>{conference}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="font-bold mb-2" style={{ display: 'block' }}>
              Filter by Division:
            </label>
            <select
              value={selectedDivision}
              onChange={(e) => setSelectedDivision(e.target.value)}
              className="select"
            >
              <option value="">All Divisions</option>
              {uniqueDivisions.map(division => (
                <option key={division} value={division}>{division}</option>
              ))}
            </select>
          </div>
        </div>

        <button onClick={clearFilters} className="btn btn-gray">
          Clear All Filters
        </button>
      </div>

      {/* Results */}
      {filteredTeams.length === 0 ? (
        <div className="no-results">
          <h3>No teams found</h3>
          <p>Try adjusting your search criteria or clear filters.</p>
        </div>
      ) : (
        <div className="grid grid-auto gap-5">
          {filteredTeams.map(team => (
            <Link 
              key={team.id} 
              to={`/teams/${team.id}`}
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              <div className="card hover-lift">
                {/* Team Header */}
                <div className="flex items-center mb-4" style={{ 
                  paddingBottom: '15px',
                  borderBottom: '1px solid #f3f4f6'
                }}>
                  <img 
                    src={team.logo_url} 
                    alt={`${team.team_name} logo`}
                    style={{ width: '50px', height: '50px', marginRight: '15px' }}
                    onError={(e) => {
                      e.target.style.display = 'none'
                    }}
                  />
                  <div>
                    <h3 className="text-xl font-bold text-gray-800">{team.team_name}</h3>
                    <p className="text-gray-600" style={{ fontSize: '0.9rem' }}>
                      {team.city} • {team.team_abbreviation}
                    </p>
                  </div>
                </div>

                {/* Team Info */}
                <div className="grid grid-2 gap-4 mb-4">
                  <div>
                    <p className="text-gray-600" style={{ fontSize: '0.875rem' }}>Conference</p>
                    <p className="font-bold text-gray-700">{team.conference}</p>
                  </div>
                  <div>
                    <p className="text-gray-600" style={{ fontSize: '0.875rem' }}>Division</p>
                    <p className="font-bold text-gray-700">{team.division}</p>
                  </div>
                  <div>
                    <p className="text-gray-600" style={{ fontSize: '0.875rem' }}>Arena</p>
                    <p className="font-bold text-gray-700">{team.arena_name}</p>
                  </div>
                  <div>
                    <p className="text-gray-600" style={{ fontSize: '0.875rem' }}>Head Coach</p>
                    <p className="font-bold text-gray-700">{team.head_coach}</p>
                  </div>
                </div>

                {/* Season Record */}
                <div className="bg-gray-50 p-4 rounded text-center">
                  <p className="text-gray-600" style={{ fontSize: '0.875rem' }}>
                    Current Season Record
                  </p>
                  <p className="text-xl font-bold text-gray-800 mt-1">
                    {team.current_season_wins}-{team.current_season_losses}
                  </p>
                </div>

                {/* Championships */}
                {team.championship_titles > 0 && (
                  <div className="text-center mt-3">
                    <span style={{
                      backgroundColor: '#fef3c7',
                      color: '#92400e',
                      padding: '4px 8px',
                      borderRadius: '4px',
                      fontSize: '0.75rem',
                      fontWeight: 'bold'
                    }}>
                      🏆 {team.championship_titles} Championship{team.championship_titles > 1 ? 's' : ''}
                    </span>
                  </div>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}