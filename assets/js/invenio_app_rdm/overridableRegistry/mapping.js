// TODO: move this component to a separate file and import here.
// This is the example from the documentation of invenio. Will have to implement your own custom component.
import React from "react";
import { Checkbox } from "semantic-ui-react";
import { useFormikContext } from "formik";
import PropTypes from "prop-types";

const MetadataToggle = (props) => {
    const { filesEnabled } = props;
    const { setFieldValue } = useFormikContext();

    const handleOnChangeMetadataOnly = () => {
        setFieldValue("files.enabled", !filesEnabled);
        setFieldValue("access.files", "public");
    };

    return (
        <Checkbox
        toggle
        label="Metadata-only record"
        onChange={handleOnChangeMetadataOnly}
        />
    );
};

export default MetadataToggle;

MetadataToggle.propTypes = {
    filesEnabled: PropTypes.bool.isRequired,
};

// map that contains the overriden components
// TODO: once testing is done, add the community header override
export const overridenComponents = {
    /*
        example from https://inveniordm.docs.cern.ch/develop/best-practices/react/
        [InvenioModuleName].[ReactApp].[Component].[Element]
        [InvenioModuleName]: the Invenio module name, e.g. InvenioCommunities or InvenioAppRDM.
        [ReactApp]: the name of the web page where the ReactApp will be rendered, e.g. MembersList, MyDashboard, MyUploads, MyCommunities, DepositForm. There is no exact naming here, try to be consistent with the existing ones.
        [Component]: the name of the component in the React app, e.g. ResultsList, SortBy, ListItem, BtnAccept.
        [Element]: the name of the UI section inside the component. Layout is normally used of the entire Overridable component, inside the render() function, Container or Title might be used in an inner section, in case of large components:
    */
    // InvenioAppRdm.Deposit.CommunityHeader.layout": () => null,
    // example from Samk13 https://github.com/Samk13/test-overrides/blob/master/assets/js/invenio_app_rdm/overridableRegistry/mapping.js
    // "invenioAppRdm.Deposit.MeataDataOnlyToggle.layout": () => null,
    // example from documentation
    // ReactInvenioDeposit
    // ReactInvenioDeposit.MetadataOnlyToggle.layout
    // "InvenioAppRdm.MetadataOnlyToggle.layout": () => null,
    "ReactInvenioDeposit.MetadataOnlyToggle.layout": () => null,
  };