import type { SyntaxReminder } from '../types'

interface Props {
  reminder: SyntaxReminder
}

const REMINDER_STYLES: Record<SyntaxReminder['type'], {
  bg: string
  border: string
  icon: string
  iconBg: string
  iconColor: string
  label: string
}> = {
  indentation_reminder: {
    bg: 'bg-orange-50',
    border: 'border-orange-400',
    icon: 'format_indent_increase',
    iconBg: 'bg-orange-100',
    iconColor: 'text-orange-600',
    label: 'ВНИМАНИЕ: ОТСТУПЫ',
  },
  colon_reminder: {
    bg: 'bg-blue-50',
    border: 'border-blue-400',
    icon: 'more_horiz',
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600',
    label: 'ВНИМАНИЕ: ДВОЕТОЧИЕ',
  },
  block_structure_reminder: {
    bg: 'bg-violet-50',
    border: 'border-violet-400',
    icon: 'layers',
    iconBg: 'bg-violet-100',
    iconColor: 'text-violet-600',
    label: 'ВНИМАНИЕ: СТРУКТУРА БЛОКА',
  },
  input_conversion_reminder: {
    bg: 'bg-purple-50',
    border: 'border-purple-400',
    icon: 'swap_horiz',
    iconBg: 'bg-purple-100',
    iconColor: 'text-purple-600',
    label: 'ВНИМАНИЕ: ТИП ДАННЫХ',
  },
  index_reminder: {
    bg: 'bg-cyan-50',
    border: 'border-cyan-400',
    icon: 'tag',
    iconBg: 'bg-cyan-100',
    iconColor: 'text-cyan-600',
    label: 'ВНИМАНИЕ: ИНДЕКСЫ',
  },
  range_reminder: {
    bg: 'bg-teal-50',
    border: 'border-teal-400',
    icon: 'swap_horiz',
    iconBg: 'bg-teal-100',
    iconColor: 'text-teal-600',
    label: 'ВНИМАНИЕ: ГРАНИЦЫ',
  },
  loop_stop_reminder: {
    bg: 'bg-red-50',
    border: 'border-red-400',
    icon: 'block',
    iconBg: 'bg-red-100',
    iconColor: 'text-red-600',
    label: 'ВНИМАНИЕ: ЦИКЛ',
  },
  mutation_reminder: {
    bg: 'bg-amber-50',
    border: 'border-amber-400',
    icon: 'edit_square',
    iconBg: 'bg-amber-100',
    iconColor: 'text-amber-600',
    label: 'ВНИМАНИЕ: ИЗМЕНЕНИЕ',
  },
  copy_reference_reminder: {
    bg: 'bg-indigo-50',
    border: 'border-indigo-400',
    icon: 'file_copy',
    iconBg: 'bg-indigo-100',
    iconColor: 'text-indigo-600',
    label: 'ВНИМАНИЕ: ССЫЛКИ',
  },
  function_def_reminder: {
    bg: 'bg-emerald-50',
    border: 'border-emerald-400',
    icon: 'function',
    iconBg: 'bg-emerald-100',
    iconColor: 'text-emerald-600',
    label: 'ВНИМАНИЕ: ФУНКЦИЯ',
  },
  function_params_reminder: {
    bg: 'bg-lime-50',
    border: 'border-lime-400',
    icon: 'settings',
    iconBg: 'bg-lime-100',
    iconColor: 'text-lime-600',
    label: 'ВНИМАНИЕ: ПАРАМЕТРЫ',
  },
  return_reminder: {
    bg: 'bg-rose-50',
    border: 'border-rose-400',
    icon: 'keyboard_return',
    iconBg: 'bg-rose-100',
    iconColor: 'text-rose-600',
    label: 'ВНИМАНИЕ: ВОЗВРАТ',
  },
  dict_syntax_reminder: {
    bg: 'bg-yellow-50',
    border: 'border-yellow-400',
    icon: 'dictionary',
    iconBg: 'bg-yellow-100',
    iconColor: 'text-yellow-600',
    label: 'ВНИМАНИЕ: СЛОВАРЬ',
  },
  try_except_reminder: {
    bg: 'bg-sky-50',
    border: 'border-sky-400',
    icon: 'shield',
    iconBg: 'bg-sky-100',
    iconColor: 'text-sky-600',
    label: 'ВНИМАНИЕ: ЗАЩИТА',
  },
}

// Fallback for unknown/missing reminder types — prevents runtime crash
const DEFAULT_STYLE = {
  bg: 'bg-gray-50',
  border: 'border-gray-400',
  icon: 'info',
  iconBg: 'bg-gray-100',
  iconColor: 'text-gray-600',
  label: 'ВНИМАНИЕ',
}

export default function SyntaxReminderBlock({ reminder }: Props) {
  const style = REMINDER_STYLES[reminder.type] ?? DEFAULT_STYLE

  return (
    <section className={`${style.bg} border-l-8 ${style.border} rounded-2xl p-5 shadow-sm`}>
      <div className="flex items-center gap-3 mb-3">
        <div className={`w-9 h-9 ${style.iconBg} rounded-xl flex items-center justify-center ${style.iconColor}`}>
          <span className="material-symbols-outlined text-lg" style={{ fontVariationSettings: "'FILL' 1" }}>{style.icon}</span>
        </div>
        <span className={`font-sans text-[13px] font-bold ${style.iconColor} tracking-wider`}>{style.label}</span>
      </div>
      <p className="font-sans text-[15px] leading-[22px] text-on-surface">{reminder.message}</p>
    </section>
  )
}
