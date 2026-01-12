export type YesNo = 'Yes' | 'No'

export type GameState = 'asking' | 'guess_only' | 'won' | 'lost'

export interface StartGameResponse {
  game_id: string
  secret_number_set: boolean
  possible_count: number
  max_questions: number
  max_guesses: number
}

export interface GameStatusResponse {
  game_id: string
  question_count: number
  remaining_questions: number
  possible_count: number
  guess_attempts: number
  remaining_guesses: number
  game_state: GameState
  won: boolean
  game_over: boolean
}

export interface AskQuestionResponse {
  answer: YesNo
  possible_count: number
  question_count: number
  remaining_questions: number
  game_state: GameState
}

export interface MakeGuessResponse {
  correct: boolean
  game_over: boolean
  won: boolean
  secret_number?: number | null
  remaining_guesses: number
}

export interface StatsResponse {
  total_games: number
  wins: number
  losses: number
  total_questions: number
  best_game_questions: number | null
  mode1_games: number
  mode1_wins: number
  mode2_games: number
  mode2_wins: number
}


