import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
import {apiCall} from '../utils/api'

function getNBATeamURL(abbreviation) {
  const teamURLMap = {
    'ATL': 'hawks',
    'BOS': 'celtics', 
    'BKN': 'nets',
    'CHA': 'hornets',
    'CHI': 'bulls',
    'CLE': 'cavaliers',
    'DAL': 'mavericks',
    'DEN': 'nuggets',
    'DET': 'pistons',
    'GSW': 'warriors',
    'HOU': 'rockets',
    'IND': 'pacers',
    'LAC': 'clippers',
    'LAL': 'lakers',
    'MEM': 'grizzlies',
    'MIA': 'heat',
    'MIL': 'bucks',
    'MIN': 'timberwolves',
    'NOP': 'pelicans',
    'NYK': 'knicks',
    'OKC': 'thunder',
    'ORL': 'magic',
    'PHI': 'sixers',
    'PHX': 'suns',
    'POR': 'blazers',
    'SAC': 'kings',
    'SAS': 'spurs',
    'TOR': 'raptors',
    'UTA': 'jazz',
    'WAS': 'wizards'
  }
  
  return teamURLMap[abbreviation] || abbreviation.toLowerCase()
}

export default function TeamDetail() {
  const { team_id } = useParams()
  const [team, setTeam] = useState(null)
  const [teamPlayers, setTeamPlayers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    console.log('Starting API calls for team:', team_id)
    
    Promise.all([
      apiCall(`/api/v1/teams/${team_id}`),
      apiCall('/api/v1/players/')
    ])
    .then(async ([teamResponse, playersResponse]) => {
      const teamData = await teamResponse.json()
      const allPlayers = await playersResponse.json()
      
      // ✅ Filter players by team_id on the frontend
      const teamPlayers = allPlayers.filter(player => player.team_id == team_id)
      
      setTeam(teamData)
      setTeamPlayers(teamPlayers)
      setLoading(false)
    })
    .catch(error => {
      console.error('Error fetching team data:', error)
      setError(error.message)
      setTeamPlayers([])
      setLoading(false)
    })
  }, [team_id])

  if (loading) {
    return <div className="container p-5">Loading team details...</div>
  }

  if (!team) {
    return <div className="container p-5">Team not found</div>
  }

  return (
    <div className="container">
      {/* Back button */}
      <Link to="/teams" className="nav-link" style={{ 
        color: '#1f2937', 
        marginBottom: '20px', 
        display: 'inline-block' 
      }}>
        ← Back to Teams
      </Link>

      {/* Team Header */}
      <div className="card mb-5" style={{ background: 'linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%)' }}>
        <div className="flex items-center mb-4">
          <img 
            src={team.logo_url} 
            alt={`${team.team_name} logo`}
            style={{ width: '80px', height: '80px', marginRight: '20px' }}
            onError={(e) => {
              e.target.style.display = 'none'
            }}
          />
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">
              {team.team_name}
            </h1>
            <p className="text-xl text-gray-600">
              {team.city} • {team.team_abbreviation}
            </p>
            <p className="text-gray-600">
              {team.conference} Conference • {team.division} Division
            </p>
          </div>
        </div>

        {/* Team Stats Overview */}
        <div className="grid grid-3 gap-4 mt-5">
          <div className="stat-card bg-white">
            <div className="stat-value text-gray-800">
              {team.current_season_wins}-{team.current_season_losses}
            </div>
            <div className="stat-label text-gray-600">
              Season Record
            </div>
          </div>
          
          <div className="stat-card bg-white">
            <div className="stat-value text-gray-800">
              {team.championship_titles}
            </div>
            <div className="stat-label text-gray-600">
              Championships
            </div>
          </div>
          
          <div className="stat-card bg-white">
            <div className="stat-value text-gray-800">
              {team.playoff_appearances}
            </div>
            <div className="stat-label text-gray-600">
              Playoff Appearances
            </div>
          </div>
        </div>
      </div>

      {/* Team Information */}
      <div className="grid grid-2 gap-5 mb-5">
        {/* Basic Info */}
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Team Information</h2>
          <div className="grid gap-3">
            <div>
              <p className="text-gray-600 text-sm">Arena</p>
              <p className="font-bold text-gray-800">{team.arena_name}</p>
            </div>
            <div>
              <p className="text-gray-600 text-sm">Head Coach</p>
              <p className="font-bold text-gray-800">{team.head_coach}</p>
            </div>
            <div>
              <p className="text-gray-600 text-sm">Founded</p>
              <p className="font-bold text-gray-800">{team.founded_year}</p>
            </div>
            <div>
              <p className="text-gray-600 text-sm">Team Colors</p>
              <div className="flex gap-2 mt-1">
                {team.team_colors.map((color, index) => (
                  <div 
                    key={index}
                    style={{ 
                      backgroundColor: color,
                      width: '20px',
                      height: '20px',
                      borderRadius: '50%',
                      border: '1px solid #ccc'
                    }}
                    title={color}
                  ></div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* External Links */}
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Links</h2>
          <div className="grid gap-3">
            <a 
              href="https://www.nba.com/" 
              target="_blank" 
              rel="noopener noreferrer"
              className="btn btn-gray text-center"
              style={{ textDecoration: 'none', color: 'white' }}
            >
              NBA Official Website
            </a>
            <a 
              href={`https://www.nba.com/${getNBATeamURL(team.team_abbreviation)}/`}
              target="_blank" 
              rel="noopener noreferrer"
              className="btn btn-gray text-center"
              style={{ textDecoration: 'none', color: 'white' }}
            >
              NBA.com Team Page
            </a>
          </div>
        </div>
      </div>

      {/* Team Roster */}
      <div className="card">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
          Current Roster ({teamPlayers.length} players)
        </h2>
        
        {teamPlayers.length === 0 ? (
          <p className="text-gray-600">No players found for this team in our database.</p>
        ) : (
          <div className="grid gap-3">
            {teamPlayers.map(player => (
              <Link 
                key={player.id} 
                to={`/players/${player.id}`}
                style={{ textDecoration: 'none', color: 'inherit' }}
              >
                <div className="player-card flex items-center justify-between">
                  <div>
                    <h3 className="font-bold text-gray-800">{player.name}</h3>
                    <p className="text-gray-600">
                      {player.position} • {player.height} • {player.weight} lbs
                    </p>
                    <p className="text-gray-600 text-sm">
                      Age: {player.age} • {player.college}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-gray-600 text-sm">Jersey #</p>
                    <p className="font-bold text-gray-800 text-xl">
                      {/* placeholder for jersey numbers need to add to player database model */}
                      #{Math.floor(Math.random() * 99) + 1}
                    </p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Team History Section */}
      {team.championship_titles > 0 && (
        <div className="card mt-5">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Team Achievements</h2>
          <div className="bg-yellow-50 p-4 rounded-lg">
            <div className="flex items-center">
              <span style={{ fontSize: '2rem', marginRight: '15px' }}>🏆</span>
              <div>
                <p className="font-bold text-gray-800">
                  {team.championship_titles} NBA Championship{team.championship_titles > 1 ? 's' : ''}
                </p>
                <p className="text-gray-600">
                  {team.playoff_appearances} playoff appearances since franchise founding
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}