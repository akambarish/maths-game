import { useEffect, useMemo, useState } from 'react'
import { api } from '../services/api'
import type {
  AskQuestionResponse,
  GameStatusResponse,
  MakeGuessResponse,
  StartGameResponse,
} from '../types/game'

type QaItem = { q: string; a: string }

const STORAGE_KEY = 'maths-game:game_id'

export default function GamePage() {
  const [gameId, setGameId] = useState<string | null>(() => localStorage.getItem(STORAGE_KEY))
  const [status, setStatus] = useState<GameStatusResponse | null>(null)
  const [question, setQuestion] = useState('')
  const [guess, setGuess] = useState('')
  const [qa, setQa] = useState<QaItem[]>([])
  const [lastGuessResult, setLastGuessResult] = useState<MakeGuessResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const canAsk = useMemo(() => status?.game_state === 'asking', [status?.game_state])
  const gameOver = useMemo(() => status?.game_over === true, [status?.game_over])

  async function refresh(currentGameId: string) {
    const { data } = await api.get<GameStatusResponse>(`/api/game/${currentGameId}/status`)
    setStatus(data)
    return data
  }

  async function startNewGame() {
    setLoading(true)
    setError(null)
    setQa([])
    setLastGuessResult(null)
    try {
      const { data } = await api.post<StartGameResponse>('/api/game/start')
      localStorage.setItem(STORAGE_KEY, data.game_id)
      setGameId(data.game_id)
      await refresh(data.game_id)
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? e?.message ?? 'Failed to start game')
    } finally {
      setLoading(false)
    }
  }

  async function ask() {
    if (!gameId) return
    if (!question.trim()) return

    setLoading(true)
    setError(null)
    try {
      const { data } = await api.post<AskQuestionResponse>(`/api/game/${gameId}/question`, {
        question: question.trim(),
      })
      setQa((prev) => [...prev, { q: question.trim(), a: data.answer }])
      setQuestion('')
      await refresh(gameId)
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? e?.message ?? 'Failed to ask question')
    } finally {
      setLoading(false)
    }
  }

  async function submitGuess() {
    if (!gameId) return
    const n = Number(guess)
    if (!Number.isFinite(n)) return

    setLoading(true)
    setError(null)
    try {
      const { data } = await api.post<MakeGuessResponse>(`/api/game/${gameId}/guess`, { guess: n })
      setLastGuessResult(data)
      setGuess('')
      const s = await refresh(gameId)
      if (s.game_over) {
        // Record stats
        await api.post(`/api/game/${gameId}/end`)
      }
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? e?.message ?? 'Failed to guess')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (!gameId) return
    setLoading(true)
    setError(null)
    refresh(gameId)
      .catch((e: any) => {
        setError(e?.response?.data?.detail ?? e?.message ?? 'Failed to load game')
        localStorage.removeItem(STORAGE_KEY)
        setGameId(null)
      })
      .finally(() => setLoading(false))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [gameId])

  return (
    <div>
      <h3 style={{ marginTop: 0 }}>You guess the computer&apos;s number</h3>

      {error && (
        <div style={{ padding: 12, border: '1px solid #f99', background: '#fff5f5', marginBottom: 12 }}>
          {error}
        </div>
      )}

      {!gameId ? (
        <button onClick={startNewGame} disabled={loading}>
          Start new game
        </button>
      ) : (
        <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
          <div>
            <strong>Game:</strong> {gameId.slice(0, 8)}…
          </div>
          <button onClick={startNewGame} disabled={loading}>
            New game
          </button>
        </div>
      )}

      {status && (
        <div style={{ marginTop: 12, padding: 12, border: '1px solid #ddd', borderRadius: 6 }}>
          <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
            <div>
              <strong>Questions</strong>: {status.question_count} (remaining {status.remaining_questions})
            </div>
            <div>
              <strong>Possible numbers</strong>: {status.possible_count}
            </div>
            <div>
              <strong>Guesses</strong>: {status.guess_attempts} (remaining {status.remaining_guesses})
            </div>
            <div>
              <strong>State</strong>: {status.game_state}
            </div>
          </div>
        </div>
      )}

      {gameId && (
        <div style={{ marginTop: 16, display: 'grid', gap: 12 }}>
          <div style={{ padding: 12, border: '1px solid #ddd', borderRadius: 6 }}>
            <h4 style={{ marginTop: 0 }}>Ask a Yes/No math question</h4>
            <div style={{ display: 'flex', gap: 8 }}>
              <input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="e.g. Is it divisible by 7?"
                style={{ flex: 1, padding: 8 }}
                disabled={!canAsk || loading || gameOver}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') ask()
                }}
              />
              <button onClick={ask} disabled={!canAsk || loading || gameOver || !question.trim()}>
                Ask
              </button>
            </div>
            {!canAsk && !gameOver && (
              <p style={{ marginBottom: 0, opacity: 0.8 }}>
                You&apos;ve reached the max questions. You can only guess now.
              </p>
            )}
          </div>

          <div style={{ padding: 12, border: '1px solid #ddd', borderRadius: 6 }}>
            <h4 style={{ marginTop: 0 }}>Make a guess</h4>
            <div style={{ display: 'flex', gap: 8 }}>
              <input
                value={guess}
                onChange={(e) => setGuess(e.target.value)}
                placeholder="Enter a number (0-500)"
                style={{ flex: 1, padding: 8 }}
                disabled={loading || gameOver}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') submitGuess()
                }}
              />
              <button onClick={submitGuess} disabled={loading || gameOver || !guess.trim()}>
                Guess
              </button>
            </div>

            {lastGuessResult && (
              <div style={{ marginTop: 8 }}>
                {lastGuessResult.correct ? (
                  <strong>Correct!</strong>
                ) : (
                  <strong>Incorrect.</strong>
                )}{' '}
                {lastGuessResult.game_over && lastGuessResult.secret_number != null && (
                  <span>The secret number was {lastGuessResult.secret_number}.</span>
                )}
              </div>
            )}

            {status?.game_over && (
              <div style={{ marginTop: 8 }}>
                <strong>{status.won ? 'You won!' : 'You lost.'}</strong>
              </div>
            )}
          </div>

          {qa.length > 0 && (
            <div style={{ padding: 12, border: '1px solid #ddd', borderRadius: 6 }}>
              <h4 style={{ marginTop: 0 }}>Q&A History</h4>
              <ol style={{ margin: 0, paddingLeft: 20 }}>
                {qa.map((item, idx) => (
                  <li key={idx} style={{ marginBottom: 6 }}>
                    <div>{item.q}</div>
                    <div>
                      <strong>Answer:</strong> {item.a}
                    </div>
                  </li>
                ))}
              </ol>
            </div>
          )}
        </div>
      )}
    </div>
  )
}


