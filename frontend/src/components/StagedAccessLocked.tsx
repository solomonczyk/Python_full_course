import { useState } from 'react'

interface Props {
  currentStage: number
  maxStage: number
  lessonPart: number
  hasFeedback: boolean
  feedbackSubmittedAt: string | null
  onSubmitFeedback: (text: string, rating?: number) => Promise<{ ok: boolean; error?: string }>
}

export default function StagedAccessLocked({
  currentStage,
  maxStage,
  lessonPart,
  hasFeedback,
  feedbackSubmittedAt,
  onSubmitFeedback,
}: Props) {
  const [feedbackText, setFeedbackText] = useState('')
  const [rating, setRating] = useState<number>(0)
  const [submitting, setSubmitting] = useState(false)
  const [submitResult, setSubmitResult] = useState<{ ok: boolean; message: string } | null>(null)

  const isLastStage = currentStage >= maxStage
  const isNextPart = lessonPart === currentStage + 1

  const handleSubmit = async () => {
    if (feedbackText.trim().length < 10) return
    setSubmitting(true)
    const result = await onSubmitFeedback(feedbackText.trim(), rating > 0 ? rating : undefined)
    setSubmitting(false)
    if (result.ok) {
      setSubmitResult({ ok: true, message: 'Feedback submitted! Waiting for operator review.' })
    } else {
      setSubmitResult({ ok: false, message: result.error ?? 'Failed to submit feedback.' })
    }
  }

  return (
    <div className="w-full max-w-[600px] mx-auto py-8">
      <section
        className="rounded-2xl p-8 text-center"
        style={{ background: '#1a1924', border: '1px solid rgba(255,107,107,0.3)' }}
      >
        <span
          className="material-symbols-outlined text-5xl"
          style={{ color: '#ff6b6b', fontVariationSettings: "'FILL' 1" }}
        >
          lock
        </span>

        <h2 className="text-2xl font-bold mt-4" style={{ color: '#ffd700' }}>
          {isLastStage ? 'All Content Unlocked' : `Part ${lessonPart} is not yet available`}
        </h2>

        {!isLastStage && (
          <>
            <p className="text-sm mt-2 leading-relaxed" style={{ color: '#9b98a8' }}>
              You are currently on <strong style={{ color: '#e8e6f0' }}>Stage {currentStage}/{maxStage}</strong>.
              This gives you access to Parts 1{currentStage > 1 ? `–${currentStage}` : ''}.
            </p>

            <div className="mt-4 mx-auto max-w-[400px]">
              <div className="flex gap-1 justify-center">
                {Array.from({ length: maxStage }, (_, i) => (
                  <div
                    key={i}
                    className="h-2 rounded-full flex-1 transition-all"
                    style={{
                      background: i < currentStage ? '#00d4aa' : i === currentStage ? '#c9a227' : 'rgba(155,152,168,0.2)',
                    }}
                  />
                ))}
              </div>
              <p className="text-[10px] mt-1" style={{ color: '#9b98a8' }}>
                Stage {currentStage}/{maxStage} — {isNextPart ? `Part ${lessonPart} is next` : `${currentStage + 1} more stages to unlock`}
              </p>
            </div>

            {!hasFeedback && !submitResult && (
              <div className="mt-6 text-left">
                <p className="text-sm font-semibold mb-3" style={{ color: '#e8e6f0' }}>
                  Share your feedback to unlock the next stage
                </p>

                <textarea
                  value={feedbackText}
                  onChange={(e) => setFeedbackText(e.target.value)}
                  placeholder="Tell us about your experience so far... (min 10 characters)"
                  className="w-full rounded-lg p-3 text-sm resize-none border-none outline-none"
                  rows={4}
                  style={{
                    background: '#0f0e17',
                    color: '#e8e6f0',
                    border: '1px solid rgba(201,162,39,0.2)',
                  }}
                />

                <div className="flex justify-between items-center mt-1 mb-3">
                  <span className="text-[10px]" style={{ color: feedbackText.length >= 10 ? '#00d4aa' : '#ff6b6b' }}>
                    {feedbackText.length}/10 min
                  </span>
                  <span className="text-[10px]" style={{ color: '#9b98a8' }}>
                    {feedbackText.length}/2000
                  </span>
                </div>

                {/* Star rating */}
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-[10px]" style={{ color: '#9b98a8' }}>Rating (optional):</span>
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      onClick={() => setRating(star === rating ? 0 : star)}
                      className="text-lg cursor-pointer bg-transparent border-none p-0 transition-all hover:scale-110"
                      style={{ color: star <= rating ? '#ffd700' : 'rgba(155,152,168,0.3)' }}
                    >
                      ★
                    </button>
                  ))}
                </div>

                <button
                  onClick={handleSubmit}
                  disabled={feedbackText.trim().length < 10 || submitting}
                  className="w-full px-8 py-3 rounded-lg text-xs font-bold cursor-pointer border-none transition-all hover:scale-105 disabled:opacity-40 disabled:cursor-not-allowed"
                  style={{
                    background: '#00d4aa',
                    color: '#0f0e17',
                  }}
                >
                  {submitting ? 'Submitting...' : 'Submit Feedback'}
                </button>
              </div>
            )}

            {hasFeedback && !submitResult && (
              <div className="mt-6 p-4 rounded-lg" style={{ background: 'rgba(0,212,170,0.1)', border: '1px solid rgba(0,212,170,0.2)' }}>
                <span className="material-symbols-outlined text-2xl" style={{ color: '#00d4aa' }}>check_circle</span>
                <p className="text-sm mt-1" style={{ color: '#00d4aa' }}>
                  Feedback submitted!
                </p>
                <p className="text-xs mt-1" style={{ color: '#9b98a8' }}>
                  Waiting for operator review. Check back later.
                </p>
                {feedbackSubmittedAt && (
                  <p className="text-[10px] mt-1" style={{ color: '#9b98a8' }}>
                    Submitted: {new Date(feedbackSubmittedAt).toLocaleDateString()}
                  </p>
                )}
              </div>
            )}

            {submitResult && (
              <div className="mt-6 p-4 rounded-lg" style={{
                background: submitResult.ok ? 'rgba(0,212,170,0.1)' : 'rgba(255,107,107,0.1)',
                border: `1px solid ${submitResult.ok ? 'rgba(0,212,170,0.2)' : 'rgba(255,107,107,0.2)'}`,
              }}>
                <span className="material-symbols-outlined text-2xl" style={{ color: submitResult.ok ? '#00d4aa' : '#ff6b6b' }}>
                  {submitResult.ok ? 'check_circle' : 'error'}
                </span>
                <p className="text-sm mt-1" style={{ color: submitResult.ok ? '#00d4aa' : '#ff6b6b' }}>
                  {submitResult.message}
                </p>
              </div>
            )}
          </>
        )}

        <button
          onClick={() => window.history.back()}
          className="mt-6 px-8 py-3 rounded-lg text-xs font-bold inline-flex items-center gap-2 cursor-pointer border-none transition-all hover:scale-105"
          style={{ background: 'rgba(201,162,39,0.15)', color: '#c9a227', border: '1px solid rgba(201,162,39,0.3)' }}
        >
          <span className="material-symbols-outlined text-sm">arrow_back</span>
          Back to Home
        </button>
      </section>
    </div>
  )
}
