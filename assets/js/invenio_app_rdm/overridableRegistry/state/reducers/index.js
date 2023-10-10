// This file is part of React-Invenio-Deposit
// Copyright (C) 2020-2022 CERN.
// Copyright (C) 2020-2022 Northwestern University.
//
// React-Invenio-Deposit is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { combineReducers } from "redux";
import depositReducer from "./deposit";
import fileReducer from "./files";

export default combineReducers({
  deposit: depositReducer,
  files: fileReducer,
});
