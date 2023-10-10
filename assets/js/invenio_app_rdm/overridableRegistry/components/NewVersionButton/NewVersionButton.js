// This file is part of React-Invenio-Deposit
// Copyright (C) 2021 CERN.
// Copyright (C) 2021 Graz University of Technology.
//
// React-Invenio-Deposit is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

// this component was not changed from the original https://github.com/inveniosoftware/react-invenio-deposit/blob/c53392300bcf460a2072cc3abbf4f0049fee4812/src/lib/components/NewVersionButton.js
// but was necessary for the override imports of NewVersionButtonContainerOverride.js

import React, { useState } from "react";
import { http } from "react-invenio-forms";
import { Icon, Button, Popup } from "semantic-ui-react";
// import { i18next } from "translations/i18next";
import { i18next } from "@translations/invenio_app_rdm/i18next";
import PropTypes from "prop-types";

export const NewVersionButton = ({ onError, record, disabled, ...uiProps }) => {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);

    try {
      const response = await http.post(record.links.versions);
      window.location = response.data.links.self_html;
    } catch (error) {
      console.error(error);
      setLoading(false);
      onError(error.response.data.message);
    }
  };

  return (
    <Popup
      content={i18next.t("You don't have permissions to create a new version.")}
      disabled={!disabled}
      trigger={
        <Button
          type="button"
          positive
          size="mini"
          onClick={handleClick}
          loading={loading}
          icon
          labelPosition="left"
          {...uiProps}
        >
          <Icon name="tag" />
          {i18next.t("New version")}
        </Button>
      }
    />
  );
};

NewVersionButton.propTypes = {
  onError: PropTypes.func.isRequired,
  record: PropTypes.object.isRequired,
  disabled: PropTypes.bool,
};

NewVersionButton.defaultProps = {
  disabled: false,
};
