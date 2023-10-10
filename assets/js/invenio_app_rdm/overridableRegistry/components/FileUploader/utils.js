// Taken from v1.2.0 react-invenio-deposit
// https://github.com/inveniosoftware/react-invenio-deposit/blob/v1.2.0/src/lib/components/FileUploader/utils.js
// This file is part of React-Invenio-Deposit
// Copyright (C) 2020 CERN.
// Copyright (C) 2020 Northwestern University.
// Copyright (C) 2022 TU Wien.
//
// React-Invenio-Deposit is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import _isNumber from "lodash/isNumber";

export function humanReadableBytes(bytes, decimalDisplay = false) {
  if (_isNumber(bytes)) {
    const base = decimalDisplay ? 1000 : 1024;
    const kiloBytes = base;
    const megaBytes = base * kiloBytes;
    const gigaBytes = base * megaBytes;

    if (bytes < kiloBytes) {
      return `${bytes} bytes`;
    } else if (bytes < megaBytes) {
      return `${(bytes / kiloBytes).toFixed(2)} ${decimalDisplay ? "KB" : "KiB"}`;
    } else if (bytes < gigaBytes) {
      return `${(bytes / megaBytes).toFixed(2)} ${decimalDisplay ? "MB" : "MiB"}`;
    } else {
      return `${(bytes / gigaBytes).toFixed(2)} ${decimalDisplay ? "GB" : "GiB"}`;
    }
  }
  return "";
}
