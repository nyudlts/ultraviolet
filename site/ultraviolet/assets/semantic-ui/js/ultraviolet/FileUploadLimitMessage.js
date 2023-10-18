import React from "react";
import ReactDOM from "react-dom";
import { Message, Icon } from "semantic-ui-react";

const rootContainer = document.getElementById("div.ui.visible.warning.message.parent").parentNode;

ReactDOM.render(
  <Message visible warning>
    <p>
      <Icon name="warning sign" />
      {i18next.t(
        "File addition, removal or modification are not allowed after you have published your upload."
      )}
    </p>
  </Message>
  ,
  rootContainer
);
