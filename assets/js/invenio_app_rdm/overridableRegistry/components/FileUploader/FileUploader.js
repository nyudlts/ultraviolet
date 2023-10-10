// Taken from v1.2.0
// https://github.com/inveniosoftware/react-invenio-deposit/blob/v1.2.0/src/lib/components/FileUploader/FileUploader.js
// This file is part of React-Invenio-Deposit
// Copyright (C) 2020-2022 CERN.
// Copyright (C) 2020-2022 Northwestern University.
// Copyright (C)      2022 Graz University of Technology.
// Copyright (C)      2022 TU Wien.
//
// React-Invenio-Deposit is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.
// import { i18next } from "@translations/i18next";
import { i18next } from "@translations/invenio_app_rdm/i18next";
import { useFormikContext } from "formik";
import _get from "lodash/get";
import _isEmpty from "lodash/isEmpty";
import _map from "lodash/map";
import PropTypes from "prop-types";
import React, { useState } from "react";
import { Button, Grid, Icon, Message, Modal } from "semantic-ui-react";
import { UploadState } from "../../state/reducers/files";
import { NewVersionButton } from "../NewVersionButton/NewVersionButton";
import { FileUploaderArea } from "./FileUploaderArea";
import { FileUploaderToolbar } from "./FileUploaderToolbar";
import { humanReadableBytes } from "./utils";

// NOTE: This component has to be a function component to allow
//       the `useFormikContext` hook.
export const FileUploaderComponent = ({
  config,
  files,
  isDraftRecord,
  hasParentRecord,
  quota,
  permissions,
  record,
  uploadFiles,
  deleteFile,
  importParentFiles,
  importButtonIcon,
  importButtonText,
  isFileImportInProgress,
  decimalSizeDisplay,
  ...uiProps
}) => {
  // We extract the working copy of the draft stored as `values` in formik
  const { values: formikDraft } = useFormikContext();
  const filesEnabled = _get(formikDraft, "files.enabled", false);
  const [warningMsg, setWarningMsg] = useState();

  const filesList = Object.values(files).map((fileState) => {
    return {
      name: fileState.name,
      size: fileState.size,
      checksum: fileState.checksum,
      links: fileState.links,
      uploadState: {
        // initial: fileState.status === UploadState.initial,
        isFailed: fileState.status === UploadState.error,
        isUploading: fileState.status === UploadState.uploading,
        isFinished: fileState.status === UploadState.finished,
        isPending: fileState.status === UploadState.pending,
      },
      progressPercentage: fileState.progressPercentage,
      cancelUploadFn: fileState.cancelUploadFn,
    };
  });

  const filesSize = filesList.reduce((totalSize, file) => (totalSize += file.size), 0);

  const dropzoneParams = {
    preventDropOnDocument: true,
    onDropAccepted: (acceptedFiles) => {
      const maxFileNumberReached =
        filesList.length + acceptedFiles.length > quota.maxFiles;
      const acceptedFilesSize = acceptedFiles.reduce(
        (totalSize, file) => (totalSize += file.size),
        0
      );
      const maxFileStorageReached = filesSize + acceptedFilesSize > quota.maxStorage;

      const filesNames = _map(filesList, "name");
      const duplicateFiles = acceptedFiles.filter((acceptedFile) =>
        filesNames.includes(acceptedFile.name)
      );

      if (maxFileNumberReached) {
        setWarningMsg(
          <div className="content">
            <Message
              warning
              icon="warning circle"
              header="Could not upload files."
              content={`Uploading the selected files would result in ${
                filesList.length + acceptedFiles.length
              } files (max.${quota.maxFiles})`}
            />
          </div>
        );
      } else if (maxFileStorageReached) {
        setWarningMsg(
          <div className="content">
            <Message
              warning
              icon="warning circle"
              header="Could not upload files."
              content={
                <>
                  {i18next.t("Uploading the selected files would result in")}{" "}
                  {humanReadableBytes(
                    filesSize + acceptedFilesSize,
                    decimalSizeDisplay
                  )}
                  {i18next.t("but the limit is")}
                  {humanReadableBytes(quota.maxStorage, decimalSizeDisplay)}.
                </>
              }
            />
          </div>
        );
      } else if (!_isEmpty(duplicateFiles)) {
        setWarningMsg(
          <div className="content">
            <Message
              warning
              icon="warning circle"
              header={i18next.t(`The following files already exist`)}
              list={_map(duplicateFiles, "name")}
            />
          </div>
        );
      } else {
        uploadFiles(formikDraft, acceptedFiles);
      }
    },
    multiple: true,
    noClick: true,
    noKeyboard: true,
    disabled: false,
  };

  const filesLeft = filesList.length < quota.maxFiles;
  if (!filesLeft) {
    dropzoneParams["disabled"] = true;
  }

  const displayImportBtn =
    filesEnabled && isDraftRecord && hasParentRecord && !filesList.length;

  return (
    <>
      <Grid>
        <Grid.Row className="pt-10 pb-5">
          {isDraftRecord && (
            <FileUploaderToolbar
              {...uiProps}
              config={config}
              filesEnabled={filesEnabled}
              filesList={filesList}
              filesSize={filesSize}
              isDraftRecord={isDraftRecord}
              quota={quota}
              decimalSizeDisplay={decimalSizeDisplay}
            />
          )}
        </Grid.Row>
        {displayImportBtn && (
          <Grid.Row className="pb-5 pt-5">
            <Grid.Column width={16}>
              <Message visible info>
                <div style={{ display: "inline-block", float: "right" }}>
                  <Button
                    type="button"
                    size="mini"
                    primary
                    icon={importButtonIcon}
                    content={importButtonText}
                    onClick={() => importParentFiles()}
                    disabled={isFileImportInProgress}
                    loading={isFileImportInProgress}
                  />
                </div>
                <p style={{ marginTop: "5px", display: "inline-block" }}>
                  <Icon name="info circle" />
                  {i18next.t("You can import files from the previous version.")}
                </p>
              </Message>
            </Grid.Column>
          </Grid.Row>
        )}
        {filesEnabled && (
          <Grid.Row className="pt-0 pb-0">
            <FileUploaderArea
              {...uiProps}
              filesList={filesList}
              dropzoneParams={dropzoneParams}
              isDraftRecord={isDraftRecord}
              filesEnabled={filesEnabled}
              deleteFile={deleteFile}
              decimalSizeDisplay={decimalSizeDisplay}
            />
          </Grid.Row>
        )}
        {isDraftRecord ? (
          <Grid.Row className="file-upload-note pt-5">
            <Grid.Column width={16}>
              <Message visible warning>
                <p>
                  <Icon name="warning sign" />
                  {i18next.t(
                    "File addition, removal or modification are not allowed after you have published your upload."
                  )}
                </p>
              </Message>
              {/* THIS IS THE OVERRIDE, that's all */}
              <Message visible warning>
                <p>
                  <Icon name="warning sign" />
                  {i18next.t(
                    "Contact the NYU Libraries UltraViolet service team at uv@nyu.edu if you have more than 100 files or 50GB."
                  )}
                </p>
              </Message>
              {/* END OF OVERRIDE */}
            </Grid.Column>
          </Grid.Row>
        ) : (
          <Grid.Row className="file-upload-note pt-5">
            <Grid.Column width={16}>
              <Message info>
                <NewVersionButton
                  record={record}
                  onError={() => {}}
                  className=""
                  disabled={!permissions.can_new_version}
                  style={{ float: "right" }}
                />
                <p style={{ marginTop: "5px", display: "inline-block" }}>
                  <Icon name="info circle" size="large" />
                  {i18next.t(
                    "You must create a new version to add, modify or delete files."
                  )}
                </p>
              </Message>
            </Grid.Column>
          </Grid.Row>
        )}
      </Grid>
      <Modal
        open={!!warningMsg}
        header="Warning!"
        content={warningMsg}
        onClose={() => setWarningMsg()}
        closeIcon
      />
    </>
  );
};

const fileDetailsShape = PropTypes.objectOf(
  PropTypes.shape({
    name: PropTypes.string,
    size: PropTypes.number,
    progressPercentage: PropTypes.number,
    checksum: PropTypes.string,
    links: PropTypes.object,
    cancelUploadFn: PropTypes.func,
    state: PropTypes.oneOf(Object.values(UploadState)),
    enabled: PropTypes.bool,
  })
);

FileUploaderComponent.propTypes = {
  config: PropTypes.object,
  dragText: PropTypes.string,
  files: fileDetailsShape,
  isDraftRecord: PropTypes.bool,
  hasParentRecord: PropTypes.bool,
  quota: PropTypes.shape({
    maxStorage: PropTypes.number,
    maxFiles: PropTypes.number,
  }),
  record: PropTypes.object,
  uploadButtonIcon: PropTypes.string,
  uploadButtonText: PropTypes.string,
  importButtonIcon: PropTypes.string,
  importButtonText: PropTypes.string,
  isFileImportInProgress: PropTypes.bool,
  importParentFiles: PropTypes.func.isRequired,
  uploadFiles: PropTypes.func.isRequired,
  deleteFile: PropTypes.func.isRequired,
  decimalSizeDisplay: PropTypes.bool,
  permissions: PropTypes.object,
};

FileUploaderComponent.defaultProps = {
  permissions: undefined,
  config: undefined,
  files: undefined,
  record: undefined,
  isFileImportInProgress: false,
  dragText: i18next.t("Drag and drop files"),
  isDraftRecord: true,
  hasParentRecord: false,
  quota: {
    maxFiles: 5,
    maxStorage: 10 ** 10,
  },
  uploadButtonIcon: "upload",
  uploadButtonText: i18next.t("Upload files"),
  importButtonIcon: "sync",
  importButtonText: i18next.t("Import files"),
  decimalSizeDisplay: true,
};
