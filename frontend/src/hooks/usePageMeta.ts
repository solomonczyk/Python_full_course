/** Route-level SEO metadata hook.
 *
 * Updates document.title, meta description, OpenGraph, Twitter card, and
 * canonical URL on every route change.  Restores sensible defaults when
 * the component unmounts.
 *
 * Usage:
 *   usePageMeta({ title: 'Python Quest', description: '...' });
 *
 * Because this is a client-side SPA (Vite + React Router), the meta tags
 * are set dynamically in the browser.  Search engines that execute JS will
 * see them; for full SSR the app would need Next.js or similar.
 */

const BASE_TITLE = 'Python Quest'
const BASE_DESCRIPTION =
  'Игровой курс Python для новичков. Научись программировать на Python в формате квеста с персонажами, миссиями и магией.'
const BASE_OG_IMAGE = '/og-image.png'

interface PageMeta {
  title?: string
  description?: string
  ogTitle?: string
  ogDescription?: string
  ogType?: string
  ogUrl?: string
  ogImage?: string
  twitterCard?: 'summary' | 'summary_large_image'
  canonical?: string
}

function getOrCreateMeta(name: string, property = false): HTMLMetaElement {
  const attr = property ? 'property' : 'name'
  let el = document.querySelector(`meta[${attr}="${name}"]`) as HTMLMetaElement | null
  if (!el) {
    el = document.createElement('meta')
    el.setAttribute(attr, name)
    document.head.appendChild(el)
  }
  return el
}

function setMeta(name: string, value: string, property = false) {
  const el = getOrCreateMeta(name, property)
  el.setAttribute(property ? 'property' : 'name', name)
  el.content = value
}

function removeMeta(name: string, property = false) {
  const attr = property ? 'property' : 'name'
  const el = document.querySelector(`meta[${attr}="${name}"]`)
  if (el) el.remove()
}

let previousMeta: PageMeta | null = null

const DEFAULTS: PageMeta = {
  title: BASE_TITLE,
  description: BASE_DESCRIPTION,
  ogTitle: BASE_TITLE,
  ogDescription: BASE_DESCRIPTION,
  ogType: 'website',
  ogImage: BASE_OG_IMAGE,
  twitterCard: 'summary_large_image',
}

export function applyPageMeta(meta: PageMeta) {
  // Sanity — allow overriding with custom title but keep suffix
  const fullTitle = meta.title
    ? meta.title.includes(BASE_TITLE)
      ? meta.title
      : `${meta.title} | ${BASE_TITLE}`
    : BASE_TITLE

  document.title = fullTitle

  const desc = meta.description ?? BASE_DESCRIPTION
  setMeta('description', desc)

  // OpenGraph
  const ogTitle = meta.ogTitle ?? meta.title ?? BASE_TITLE
  setMeta('og:title', ogTitle, true)
  setMeta('og:description', meta.ogDescription ?? desc, true)
  setMeta('og:type', meta.ogType ?? 'website', true)
  setMeta('og:url', meta.ogUrl ?? window.location.href, true)
  setMeta('og:image', meta.ogImage ?? BASE_OG_IMAGE, true)
  setMeta('og:locale', 'ru_RU', true)
  setMeta('og:site_name', BASE_TITLE, true)

  // Twitter card
  setMeta('twitter:card', meta.twitterCard ?? 'summary_large_image')
  setMeta('twitter:title', ogTitle)
  setMeta('twitter:description', meta.ogDescription ?? desc)
  setMeta('twitter:image', meta.ogImage ?? BASE_OG_IMAGE)

  // Canonical
  let canonicalEl = document.querySelector('link[rel="canonical"]') as HTMLLinkElement | null
  if (meta.canonical) {
    if (!canonicalEl) {
      canonicalEl = document.createElement('link')
      canonicalEl.rel = 'canonical'
      document.head.appendChild(canonicalEl)
    }
    canonicalEl.href = meta.canonical
  } else if (canonicalEl) {
    canonicalEl.remove()
  }

  previousMeta = meta
}

export function restoreDefaults() {
  applyPageMeta(DEFAULTS)
}

export function usePageMeta(meta: PageMeta) {
  // We can't use React hooks in a utility function, but we can export
  // this to be called from useEffect in each page component.
  // For convenience, this function just applies the meta immediately.
  applyPageMeta(meta)

  // Return a cleanup function
  return restoreDefaults
}

/** Generate a canonical URL for a route path. */
export function canonicalUrl(path: string): string {
  const origin = typeof window !== 'undefined' ? window.location.origin : 'https://python-quest.app'
  return `${origin}${path}`
}

/** List of all public routes with their metadata. */
export const PUBLIC_ROUTES: Record<string, PageMeta> = {
  '/': {
    title: BASE_TITLE,
    description: BASE_DESCRIPTION,
    ogTitle: 'Python Quest — игровой курс Python',
    ogDescription: BASE_DESCRIPTION,
    ogType: 'website',
  },
  '/course': {
    title: 'Каталог уроков',
    description: 'Все уроки Python Quest: от основ print() до функций и алгоритмов. Изучай Python в формате квеста.',
    ogTitle: 'Каталог уроков Python Quest',
    ogDescription: 'Все уроки Python Quest: от основ print() до функций и алгоритмов.',
    ogType: 'website',
  },
}
