/**
 * Navigation helper with reliable fallback.
 *
 * React Router's navigate() can fail to trigger in certain contexts
 * (CDP-triggered events, async callbacks outside React tree).
 * This helper tries navigate() first, then falls back to
 * window.location.href after a timeout.
 */

/**
 * Navigate to a URL using React Router, with window.location fallback.
 *
 * @param navigate - React Router navigate function
 * @param to - Target URL path (e.g. '/lesson/1-1')
 * @param replace - Whether to replace history entry (default: false)
 */
export function navigateWithFallback(
  navigate: (to: string, options?: { replace?: boolean }) => void,
  to: string,
  replace = false,
): void {
  const currentPath = window.location.pathname

  // Try React Router navigation first
  navigate(to, replace ? { replace: true } : undefined)

  // If URL didn't change after a short delay, use window.location as fallback
  // This handles cases where navigate() is called outside React event context
  // and doesn't trigger (e.g. CDP automation events)
  setTimeout(() => {
    if (window.location.pathname === currentPath) {
      console.debug('[nav] React Router navigate did not trigger, using window.location fallback')
      if (replace) {
        window.location.replace(to)
      } else {
        window.location.href = to
      }
    }
  }, 300)
}
