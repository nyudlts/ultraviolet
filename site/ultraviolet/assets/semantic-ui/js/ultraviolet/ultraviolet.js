document.addEventListener('DOMContentLoaded', async () => {

  // https://stackoverflow.com/questions/5525071/how-to-wait-until-an-element-exists
  async function waitForElm(selector) {
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

  // INVENIO-114
  // Change text for "Dates" on deposit form to "Additional Dates"
  const metadataDatesField = await waitForElm('label[for="metadata.dates"]')
  if (metadataDatesField) {
    metadataDatesField.innerHTML = metadataDatesField.innerHTML.replace('Dates', 'Additional Dates')
  }

})
