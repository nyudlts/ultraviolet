import { waitForElement } from "./helpers"

/**
 * Changes the text for "Dates" on the deposit form to "Additional Dates"
 * https://jira.nyu.edu/browse/INVENIO-114
 */
export async function uvDepositDatesLabel() {
  const metadataDatesField = await waitForElement('label[for="metadata.dates"]')
  if (metadataDatesField) {
    metadataDatesField.innerHTML = `<p><i aria-hidden="true" class="calendar icon"></i>Additional Dates</p>`
  }
}
