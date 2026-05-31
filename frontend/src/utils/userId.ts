const USER_ID_KEY = 'pq_user_id'

export function getUserId(): string {
  let uid = localStorage.getItem(USER_ID_KEY)
  if (!uid) {
    uid = crypto.randomUUID()
    localStorage.setItem(USER_ID_KEY, uid)
  }
  return uid
}
