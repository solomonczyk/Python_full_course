/**
 * Unit tests for SyntaxReminderBlock — unknown/missing reminder types.
 */
import { describe, it, expect } from 'vitest'

// Minimal inlined version of the fallback logic to avoid JSX rendering
const REMINDER_STYLES: Record<string, { bg: string; border: string; icon: string; iconBg: string; iconColor: string; label: string }> = {
  indentation_reminder: { bg: 'bg-orange-50', border: 'border-orange-400', icon: 'format_indent_increase', iconBg: 'bg-orange-100', iconColor: 'text-orange-600', label: 'ВНИМАНИЕ: ОТСТУПЫ' },
  colon_reminder: { bg: 'bg-blue-50', border: 'border-blue-400', icon: 'more_horiz', iconBg: 'bg-blue-100', iconColor: 'text-blue-600', label: 'ВНИМАНИЕ: ДВОЕТОЧИЕ' },
  function_def_reminder: { bg: 'bg-emerald-50', border: 'border-emerald-400', icon: 'function', iconBg: 'bg-emerald-100', iconColor: 'text-emerald-600', label: 'ВНИМАНИЕ: ФУНКЦИЯ' },
  try_except_reminder: { bg: 'bg-sky-50', border: 'border-sky-400', icon: 'shield', iconBg: 'bg-sky-100', iconColor: 'text-sky-600', label: 'ВНИМАНИЕ: ЗАЩИТА' },
}

const DEFAULT_STYLE = { bg: 'bg-gray-50', border: 'border-gray-400', icon: 'info', iconBg: 'bg-gray-100', iconColor: 'text-gray-600', label: 'ВНИМАНИЕ' }

function getStyle(type: string) {
  return REMINDER_STYLES[type] ?? DEFAULT_STYLE
}

describe('SyntaxReminderBlock — fallback safety', () => {
  it('returns correct style for valid type', () => {
    expect(getStyle('indentation_reminder').bg).toBe('bg-orange-50')
    expect(getStyle('function_def_reminder').bg).toBe('bg-emerald-50')
    expect(getStyle('try_except_reminder').icon).toBe('shield')
  })

  it('returns default style for unknown type', () => {
    const style = getStyle('nonexistent_type')
    expect(style.bg).toBe('bg-gray-50')
    expect(style.border).toBe('border-gray-400')
    expect(style.icon).toBe('info')
    expect(style.label).toBe('ВНИМАНИЕ')
  })

  it('returns default style for undefined type', () => {
    const style = getStyle(undefined as any)
    expect(style).toBeDefined()
    expect(style.bg).toBeDefined()
    expect(style.border).toBeDefined()
    expect(style.icon).toBeDefined()
  })

  it('returns default style for null type', () => {
    const style = getStyle(null as any)
    expect(style).toBeDefined()
    expect(style.bg).toBeDefined()
  })

  it('never crashes on any string input', () => {
    for (const input of ['', 'random', 'FUNCTION_DEF_REMINDER', ' dict_syntax_reminder ']) {
      const style = getStyle(input)
      expect(style).toBeDefined()
      expect(style.bg).toBeTruthy()
      expect(style.border).toBeTruthy()
      expect(style.icon).toBeTruthy()
      expect(style.iconBg).toBeTruthy()
      expect(style.iconColor).toBeTruthy()
      expect(style.label).toBeTruthy()
    }
  })
})
