import { Link, Route, Routes } from 'react-router-dom'
import GamePage from './pages/GamePage'
import StatsPage from './pages/StatsPage'

export default function App() {
  return (
    <div style={{ maxWidth: 980, margin: '0 auto', padding: 16 }}>
      <header style={{ display: 'flex', alignItems: 'baseline', gap: 16 }}>
        <h2 style={{ margin: 0 }}>Math Guessing Game</h2>
        <nav style={{ display: 'flex', gap: 12 }}>
          <Link to="/">Game</Link>
          <Link to="/stats">Stats</Link>
        </nav>
      </header>
      <hr />
      <Routes>
        <Route path="/" element={<GamePage />} />
        <Route path="/stats" element={<StatsPage />} />
      </Routes>
    </div>
  )
}


