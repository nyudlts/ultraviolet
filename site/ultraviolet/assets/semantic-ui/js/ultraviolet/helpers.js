/**
 * places an observer on the body to wait for changes and check if an element exists
 * https://stackoverflow.com/questions/5525071/how-to-wait-until-an-element-exists
 * @param {string} selector 
 * @returns {Promise<HTMLElement>} 
 */
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
