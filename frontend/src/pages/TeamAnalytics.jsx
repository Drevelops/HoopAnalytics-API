import { useState, useEffect } from 'react'
// import TeamComparisonChart from '../components/TeamComparisonChart'
import {apiCall} from '../utils/api'

export default function TeamAnalytics() {
  const [teams, setTeams] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    console.log('🔍 Analytics page - about to make API call')
    apiCall('/api/v1/teams/')
      .then(response => {
        console.log('✅ Analytics API response:', response.status)
        return response.json()
      })
      .then(data => {
        console.log('📊 Analytics data loaded:', data.length, 'teams')
        setTeams(data)
        setLoading(false)
      })
      .catch(error => {
        console.error('❌ Analytics API Error:', error)
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

      <div>Loaded {teams.length} teams - Chart temporarily disabled for debugging</div>
      {/* <TeamComparisonChart teams={teams} /> */}
    </div>
  )
}