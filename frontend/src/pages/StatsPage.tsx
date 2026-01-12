import { useEffect, useState } from 'react'
import { api } from '../services/api'
import type { StatsResponse } from '../types/game'

export default function StatsPage() {
  const [stats, setStats] = useState<StatsResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    api
      .get<StatsResponse>('/api/stats')
      .then((r) => setStats(r.data))
      .catch((e: any) => setError(e?.response?.data?.detail ?? e?.message ?? 'Failed to load stats'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div>Loading…</div>
  if (error) return <div style={{ color: 'crimson' }}>{error}</div>
  if (!stats) return null

  const total = stats.total_games
  const winRate = total > 0 ? (stats.wins / total) * 100 : 0
  const avgQ = total > 0 ? stats.total_questions / total : 0

  return (
    <div>
      <h3 style={{ marginTop: 0 }}>Statistics</h3>
      {total === 0 ? (
        <p>No games played yet.</p>
      ) : (
        <div style={{ display: 'grid', gap: 10 }}>
          <div>
            <strong>Total games:</strong> {total}
          </div>
          <div>
            <strong>Wins:</strong> {stats.wins} &nbsp; <strong>Losses:</strong> {stats.losses}
          </div>
          <div>
            <strong>Win rate:</strong> {winRate.toFixed(1)}%
          </div>
          <div>
            <strong>Average questions/game:</strong> {avgQ.toFixed(1)}
          </div>
          {stats.best_game_questions != null && (
            <div>
              <strong>Best game:</strong> {stats.best_game_questions} questions
            </div>
          )}
          <hr />
          <div>
            <strong>Mode 2 (User Guesses)</strong>: Games {stats.mode2_games}, Wins {stats.mode2_wins}
          </div>
        </div>
      )}
    </div>
  )
}


