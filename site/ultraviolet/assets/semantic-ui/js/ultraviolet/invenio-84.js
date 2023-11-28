import { waitForElement } from "./helpers"

/**
 * Adds a warning message to the file upload section of the deposit form
 * https://jira.nyu.edu/browse/INVENIO-84
 */
export async function invenio84() {
  const fileUploadWarningContainer = await waitForElement(".file-upload-note div.column")
  if (fileUploadWarningContainer) {
    let secondWarning = document.createElement("div")
    secondWarning.classList.add("ui", "visible",  "warning", "message")
    secondWarning.setAttribute("id", "invenio-84-file-limits-msg")
    const message = `Contact the NYU Libraries UltraViolet service team at <a href="mailto:uv@nyu.edu">uv@nyu.edu</a> if you have more than 100 files or 50GB.`
    secondWarning.innerHTML = `<p><i aria-hidden="true" class="warning sign icon"></i>${message}</p>`
    fileUploadWarningContainer.append(secondWarning)
  }
}
