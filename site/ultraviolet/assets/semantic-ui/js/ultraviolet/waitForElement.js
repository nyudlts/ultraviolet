/**
 * waits for the dom to load and places an observer on the body
 * to wait for more changes on the DOM to look up that element
 * should be called within a DOMContentLoaded
 * @param {string} selector 
 */
// https://stackoverflow.com/questions/5525071/how-to-wait-until-an-element-exists
export async function waitForElement(selector) {
  return new Promise(resolve => {
    if (document.querySelector(selector)) {
      return resolve(document.querySelector(selector))
    }    
    const observer = new MutationObserver(mutations => {
      if (document.querySelector(selector)) {
        observer.disconnect()
        resolve(document.querySelector(selector))
      }
    })    
    observer.observe(document.body, { childList: true, subtree: true })
  })
}
