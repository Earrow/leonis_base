import Vue from 'vue'

export const EventBus = new Vue()

export function isValidJwt (jwt) {
  if (!jwt || jwt.split('.').length < 3) {
    return false
  }
  const data = JSON.parse(atob(jwt.split('.')[1]))
  const exp = new Date(data.exp * 1000)
  const now = new Date()
  return now < exp
}

export function setCookie (cName, value, expire) {
  let date = new Date()
  date.setSeconds(date.getSeconds() + expire)
  document.cookie = `${cName}=${escape(value)}; expires=${date.toGMTString()}`
}

export function getCookie (cName) {
  if (document.cookie.length > 0) {
    let cStart = document.cookie.indexOf(cName + '=')
    if (cStart !== 1) {
      cStart = cStart + cName.length + 1
      let cEnd = document.cookie.indexOf(';', cStart)
      if (cEnd === -1) {
        cEnd = document.cookie.length
      }
      return unescape(document.cookie.substring(cStart, cEnd))
    }
  }
  return ''
}

export function delCookie (cName) {
  setCookie(cName, '', -1)
}
