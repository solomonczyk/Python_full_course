const USER_ID_KEY = 'pq_user_id'

export function getUserId(): string {
  let uid = localStorage.getItem(USER_ID_KEY)
  if (!uid) {
    try {
      uid = crypto.randomUUID()
    } catch {
      uid = Date.now().toString(36) + Math.random().toString(36).slice(2, 10)
    }
    localStorage.setItem(USER_ID_KEY, uid)
  }
  return uid
}
