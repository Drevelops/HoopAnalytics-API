import { useState, useEffect } from 'react'
import TeamComparisonChart from '../components/TeamComparisonChart'

export default function TeamAnalytics() {
  const [teams, setTeams] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/v1/teams/`)
      .then(response => response.json())
      .then(data => {
        setTeams(data)
        setLoading(false)
      })
      .catch(error => {
        console.error('API Error:', error)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div className="container p-5">Loading team analytics...</div>
  }

  return (
    <div className="container">
      <div className="text-center mb-5">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          🏀 NBA Team Analytics
        </h1>
        <p className="text-gray-600">
          Compare team performance, records, and championship history across the league
        </p>
      </div>

      <TeamComparisonChart teams={teams} />
    </div>
  )
}