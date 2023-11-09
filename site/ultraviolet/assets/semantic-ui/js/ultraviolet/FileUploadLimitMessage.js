import { waitForElement } from "./waitForElement";

document.addEventListener('DOMContentLoaded', async () => {

  const fileUploadWarning = await waitForElement("div.ui.visible.warning.message")
  if (fileUploadWarning) {
    let secondWarning = fileUploadWarning.cloneNode(true) // true for deepclone
    // using replace to preserve the icon
    secondWarning.innerHTML = secondWarning.innerHTML.replace("File addition, removal or modification are not allowed after you have published your upload.", "Contact the NYU Libraries UltraViolet service team at <a href='mailto:uv@nyu.edu'>uv@nyu.edu</a> if you have more than 100 files or 50GB.")
    // satisfying react's need for unique IDs
    secondWarning.id = fileUploadWarning.id + "1"
    fileUploadWarning.parentNode.append(secondWarning)
  }
});
