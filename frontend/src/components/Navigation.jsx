import { Link } from 'react-router-dom'

export default function Navigation() {
  return (
    <nav className="nav">
      <div className="flex">
        <Link to="/" className="nav-brand">
          🏀 NBA Analytics
        </Link>
        <Link to="/players" className="nav-link">
          Players
        </Link>
        <Link to="/teams" className="nav-link">
          Teams
        </Link>
        <Link to="/analytics" className="nav-link">
        Analytics
        </Link>
      </div>
    </nav>
  )
}