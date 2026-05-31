interface Props {
  userName: string
}

export default function Certificate({ userName }: Props) {
  const today = new Date().toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })

  return (
    <div id="certificate">
      <div
        className="rounded-xl p-8 text-center relative overflow-hidden"
        style={{
          background: 'linear-gradient(135deg, #1a1924 0%, #2a1a3a 100%)',
          border: '3px double #c9a227',
          boxShadow: '0 0 30px rgba(201,162,39,0.3)',
          fontFamily: "'Plus Jakarta Sans', sans-serif",
        }}
      >
        {/* Decorative corners */}
        <div className="absolute top-0 left-0 w-16 h-16 border-t-2 border-l-2" style={{ borderColor: '#c9a227' }} />
        <div className="absolute top-0 right-0 w-16 h-16 border-t-2 border-r-2" style={{ borderColor: '#c9a227' }} />
        <div className="absolute bottom-0 left-0 w-16 h-16 border-b-2 border-l-2" style={{ borderColor: '#c9a227' }} />
        <div className="absolute bottom-0 right-0 w-16 h-16 border-b-2 border-r-2" style={{ borderColor: '#c9a227' }} />

        {/* Content */}
        <div className="relative z-10">
          <div className="text-5xl mb-4">🏆</div>
          <h1 className="text-2xl font-bold mb-2" style={{ color: '#c9a227' }}>
            Сертификат
          </h1>
          <p className="text-xs mb-6" style={{ color: '#9b98a8' }}>
            подтверждает, что
          </p>
          <div
            className="text-3xl font-bold mb-4 py-3 px-6 inline-block"
            style={{
              color: '#00d4aa',
              borderBottom: '2px solid rgba(0,212,170,0.3)',
              fontFamily: "'Plus Jakarta Sans', sans-serif",
            }}
          >
            {userName}
          </div>
          <p className="text-sm mb-6" style={{ color: '#e8e6f0' }}>
            успешно прошёл(а) полный курс
          </p>
          <h2 className="text-xl font-bold mb-2" style={{ color: '#c9a227' }}>
            Python Quest
          </h2>
          <p className="text-xs mb-6" style={{ color: '#9b98a8' }}>
            Интерактивный курс по основам программирования на Python
          </p>
          <div
            className="inline-block px-3 py-1 rounded-full text-xs font-bold mb-4"
            style={{ background: 'rgba(0,212,170,0.15)', color: '#00d4aa', border: '1px solid #00d4aa' }}
          >
            Уровень A2+ — уверенный начинающий
          </div>
          <div className="flex justify-center gap-8 mt-6 text-xs" style={{ color: '#9b98a8' }}>
            <div>
              <div className="font-bold" style={{ color: '#e8e6f0' }}>Дата</div>
              <div>{today}</div>
            </div>
            <div>
              <div className="font-bold" style={{ color: '#e8e6f0' }}>Частей</div>
              <div>4</div>
            </div>
            <div>
              <div className="font-bold" style={{ color: '#e8e6f0' }}>Уроков</div>
              <div>87</div>
            </div>
          </div>
        </div>
      </div>

      {/* Print button */}
      <div className="mt-3 text-center">
        <button
          onClick={() => window.print()}
          className="px-6 py-2 rounded-lg text-xs font-bold cursor-pointer border-none"
          style={{ background: '#c9a227', color: '#0f0e17' }}
        >
          🖨️ Скачать / Распечатать
        </button>
      </div>

      {/* Print styles */}
      <style>{`
        @media print {
          body * { visibility: hidden; }
          #certificate, #certificate * { visibility: visible; }
          #certificate {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
          }
          #certificate button { display: none; }
        }
      `}</style>
    </div>
  )
}

// Allow window.print() to target this component
// Usage: add id="certificate-wrapper" and use @media print { body * { visibility: hidden; } #certificate-wrapper, #certificate-wrapper * { visibility: visible; } }
