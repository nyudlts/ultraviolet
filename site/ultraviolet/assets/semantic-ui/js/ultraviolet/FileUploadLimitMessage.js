import React from "react";
import ReactDOM from "react-dom";
import { Message, Icon } from "semantic-ui-react";
import waitForElement from "./waitForElement";

document.addEventListener('DOMContentLoaded', async () => {

  const fileUploadTargetExists = await waitForElement('.file-upload-note > div')
  if (fileUploadTargetExists) {

    const rootContainer = document.querySelector(".file-upload-note > div");
    // FIXME: causes a double render error for now
    ReactDOM.render(
      <>
        <Message visible warning key="file-upload-message-warning-1">
          <p>
            <Icon name="warning sign" />
            File addition, removal or modification are not allowed after you have published your upload.
          </p>
        </Message>
        <Message visible warning key="file-upload-message-warning-2">
          <p>
            <Icon name="warning sign" />
            Contact the NYU Libraries UltraViolet service team at <a href="mailto:uv@nyu.com">uv@nyu.edu</a> if you have more than 100 files or 50GB.
          </p>
        </Message>
      </>
      ,
      rootContainer
    );
  }
});
