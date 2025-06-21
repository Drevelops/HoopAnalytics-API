import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
} from 'chart.js'
import { Bar, Radar } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler
)

export default function PlayerStatsChart({ stats, playerName }) {
  if (!stats || stats.length === 0) {
    return <div className="text-gray-600">No stats available for charts</div>
  }

  // Use the first/most recent season stats
  const seasonStats = stats[0]

  // Bar Chart for main stats
  const barChartData = {
    labels: ['Points', 'Rebounds', 'Assists', 'Steals', 'Blocks'],
    datasets: [
      {
        label: `${playerName} - ${seasonStats.season}`,
        data: [
          seasonStats.ppg,
          seasonStats.rpg, 
          seasonStats.apg,
          seasonStats.spg,
          seasonStats.bpg
        ],
        backgroundColor: [
          'rgba(252, 211, 77, 0.8)',   // Gold for points
          'rgba(59, 130, 246, 0.8)',   // Blue for rebounds
          'rgba(34, 197, 94, 0.8)',    // Green for assists
          'rgba(236, 72, 153, 0.8)',   // Pink for steals
          'rgba(139, 69, 19, 0.8)',    // Brown for blocks
        ],
        borderColor: [
          'rgba(252, 211, 77, 1)',
          'rgba(59, 130, 246, 1)',
          'rgba(34, 197, 94, 1)',
          'rgba(236, 72, 153, 1)',
          'rgba(139, 69, 19, 1)',
        ],
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
      },
    ],
  }

  const barChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `${playerName} - Per Game Statistics`,
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.label}: ${context.parsed.y}`
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
          text: 'Per Game Average'
        }
      },
      x: {
        grid: {
          display: false,
        }
      }
    },
  }

  // Radar Chart for shooting percentages
  const radarChartData = {
    labels: [
      'Field Goal %',
      'Free Throw %', 
      '3-Point %',
      'Points/Game',
      'Assists/Game'
    ],
    datasets: [
      {
        label: playerName,
        data: [
          (seasonStats.fg_pct * 100).toFixed(1),
          (seasonStats.ft_pct * 100).toFixed(1),
          (seasonStats.threept_pct * 100).toFixed(1),
          ((seasonStats.ppg / 35) * 100).toFixed(1), // Normalize to percentage (35 ppg = 100%)
          ((seasonStats.apg / 15) * 100).toFixed(1), // Normalize to percentage (15 apg = 100%)
        ],
        fill: true,
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        borderColor: 'rgba(59, 130, 246, 1)',
        pointBackgroundColor: 'rgba(59, 130, 246, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(59, 130, 246, 1)',
        pointRadius: 6,
        pointHoverRadius: 8,
        borderWidth: 3,
      },
    ],
  }

  const radarChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `${playerName} - Performance Radar`,
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            if (context.label.includes('%')) {
              return `${context.label}: ${context.parsed.r}%`
            } else {
              return `${context.label}: ${context.parsed.r}% (normalized)`
            }
          }
        }
      }
    },
    scales: {
      r: {
        angleLines: {
          display: true
        },
        suggestedMin: 0,
        suggestedMax: 100,
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
        pointLabels: {
          font: {
            size: 12
          }
        },
        ticks: {
          display: false
        }
      }
    },
  }

  return (
    <div className="mt-5">
      <h2 className="text-2xl font-bold text-gray-800 mb-5">Performance Charts</h2>
      
      {/* Charts Grid */}
      <div className="grid grid-2 gap-5">
        {/* Bar Chart */}
        <div className="card">
          <Bar data={barChartData} options={barChartOptions} />
        </div>

        {/* Radar Chart */}
        <div className="card">
          <Radar data={radarChartData} options={radarChartOptions} />
        </div>
      </div>
      
      {/* Stats Summary */}
      <div className="card mt-5">
        <h3 className="text-xl font-bold text-gray-800 mb-3">Chart Insights</h3>
        <div className="grid grid-3 gap-4 text-center">
          <div className="bg-yellow-50 p-3 rounded">
            <p className="text-sm text-gray-600">Highest Stat</p>
            <p className="font-bold text-gray-800">
              {seasonStats.ppg >= Math.max(seasonStats.rpg, seasonStats.apg, seasonStats.spg, seasonStats.bpg) ? 'Scoring' :
               seasonStats.rpg >= Math.max(seasonStats.ppg, seasonStats.apg, seasonStats.spg, seasonStats.bpg) ? 'Rebounding' :
               seasonStats.apg >= Math.max(seasonStats.ppg, seasonStats.rpg, seasonStats.spg, seasonStats.bpg) ? 'Playmaking' : 'Defense'}
            </p>
          </div>
          
          <div className="bg-blue-50 p-3 rounded">
            <p className="text-sm text-gray-600">Best Shooting</p>
            <p className="font-bold text-gray-800">
              {seasonStats.ft_pct >= Math.max(seasonStats.fg_pct, seasonStats.threept_pct) ? 'Free Throws' :
               seasonStats.fg_pct >= seasonStats.threept_pct ? 'Field Goals' : '3-Pointers'}
            </p>
          </div>
          
          <div className="bg-green-50 p-3 rounded">
            <p className="text-sm text-gray-600">Overall Rating</p>
            <p className="font-bold text-gray-800">
              {((seasonStats.ppg + seasonStats.rpg + seasonStats.apg) / 3).toFixed(1)} AVG
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}