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

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

export default function TeamComparisonChart({ teams }) {
  if (!teams || teams.length === 0) {
    return <div className="text-gray-600">No team data available for charts</div>
  }

  // Sort teams by wins for better visualization
  const sortedTeams = [...teams].sort((a, b) => b.current_season_wins - a.current_season_wins)

  // Conference Wins Comparison (Top 10 teams)
  const topTeams = sortedTeams.slice(0, 10)
  const conferenceData = {
    labels: topTeams.map(team => team.team_abbreviation),
    datasets: [
      {
        label: 'Wins',
        data: topTeams.map(team => team.current_season_wins),
        backgroundColor: 'rgba(34, 197, 94, 0.8)',
        borderColor: 'rgba(34, 197, 94, 1)',
        borderWidth: 2,
        borderRadius: 6,
      },
      {
        label: 'Losses', 
        data: topTeams.map(team => team.current_season_losses),
        backgroundColor: 'rgba(239, 68, 68, 0.8)',
        borderColor: 'rgba(239, 68, 68, 1)',
        borderWidth: 2,
        borderRadius: 6,
      }
    ],
  }

  const conferenceOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Top 10 Teams - Season Record Comparison',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        callbacks: {
          afterLabel: function(context) {
            const team = topTeams[context.dataIndex]
            const winPct = (team.current_season_wins / (team.current_season_wins + team.current_season_losses) * 100).toFixed(1)
            return `Win %: ${winPct}%`
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 82,
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
        title: {
          display: true,
          text: 'Games'
        }
      },
      x: {
        grid: {
          display: false,
        }
      }
    },
  }

  // Conference Distribution Pie Chart
  const easternTeams = teams.filter(team => team.conference === 'Eastern')
  const westernTeams = teams.filter(team => team.conference === 'Western')
  const easternWins = easternTeams.reduce((sum, team) => sum + team.current_season_wins, 0)
  const westernWins = westernTeams.reduce((sum, team) => sum + team.current_season_wins, 0)

  const conferenceDistributionData = {
    labels: ['Eastern Conference', 'Western Conference'],
    datasets: [
      {
        label: 'Total Wins',
        data: [easternWins, westernWins],
        backgroundColor: [
          'rgba(59, 130, 246, 0.8)',   // Blue for Eastern
          'rgba(239, 68, 68, 0.8)',    // Red for Western
        ],
        borderColor: [
          'rgba(59, 130, 246, 1)',
          'rgba(239, 68, 68, 1)',
        ],
        borderWidth: 3,
      },
    ],
  }

  const pieOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
      },
      title: {
        display: true,
        text: 'Conference Win Distribution',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const total = easternWins + westernWins
            const percentage = ((context.parsed / total) * 100).toFixed(1)
            return `${context.label}: ${context.parsed} wins (${percentage}%)`
          }
        }
      }
    },
  }

  // Championships Distribution
  const championshipData = teams.filter(team => team.championship_titles > 0)
    .sort((a, b) => b.championship_titles - a.championship_titles)
    .slice(0, 8) // Top 8 teams with championships

  const championshipChartData = {
    labels: championshipData.map(team => team.team_abbreviation),
    datasets: [
      {
        label: 'Championships',
        data: championshipData.map(team => team.championship_titles),
        backgroundColor: [
          'rgba(255, 215, 0, 0.8)',    // Gold
          'rgba(192, 192, 192, 0.8)',  // Silver 
          'rgba(205, 127, 50, 0.8)',   // Bronze
          'rgba(138, 43, 226, 0.8)',   // Purple
          'rgba(255, 69, 0, 0.8)',     // Red-Orange
          'rgba(0, 191, 255, 0.8)',    // Deep Sky Blue
          'rgba(50, 205, 50, 0.8)',    // Lime Green
          'rgba(255, 20, 147, 0.8)',   // Deep Pink
        ],
        borderColor: [
          'rgba(255, 215, 0, 1)',
          'rgba(192, 192, 192, 1)',
          'rgba(205, 127, 50, 1)',
          'rgba(138, 43, 226, 1)',
          'rgba(255, 69, 0, 1)',
          'rgba(0, 191, 255, 1)',
          'rgba(50, 205, 50, 1)',
          'rgba(255, 20, 147, 1)',
        ],
        borderWidth: 2,
        borderRadius: 8,
      },
    ],
  }

  const championshipOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'All-Time Championships by Team',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        callbacks: {
          afterLabel: function(context) {
            const team = championshipData[context.dataIndex]
            return `Last title: Franchise history`
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
        title: {
          display: true,
          text: 'Championships'
        }
      },
      x: {
        grid: {
          display: false,
        }
      }
    },
  }

  return (
    <div className="mt-5">
      <h2 className="text-2xl font-bold text-gray-800 mb-5">League Analytics</h2>
      
      {/* Charts Grid */}
      <div className="grid grid-2 gap-5 mb-5">
        {/* Season Record Comparison */}
        <div className="card">
          <Bar data={conferenceData} options={conferenceOptions} />
        </div>

        {/* Conference Distribution */}
        <div className="card">
          <Doughnut data={conferenceDistributionData} options={pieOptions} />
        </div>
      </div>

      {/* Championship History - Full Width */}
      <div className="card mb-5">
        <Bar data={championshipChartData} options={championshipOptions} />
      </div>
      
      {/* League Insights */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-800 mb-4">League Insights</h3>
        <div className="grid grid-3 gap-4">
          <div className="bg-green-50 p-4 rounded text-center">
            <p className="text-sm text-gray-600">Best Record</p>
            <p className="font-bold text-gray-800 text-lg">
              {sortedTeams[0]?.team_abbreviation}
            </p>
            <p className="text-gray-600 text-sm">
              {sortedTeams[0]?.current_season_wins}-{sortedTeams[0]?.current_season_losses}
            </p>
          </div>
          
          <div className="bg-blue-50 p-4 rounded text-center">
            <p className="text-sm text-gray-600">Most Championships</p>
            <p className="font-bold text-gray-800 text-lg">
              {championshipData[0]?.team_abbreviation}
            </p>
            <p className="text-gray-600 text-sm">
              {championshipData[0]?.championship_titles} titles
            </p>
          </div>
          
          <div className="bg-yellow-50 p-4 rounded text-center">
            <p className="text-sm text-gray-600">Conference Leader</p>
            <p className="font-bold text-gray-800 text-lg">
              {easternWins > westernWins ? 'Eastern' : 'Western'}
            </p>
            <p className="text-gray-600 text-sm">
              {Math.max(easternWins, westernWins)} total wins
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}