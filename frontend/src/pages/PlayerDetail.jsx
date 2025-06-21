import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
import PlayerStatsChart from '../components/PlayerStatsChart'

export default function PlayerDetail() {
  const { player_id } = useParams()
  const [player, setPlayer] = useState(null)
  const [stats, setStats] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
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
    return <div className="container p-5">Loading player details...</div>
  }

  if (!player) {
    return <div className="container p-5">Player not found</div>
  }

  return (
    <div className="container" style={{ maxWidth: '1200px' }}>
      {/* Back button */}
      <Link to="/players" className="nav-link" style={{ 
        color: '#1f2937', 
        marginBottom: '20px', 
        display: 'inline-block' 
      }}>
        ← Back to Players
      </Link>

      {/* Player Header */}
      <div className="bg-gray-100 p-6 rounded-lg mb-5">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">
          {player.name}
        </h1>
        <div className="grid grid-2 gap-4">
          <div>
            <p className="mb-2"><strong>Team:</strong> {player.team_name}</p>
            <p className="mb-2"><strong>Position:</strong> {player.position}</p>
            <p className="mb-2"><strong>Height:</strong> {player.height}</p>
          </div>
          <div>
            <p className="mb-2"><strong>Weight:</strong> {player.weight} lbs</p>
            <p className="mb-2"><strong>Age:</strong> {player.age}</p>
            <p className="mb-2"><strong>College:</strong> {player.college}</p>
          </div>
        </div>
      </div>

      {/* Player Stats */}
      {stats.length > 0 ? (
        <div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Season Statistics</h2>
          {stats.map((stat, index) => (
            <div key={index} className="card mb-4">
              <h3 className="text-xl font-bold text-gray-800 mb-4">
                {stat.season} Season
              </h3>
              
              {/* Stats Grid */}
              <div className="grid grid-3 gap-4">
                <div className="stat-card" style={{ backgroundColor: '#fef3c7' }}>
                  <div className="stat-value" style={{ color: '#92400e' }}>
                    {stat.ppg}
                  </div>
                  <div className="stat-label" style={{ color: '#78350f' }}>
                    Points per Game
                  </div>
                </div>
                
                <div className="stat-card" style={{ backgroundColor: '#dbeafe' }}>
                  <div className="stat-value" style={{ color: '#1e40af' }}>
                    {stat.rpg}
                  </div>
                  <div className="stat-label" style={{ color: '#1e3a8a' }}>
                    Rebounds per Game
                  </div>
                </div>
                
                <div className="stat-card" style={{ backgroundColor: '#dcfce7' }}>
                  <div className="stat-value" style={{ color: '#166534' }}>
                    {stat.apg}
                  </div>
                  <div className="stat-label" style={{ color: '#14532d' }}>
                    Assists per Game
                  </div>
                </div>
                
                <div className="stat-card" style={{ backgroundColor: '#fce7f3' }}>
                  <div className="stat-value" style={{ color: '#be185d' }}>
                    {(stat.fg_pct * 100).toFixed(1)}%
                  </div>
                  <div className="stat-label" style={{ color: '#9d174d' }}>
                    Field Goal %
                  </div>
                </div>
                
                <div className="stat-card" style={{ backgroundColor: '#f3e8ff' }}>
                  <div className="stat-value" style={{ color: '#7c3aed' }}>
                    {(stat.threept_pct * 100).toFixed(1)}%
                  </div>
                  <div className="stat-label" style={{ color: '#6b21a8' }}>
                    3-Point %
                  </div>
                </div>
                
                <div className="stat-card" style={{ backgroundColor: '#fef2f2' }}>
                  <div className="stat-value" style={{ color: '#dc2626' }}>
                    {stat.spg}
                  </div>
                  <div className="stat-label" style={{ color: '#b91c1c' }}>
                    Steals per Game
                  </div>
                </div>
              </div>
            </div>
          ))}
           <PlayerStatsChart stats={stats} playerName={player.name} />
        </div>
      ) : (
        <p>No stats available for this player.</p>
      )}
    </div>
  )
}