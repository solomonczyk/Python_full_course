import { useParams, useNavigate } from 'react-router-dom'
import DialogueScene from '../components/DialogueScene'
import type { DialogueLine } from '../types'

interface TransitionData {
  title: string
  subtitle: string
  recap: string
  dialogue: DialogueLine[]
  cta: string
}

const TRANSITIONS: Record<number, TransitionData> = {
  1: {
    title: 'Конец части 1: Пробуждение героя',
    subtitle: 'Ты сделал свои первые шаги в мире программирования!',
    recap: 'Ты изучил вывод текста через print(), переменные, ввод данных через input(), арифметику и базовый выбор сценариев с if/else.',
    dialogue: [
      { character: 'ksyu', text: 'В начале ты просто смотрел на `print()` и не понимал, что происходит.' },
      { character: 'novice', text: 'Да, и даже она казалась странной.' },
      { character: 'va', text: 'Это маленький шаг, но важный. У тебя уже есть основа игры: ввод, хранение данных, расчёт и решение.' },
      { character: 'da', text: 'Первый кирпич игры заложен. Проверим, готов ли твой герой войти в настоящее приключение!' },
    ],
    cta: 'Пройти испытание «Проверка героя»',
  },
  2: {
    title: 'Конец части 2: Условия и циклы',
    subtitle: 'Твой код обретает гибкость и случайность!',
    recap: 'Ты научился делать сложные ветвления с elif, использовать случайные числа с random, строить циклы for и range для повторения команд.',
    dialogue: [
      { character: 'da', text: 'Теперь твоя программа умеет случайность.' },
      { character: 'novice', text: 'Кубик судьбы был прикольный!' },
      { character: 'ksyu', text: 'И важный. Потому что игры без случайности часто скучные.' },
      { character: 'va', text: 'Но ты также научился проверять условия точнее. Случайность должна быть под контролем логики.' },
      { character: 'bagus', text: 'Ха! Я всё равно найду, где ты перепутал `if`!' },
      { character: 'ksyu', text: 'Найдёт. А ты исправишь. Вперёд к кубику судьбы!' },
    ],
    cta: 'Пройти испытание «Кубик судьбы»',
  },
  3: {
    title: 'Конец части 3: Уверенная база Python',
    subtitle: 'У твоего героя появляется настоящая память!',
    recap: 'Ты освоил работу со сложными структурами данных: индексами и срезами строк, списками, их методами (append, remove, in), вложенными списками и генератором случайных событий.',
    dialogue: [
      { character: 'ksyu', text: 'Теперь у героя есть инвентарь.' },
      { character: 'novice', text: 'Список предметов, проверка ключа, случайные находки...' },
      { character: 'da', text: 'Вот именно! Это уже настоящая игровая механика.' },
      { character: 'va', text: 'Ты больше не работаешь с одной переменной. Ты работаешь с набором данных.' },
      { character: 'ksyu', text: 'Это огромный рост. Давай проверим твой инвентарь на практике!' },
    ],
    cta: 'Пройти испытание «Инвентарь героя»',
  },
  4: {
    title: 'Конец части 4: Башня алгоритмов',
    subtitle: 'Все знания собираются воедино!',
    recap: 'Ты освоил циклы while, флаги состояния, сортировки данных и работу с таблицами комнат. Ты готов встретиться с главным испытанием курса!',
    dialogue: [
      { character: 'ksyu', text: 'Мы дошли до финального босса.' },
      { character: 'novice', text: 'Мне кажется, я всё забуду...' },
      { character: 'va', text: 'Ты не должен помнить всё идеально. Ты должен уметь разбить задачу на части.' },
      { character: 'da', text: 'Сначала меню. Потом герой. Потом комнаты. Потом команды. Потом условия победы и поражения.' },
      { character: 'ksyu', text: 'Не пытайся написать всю игру одной строкой. Собирай её как башню — этаж за этажом. Удачи!' },
    ],
    cta: '🚀 Войти в Башню Багуса',
  },
}

export default function PartTransitionPage() {
  const { part: partStr } = useParams<{ part: string }>()
  const navigate = useNavigate()
  const part = Number(partStr)

  const data = TRANSITIONS[part]

  if (!data) {
    return (
      <div className="w-full max-w-[800px] flex items-center justify-center h-64">
        <div className="text-center text-error">
          <span className="material-symbols-outlined text-5xl block mb-2">error</span>
          <p>Неверная часть перехода</p>
          <button
            onClick={() => navigate('/')}
            className="mt-4 px-4 py-2 bg-primary text-on-primary rounded-xl"
          >
            На главную
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="w-full max-w-[800px] flex flex-col gap-10 animate-fade-in">
      {/* Title block */}
      <section className="bg-gradient-to-r from-primary/10 via-secondary/10 to-transparent p-8 rounded-[24px] border border-outline-variant/30">
        <div className="flex items-center gap-3 mb-2">
          <span className="bg-secondary text-on-secondary text-[12px] font-bold px-3 py-1 rounded-full uppercase tracking-wider">
            Достижение
          </span>
        </div>
        <h2 className="font-display font-extrabold text-[32px] leading-[40px] text-on-surface mb-2">
          {data.title}
        </h2>
        <p className="font-sans text-[18px] text-secondary font-medium leading-relaxed">
          {data.subtitle}
        </p>
      </section>

      {/* Recap block */}
      <section className="bg-white border border-outline-variant p-6 rounded-2xl shadow-sm">
        <h3 className="font-display text-[20px] font-bold text-on-surface mb-3 flex items-center gap-2">
          <span className="material-symbols-outlined text-secondary">history_edu</span>
          Что ты теперь умеешь:
        </h3>
        <p className="font-sans text-[15px] leading-[24px] text-on-surface-variant">
          {data.recap}
        </p>
      </section>

      {/* Dialogue block */}
      <div className="flex flex-col gap-6">
        <h3 className="font-display text-[16px] font-bold tracking-wider text-on-surface-variant uppercase">
          Разговор перед испытанием:
        </h3>
        <DialogueScene lines={data.dialogue} />
      </div>

      {/* Actions */}
      <section className="flex flex-col items-center gap-4 pt-6 border-t border-outline-variant">
        <button
          onClick={() => navigate(`/mini-game/${part}`)}
          className="w-full max-w-[400px] flex items-center justify-center gap-2 px-8 py-5 rounded-2xl bg-action-da text-white shadow-lg hover:brightness-110 active:scale-[0.98] transition-all font-display text-[18px] font-extrabold"
        >
          <span>{data.cta}</span>
          <span className="material-symbols-outlined">arrow_forward</span>
        </button>
        <button
          onClick={() => navigate('/')}
          className="text-on-surface-variant hover:text-secondary font-sans text-[14px] font-medium"
        >
          Вернуться на карту курса
        </button>
      </section>
    </div>
  )
}
