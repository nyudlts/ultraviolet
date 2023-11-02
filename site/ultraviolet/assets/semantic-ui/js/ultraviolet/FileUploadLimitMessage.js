import React from "react";
import ReactDOM from "react-dom";
import { Message, Icon } from "semantic-ui-react";
import { i18next } from "@translations/invenio_app_rdm/i18next";

const rootContainer = document.getElementById("div.ui.visible.warning.message.parent").parentNode;

ReactDOM.render(
  <Message visible warning>
    <p>
      <Icon name="warning sign" />
      {i18next.t("Contact the NYU Libraries UltraViolet service team at ")}
      <a href="mailto:email@example.com">uv@nyu.edu</a>
      {i18next.t(" if you have more than 100 files or 50GB.")}
    </p>
  </Message>,
  rootContainer
);
