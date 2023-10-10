import { FileUploader } from "./components/FileUploader"

export const overriddenComponents = {
  // use this to test and hide the communities section:
  // "InvenioAppRdm.Deposit.CommunityHeader.layout": () => null,
  // react-invenio-deposit v1.2.0
  "InvenioAppRdm.Deposit.FileUploader.layout": FileUploader,
};
