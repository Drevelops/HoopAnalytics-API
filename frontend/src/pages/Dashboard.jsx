import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js'
import { Bar, Doughnut } from 'react-chartjs-2'
import {apiCall} from '../utils/api'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)


export default function Dashboard() {
  const [players, setPlayers] = useState([])
  const [teams, setTeams] = useState([])
  const [playerStats, setPlayerStats] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      apiCall('/api/v1/players/'),
      apiCall('/api/v1/teams/'),
      apiCall('/api/v1/players/stats')
    ])
    .then(async ([playersResponse, teamsResponse, statsResponse]) => {
      const playersData = await playersResponse.json()
      const teamsData = await teamsResponse.json()
      const statsData = await statsResponse.json()
      
      setPlayers(playersData)
      setTeams(teamsData)
      setPlayerStats(statsData)
      setLoading(false)
    })
    .catch(error => {
      console.error('Dashboard API Error:', error)
      setLoading(false)
    })
  }, [])

  if (loading) {
    return <div className="container p-5">Loading dashboard...</div>
  }

  // Get top performers
  const topScorers = playerStats
    .sort((a, b) => b.ppg - a.ppg)
    .slice(0, 5)
    .map(stat => {
      const player = players.find(p => p.id === stat.player_id)
      return { ...stat, playerName: player?.name || 'Unknown', teamName: player?.team_name || 'Unknown' }
    })

  const topRebounders = playerStats
    .sort((a, b) => b.rpg - a.rpg)
    .slice(0, 5)
    .map(stat => {
      const player = players.find(p => p.id === stat.player_id)
      return { ...stat, playerName: player?.name || 'Unknown' }
    })

  const topAssists = playerStats
    .sort((a, b) => b.apg - a.apg)
    .slice(0, 5)
    .map(stat => {
      const player = players.find(p => p.id === stat.player_id)
      return { ...stat, playerName: player?.name || 'Unknown' }
    })

  // Top teams by wins
  const topTeams = teams
    .sort((a, b) => b.current_season_wins - a.current_season_wins)
    .slice(0, 8)

  // Top Scorers Chart
  const scorersChartData = {
    labels: topScorers.map(player => player.playerName?.split(' ').slice(-1)[0] || 'Unknown'), // Last name only
    datasets: [
      {
        label: 'Points Per Game',
        data: topScorers.map(player => player.ppg),
        backgroundColor: 'rgba(252, 211, 77, 0.8)',
        borderColor: 'rgba(252, 211, 77, 1)',
        borderWidth: 2,
        borderRadius: 6,
      },
    ],
  }

  const scorersChartOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: {
        display: true,
        text: 'Top 5 Scorers',
        font: { size: 14, weight: 'bold' }
      },
    },
    scales: {
      y: { beginAtZero: true, grid: { color: 'rgba(0, 0, 0, 0.1)' } },
      x: { grid: { display: false } }
    },
  }

  // Conference distribution
  const easternTeams = teams.filter(team => team.conference === 'Eastern')
  const westernTeams = teams.filter(team => team.conference === 'Western')

  const conferenceData = {
    labels: ['Eastern Conference', 'Western Conference'],
    datasets: [
      {
        data: [easternTeams.length, westernTeams.length],
        backgroundColor: ['rgba(59, 130, 246, 0.8)', 'rgba(239, 68, 68, 0.8)'],
        borderColor: ['rgba(59, 130, 246, 1)', 'rgba(239, 68, 68, 1)'],
        borderWidth: 2,
      },
    ],
  }

  const conferenceOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'bottom' },
      title: {
        display: true,
        text: 'Conference Distribution',
        font: { size: 14, weight: 'bold' }
      },
    },
  }

  return (
    <div className="container">
      {/* Hero Section */}
      <div className="text-center mb-5" style={{ 
        background: 'linear-gradient(135deg, #1f2937 0%, #374151 100%)',
        padding: '3rem 2rem',
        borderRadius: '12px',
        color: 'white',
        marginBottom: '2rem'
      }}>
        <h1 className="text-3xl font-bold mb-2">
          🏀 NBA Analytics Dashboard
        </h1>
        <p className="text-xl" style={{ opacity: 0.9 }}>
          Your complete source for NBA player and team statistics
        </p>
        <div className="flex justify-center gap-4 mt-4">
          <span className="bg-white" style={{ 
            color: '#1f2937', 
            padding: '0.5rem 1rem', 
            borderRadius: '6px',
            fontWeight: 'bold',
            fontSize: '0.9rem'
          }}>
            {teams.length} Teams
          </span>
          <span className="bg-white" style={{ 
            color: '#1f2937', 
            padding: '0.5rem 1rem', 
            borderRadius: '6px',
            fontWeight: 'bold',
            fontSize: '0.9rem'
          }}>
            {players.length} Players
          </span>
          <span className="bg-white" style={{ 
            color: '#1f2937', 
            padding: '0.5rem 1rem', 
            borderRadius: '6px',
            fontWeight: 'bold',
            fontSize: '0.9rem'
          }}>
            {playerStats.length} Stat Records
          </span>
        </div>
      </div>

      {/* Quick Stats Grid */}
      <div className="grid grid-3 gap-5 mb-5">
        <div className="card text-center">
          <h3 className="text-lg font-bold text-gray-800 mb-2">League Leader</h3>
          <div className="text-2xl font-bold text-yellow-600 mb-1">
            {topScorers[0]?.ppg || 'N/A'} PPG
          </div>
          <p className="text-gray-600 text-sm">
            {topScorers[0]?.playerName || 'No data'}
          </p>
        </div>

        <div className="card text-center">
          <h3 className="text-lg font-bold text-gray-800 mb-2">Best Record</h3>
          <div className="text-2xl font-bold text-green-600 mb-1">
            {topTeams[0]?.current_season_wins || 0}-{topTeams[0]?.current_season_losses || 0}
          </div>
          <p className="text-gray-600 text-sm">
            {topTeams[0]?.team_abbreviation || 'No data'}
          </p>
        </div>

        <div className="card text-center">
          <h3 className="text-lg font-bold text-gray-800 mb-2">Top Rebounder</h3>
          <div className="text-2xl font-bold text-blue-600 mb-1">
            {topRebounders[0]?.rpg || 'N/A'} RPG
          </div>
          <p className="text-gray-600 text-sm">
            {topRebounders[0]?.playerName || 'No data'}
          </p>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-2 gap-5 mb-5">
        <div className="card">
          <Bar data={scorersChartData} options={scorersChartOptions} />
        </div>
        <div className="card">
          <Doughnut data={conferenceData} options={conferenceOptions} />
        </div>
      </div>

      {/* Top Performers Section */}
      <div className="grid grid-3 gap-5 mb-5">
        {/* Top Scorers */}
        <div className="card">
          <h3 className="text-lg font-bold text-gray-800 mb-3">🏆 Top Scorers</h3>
          <div className="space-y-2">
            {topScorers.map((player, index) => (
              <Link 
                key={index}
                to={`/players/${player.player_id}`}
                style={{ textDecoration: 'none', color: 'inherit' }}
              >
                <div className="flex justify-between items-center p-2 hover:bg-gray-50 rounded transition">
                  <div>
                    <p className="font-bold text-sm">{player.playerName}</p>
                    <p className="text-gray-600 text-xs">{player.teamName}</p>
                  </div>
                  <span className="font-bold text-yellow-600">{player.ppg}</span>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Top Rebounders */}
        <div className="card">
          <h3 className="text-lg font-bold text-gray-800 mb-3">🏀 Top Rebounders</h3>
          <div className="space-y-2">
            {topRebounders.map((player, index) => (
              <Link 
                key={index}
                to={`/players/${player.player_id}`}
                style={{ textDecoration: 'none', color: 'inherit' }}
              >
                <div className="flex justify-between items-center p-2 hover:bg-gray-50 rounded transition">
                  <p className="font-bold text-sm">{player.playerName}</p>
                  <span className="font-bold text-blue-600">{player.rpg}</span>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Top Assist Leaders */}
        <div className="card">
          <h3 className="text-lg font-bold text-gray-800 mb-3">🎯 Assist Leaders</h3>
          <div className="space-y-2">
            {topAssists.map((player, index) => (
              <Link 
                key={index}
                to={`/players/${player.player_id}`}
                style={{ textDecoration: 'none', color: 'inherit' }}
              >
                <div className="flex justify-between items-center p-2 hover:bg-gray-50 rounded transition">
                  <p className="font-bold text-sm">{player.playerName}</p>
                  <span className="font-bold text-green-600">{player.apg}</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Navigation */}
      <div className="card text-center">
        <h3 className="text-xl font-bold text-gray-800 mb-4">Explore More</h3>
        <div className="flex justify-center gap-4">
          <Link to="/players" className="btn btn-gray">
            Browse All Players →
          </Link>
          <Link to="/teams" className="btn btn-gray">
            View All Teams →
          </Link>
          <Link to="/analytics" className="btn btn-gray">
            Team Analytics →
          </Link>
        </div>
      </div>
    </div>
  )
}